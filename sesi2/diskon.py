harga_awal = int(input("masukan harga produk : "))
diskon = int(input("masukan diskon : "))
setelah_diskon = int((100-diskon)/100*harga_awal)
print(f"total yang harus dibayar setelah diskon adalah : ", setelah_diskon)