import streamlit as st
import joblib
import numpy as np
import pandas as pd

# Memuat model dari file
model = joblib.load('../model/Dt_model6.pkl')

# Memuat scaler dari file
scaler = joblib.load('../model/scaler6.pkl')
# Dictionary untuk mapping input
periode_pembayaran_dict = {'MONTHLY': 4, 'YEARLY': 5, 'HOURLY': 2, 'NOTPAID': 1, 'WEEKLY': 3}
tingkat_pengalaman_terformat_dict = {'Entry level': 2, 'Mid-Senior level': 4, 'Director': 6, 'Associate': 3, 'Executive': 5, 'Internship': 1}
tipe_pendaftaran_dict = {'OffsiteApply': 1, 'SimpleOnsiteApply': 2, 'ComplexOnsiteApply': 3}

# Judul Aplikasi
st.title("Interface untuk Model Klasifikasi Multi Label")

# Input Data
st.header("Masukkan Data")

# Pilihan dropdown Ya/Tidak untuk diperbolehkan jarak jauh
diperbolehkan_jarak_jauh = st.selectbox('Diperbolehkan Jarak Jauh', ['Tidak', 'Ya'])
diperbolehkan_jarak_jauh_encoded = 1 if diperbolehkan_jarak_jauh == 'Ya' else 0

# Pilihan dropdown dengan nama dari dictionary
periode_pembayaran = st.selectbox('Periode Pembayaran', list(periode_pembayaran_dict.keys()))
periode_pembayaran_encoded = periode_pembayaran_dict[periode_pembayaran]

tingkat_pengalaman_terformat = st.selectbox('Tingkat Pengalaman Terformat', list(tingkat_pengalaman_terformat_dict.keys()))
tingkat_pengalaman_terformat_encoded = tingkat_pengalaman_terformat_dict[tingkat_pengalaman_terformat]

tipe_pendaftaran = st.selectbox('Tipe Pendaftaran', list(tipe_pendaftaran_dict.keys()))
tipe_pendaftaran_encoded = tipe_pendaftaran_dict[tipe_pendaftaran]

st.header("Jenis Pekerjaan")
jenis_pekerjaan_Contract = st.checkbox('Contract', value=False)
jenis_pekerjaan_Full_time = st.checkbox('Full-time', value=True)
jenis_pekerjaan_Internship = st.checkbox('Internship', value=False)
jenis_pekerjaan_Other = st.checkbox('Other', value=False)
jenis_pekerjaan_Part_time = st.checkbox('Part-time', value=False)
jenis_pekerjaan_Temporary = st.checkbox('Temporary', value=False)
jenis_pekerjaan_Volunteer = st.checkbox('Volunteer', value=False)

jumlah_skill_perindustri = st.number_input('Jumlah Skill Perindustri', min_value=0, max_value=10, value=2)
standar_gaji = st.number_input('Standar Gaji', min_value=0, value=10000)

# Penjelasan untuk kategori lamaran industri
kategori_lamaran_industri_options = {
    1: 'Sepi',
    2: 'Biasa',
    3: 'Ramai'
}
kategori_lamaran_industri = st.selectbox('Kategori Lamaran Industri', options=list(kategori_lamaran_industri_options.keys()), format_func=lambda x: kategori_lamaran_industri_options[x])

st.header("Skill")
skill_Accounting_Auditing = st.checkbox('Accounting/Auditing', value=False)
skill_Administrative = st.checkbox('Administrative', value=False)
skill_Advertising = st.checkbox('Advertising', value=False)
skill_Analyst = st.checkbox('Analyst', value=False)
skill_Art_Creative = st.checkbox('Art/Creative', value=False)
skill_Business_Development = st.checkbox('Business Development', value=False)
skill_Consulting = st.checkbox('Consulting', value=False)
skill_Customer_Service = st.checkbox('Customer Service', value=False)
skill_Design = st.checkbox('Design', value=False)
skill_Distribution = st.checkbox('Distribution', value=False)
skill_Education = st.checkbox('Education', value=False)
skill_Engineering = st.checkbox('Engineering', value=True)
skill_Finance = st.checkbox('Finance', value=False)
skill_General_Business = st.checkbox('General Business', value=False)
skill_Health_Care_Provider = st.checkbox('Health Care Provider', value=False)
skill_Human_Resources = st.checkbox('Human Resources', value=False)
skill_Information_Technology = st.checkbox('Information Technology', value=True)
skill_Legal = st.checkbox('Legal', value=False)
skill_Management = st.checkbox('Management', value=False)
skill_Manufacturing = st.checkbox('Manufacturing', value=True)
skill_Marketing = st.checkbox('Marketing', value=False)
skill_Other = st.checkbox('Other', value=False)
skill_Product_Management = st.checkbox('Product Management', value=False)
skill_Production = st.checkbox('Production', value=False)
skill_Project_Management = st.checkbox('Project Management', value=False)
skill_Public_Relations = st.checkbox('Public Relations', value=False)
skill_Purchasing = st.checkbox('Purchasing', value=False)
skill_Quality_Assurance = st.checkbox('Quality Assurance', value=False)
skill_Research = st.checkbox('Research', value=False)
skill_Sales = st.checkbox('Sales', value=False)
skill_Science = st.checkbox('Science', value=False)
skill_Strategy_Planning = st.checkbox('Strategy/Planning', value=False)
skill_Supply_Chain = st.checkbox('Supply Chain', value=False)
skill_Training = st.checkbox('Training', value=False)
skill_Writing_Editing = st.checkbox('Writing/Editing', value=False)

