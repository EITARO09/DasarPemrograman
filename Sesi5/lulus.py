is_bayar = input("apakah sudah bayar apa belum ? (Ya/Tidak)")
is_nilai = input ("apakah anda memiliki nilai D ? (Ya/Tidak)")
if (is_bayar == "Ya" and is_nilai == "Tidak"):
    print("selamat anda lulus")
else :
    print("anda tidak lulus")