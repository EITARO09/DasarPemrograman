matematika = int(input("masukan nilai matematika : "))
sains = int(input("masukan nilai sains : "))
inggris = int(input("masukan nilai inggris : "))
rata_rata = (matematika + sains + inggris) / 3

# Hitung jumlah mata pelajaran di bawah 70
jumlah_bawah_70 = 0
if matematika < 70:
    jumlah_bawah_70 += 1
if sains < 70:
    jumlah_bawah_70 += 1
if inggris < 70:
    jumlah_bawah_70 += 1

# Cek apakah ada nilai sempurna
nilai_sempurna = (matematika == 100 or sains == 100 or inggris == 100)

# Tentukan kelulusan
if rata_rata > 75 and jumlah_bawah_70 <= 1 and nilai_sempurna:
    print("Anda Lulus!")
else:
    print("Anda Tidak Lulus.")