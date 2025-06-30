"""
--- 1. ARSITEKTUR UTAMA & KONFIGURASI ---
Aplikasi ini adalah sistem manajemen jadwal berbasis web yang dibangun menggunakan
framework Flask dari Python. Bagian di bawah ini melakukan inisialisasi aplikasi,
mengkonfigurasi koneksi ke database SQLite (`database.db`) menggunakan
Flask-SQLAlchemy, dan mendefinisikan `secret_key` untuk keamanan sesi. SQLite
dipilih karena portabel dan tidak memerlukan server terpisah.
"""
import os
import pandas as pd
from flask import Flask, render_template, request, redirect, url_for, flash, send_file
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime, time, timedelta
import io
from collections import defaultdict
import json

# --- Inisialisasi & Konfigurasi ---
app = Flask(__name__)
app.config['SECRET_KEY'] = 'proyek-final-tanpa-login' # Secret key diubah karena tidak ada login
db_path = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'database.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{db_path}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


"""
--- Data Statis `data_gedung` ---
Ini adalah variabel dictionary Python biasa yang menyimpan informasi struktur
gedung, lantai, dan ruangan. Data ini sengaja dibuat 'hardcoded' karena jarang
berubah dan lebih cepat diakses daripada melakukan query ke database.
"""
# --- Data Gedung dan Ruangan (Tetap sama) ---
data_gedung = {
    "A": {
        "3": ["Lab Komputer Mesin 1", "Lab Komputer Mesin 2", "A3A"],
        "4": ["Lab Komputer Hardware", "Lab Komputer Software", "A4A"],
        "5": ["Lab Komputer DKV 1", "Lab Komputer DKV 2", "A5A"]
    },
    "B": {
        "1": ["Lab Teknik Sipil", "Lab Teknik Elektro"],
        "2": [f"B2{huruf}" for huruf in "ABCDEFGH"],
        "3": [f"B3{huruf}" for huruf in "ABCDEFGH"],
        "4": [f"B4{huruf}" for huruf in "ABCDEFGH"],
        "5": [f"B5{huruf}" for huruf in "ABCDEFGH"]
    }
}
HARI_LIST = ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat', 'Sabtu', 'Minggu']
ALLOWED_LANTAI3_ROOMS = ['B3A', 'B3B', 'B3C', 'B3D', 'B3E', 'B3F', 'B3G', 'B3H']
EXCLUDED_LAB_ROOMS_FOR_GENERATION = set([
    "Lab Komputer Hardware", "Lab Komputer Software",
    "Lab Komputer Mesin 1", "Lab Komputer Mesin 2",
    "Lab Komputer DKV 1", "Lab Komputer DKV 2",
    "Lab Teknik Sipil", "Lab Teknik Elektro"
])
generate_progress_status = {
    'total_items': 0, 'processed_items': 0, 'status': 'idle', 'message': ''
}


"""
--- 2. STRUKTUR DATA UTAMA (MODEL DATABASE) ---
- Model `Jadwal` (class Jadwal): Ini adalah cetak biru untuk tabel 'jadwal' di
  database kita. Setiap properti di kelas ini (seperti `nama_dosen`, `mata_kuliah`,
  `hari`, `jam_mulai`, dll.) merepresentasikan satu kolom di tabel. Ini adalah
  cara SQLAlchemy memetakan objek Python ke tabel database (disebut ORM).
"""
# --- Model Database ---
# Model User sengaja dibiarkan agar tidak error saat inisialisasi database,
# namun tidak akan digunakan secara aktif.
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(80), unique=True, nullable=False)
    password = db.Column(db.String(120), nullable=False)
    role = db.Column(db.String(80), nullable=False)

