import pandas as pd

#1
data = pd.read_excel('data_penjualan.xlsx')
print("5 baris pertama")
print(data.head())

#2
data['Total Harga'] = data['Jumlah'] * data['Harga Satuan']
print("\nData dengan Total Harga:")
print(data.head())

#3
data_elektronik = data[data['Kategori'] == 'Elektronik']
data_elektronik.to_excel('elektronik.xlsx', index=False)
print("\nData elektronik disimpan di elektronik.xlsx")

#4
rekap = data.groupby('Kategori')['Total Harga'].sum().reset_index()
rekap.columns = ['Kategori', 'Total Pendapatan']
print("\nRekapitulasi Total Pendapatan Per Kategori:")
print(rekap)

#5
data_sorted = data.sort_values(by='Total Harga', ascending=False)
data_sorted.to_excel('penjualan_terurut.xlsx', index=False)
print("\nData penjualan terurut berdasarkan total harga disimpan di penjualan_terurut.xlsx")