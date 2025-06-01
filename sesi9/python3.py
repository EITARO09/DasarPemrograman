import array as arr

angka = arr.array('f', [])

for i in range(10):
    num = float(input(f"Masukkan angka ke-{i+1}: "))
    angka.append(num)

jumlah = sum(angka)

print("Array angka:", angka.tolist())
print("Jumlah semua elemen dalam array:", jumlah)
