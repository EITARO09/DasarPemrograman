data_mahasiswa = {}

def tambah_data():
    NIM = input("Masukkan NIM: ")
    NAMA = input("Masukkan NAMA: ")
    JURUSAN = input("Masukkan JURUSAN: ")
    IPK = input("Masukkan IPK: ")

    data_mahasiswa[NIM] = {"Nama": NAMA, "Jurusan": JURUSAN, "Ipk": IPK}
    print("Data Mahasiswa Berhasil Ditambahkan")

def tampilan_data():
    if not data_mahasiswa:
        print("Tidak ada data mahasiswa")
    else:
        for NIM, info in data_mahasiswa.items():
            mahasiswa_info = (NIM, info['Nama'], info['Jurusan'], info['IPK'])
            print(f"NIM: {mahasiswa_info[0]}, Nama: {mahasiswa_info[1]}, Jurusan: {mahasiswa_info[2]}, IPK: {mahasiswa_info[3]}")

def cari_data():
    NIM = input("Masukkan NIM yang akan dicari: ")
    if NIM in data_mahasiswa:
        info = data_mahasiswa[NIM]
        mahasiswa_info = (NIM, info['Nama'], info['Jurusan'], info['IPK'])
        print(f"NIM: {mahasiswa_info[0]}, Nama: {mahasiswa_info[1]}, Jurusan: {mahasiswa_info[2]}, IPK: {mahasiswa_info[3]}")
    else:
        print("Data Mahasiswa Tidak Ditemukan")

def hapus_data():
    NIM = input("Masukkan NIM yang ingin dihapus: ")
    if NIM in data_mahasiswa:
        del data_mahasiswa[NIM]
        print("Data Mahasiswa Berhasil Dihapus")
    else:
        print("Data Mahasiswa Tidak Ditemukan")

def main():
    while True:
        print("\nMenu Pengelolaan Data Mahasiswa")
        print("1. Tambah Data Mahasiswa Yang Baru")
        print("2. Tampilkan Semua Data Mahasiswa")
        print("3. Cari Data Mahasiswa Berdasarkan NIM")
        print("4. Hapus Data Mahasiswa Berdasarkan NIM")
        print("5. Keluar")
        
        pilihan = input("Pilih menu opsi (1-5): ")

        if pilihan == '1':
            tambah_data()
        elif pilihan == '2':
            tampilan_data()
        elif pilihan == '3':
            cari_data()
        elif pilihan == '4':
            hapus_data()
        elif pilihan == '5':
            print("Terima Kasih! Program Selesai")
            break 
        else:
            print("Pilihan tidak valid. Silahkan coba lagi")

if __name__ == "__main__":
    main()