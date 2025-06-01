berat_badan= float(input("masukan berat badan (kg) :"))
tinggi_badan = float(input("masukan tinggi badan (m) :"))
BMI = berat_badan / (tinggi_badan ** 2)
if BMI < 18.5 :
    print("berat badan kurang")
elif 18.5 <= BMI < 25.0 :
    print("berat badan normal")
elif 25.0 <= BMI < 30.0 :
    print("berat badan berlebihan")
elif 30.0 >= BMI :
    print("berat badan obesitas")

