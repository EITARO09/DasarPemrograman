harga_dasar = 2500000
harga_jual = 3000000
jumlah_domba = int(input("Masukkan jumlah domba yang dijual: "))
total_modal = jumlah_domba * harga_dasar
total_pendapatan = jumlah_domba * harga_jual
keuntungan = total_pendapatan - total_modal
print(f"\nTotal modal yang dikeluarkan: Rp {total_modal:,}")
print(f"Total pendapatan dari penjualan: Rp {total_pendapatan:,}")
print(f"Keuntungan yang didapatkan: Rp {keuntungan:,}")