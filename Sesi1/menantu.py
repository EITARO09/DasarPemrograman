is_tampan = input("Apakah kamu tampan? (Ya/Tidak) ")
is_kaya = input("Apakah kamu kaya? (Ya/Tidak) ")
is_soleh = input("Apakah kamu soleh? (Ya/Tidak) ")
is_pinter = input("Apakah kamu pinter? (Ya/Tidak) ")
is_setia = input("Apakah kamu setia? (Ya/Tidak) ")
jumlahyes = 0;

if (is_tampan == "Ya" or is_tampan == "ya"):
    jumlahyes += 1

if (is_kaya == "Ya" or is_kaya == "ya"):
    jumlahyes += 1

if (is_soleh == "Ya" or is_soleh == "ya"):
    jumlahyes += 1

if (is_pinter == "Ya" or is_pinter == "ya"):
    jumlahyes += 1
    
if (is_setia == "Ya" or is_setia == "ya"):
    jumlahyes += 1

if (jumlahyes >=3) :
    print("Kamu lolos menjadi calon suami")
else:
    print("Kamu tidak lolos menjadi calon suami")
