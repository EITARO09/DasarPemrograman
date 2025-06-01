nilai = int(input("masukan nilai anda :"))
if nilai >= 80 and nilai <= 100 :
    grade = "A"
if nilai >= 70 and nilai <= 79 :
    grade = "B"
if nilai >= 60 and nilai <= 69 :
    grade = "C"
if nilai >= 50 and nilai <= 59 :
    grade = "D"
if nilai >= 0 and nilai <= 49 :
    grade = "E"
print ("nilai anda adalah", nilai, "grade anda adalah", grade)