sentence = '''Tim Hukum KPK meminta penundaan sidang praperadilan jilid II Sekjen PDIP Hasto Kristiyanto terkait penetapan status tersangka.
Kuasa hukum Hasto berharap penundaan itu bukan akal-akalan KPK untuk menyelesaikan berkas perkara.'''
sentence_2 = '''Tentu kita harapkan bahwa ini bukan akal-akalan ya, agar supaya KPK bisa menyelesaikan berkas perkara. 
Kemudian, mereka melimpahkan berkas perkara itu sehingga nanti seolah-olah permohonan praperadilan ini akan diputus dengan cara mengatakan bahwa ini sudah, apa ya, karena berkas perkaranya sudah digugurkan mengingat berkas perkara, perkara pokok, sudah dilimpahkan ke pengadilan," kata kuasa hukum Hasto, Maqdir Ismail, usai sidang di Pengadilan Negeri Jakarta Selatan'''

sentence = sentence.split(' ')
short_sentence = ' '.join(sentence[:6])
print(short_sentence)

sentence = sentence_2.split(' ')
short_sentence = ' '.join(sentence[:6])
print(short_sentence)