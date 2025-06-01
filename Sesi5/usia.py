usia = int(input("masukan usia bayi : "))
kategori = 'bayi, balita, anak anak ,remaja, dewasa'
if (usia > 0 and usia <= 2):
    kategori = 'bayi'
elif (usia <= 5 and usia > 2):
    kategori = 'balita'
elif (usia <= 12 and usia > 5):
    kategori = 'anak anak '
elif (usia <= 18 and usia > 12):
    kategori = 'remaja'
elif (usia <= 60 and usia > 18):
    kategori = 'dewasa'

print ("kategori usia bayi adalah : ", kategori)