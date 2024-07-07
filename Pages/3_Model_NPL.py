import streamlit as st
import numpy as np

# Define the logistic regression model coefficients
coefficients = {
    '(Intercept)': -10.203,
    'dummy.wilayah.1': 0.198,
    'dummy.wilayah.3': 0.265,
    'dummy.wilayah.4': 0.231,
    'dummy.wilayah.5': -0.173,
    'dummy.wilayah.6': -1.929,
    'P05.coded': -0.494,
    'P08': 0.023,
    'P20': 0.152,
    'P26.coded': 0.616,
    'P30': -0.023,
    'P32.1.coded': -0.102,
    'P33.coded': 0.083,
    'P37': -0.000,
    'P48': 0.013,
    'P49': 0.051,
    'P51.coded': 3.395,
    'P54.coded': -1.114,
    'P56.1.coded': 3.790,
    'P56.2': 0.061,
    'P58.1.coded': 0.277,
    'P60.1.coded': 0.047,
    'P68.1.coded': -0.087
}

# Define the logistic function
def logistic_function(x):
    return 1 / (1 + np.exp(-x))

# Define the prediction function
def predict(features):
    intercept = coefficients['(Intercept)']
    logit = intercept
    for feature_name, feature_value in features.items():
        logit += coefficients[feature_name] * feature_value
    probability = logistic_function(logit)
    return probability

# Streamlit app
st.title('Model Prediksi NPL berdasarkan Karakteristik Debitur')
st.write("Input data terkait Debitur yang ingin diprediksi apakah akan NPL/tidak:")

# User input for features
st.markdown('#### Wilayah Debitur')
wilayah = st.selectbox('', ['Wilayah 1', 'Wilayah 2', 'Wilayah 3', 'Wilayah 4', 'Wilayah 5', 'Wilayah 6'], index=0)
st.write(f"Debitur berada di {wilayah}")
wilayah_features = {
    'dummy.wilayah.1': 0,
    'dummy.wilayah.3': 0,
    'dummy.wilayah.4': 0,
    'dummy.wilayah.5': 0,
    'dummy.wilayah.6': 0
}
if wilayah == 'Wilayah 1':
    wilayah_features['dummy.wilayah.1'] = 1
elif wilayah == 'Wilayah 3':
    wilayah_features['dummy.wilayah.3'] = 1
elif wilayah == 'Wilayah 4':
    wilayah_features['dummy.wilayah.4'] = 1
elif wilayah == 'Wilayah 5':
    wilayah_features['dummy.wilayah.5'] = 1
elif wilayah == 'Wilayah 6':
    wilayah_features['dummy.wilayah.6'] = 1

st.markdown('#### Apakah usaha Debitur sudah memiliki NIB (Nomor Izin Berusaha) atau SKU (Surat Keterangan Usaha)?')
p05_coded = st.selectbox('', ['Sudah', 'Belum'], index=0)
st.write(f"Debitur {p05_coded} memiliki NIB atau SKU")
p05_coded = 1 if p05_coded == 'Sudah' else 0

st.markdown('#### Berapa banyaknya karyawan yang aktif di Usaha Debitur saat ini?')
p08 = st.number_input('', min_value=0, max_value=100, value=25, key='p08')
st.write(f"Jumlah karyawan di usaha debitur adalah sebanyak: {p08} orang")

st.markdown('#### Berapa jumlah tanggungan (di luar keluarga inti seperti anak dan istri) Debitur saat ini?')
p20 = st.number_input('', min_value=0, max_value=100, value=5, key='p20')
st.write(f"Jumlah tanggungan Debitur saat ini adalah sebanyak: {p20} orang")

st.markdown('#### Apa Lapangan usaha pekerajaan utama Debitur?')
p26_coded = st.selectbox('', ['Ya', 'Tidak'], index=0)
st.write(f"Debitur {p26_coded} memiliki pekerjaan tetap")
p26_coded = 1 if p26_coded == 'Ya' else 0

st.markdown('#### Berapa pengeluaran per bulan debitur (dalam ribuan)?')
p30 = st.number_input('', min_value=0, max_value=100000, value=5000, key='p30')
st.write(f"Pengeluaran per bulan debitur adalah sebesar: Rp {(p30 * 1000):,}".replace(',', '.'))

