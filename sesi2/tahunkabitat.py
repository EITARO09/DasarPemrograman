tahun = int(input("masukan tahun :"))
if (tahun % 400 ==0) :
    print(tahun,"tahun kabisat")
elif (tahun % 100 == 0):
    print(tahun,"bukan tahun kabisat")
elif (tahun % 4 == 0):
    print(tahun,"tahun kabisat")
else :
    print(tahun,"bukan tahun kabisat")