class Jadwal(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    nama_dosen = db.Column(db.String(120), nullable=False)
    mata_kuliah = db.Column(db.String(120), nullable=False)
    kelas = db.Column(db.String(80), nullable=False)
    hari = db.Column(db.String(20), nullable=False)
    jam_mulai = db.Column(db.String(5), nullable=False)
    jam_selesai = db.Column(db.String(5), nullable=False)
    gedung = db.Column(db.String(20))
    lantai = db.Column(db.String(20))
    ruangan = db.Column(db.String(80))
    tipe_kelas = db.Column(db.String(20), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=True) # Dibuat nullable
    sks = db.Column(db.Integer, nullable=False)


"""
--- 3. FUNGSI INTI & PENDUKUNG ---
Bagian ini berisi fungsi-fungsi yang menjadi logika utama aplikasi.

- `parse_time(...)`: Fungsi kecil namun penting yang tugasnya mengubah teks jam
  (misal: "08:00" atau "08.00") menjadi format waktu yang konsisten agar bisa
  dibandingkan secara matematis.

- `is_bentrok` & `is_bentrok_cached`: Ini adalah jantung dari aplikasi untuk
  memastikan tidak ada sumber daya (ruangan, kelas, atau dosen) yang dijadwalkan
  ganda pada waktu yang bersamaan.
    - `is_bentrok(...)`: Digunakan untuk pengecekan tunggal (booking manual).
      Fungsi ini memeriksa ke database secara langsung.
    - `is_bentrok_cached(...)`: Versi optimal untuk "Generate Jadwal". Fungsi ini
      menggunakan data dari memori (cache) untuk pengecekan super cepat,
      menghindari ribuan query ke database.
"""
# --- Fungsi Inti (Fungsi is_bentrok disederhanakan) ---
def parse_time(t_str):
    try:
        if isinstance(t_str, time): return t_str
        return datetime.strptime(str(t_str), "%H:%M").time()
    except (ValueError, TypeError):
        try:
            return datetime.strptime(str(t_str), "%H.%M").time()
        except (ValueError, TypeError):
            try:
                return datetime.strptime(str(t_str), "%H:%M:%S").time()
            except (ValueError, TypeError): return None
    return None

def is_bentrok_cached(hari, mulai_baru_time, selesai_baru_time, ruangan, kelas, nama_dosen_baru, tipe_kelas, existing_schedules_cache):
    if tipe_kelas == 'Offline':
        for jadwal_existing in existing_schedules_cache['ruangan'].get(hari, {}).get(ruangan, []):
            if parse_time(jadwal_existing.jam_mulai) < selesai_baru_time and parse_time(jadwal_existing.jam_selesai) > mulai_baru_time: return True
    for jadwal_existing in existing_schedules_cache['kelas'].get(hari, {}).get(kelas, []):
        if parse_time(jadwal_existing.jam_mulai) < selesai_baru_time and parse_time(jadwal_existing.jam_selesai) > mulai_baru_time: return True
    for jadwal_existing in existing_schedules_cache['dosen'].get(hari, {}).get(nama_dosen_baru, []):
        if parse_time(jadwal_existing.jam_mulai) < selesai_baru_time and parse_time(jadwal_existing.jam_selesai) > mulai_baru_time: return True
    return False

def is_bentrok(hari, mulai_baru, selesai_baru, ruangan, kelas, nama_dosen_baru, tipe_kelas, jadwal_id_to_ignore=None):
    mulai_baru_time, selesai_baru_time = parse_time(mulai_baru), parse_time(selesai_baru)
    if not (mulai_baru_time and selesai_baru_time): return False
    query = Jadwal.query.filter(Jadwal.hari == hari, Jadwal.id != jadwal_id_to_ignore, db.func.time(Jadwal.jam_selesai) > mulai_baru_time, db.func.time(Jadwal.jam_mulai) < selesai_baru_time)
    for sched in query.all():
        if (tipe_kelas == 'Offline' and sched.tipe_kelas == 'Offline' and sched.ruangan == ruangan) or (sched.kelas == kelas) or (sched.nama_dosen == nama_dosen_baru):
            return True
    return False


"""
--- 4. FITUR UTAMA (RUTE/ENDPOINT APLIKASI) ---
Setiap fungsi yang diawali dengan `@app.route(...)` mendefinisikan sebuah halaman
atau endpoint pada aplikasi web. Ini adalah "wajah" dari aplikasi kita yang
dilihat dan diakses oleh pengguna.

- `@app.route('/booking')`: Halaman untuk form booking manual. Salah satu fitur
  penting di sini adalah logika untuk menampilkan visualisasi "Blok Ketersediaan
  Ruangan". Ini membantu pengguna melihat slot waktu mana saja yang masih kosong
  pada hari dan ruangan tertentu.

- `@app.route('/generate_jadwal')`: Ini adalah fitur paling kompleks dan unggulan.
  Alur kerjanya adalah:
  1. Menerima upload file Excel dari pengguna.
  2. Mengurutkan data berdasarkan SKS terbesar (strategi menempatkan jadwal sulit
     lebih dulu).
  3. Menentukan "Profil Waktu" (reguler, malam, weekend) berdasarkan kode kelas.
  4. Melakukan iterasi untuk mencari slot waktu dan ruangan yang tersedia.
  5. Menggunakan `is_bentrok_cached` untuk pengecekan yang sangat cepat.
  6. Memiliki logika prioritas ruangan (`lantai_pref`) untuk efisiensi penempatan.
  7. Melaporkan jadwal yang berhasil dan gagal dibuat.

- `@app.route('/jadwal')`: Halaman utama untuk menampilkan semua jadwal dalam
  bentuk tabel, dilengkapi fitur filter data.

- Fitur Bantu Lainnya: Termasuk endpoint untuk menghapus jadwal
  (`/delete_jadwal/...`), mengunduh data ke Excel (`/download_excel`), dan
  mengunduh template (`/download_template`).
"""
# --- Rute Aplikasi (Tanpa Login) ---
@app.route('/')
def landing_page():
    return render_template('landing_page.html')

@app.route('/booking', methods=['GET'])
def halaman_booking():
    # Logika untuk mengambil data dosen dari file CSV (opsional, bisa disesuaikan)
    lecturer_data = defaultdict(list)
    try:
        df = pd.read_csv('template_generate_jadwal.xlsx - Sheet1.csv')
        for _, row in df[['DOSEN PENGAJAR', 'MATA KULIAH']].drop_duplicates().iterrows():
            dosen = str(row['DOSEN PENGAJAR']).strip()
            matkul = str(row['MATA KULIAH']).strip()
            if dosen != 'nan' and matkul != 'nan' and matkul not in lecturer_data[dosen]:
                lecturer_data[dosen].append(matkul)
    except FileNotFoundError:
        print("PERINGATAN: File 'template_generate_jadwal.xlsx - Sheet1.csv' tidak ditemukan.")
    except Exception as e:
        print(f"ERROR saat memproses file CSV: {e}")

    lecturer_data_json = json.dumps(lecturer_data)

    # Ambil parameter dari URL untuk pengecekan ketersediaan
    selected_day = request.args.get('hari_cek')
    selected_gedung = request.args.get('gedung_cek')
    selected_lantai = request.args.get('lantai_cek')

    room_availability_blocks = {}

    if selected_day and selected_gedung and selected_lantai:
        rooms_to_check = data_gedung.get(selected_gedung, {}).get(selected_lantai, [])
        existing_schedules_today = Jadwal.query.filter_by(hari=selected_day, tipe_kelas='Offline').all()
        booked_slots = defaultdict(set)
        for schedule in existing_schedules_today:
            start_t, end_t = parse_time(schedule.jam_mulai), parse_time(schedule.jam_selesai)
            if not start_t or not end_t: continue
            temp_dt, end_dt = datetime.combine(datetime.min.date(), start_t), datetime.combine(datetime.min.date(), end_t)
            while temp_dt < end_dt:
                booked_slots[schedule.ruangan].add(temp_dt.time())
                temp_dt += timedelta(minutes=15)

        display_start_time, display_end_time = time(7, 0), time(22, 0)
        jam_istirahat_mulai, jam_istirahat_selesai = time(12, 0), time(13, 0)

        for room in rooms_to_check:
            blocks_for_room = []
            slots = []
            temp_t = display_start_time
            while temp_t < display_end_time:
                slots.append(temp_t)
                temp_t = (datetime.combine(datetime.min.date(), temp_t) + timedelta(minutes=15)).time()

            available_slots = []
            for slot in slots:
                is_break_time = jam_istirahat_mulai <= slot < jam_istirahat_selesai
                is_booked = slot in booked_slots.get(room, set())
                if not is_break_time and not is_booked:
                    available_slots.append(slot)

            if available_slots:
                start_block = available_slots[0]
                for i in range(1, len(available_slots)):
                    prev_slot_dt = datetime.combine(datetime.min.date(), available_slots[i-1])
                    current_slot_dt = datetime.combine(datetime.min.date(), available_slots[i])
                    if current_slot_dt - prev_slot_dt > timedelta(minutes=15):
                        end_block_dt = prev_slot_dt + timedelta(minutes=15)
                        blocks_for_room.append({'start': start_block.strftime('%H:%M'), 'end': end_block_dt.strftime('%H:%M'), 'status': 'Tersedia'})
                        start_block = available_slots[i]

                last_slot_dt = datetime.combine(datetime.min.date(), available_slots[-1])
                end_block_dt = last_slot_dt + timedelta(minutes=15)
                blocks_for_room.append({'start': start_block.strftime('%H:%M'), 'end': end_block_dt.strftime('%H:%M'), 'status': 'Tersedia'})

            if blocks_for_room:
                room_availability_blocks[room] = blocks_for_room

    form_data = {}
    form_data.setdefault('tipe_kelas', 'Offline')
    for key in ['gedung', 'lantai', 'ruangan', 'jam_mulai', 'jam_selesai', 'hari']:
        if request.args.get(key): form_data[key] = request.args.get(key)

    form_data['hari_cek'] = selected_day
    form_data['gedung_cek'] = selected_gedung
    form_data['lantai_cek'] = selected_lantai

    return render_template('booking_form.html', form_data=form_data, days=HARI_LIST, room_availability_blocks=room_availability_blocks, lecturer_data_json=lecturer_data_json)


@app.route('/jadwal')
def halaman_jadwal():
    filter_by, filter_value = request.args.get('filter_by', 'Hari'), request.args.get('filter_value', '').strip()
    query = Jadwal.query
    if filter_value:
        if filter_by == 'Hari': query = query.filter(Jadwal.hari.ilike(f'%{filter_value}%'))
        elif filter_by == 'Ruangan': query = query.filter(Jadwal.ruangan.ilike(f'%{filter_value}%'))
        elif filter_by == 'Kelas': query = query.filter(Jadwal.kelas.ilike(f'%{filter_value}%'))
        elif filter_by == 'Dosen': query = query.filter(Jadwal.nama_dosen.ilike(f'%{filter_value}%'))
    jadwal_list = query.order_by(Jadwal.id.desc()).all()
    header = ["ID", "Dosen", "Matkul", "SKS", "Kelas", "Hari", "Mulai", "Selesai", "Gedung", "Lantai", "Ruangan", "Tipe"]
    return render_template('view_jadwal.html', header=header, jadwal_list=jadwal_list, filter_by=filter_by, filter_value=filter_value)

@app.route('/generate_progress')
def get_generate_progress():
    return json.dumps(generate_progress_status)

@app.route('/download_template')
def download_template():
    output = io.BytesIO()
    df_template = pd.DataFrame(columns=['KODE', 'DOSEN PENGAJAR', 'MATA KULIAH', 'SMT', 'SKS', 'KELAS', 'DOSEN_HARI_KAMPUS', 'DOSEN_JAM_KAMPUS', 'TIPE_KELAS'])
    with pd.ExcelWriter(output, engine='openpyxl') as writer: df_template.to_excel(writer, index=False, sheet_name='Sheet1')
    output.seek(0)
    return send_file(output, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet', download_name='template_generate_jadwal.xlsx', as_attachment=True)

@app.route('/generate_jadwal', methods=['GET', 'POST'])
def halaman_generate():
    if request.method == 'POST':
        file = request.files.get('file')
        if not file or file.filename == '':
            flash('Tidak ada file yang dipilih.', 'warning')
            return redirect(request.url)

        global generate_progress_status
        generate_progress_status = {'total_items': 0, 'processed_items': 0, 'status': 'processing', 'message': 'Memulai...'}
        try:
            df = pd.read_excel(file) if file.filename.endswith('.xlsx') else pd.read_csv(file)
            df.columns = [col.strip().upper() for col in df.columns]
            required_columns = ['MATA KULIAH', 'SKS', 'KELAS', 'DOSEN PENGAJAR']
            if not all(col in df.columns for col in required_columns):
                flash(f"File harus memiliki kolom: {', '.join(required_columns)}", 'danger')
                return redirect(request.url)

            for col in ['DOSEN PENGAJAR', 'MATA KULIAH', 'SKS', 'DOSEN_HARI_KAMPUS', 'DOSEN_JAM_KAMPUS', 'TIPE_KELAS', 'KELAS']:
                if col in df.columns: df[col] = df[col].ffill()

            if 'SKS' in df.columns:
                df['SKS'] = pd.to_numeric(df['SKS'], errors='coerce').fillna(0).astype(int)
                df = df.sort_values(by='SKS', ascending=False).reset_index(drop=True)

            generate_progress_status['total_items'] = len(df)
            existing_schedules_cache = {'ruangan': defaultdict(lambda: defaultdict(list)), 'kelas': defaultdict(lambda: defaultdict(list)), 'dosen': defaultdict(lambda: defaultdict(list))}
            for sch in Jadwal.query.all():
                existing_schedules_cache['ruangan'][sch.hari][sch.ruangan].append(sch)
                existing_schedules_cache['kelas'][sch.hari][sch.kelas].append(sch)
                existing_schedules_cache['dosen'][sch.hari][sch.nama_dosen].append(sch)

            new_schedules, failed_schedules = [], []
            time_profiles = {
                'reguler': {'days': ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'], 'start_hour': 8, 'end_hour': 18},
                'weekend_B': {'days': ['Sabtu'], 'start_hour': 8, 'end_hour': 21},
                'weekend_CD': {'days': ['Minggu'], 'start_hour': 8, 'end_hour': 21},
                'malam': {'days': ['Senin', 'Selasa', 'Rabu', 'Kamis', 'Jumat'], 'start_hour': 18, 'start_minute': 30, 'end_hour': 22}
            }
            jam_istirahat_mulai, jam_istirahat_selesai = time(12, 0), time(13, 0)
            lantai_pref = {'SD': '2', 'HK': '2', 'AK': '3', 'MN': '3', 'TI': '4', 'SI': '4', 'DKV': '4', 'SP': '5', 'EL': '5', 'MS': '5'}

            for idx, row in df.iterrows():
                kelas, dosen, matkul = str(row.get('KELAS', '')).strip().upper(), str(row.get('DOSEN PENGAJAR', '')).strip(), str(row.get('MATA KULIAH', '')).strip()
                sks_val = int(row.get('SKS', 0))
                generate_progress_status['message'] = f"Memproses: {matkul} ({kelas})"
                last_char, profile = kelas[-1] if kelas else '', None
                if last_char in ['A', 'E', 'F', 'G', 'H', 'I', 'J', 'T']: profile = time_profiles['reguler']
                elif last_char == 'B': profile = time_profiles['weekend_B']
                elif last_char == 'C': profile = time_profiles['weekend_CD']
                elif last_char == 'M': profile = time_profiles['malam']

                if not profile or sks_val <= 0:
                    reason = 'Profil kelas tidak dikenal' if not profile else 'SKS tidak valid'
                    failed_schedules.append({'course': f"{matkul} ({kelas})", 'reason': reason})
                    generate_progress_status['processed_items'] += 1
                    continue

                duration_minutes = sks_val * 50
                tipe_kelas = str(row.get('TIPE_KELAS', 'Offline')).strip().title()
                slot_found = False

                for day in profile['days']:
                    if slot_found: break
                    current_dt = datetime.strptime(f"{profile.get('start_hour', 8)}:{profile.get('start_minute', 0):02d}", "%H:%M")
                    end_of_day = time(profile.get('end_hour', 22), 0)

                    while current_dt.time() < end_of_day:
                        if jam_istirahat_mulai <= current_dt.time() < jam_istirahat_selesai:
                            current_dt = datetime.combine(current_dt.date(), jam_istirahat_selesai)
                            continue

                        end_dt = current_dt + timedelta(minutes=duration_minutes)
                        if end_dt.time() > end_of_day or (current_dt.time() < jam_istirahat_selesai and end_dt.time() > jam_istirahat_mulai):
                            current_dt += timedelta(minutes=15)
                            continue

                        start_t, end_t = current_dt.time(), end_dt.time()

                        if tipe_kelas == 'Online':
                            if not is_bentrok_cached(day, start_t, end_t, 'N/A', kelas, dosen, 'Online', existing_schedules_cache):
                                new_jadwal = Jadwal(nama_dosen=dosen, mata_kuliah=matkul, kelas=kelas, hari=day, jam_mulai=start_t.strftime("%H:%M"), jam_selesai=end_t.strftime("%H:%M"), gedung='Online', lantai='N/A', ruangan='Online', tipe_kelas='Online', sks=sks_val)
                                new_schedules.append(new_jadwal)
                                existing_schedules_cache['kelas'][day][kelas].append(new_jadwal)
                                existing_schedules_cache['dosen'][day][dosen].append(new_jadwal)
                                slot_found = True
                                break
                        else: # Offline
                            pref_floor = lantai_pref.get(kelas[:2], None)
                            room_priority = []
                            if pref_floor:
                                room_priority.extend([r for g in data_gedung for l, rooms in data_gedung[g].items() if l == pref_floor for r in rooms if r not in EXCLUDED_LAB_ROOMS_FOR_GENERATION])
                            room_priority.extend([r for g in data_gedung for l, rooms in data_gedung[g].items() for r in rooms if r not in room_priority and r not in EXCLUDED_LAB_ROOMS_FOR_GENERATION])

                            for room in room_priority:
                                if not is_bentrok_cached(day, start_t, end_t, room, kelas, dosen, 'Offline', existing_schedules_cache):
                                    gedung_ruangan, lantai_ruangan = next(((g, l) for g, floors in data_gedung.items() for l, rooms in floors.items() if room in rooms), ('N/A', 'N/A'))
                                    new_jadwal = Jadwal(nama_dosen=dosen, mata_kuliah=matkul, kelas=kelas, hari=day, jam_mulai=start_t.strftime("%H:%M"), jam_selesai=end_t.strftime("%H:%M"), gedung=gedung_ruangan, lantai=lantai_ruangan, ruangan=room, tipe_kelas='Offline', sks=sks_val)
                                    new_schedules.append(new_jadwal)
                                    existing_schedules_cache['ruangan'][day][room].append(new_jadwal)
                                    existing_schedules_cache['kelas'][day][kelas].append(new_jadwal)
                                    existing_schedules_cache['dosen'][day][dosen].append(new_jadwal)
                                    slot_found = True
                                    break
                        if slot_found: break
                        current_dt += timedelta(minutes=15)

                if not slot_found:
                    failed_schedules.append({'course': f"{matkul} ({kelas})", 'reason': 'Tidak ada slot waktu/ruangan tersedia'})

                generate_progress_status['processed_items'] += 1

            db.session.add_all(new_schedules)
            db.session.commit()

            generate_progress_status['status'] = 'completed'
            if new_schedules:
                flash(f"Generate Selesai! {len(new_schedules)} jadwal berhasil dibuat.", 'success')
            if failed_schedules:
                flash(f"{len(failed_schedules)} mata kuliah gagal dijadwalkan:", 'warning')
                for item in failed_schedules:
                    flash(f"- {item['course']}: {item['reason']}", 'warning')

            return redirect(url_for('halaman_jadwal'))
        except Exception as e:
            db.session.rollback()
            generate_progress_status['status'] = 'failed'
            generate_progress_status['message'] = f"Error: {e}"
            flash(f"Terjadi error saat generate jadwal: {e}", 'danger')
            return redirect(request.url)

    return render_template('generate_jadwal.html')

@app.route('/download_excel')
def download_excel():
    filter_by, filter_value = request.args.get('filter_by', None), request.args.get('filter_value', '').strip()
    query = Jadwal.query
    if filter_value and filter_by:
        if filter_by == 'Hari': query = query.filter(Jadwal.hari.ilike(f'%{filter_value}%'))
        elif filter_by == 'Ruangan': query = query.filter(Jadwal.ruangan.ilike(f'%{filter_value}%'))
        elif filter_by == 'Kelas': query = query.filter(Jadwal.kelas.ilike(f'%{filter_value}%'))
        elif filter_by == 'Dosen': query = query.filter(Jadwal.nama_dosen.ilike(f'%{filter_value}%'))

    jadwal_data = query.order_by(Jadwal.hari, Jadwal.jam_mulai, Jadwal.ruangan).all()
    if not jadwal_data:
        flash("Tidak ada jadwal yang ditemukan.", 'warning')
        return redirect(url_for('halaman_jadwal'))

    data_for_excel = [[r.id, r.nama_dosen, r.mata_kuliah, r.sks, r.kelas, r.hari, r.jam_mulai, r.jam_selesai, r.gedung, r.lantai, r.ruangan, r.tipe_kelas] for r in jadwal_data]
    df_export = pd.DataFrame(data_for_excel, columns=["ID", "Dosen", "Matkul", "SKS", "Kelas", "Hari", "Mulai", "Selesai", "Gedung", "Lantai", "Ruangan", "Tipe"])

    output = io.BytesIO()
    with pd.ExcelWriter(output, engine='openpyxl') as writer:
        df_export.to_excel(writer, index=False, sheet_name='Jadwal_Kelas')
    output.seek(0)

    filename = f"Jadwal_{filter_by}_{filter_value}.xlsx" if filter_value else "Jadwal_Lengkap.xlsx"
    return send_file(output, as_attachment=True, download_name=filename, mimetype='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')

@app.route('/submit_booking', methods=['POST'])
def submit_booking():
    form = {k: v.strip() for k, v in request.form.items()}
    required = ['dosen', 'matkul', 'kelas', 'tipe_kelas', 'hari', 'jam_mulai', 'jam_selesai']
    if not all(form.get(f) for f in required):
        flash("Semua kolom utama wajib diisi.", "danger")
        return render_template('booking_form.html', form_data=form, days=HARI_LIST)

    tipe_kelas = form['tipe_kelas']
    if tipe_kelas == "Offline" and not all(form.get(f) for f in ['gedung', 'lantai', 'ruangan']):
        flash("Untuk kelas Offline, lokasi wajib diisi.", "warning")
        return render_template('booking_form.html', form_data=form, days=HARI_LIST)

    mulai, selesai = parse_time(form['jam_mulai']), parse_time(form['jam_selesai'])
    if not (mulai and selesai) or mulai >= selesai:
        flash("Jam mulai harus lebih kecil dari jam selesai.", "danger")
        return render_template('booking_form.html', form_data=form, days=HARI_LIST)

    jam_istirahat_mulai, jam_istirahat_selesai = time(12,0), time(13,0)
    if (mulai < jam_istirahat_selesai and selesai > jam_istirahat_mulai):
        flash("Jadwal tidak boleh bentrok dengan jam istirahat (12:00 - 13:00).", "warning")
        return render_template('booking_form.html', form_data=form, days=HARI_LIST)

    ruangan = form.get('ruangan') if tipe_kelas == 'Offline' else 'N/A'
    if is_bentrok(form['hari'], form['jam_mulai'], form['jam_selesai'], ruangan, form['kelas'], form['dosen'], tipe_kelas):
        flash(f"Jadwal Bentrok! Ruangan, kelas, atau dosen sudah digunakan pada waktu tersebut.", "danger")
        return render_template('booking_form.html', form_data=form, days=HARI_LIST)

    new_jadwal = Jadwal(nama_dosen=form['dosen'], mata_kuliah=form['matkul'], kelas=form['kelas'], hari=form['hari'], jam_mulai=form['jam_mulai'], jam_selesai=form['jam_selesai'], gedung=form.get('gedung', 'Online'), lantai=form.get('lantai', 'N/A'), ruangan=ruangan, tipe_kelas=tipe_kelas, sks=int(form.get('sks', 0)))
    db.session.add(new_jadwal)
    db.session.commit()

    flash('Booking berhasil disimpan!', 'success')
    return redirect(url_for('halaman_jadwal'))

@app.route('/delete_jadwal/<int:jadwal_id>', methods=['POST'])
def delete_jadwal(jadwal_id):
    jadwal = Jadwal.query.get_or_404(jadwal_id)
    db.session.delete(jadwal)
    db.session.commit()
    flash('Jadwal berhasil dihapus.', 'success')
    return redirect(url_for('halaman_jadwal'))

@app.route('/delete_all_schedules', methods=['POST'])
def delete_all_schedules():
    try:
        num = db.session.query(Jadwal).delete()
        db.session.commit()
        flash(f'{num} jadwal berhasil dihapus.', 'success')
    except Exception as e:
        db.session.rollback()
        flash(f'Error: {e}', 'danger')
    return redirect(url_for('halaman_jadwal'))

@app.context_processor
def inject_data():
    return dict(data_gedung=data_gedung)

def init_database():
    with app.app_context():
        db.create_all()
        # Logika untuk membuat user admin awal sudah tidak relevan lagi,
        # jadi bisa dikosongkan atau dihapus.
        # Namun, membiarkannya kosong tidak akan menimbulkan masalah.
        if not User.query.filter_by(username='admin').first():
            # Anda bisa menghapus bagian ini jika model User juga dihapus total
            pass

if __name__ == '__main__':
    if not os.path.exists(db_path):
        init_database()
    app.run(debug=True)