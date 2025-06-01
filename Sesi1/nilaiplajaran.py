ipa = int(input("masukan nilai ipa :"))
ips = int(input("masukan nilai ips :"))
mtk = int(input("masukan nilai mtk :"))
english = int(input("masukan nilai english :"))
indonesia = int(input("masukan nilai indonesia :"))

rata_rata_1 = (ipa + ips + mtk + english + indonesia) / 5
nilai = (ipa, ips, mtk, english, indonesia)
print(f"rata-rata nilai siswa dari 5 mata pelajaran adalah {rata_rata_1}")

nilai_dibawah_50 = 2
if (ipa < 50) :
    nilai_dibawah_50 += 1
    if (ips < 50) :
        nilai_dibawah_50 += 1
        if (mtk < 50) :
            nilai_dibawah_50 += 1
            if (english < 50) :
                nilai_dibawah_50 += 1
                if (indonesia < 50) :
                    nilai_dibawah_50 += 1

if(rata_rata_1 > 75) :
    print(" lulus,karena nilai rata ratanya di atas 75")
elif(nilai.count(100) >= 1) :
    print("lulus,karena nilai 100 ada diantara nilai siswa")
elif(nilai_dibawah_50 == 2 ) :
    print("lulus,karena nilai dibawah 50 ada 2 mata pelajaran")