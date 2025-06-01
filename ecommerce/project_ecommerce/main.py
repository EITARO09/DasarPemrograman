from ecommerce.pricing import hitung_diskon, hitung_total, hitung_pajak
from ecommerce.order import generate_order_id

def main():
    nama_pelanggan = input("masukan nama pelanggan :")
    nama_produk = input("masukan nama produk :")
    harga_asli = float(input("masukan harga asli :"))
    persentase_diskon = float(input("masukan persentase diskon :"))
    persentase_pajak = float(input("masukan persentase pajak :"))

    diskon = harga_asli * (persentase_diskon / 100)
    total = hitung_total(harga_asli, persentase_diskon, persentase_pajak)
    order_id = generate_order_id()

    print("="*40)
    print(" RINCIAN PEMBELIAN")
    print("="*40)
    print(f"{'ID pesanan' :20} {order_id}")
    print(f"{'Nama Pelanggan' :20} {nama_pelanggan}")
    print(f"{'Nama Produk' :20} {nama_produk}")
    print(f"{'Harga Asli' :20} {harga_asli:,.2f}")
    print(f"{'Diskon' :20} Rp {diskon:,.2f}")
    print(f"{'Pajak' :20}  Rp {hitung_pajak(harga_asli - diskon, persentase_pajak):,.2f}")
    print("=" *40)
    print(f"{'Total Belanja' :20} Rp {total:,.2f}")
    print("=" *40)

if __name__ == "__main__":
    main()