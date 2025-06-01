x = int(input("masukan nilai x :"))
y = int(input("masukan nilai y :"))
print(f"Sebelum ditukar: x = {x}, y = {y}")
x = x + y
y = x - y
x = x - y
print(f"setelah ditukar : x = {x}, y = {y}")
