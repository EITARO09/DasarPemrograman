import pandas as pd
import matplotlib.pyplot as plt

file_path = 'Data_Penduduk.xlsx'
df = pd.read_excel(file_path)

grouped = df.groupby(['Pendidikan_Terakhir', 'Jenis_Kelamin']).size().unstack(fill_value=0)

grouped.plot(kind='bar', figsize=(10,6))

plt.title('Jumlah Warga Bedasarkan Pendidika Terakhir dan Jenis Kelamain')
plt.xlabel('Pendidikan Terakhir')
plt.ylabel('Jumlah Warga')
plt.xticks(rotation=45)
plt.legend(title='Jenis Kelamin')
plt.tight_layout()
plt.show()