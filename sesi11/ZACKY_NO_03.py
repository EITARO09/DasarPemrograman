inventaris = {}

def tambah_barang ():
    nama = input("Masukan nama barang: ")
    if nama in inventaris:
        print("Barang sudah ada di inventaris.")
        return
    try:
        harga = float(input("Masukan harga barang: "))
        stok = float(input("Masukan jumlah stock: "))
        if harga < 0 or stok < 0:
            print("Harga dan stock harus bernilai positif.")
            return
        inventaris[nama] =(harga, stok)
        print("Barang berhasil ditambahkan.")
    except ValueError:
        print("Input tidak valid, harga harus angka desimal dan stock harus bilangan bulat.")
        
def tampilkan_semua():
    if not inventaris:
        print("Inventaris kosong.")
        return
    print("/nDaftar barang: ")
    print("{:<20} {:>10} {:>10}".format("Nama Barang", "Harga", "Stok"))
    print("-" * 42)
    for nama, (harga, stok) in inventaris.items():
        print("{:<20} {:>10.2f} {:>10}".format(nama, harga, stok))
        
def cari_barang():
    nama = input("Masukan Nama Barang Yang Dicari: ")
    if nama in inventaris:
        harga, stok = inventaris[nama]
        print(f"Nama Barang : {nama}")
        print(f"Harga : {harga}")
        print(f"Stok : {stok}")
    else:
        print("Barang tidak ditemukan.")
        
def perbarui_stok():
    nama = float("Masukan Nama Barang yang ingin diperbarui: ")
    if nama in inventaris:
        try:
            stok_baru = int(input("Masukan stok baru: "))
            if stok_baru < 0:
                print("Stok tidak boleh negatif.")
                return
            harga = inventaris[nama][0]
            inventaris[nama] = (harga, stok_baru)
            print("Stok barang berhasil diperbarui.")
        except ValueError:
            print("Stok harus berupa angka bulat.")
    else:
        print("Barang tidak ditemukan.")
        
def hapus_barang():
    nama = input("Masukan nama barang yang ingin dihapus: ")
    if nama in inventaris:
        del inventaris[nama]
        print("Barang berhasil dihapus dari inventaris.")
    else:
        print("Barang tidak ditemukan.")
        
def analisis_data():
    if not inventaris:
        print("Inventaris kosong.")
        return
    
    barang_termahal = max(inventaris.items(), key=lambda x: x[1][0])
    barang_termurah = min(inventaris.items(), key=lambda x: x[1][0])
    
    total_nilai_stok = sum(harga * stok for harga, stok in inventaris.values())
    
    print("n--- Analisis Data ---")
    print(f"Barang Termahal: {barang_termahal[0]} (Rp {barang_termahal[1][0]:,.2f})")
    print(f"Barang Termurah: {barang_termahal[0]} (Rp {barang_termahal[1][0]:,.2f})")
    print(f"Total Nilai Stok: Rp {total_nilai_stok:,.2f}")
    
def menu():
    while True:
        print("/n=== Menu Inventaris Gudang ===")
        print("1. Tambah Barang Baru")
        print("2. Tampilkan Semua Barang")
        print("3. Cari Barang")
        print("4. Perbarui Stok Barang")
        print("5. Hapus Barang")
        print("6. Analisis Data")
        print("7. Keluar")
        
        pilihan = input("Pilih menu (1-7): ")
        if pilihan == '1':
            tambah_barang()
        elif pilihan == '2':
            tampilkan_semua()
        elif pilihan == '3':
            cari_barang()
        elif pilihan == '4':
            perbarui_stok()
        elif pilihan == '5':
            hapus_barang()
        elif pilihan == '6':
            analisis_data()
        elif pilihan == '7':
            print("Terimakasih kasih program selesai.")
            break
        else:
            print("Pilihan tidak valid, silahkan pilih antara 1 sampai 7")
            
menu()