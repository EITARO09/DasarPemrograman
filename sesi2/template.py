hello_template = "hello , nama saya %s, saya dari %s , umur saya %s , saya suka %s"
print(hello_template % ("zacky", "Indonesia ", 19, "main game"))

template_2 = "hello ,nama saya {name} asal dari {address}"
print (template_2.format(name="zacky", address="Indonesia"))