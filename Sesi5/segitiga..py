a = float(input("masukan angka pertama (cm):"))
b = float(input("masukan angka kedua (cm):"))
c = float(input("masukan angka ketiga (cm):"))
if a == b == c :
    print("segitiga sama sisi")
elif a == b or a == c or b == c :
    print("segitiga sama kaki")
else :
    print("segitiga sembarang")