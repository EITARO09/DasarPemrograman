def hitung_angka_ganjil(r) :
    return sum(1 for x in r if x % 2 != 0)
data = (1,2,3,4,5,6)
Angka_ganjil = hitung_angka_ganjil(data)
print(f"Jumlah angka ganjil {data} adalah {Angka_ganjil}")
