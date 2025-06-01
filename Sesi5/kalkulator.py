angka_1 = float(input("masukan angka 1 : "))
operator = input("masukan operator (+, -, *, /) : ")
angka_2 = float(input("masukan angka 2 : "))


if operator == "+":
    hasil = angka_1 + angka_2
    print (f"{angka_1} + {angka_2} = {hasil}")
elif operator == "-":
    hasil = angka_1 - angka_2
    print (f"{angka_1} - {angka_2} = {hasil}")
elif operator == "*":
    hasil = angka_1 * angka_2
    print (f"{angka_1} * {angka_2} = {hasil}")
elif operator == "/":
    if angka_2 == 0:
        print("error! kamu tidak bisa membagi dengan 0")
elif operator == "/":
    hasil = angka_1 / angka_2
    print (f"{angka_1} / {angka_2} = {hasil}")
else :
    print("operator tidak valid")