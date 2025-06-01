def cek_tipe_input(input1, input2, input3):
    
    tipe_1 = isinstance(input1, str)
    tipe_2 = isinstance(input2, int)
    tipe_3 = isinstance(input3, float)

    
    if tipe_1 or tipe_2 or tipe_3:
        return "Tipe input valid"
    else:
        return "Tipe input tidak valid"
print(cek_tipe_input("Hello", 10, 3.14)) 
print(cek_tipe_input(10, "Hello", 3.14)) 
print(cek_tipe_input("Hello", 10.5, 3.14)) 
print(cek_tipe_input("Hello", 10, "3.14")) 
print(cek_tipe_input("World", 5, 2.718))