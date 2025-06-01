name = input("masukan nama minimal 7 karakter :")
if len (name) < 7 :
    print("nama kurang dari 7 karakter :")
else:
    for i in range (len(name)):
        print(name[:i + 1] +'*' * (7 - (i + 1))  )