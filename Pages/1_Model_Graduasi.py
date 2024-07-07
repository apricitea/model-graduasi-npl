import streamlit as st
import numpy as np

# Define the logistic regression model coefficients
coefficients = {
    '(Intercept)': -1.48335383,
    'P60.1.grouped': 0.227968,
    'P56.1.grouped': -0.220847,
    'P54.grouped': 1.119103,
    'P50': 0.064132,
    'P49': 0.205027,
    'P48': -0.278749,
    'P37_rasio2': -0.06346,
    'P37': 0.0026,
    'P17': 0.29341,
    'P03.grouped': 0.289041,
    'P44_rasio1': -0.173606
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
st.title('Model Prediksi Graduasi berdasarkan Karakteristik Debitur')
st.write("Input data terkait Debitur yang ingin diprediksi apakah akan graduasi/tidak: ")

# User input for features
st.markdown('#### Apakah Debitur pernah mengajukan penambahan jumlah pinjaman sebelum jatuh tempo (suplesi)?')
p60_1_grouped = st.selectbox('', ['Pernah', 'Tidak Pernah'], index=0)
st.write(f"Debitur {p60_1_grouped} mengajukan penambahan jumlah pinjaman sebelum jatuh tempo")
p60_1_grouped = 1 if p60_1_grouped == 'Pernah' else 0

st.markdown('#### Sejak pencairan pinjaman, apakah Debitur pernah?')
p56_1_grouped = st.selectbox('', ['Pernah', 'Tidak Pernah'], index=1)
st.write(f"Debitur {p56_1_grouped} menunggak angsuran pinjaman setelah pencairan")
p56_1_grouped = 1 if p56_1_grouped == 'Pernah' else 0

st.markdown('#### Apa alasan Debitur berganti jenis pinjaman dari KUR ke Kupedes/Pinjaman Komersial?')
p54_grouped = st.selectbox('', [
    '', 'Atas saran/arahan dari mantri', 'Kebutuhan dana lebih besar dari plafon KUR yang tersedia',
    'Terpaksa karena KUR tidak tersedia', 'Usaha berkembang dan sudah mampu meminjam pinjaman komersial',
    'Lainnya'], index=0)
st.write(f"Debitur berganti jenis pinjaman dari KUR ke Kupedes/Pinjaman Komersial karena: {p54_grouped}")
p54_grouped = 1 if p54_grouped in ['Kebutuhan dana lebih besar dari plafon KUR yang tersedia', 'Usaha berkembang dan sudah mampu meminjam pinjaman komersial'] else 0

st.markdown('#### Berapa angsuran per bulannya (dalam ribuan)?')
p50 = st.number_input('', min_value=0, max_value=100000, value=10, key='p50')
st.write(f"Angsuran per bulan debitur adalah sebesar: Rp {(p50*1000):,}".replace(',', '.'))

st.markdown('#### Berapa suku bunga pinjamannya (dalam % per tahun)?')
p49 = st.number_input('', min_value=0, max_value=100, value=1, key='p49')
st.write(f"Suku bunga pinjaman debitur adalah sebesar: {p49}% per tahun")

st.markdown('#### Berapa jangka waktu pinjaman atau tenornya (dalam bulan)?')
p48 = st.number_input('', min_value=0, max_value=100, value=12, key='p48')
st.write(f"Jangka waktu pinjaman debitur adalah selama: {p48} bulan")

st.markdown('#### Berapa rasio rata-rata biaya listrik rumah tinggal Debitur terhadap rata-rata pengeluaran Debitur di luar angsuran dan tabungan (%)?')
p37_rasio2 = st.number_input('', min_value=0, max_value=100, value=20, key='p37_rasio2')
st.write(f"Rasio rata-rata biaya listrik rumah tinggal terhadap rata-rata pengeluaran Debitur adalah sebesar: {p37_rasio2}%")

st.markdown('#### Berapa rata-rata biaya listrik rumah tinggal Debitur (dalam ribuan)?')
p37 = st.number_input('', min_value=0, max_value=10000, value=10, key='p37')
st.write(f"Rata-rata biaya listrik rumah tinggal Debitur adalah sebesar: Rp {(p37*1000):,}".replace(',', '.'))

st.markdown('#### Berapa usia Debitur (dalam tahun)?')
p17 = st.number_input('', min_value=0, max_value=100, value=25, key='p17')
st.write(f"Usia debitur adalah: {p17} tahun")

st.markdown('#### Berapa umur usaha yang saat ini dijalankan (dalam tahun)?')
p03_grouped = st.number_input('', min_value=0, max_value=100, value=1, key='p03_grouped')
st.write(f"Umur usaha yang saat ini dijalankan adalah: {p03_grouped} tahun")

st.markdown('#### Berapa rasio rata-rata pengeluaran per bulan untuk pulsa dan paket data HP Debitur terhadap total pemasukan Debitur (%)?')
p44_rasio1 = st.number_input('', min_value=0, max_value=100, value=5, key='p44_rasio1')
st.write(f"Rasio rata-rata pengeluaran per bulan untuk pulsa dan paket data HP terhadap total pemasukan Debitur adalah sebesar: {p44_rasio1}%")

# Create a dictionary of the input features
input_features = {
    'P60.1.grouped': p60_1_grouped,
    'P56.1.grouped': p56_1_grouped,
    'P54.grouped': p54_grouped,
    'P50': p50,
    'P49': p49,
    'P48': p48,
    'P37_rasio2': p37_rasio2,
    'P37': p37,
    'P17': p17,
    'P03.grouped': p03_grouped,
    'P44_rasio1': p44_rasio1
}

# Prediction button
if st.button('Buat Prediksi'):
    probability = predict(input_features)
    st.markdown(f"#### Berdasarkan Model Regresi Logistik, peluang Debitur tersebut untuk Graduasi adalah: {(probability*100):.2f}%. Besar kemungkinannya, Debitur tersebut akan {'Graduasi' if probability > 0.5 else 'Tidak Graduasi'}.")