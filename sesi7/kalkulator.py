def kalkulator():
    print("Pilih operator:")
    print("1. +")
    print("2. -")
    print("3. *")
    print("4. /")
    
    pilihan = input("Masukkan pilihan (1/2/3/4): ")
    
    if pilihan in ('1', '2', '3', '4'):
        try:
            angka1 = float(input("Masukkan angka pertama: "))
            angka2 = float(input("Masukkan angka kedua: "))
        except ValueError:
            print("Input tidak valid! Harap masukkan angka.")
            return
        
        if pilihan == '1':
            hasil = angka1 + angka2
            operasi = "+"
        elif pilihan == '2':
            hasil = angka1 - angka2
            operasi = "-"
        elif pilihan == '3':
            hasil = angka1 * angka2
            operasi = "*"
        elif pilihan == '4':
            if angka2 != 0:
                hasil = angka1 / angka2
                operasi = "/"
            else:
                print("Error! Kamu tidak bisa membagi dengan 0.")
                return
        
        print(f"Hasil dari {angka1} {operasi} {angka2} = {hasil}")
    else:
        print("Pilihan tidak valid! Silakan pilih 1, 2, 3, atau 4.")


kalkulator()