username = input("Masukkan username: ")
password = input("Masukkan password: ")

if username == "admin" and password == "admin123":
    print("Login Admin")
elif username == "user" and password == "user123":
    print("Akses Terbatas")
elif username == "guest" and password == "":
    print("Akses minimal")
else :
    print("Akses Ditolak")