total_belanja = float(input("Masukkan total belanjaan Anda: "))
diskon = 0
if total_belanja > 100000:
    diskon = 0.10
elif total_belanja > 50000:
    diskon = 0.05
else:
    diskon = 0.0
total_diskon = total_belanja * diskon
total_setelah_diskon = total_belanja - total_diskon
print(f"Total belanjaan: Rp {total_belanja:.2f}")
print(f"Diskon yang didapat: Rp {total_diskon:.2f}")
print(f"Total yang harus dibayar: Rp {total_setelah_diskon:.2f}")