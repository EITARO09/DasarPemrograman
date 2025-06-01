x = input("Masukkan nilai untuk x: ")
y = input("Masukkan nilai untuk y: ")

bool_x = bool(x)
bool_y = bool(y)

print(f"x AND y: {bool_x and bool_y}")
print(f"x OR y: {bool_x or bool_y}")
print(f"NOT x: {not bool_x}")
print(f"x XOR y: {bool_x != bool_y}")

print("\nPenjelasan:")
print(f"Nilai x: {x} (Boolean: {bool_x})")
print(f"Nilai y: {y} (Boolean: {bool_y})")