a = int(input("masukan bilangan bulat a :"))
b = int(input("masukan bilangan bulat b :"))
c = int(input("masukan bilangan bulat c :"))

kondisi_a = (a > b) or (a > c)
kondisi_b = (a % 2 == 0 or c % 2 != 0)
kondisi_c = (b != c)

if kondisi_a or kondisi_b or kondisi_c:
    print("kondisi terpenuhi")
else:
    print("kondisi tidak terpenuhi")