st.markdown('#### Apakah Debitur memiliki riwayat kredit buruk?')
p32_1_coded = st.selectbox('', ['Ya', 'Tidak'], index=0)
st.write(f"Debitur {p32_1_coded} memiliki riwayat kredit buruk")
p32_1_coded = 1 if p32_1_coded == 'Ya' else 0

st.markdown('#### Apakah Debitur memiliki agunan?')
p33_coded = st.selectbox('', ['Ya', 'Tidak'], index=0)
st.write(f"Debitur {p33_coded} memiliki agunan")
p33_coded = 1 if p33_coded == 'Ya' else 0

st.markdown('#### Berapa rata-rata biaya listrik rumah tinggal Debitur (dalam ribuan)?')
p37 = st.number_input('', min_value=0, max_value=10000, value=10, key='p37')
st.write(f"Rata-rata biaya listrik rumah tinggal Debitur adalah sebesar: Rp {(p37 * 1000):,}".replace(',', '.'))

st.markdown('#### Berapa jangka waktu pinjaman atau tenornya (dalam bulan)?')
p48 = st.number_input('', min_value=0, max_value=100, value=12, key='p48')
st.write(f"Jangka waktu pinjaman debitur adalah selama: {p48} bulan")

st.markdown('#### Berapa suku bunga pinjamannya (dalam % per tahun)?')
p49 = st.number_input('', min_value=0, max_value=100, value=1, key='p49')
st.write(f"Suku bunga pinjaman debitur adalah sebesar: {p49}% per tahun")

st.markdown('#### Apakah Debitur memiliki asuransi kredit?')
p51_coded = st.selectbox('', ['Ya', 'Tidak'], index=0)
st.write(f"Debitur {p51_coded} memiliki asuransi kredit")
p51_coded = 1 if p51_coded == 'Ya' else 0

st.markdown('#### Apakah Debitur memiliki pinjaman lain?')
p54_coded = st.selectbox('', ['Ya', 'Tidak'], index=0)
st.write(f"Debitur {p54_coded} memiliki pinjaman lain")
p54_coded = 1 if p54_coded == 'Ya' else 0

st.markdown('#### Apakah Debitur pernah menunggak angsuran pinjaman sebelumnya?')
p56_1_coded = st.selectbox('', ['Ya', 'Tidak'], index=0)
st.write(f"Debitur {p56_1_coded} pernah menunggak angsuran pinjaman sebelumnya")
p56_1_coded = 1 if p56_1_coded == 'Ya' else 0

st.markdown('#### Berapa banyak pinjaman yang sedang berjalan?')
p56_2 = st.number_input('', min_value=0, max_value=10, value=1, key='p56_2')
st.write(f"Debitur memiliki {p56_2} pinjaman yang sedang berjalan")

st.markdown('#### Apakah Debitur memiliki riwayat gangguan kesehatan?')
p58_1_coded = st.selectbox('', ['Ya', 'Tidak'], index=0)
st.write(f"Debitur {p58_1_coded} memiliki riwayat gangguan kesehatan")
p58_1_coded = 1 if p58_1_coded == 'Ya' else 0

st.markdown('#### Apakah Debitur pernah mengajukan penambahan jumlah pinjaman sebelum jatuh tempo (suplesi)?')
p60_1_coded = st.selectbox('', ['Ya', 'Tidak'], index=0)
st.write(f"Debitur {p60_1_coded} mengajukan penambahan jumlah pinjaman sebelum jatuh tempo")
p60_1_coded = 1 if p60_1_coded == 'Ya' else 0

st.markdown('#### Apakah Debitur memiliki tanggungan keluarga?')
p68_1_coded = st.selectbox('', ['Ya', 'Tidak'], index=0)
st.write(f"Debitur {p68_1_coded} memiliki tanggungan keluarga")
p68_1_coded = 1 if p68_1_coded == 'Ya' else 0

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
    probability = predict(input_features)
    st.markdown(f"#### Berdasarkan Model Regresi Logistik, peluang Debitur tersebut untuk NPL adalah: {(probability * 100):.2f}%. Besar kemungkinannya, Debitur tersebut akan {'NPL' if probability > 0.5 else 'PL'}.")
