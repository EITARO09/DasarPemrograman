def konfersiSuhu(suhu, dari="C", ke="R"):
    if dari == "C" and ke == "R":
        return 4/5*suhu
    elif dari == "R" and ke == "C":
        return 5/4*suhu
    elif dari == "C" and ke == "F":
        return (suhu*9/5)+32
    elif dari == "F" and ke == "C":
        return (suhu-32)*5/9
    else:
        return "Konversi tidak tersedia"
    print (konfersiSuhu(30, "C", "F"))