def konfersisuhu(suhu, dari="C", ke="R,F,K"):
    if dari == "C" and ke == "R":
        return (suhu - 32) * 5/9
    elif dari == "C" and ke == "F":
        return suhu + 32
    elif dari == "C" and ke == "K":
        return suhu + 273.15
    elif dari == "F" and ke == "R":
        return (suhu - 32) * 5/9
    elif dari == "F" and ke == "C":
        return (suhu - 32) * 5/9
    elif dari == "F" and ke == "K":
        return (suhu - 32) * 5/9 + 273.15
    elif dari == "K" and ke == "C":
        return suhu - 273.15
    elif dari == "K" and ke == "F":
        return (suhu - 273.15) * 9/5 + 32
    elif dari == "K" and ke == "R":
        return (suhu - 273.15) * 9/5
    elif dari == "R" and ke == "C":
        return (suhu * 9/5) + 32
    elif dari == "R" and ke == "F":
        return suhu * 9/5 + 32
    elif dari == "R" and ke == "K":
        return suhu * 9/5 + 273.15
    else:
        return "Invalid input"
    
suhu = float(input("Masukkan suhu: "))
dari = input("Masukkan skala dari (C, F, K, R): ")
ke = input("Masukkan skala ke (C, F, K, R): ")
hasil = konfersisuhu(suhu, dari, ke)
print(f"Suhu dalam {ke}: {hasil}")