st.header("Sector")
sector_Construction_and_Engineering = st.checkbox('Construction and Engineering', value=False)
sector_Consumer_Services_and_Retail = st.checkbox('Consumer Services and Retail', value=False)
sector_Education_and_Research = st.checkbox('Education and Research', value=False)
sector_Energy_and_Natural_Resources = st.checkbox('Energy and Natural Resources', value=False)
sector_Entertainment = st.checkbox('Entertainment', value=False)
sector_Finance_and_Legal_Services = st.checkbox('Finance and Legal Services', value=False)
sector_Health_and_Wellness = st.checkbox('Health and Wellness', value=False)
sector_Manufacturing = st.checkbox('Manufacturing', value=False)
sector_Non_profit_and_Government = st.checkbox('Non-profit and Government', value=False)
sector_Professional_and_Business_Services = st.checkbox('Professional and Business Services', value=False)
sector_Technology_and_IT = st.checkbox('Technology and IT', value=True)
sector_Transportation_and_Logistics = st.checkbox('Transportation and Logistics', value=False)
# Membuat dictionary dari input data
data = {
    'diperbolehkan_jarak_jauh': [diperbolehkan_jarak_jauh_encoded],
    'periode_pembayaran_encoded': [periode_pembayaran_encoded],
    'tingkat_pengalaman_terformat_encoded': [tingkat_pengalaman_terformat_encoded],
    'tipe_pendaftaran_encoded': [tipe_pendaftaran_encoded],
    'jenis_pekerjaan_Contract': [1 if jenis_pekerjaan_Contract else 0],
    'jenis_pekerjaan_Full-time': [1 if jenis_pekerjaan_Full_time else 0],
    'jenis_pekerjaan_Internship': [1 if jenis_pekerjaan_Internship else 0],
    'jenis_pekerjaan_Other': [1 if jenis_pekerjaan_Other else 0],
    'jenis_pekerjaan_Part-time': [1 if jenis_pekerjaan_Part_time else 0],
    'jenis_pekerjaan_Temporary': [1 if jenis_pekerjaan_Temporary else 0],
    'jenis_pekerjaan_Volunteer': [1 if jenis_pekerjaan_Volunteer else 0],
    'jumlah_skill_perindustri': [jumlah_skill_perindustri],
    'standar_gaji': [standar_gaji],
    'kategori_lamaran_industri': [kategori_lamaran_industri],
    'skill_Accounting/Auditing': [1 if skill_Accounting_Auditing else 0],
    'skill_Administrative': [1 if skill_Administrative else 0],
    'skill_Advertising': [1 if skill_Advertising else 0],
    'skill_Analyst': [1 if skill_Analyst else 0],
    'skill_Art/Creative': [1 if skill_Art_Creative else 0],
    'skill_Business Development': [1 if skill_Business_Development else 0],
    'skill_Consulting': [1 if skill_Consulting else 0],
    'skill_Customer Service': [1 if skill_Customer_Service else 0],
    'skill_Design': [1 if skill_Design else 0],
    'skill_Distribution': [1 if skill_Distribution else 0],
    'skill_Education': [1 if skill_Education else 0],
    'skill_Engineering': [1 if skill_Engineering else 0],
    'skill_Finance': [1 if skill_Finance else 0],
    'skill_General Business': [1 if skill_General_Business else 0],
    'skill_Health Care Provider': [1 if skill_Health_Care_Provider else 0],
    'skill_Human Resources': [1 if skill_Human_Resources else 0],
    'skill_Information Technology': [1 if skill_Information_Technology else 0],
    'skill_Legal': [1 if skill_Legal else 0],
    'skill_Management': [1 if skill_Management else 0],
    'skill_Manufacturing': [1 if skill_Manufacturing else 0],
    'skill_Marketing': [1 if skill_Marketing else 0],
    'skill_Other': [1 if skill_Other else 0],
    'skill_Product Management': [1 if skill_Product_Management else 0],
    'skill_Production': [1 if skill_Production else 0],
    'skill_Project Management': [1 if skill_Project_Management else 0],
    'skill_Public Relations': [1 if skill_Public_Relations else 0],
    'skill_Purchasing': [1 if skill_Purchasing else 0],
    'skill_Quality Assurance': [1 if skill_Quality_Assurance else 0],
    'skill_Research': [1 if skill_Research else 0],
    'skill_Sales': [1 if skill_Sales else 0],
    'skill_Science': [1 if skill_Science else 0],
    'skill_Strategy/Planning': [1 if skill_Strategy_Planning else 0],
    'skill_Supply Chain': [1 if skill_Supply_Chain else 0],
    'skill_Training': [1 if skill_Training else 0],
    'skill_Writing/Editing': [1 if skill_Writing_Editing else 0],
    'sector_Construction and Engineering': [1 if sector_Construction_and_Engineering else 0],
    'sector_Consumer Services and Retail': [1 if sector_Consumer_Services_and_Retail else 0],
    'sector_Education and Research': [1 if sector_Education_and_Research else 0],
    'sector_Energy and Natural Resources': [1 if sector_Energy_and_Natural_Resources else 0],
    'sector_Entertainment': [1 if sector_Entertainment else 0],
    'sector_Finance and Legal Services': [1 if sector_Finance_and_Legal_Services else 0],
    'sector_Health and Wellness': [1 if sector_Health_and_Wellness else 0],
    'sector_Manufacturing': [1 if sector_Manufacturing else 0],
    'sector_Non-profit and Government': [1 if sector_Non_profit_and_Government else 0],
    'sector_Professional and Business Services': [1 if sector_Professional_and_Business_Services else 0],
    'sector_Technology and IT': [1 if sector_Technology_and_IT else 0],
    'sector_Transportation and Logistics': [1 if sector_Transportation_and_Logistics else 0]
}

