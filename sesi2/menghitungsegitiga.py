alas = float(input("Masukkan panjang alas segitiga: "))
tinggi = float(input("Masukkan tinggi segitiga: "))
luas = 0.5 * alas * tinggi
sisi_miring = (alas**2 + tinggi**2) ** 0.5
keliling = alas + tinggi + sisi_miring 
print("Luas segitiga siku-siku:", luas)
print("Keliling segitiga siku-siku:", keliling)