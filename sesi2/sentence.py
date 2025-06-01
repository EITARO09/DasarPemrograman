sentence = "Penculikan, Pembunuhan, dan Penyiksaan"
word = sentence.split (", ")
print (word)

def clean_word(word) :
    return word.strip()

cleaned_word = list(map(clean_word, word))
print (cleaned_word)

print(",". join(cleaned_word)) #untuk merapikan