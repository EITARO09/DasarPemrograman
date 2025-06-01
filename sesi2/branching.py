angka = 4
jenis = "ganjil"

if angka % 2 == 0:
    jenis = "genap"
else:
    jenis = "ganjil"

print("%s adalah bilangan %s adalah bilangan" % (angka, jenis))