# Menampilkan dictionary data yang telah diisi
st.write(data)
# Mengubah dictionary ke DataFrame
input_df = pd.DataFrame(data)

# Scaling data input menggunakan scaler yang telah dimuat
scaled_input_df = scaler.transform(input_df)

# Melakukan prediksi
prediksi = model.predict(scaled_input_df)
# Menampilkan hasil prediksi
st.header("Hasil Prediksi")

mapping_industri = {
    1: 'Accounting', 
    2: 'Advertising Services', 
    3: 'Airlines and Aviation',
    4: 'Appliances, Electrical, and Electronics Manufacturing',
    5: 'Architecture and Planning',
    6: 'Automation Machinery Manufacturing',
    7: 'Aviation and Aerospace Component Manufacturing',
    8: 'Banking',
    9: 'Biotechnology Research',
    10: 'Book and Periodical Publishing',
    11: 'Broadcast Media Production and Distribution',
    12: 'Business Consulting and Services',
    13: 'Chemical Manufacturing',
    14: 'Civil Engineering',
    15: 'Computer Hardware Manufacturing',
    16: 'Computer and Network Security',
    17: 'Computers and Electronics Manufacturing',
    18: 'Construction',
    19: 'Consumer Services',
    20: 'Defense and Space Manufacturing',
    21: 'Design Services',
    22: 'E-Learning Providers',
    23: 'Education Administration Programs',
    24: 'Entertainment Providers',
    25: 'Environmental Services',
    26: 'Facilities Services',
    27: 'Financial Services',
    28: 'Food and Beverage Manufacturing',
    29: 'Food and Beverage Services',
    30: 'Government Administration',
    31: 'Higher Education',
    32: 'Hospitality',
    33: 'Hospitals and Health Care',
    34: 'Human Resources Services',
    35: 'IT Services and IT Consulting',
    36: 'Individual and Family Services',
    37: 'Industrial Machinery Manufacturing',
    38: 'Information Services',
    39: 'Insurance',
    40: 'Internet Marketplace Platforms',
    41: 'Investment Banking',
    42: 'Investment Management',
    43: 'Law Practice',
    44: 'Legal Services',
    45: 'Machinery Manufacturing',
    46: 'Manufacturing',
    47: 'Medical Equipment Manufacturing',
    48: 'Medical Practices',
    49: 'Mental Health Care',
    50: 'Mining',
    51: 'Motor Vehicle Manufacturing',
    52: 'Non-profit Organizations',
    53: 'Oil and Gas',
    54: 'Packaging and Containers Manufacturing',
    55: 'Pharmaceutical Manufacturing',
    56: 'Primary and Secondary Education',
    57: 'Real Estate',
    58: 'Renewable Energy Semiconductor Manufacturing',
    59: 'Research Services',
    60: 'Restaurants',
    61: 'Retail',
    62: 'Retail Apparel and Fashion',
    63: 'Semiconductor Manufacturing',
    64: 'Software Development',
    65: 'Staffing and Recruiting',
    66: 'Technology, Information and Internet',
    67: 'Telecommunications',
    68: 'Transportation, Logistics, Supply Chain and Storage',
    69: 'Travel Arrangements',
    70: 'Truck Transportation',
    71: 'Utilities',
    72: 'Veterinary Services',
    73: 'Wellness and Fitness Services',
    74: 'Wholesale',
    75: 'Wholesale Building Materials'
}

# Mapping hasil prediksi ke industri menggunakan mapping_industri
true_indices = np.where(prediksi[0])[0]
industri = true_indices + 1  # Karena indeks dimulai dari 0, tambahkan 1
nama_industri = [mapping_industri[idx] for idx in industri]

st.header("Industri")
st.write(nama_industri)