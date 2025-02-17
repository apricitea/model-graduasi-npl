import streamlit as st
from utilities import coefficients_npl
from utilities import predict

# Streamlit app
st.title('Model Prediksi NPL berdasarkan Karakteristik Debitur')
st.write("Input data terkait Debitur yang ingin diprediksi apakah akan NPL/tidak:")

# User input for features
st.markdown('#### Wilayah Debitur')
wilayah = st.selectbox('Wilayah', ['Sumatera', 'Jawa', 'Bali & Nusa Tenggara', 'Kalimantan', 'Sulawesi', 'Maluku & Papua'], index=0, label_visibility="collapsed")
st.write(f"Debitur berada di {wilayah}")
wilayah_features = {'dummy.wilayah.1': 0,'dummy.wilayah.3': 0,'dummy.wilayah.4': 0,'dummy.wilayah.5': 0,'dummy.wilayah.6': 0}
if wilayah == 'Sumatera':
    wilayah_features['dummy.wilayah.1'] = 1
elif wilayah == 'Bali & Nusa Tenggara':
    wilayah_features['dummy.wilayah.3'] = 1
elif wilayah == 'Kalimantan':
    wilayah_features['dummy.wilayah.4'] = 1
elif wilayah == 'Sulawesi':
    wilayah_features['dummy.wilayah.5'] = 1
elif wilayah == 'Maluku & Papua':
    wilayah_features['dummy.wilayah.6'] = 1

st.markdown('#### Apakah usaha Debitur sudah memiliki NIB (Nomor Izin Berusaha) atau SKU (Surat Keterangan Usaha)?')
p05_coded = st.selectbox('NIB/SKU Status', ['Sudah', 'Dalam proses pembuatan', 'Belum'], index=0, key='p05', label_visibility="collapsed")
st.write(f"Debitur {p05_coded} memiliki NIB atau SKU")
p05_coded = 2 if p05_coded == 'Sudah' else 1

st.markdown('#### Berapa banyaknya karyawan yang aktif di Usaha Debitur saat ini?')
p08 = st.number_input('Jumlah Karyawan', min_value=0, max_value=10000, value=2, key='p08', label_visibility="collapsed")
st.write(f"Jumlah karyawan di usaha debitur adalah sebanyak: {p08} orang")

st.markdown('#### Berapa jumlah tanggungan (di luar keluarga inti seperti anak dan istri) Debitur saat ini?')
p20 = st.number_input('Jumlah Tanggungan', min_value=0, max_value=100, value=2, key='p20', label_visibility="collapsed")
st.write(f"Jumlah tanggungan Debitur saat ini adalah sebanyak: {p20} orang")

st.markdown('#### Apa Lapangan usaha pekerajaan utama Debitur?')
p26_coded = st.selectbox('Lapangan Usaha', [
    'Industri pengolahan', 
    'Jasa-jasa (konstruksi, pengangkutan, akomodasi)', 
    'Pertanian (tanaman pangan, perkebunan, peternakan, perikanan, kehutanan), dan Pertambangan',
    'Perdagangan besar dan eceran',
    'Lainnya'], index=0, key='p26', label_visibility="collapsed")
st.write(f"Lapangan usaha pekerjaan utama Debitur adalah: {p26_coded}")
p26_coded = 1 if p26_coded == 'Pertanian (tanaman pangan, perkebunan, peternakan, perikanan, kehutanan), dan Pertambangan' else 2

st.markdown('#### Berapa lama Debitur telah bekerja sejak dari pekerjaan pertama sampai dengan pekerjaan terakhir saat ini (dalam tahun)?')
p30 = st.number_input('Lama Bekerja (tahun)', min_value=0, max_value=100, value=1, key='p30', label_visibility="collapsed")
st.write(f"Debitur telah bekerja selama: {p30} tahun")

st.markdown('#### Berapa rata-rata pendapatan bersih per bulan Debitur dari Pekerjaan utama?')
p32_1_coded = st.number_input('Pendapatan Bersih Bulanan', min_value=0, max_value=1000000000, value=1, key='p32_1', label_visibility="collapsed")
st.write(f"Rata-rata pendapatan bersih per bulan Debitur adalah sebesar: Rp {p32_1_coded}".replace(',', '.'))

st.markdown('#### Berapa rata-rata Pengeluaran per bulan Debitur (diluar angsuran dan tabungan)?')
p33_coded = st.number_input('Pengeluaran Bulanan', min_value=0, max_value=1000000000, value=1, key='p33', label_visibility="collapsed")
st.write(f"Rata-rata Pengeluaran per bulan Debitur adalah sebesar: Rp {p33_coded}".replace(',', '.'))

st.markdown('#### Berapa rata-rata biaya atau pembayaran listrik rumah tinggal Debitur per bulan (dalam ribuan)?')
p37 = st.number_input('Pembayaran Listrik Bulanan', min_value=0, max_value=1000000000, value=1, key='p37', label_visibility="collapsed")
st.write(f"Rata-rata biaya atau pembayaran listrik rumah tinggal Debitur per bulan adalah sebesar: Rp {(p37 * 1000):,}".replace(',', '.'))

st.markdown('#### Berapa jangka waktu pinjaman atau tenor Debitur (dalam bulan)?')
p48 = st.number_input('Tenor Pinjaman (bulan)', min_value=0, max_value=100, value=1, key='p48', label_visibility="collapsed")
st.write(f"Jangka waktu pinjaman debitur adalah selama: {p48} bulan")

