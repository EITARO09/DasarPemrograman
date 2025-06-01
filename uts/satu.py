harga_mesin = int(input("masukan harga mesin:"))
nilai_sisa = int(input ("masukan nilai sisa :"))
masa = int(input("masukan masa :"))

penyusutan = (harga_mesin - nilai_sisa) / masa
penyusutan_2_tahun = (penyusutan * 2)
asset_tersisa = (harga_mesin - penyusutan_2_tahun)
print("nilai aset tersisa" ,asset_tersisa)