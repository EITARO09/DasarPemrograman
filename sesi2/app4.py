nilai = int(input("masukan nilai :"))
grade = 'E'
if nilai >= 85 :
    grade = 'A'
elif nilai >= 75 :
    grade = 'B'
elif nilai >= 65 :
    grade = 'C'
elif nilai >= 55 :
    grade = 'D'

print ("grade anda adalah ", grade)