from datetime import datetime
def hitungumur(tahunlahir):
    tahunsekarang = datetime.now().year
    umur = tahunsekarang - tahunlahir
    return umur
tahunlahir = int(input("masukan tahun lahir:"))
umur = hitungumur(tahunlahir)
print("umur anda",umur,"tahun")