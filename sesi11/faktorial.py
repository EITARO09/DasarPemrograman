def faktorial(n):
    if n <= 1:
        return 1
    else :
        return n * faktorial(n-1)
    
angka = int(input("Masukkan angka: "))
hasil_faktorial = faktorial(angka)
print("Faktorial dari", angka, "adalah", hasil_faktorial)