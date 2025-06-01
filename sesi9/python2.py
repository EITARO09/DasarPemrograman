name = 'nugraha'
total = len (name)
name = name.upper()
#print = (name[0:1])
#print = (name[0:2])
#print = (name[:3])
for i in range (total):
    print(name[:total - i] + '-' *i)