st.markdown('#### Berapa suku bunga pinjaman Debitur (dalam % per tahun)?')
p49 = st.number_input('Suku Bunga Pinjaman (%)', min_value=0, max_value=100, value=1, key='p49', label_visibility="collapsed")
st.write(f"Suku bunga pinjaman debitur adalah sebesar: {p49}% per tahun")

st.markdown('#### Dengan pendapatan bersih dari pekerjaan utama, apakah Debitur mampu membayar angsuran?')
p51_coded = st.selectbox('Kemampuan Membayar Angsuran', ['Mampu', 'Kurang mampu', 'Tidak mampu'], index=0, label_visibility="collapsed")
st.write(f"Debitur {p51_coded} membayar angsuran dengan penghasilan dari pekerjaan utama")
p51_coded = 1 if p51_coded == 'Mampu' else 2

st.markdown('#### Apa alasan Debitur berganti jenis pinjaman dari KUR ke Kupedes/Pinjaman Komersial?')
p54_coded = st.selectbox('Alasan Berganti Jenis Pinjaman', [
    'Atas saran/arahan dari mantri', 
    'Kebutuhan dana lebih besar dari plafon KUR yang tersedia', 
    'Terpaksa karena KUR tidak tersedia',
    'Usaha berkembang dan sudah mampu meminjam pinjaman komersial',
    'Lainnya'], index=0, key='p54', label_visibility="collapsed")
st.write(f"Alasan Debitur berganti jenis pinjaman dari KUR ke Kupedes/Pinjaman Komersial adalah: {p54_coded}")
p54_coded = 1 if p54_coded in ['Kebutuhan dana lebih besar dari plafon KUR yang tersedia','Usaha berkembang dan sudah mampu meminjam pinjaman komersial'] else 0

st.markdown('#### Apakah Debitur pernah menunggak angsuran pinjaman sebelumnya?')
p56_1_coded = st.selectbox('Menunggak Angsuran Sebelumnya', ['Pernah', 'Tidak pernah'], index=0, key='p56_1', label_visibility="collapsed")
st.write(f"Debitur {p56_1_coded} menunggak angsuran pinjaman sebelumnya")
p56_1_coded = 2 if p56_1_coded == 'Pernah' else 1

st.markdown('#### Berapa kali Debitur pernah menunggak/tdk membayar angsuran?')
p56_2 = st.number_input('Jumlah Menunggak Angsuran', min_value=0, max_value=100, value=1, key='p56_2', label_visibility="collapsed")
st.write(f"Debitur menunggak angsuran sebanyak: {p56_2} kali")

st.markdown('#### Sejak pencairan pinjaman, apakah Debitur pernah mengajukan perpanjangan jangka waktu pinjaman?')
p58_1_coded = st.selectbox('Perpanjangan Jangka Waktu Pinjaman', ['Pernah', 'Tidak pernah'], index=0, key='p58_1', label_visibility="collapsed")
st.write(f"Debitur {p58_1_coded} mengajukan perpanjangan jangka waktu pinjaman")
p58_1_coded = 2 if p58_1_coded == 'Pernah' else 1

st.markdown('#### Apakah Debitur pernah mengajukan penambahan jumlah pinjaman sebelum jatuh tempo (suplesi)?')
p60_1_coded = st.selectbox('Penambahan Jumlah Pinjaman', ['Pernah', 'Tidak pernah'], index=0, key='p60_1', label_visibility="collapsed")
st.write(f"Debitur {p60_1_coded} mengajukan penambahan jumlah pinjaman sebelum jatuh tempo")
p60_1_coded = 2 if p60_1_coded == 'Pernah' else 1

st.markdown('#### Bagaimanakah rata-rata penjualan atau omset usaha Debitur saat ini dibandingkan dengan sebelum pandemi Covid-19 (tahun 2019)?')
p68_1_coded = st.selectbox('Omset Usaha Saat Ini', [
    'Masih dibawah rata-rata sebelum pandemi',
    'Sama dengan rata-rata sebelum pandemi', 
    'Sudah diatas rata-rata sebelum pandemi', 
    'Tidak relevan'], index=0, key='p68_1', label_visibility="collapsed")
st.write(f"Rata-rata penjualan atau omset usaha Debitur saat ini {p68_1_coded}")
p68_1_coded = 1 if p68_1_coded == 'Sudah diatas rata-rata sebelum pandemi' else 0

# Create a dictionary of the input features
input_features = {
    **wilayah_features,
    'P05.coded': p05_coded,
    'P08': p08,
    'P20': p20,
    'P26.coded': p26_coded,
    'P30': p30,
    'P32.1.coded': p32_1_coded,
    'P33.coded': p33_coded,
    'P37': p37,
    'P48': p48,
    'P49': p49,
    'P51.coded': p51_coded,
    'P54.coded': p54_coded,
    'P56.1.coded': p56_1_coded,
    'P56.2': p56_2,
    'P58.1.coded': p58_1_coded,
    'P60.1.coded': p60_1_coded,
    'P68.1.coded': p68_1_coded
}

# Prediction button
if st.button('Buat Prediksi'):
    probability = predict(input_features, coefficients_npl)
    st.markdown(f"#### Berdasarkan Model Regresi Logistik, probabilitas Debitur tersebut untuk NPL adalah: {(probability * 100):.2f}%. Besar kemungkinannya, Debitur tersebut akan {'NPL' if probability > 0.5 else 'PL'}.")
