tahun = int(input("masukan tahun : "))
if tahun % 4 == 0 and (tahun % 100 != 0 or tahun % 400 == 0 ):
    print("tahun ini adalah tahun kabisat")
else :
    print("tahun ini bukan tahun kabisat")