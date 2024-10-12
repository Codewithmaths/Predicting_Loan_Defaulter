import streamlit as st
import numpy as np
import pickle

# Load your trained model
model = pickle.load(open('loan_defaulter_RF_model.pickel', 'rb'))

st.title('Loan Defaulter Prediction')

# Collecting inputs from user
st.write("Enter the details to predict loan defaulter status:")

# Input fields
loan_amnt = st.number_input("Loan Amount", min_value=0, step=100)
term = st.selectbox("Term (months)", [36,60])
int_rate = st.slider("Interest Rate (%)", 0.0, 20.0, step=0.01)
installment = st.number_input("Installment", min_value=0.0, step=10.0)

# Grade and sub-grade need to be converted to numeric values
grade = st.selectbox("Grade", ['A', 'B', 'C', 'D', 'E', 'F', 'G'])
grade_numeric = {'A': 1, 'B': 2, 'C': 3, 'D': 4, 'E': 5, 'F': 6, 'G': 7}[grade]

sub_grade = st.selectbox("Sub-Grade", [f"{grade}{i}" for i in range(1, 6)])
sub_grade_numeric = {'A1': 1, 'A2': 2, 'A3': 3, 'A4': 4, 'A5': 5, 'B1': 6, 'B2': 7, 'B3': 8, 'B4': 9, 'B5': 10,
                     'C1': 11, 'C2': 12, 'C3': 13, 'C4': 14, 'C5': 15, 'D1': 16, 'D2': 17, 'D3': 18, 'D4': 19, 'D5': 20,
                     'E1': 21, 'E2': 22, 'E3': 23, 'E4': 24, 'E5': 25, 'F1': 26, 'F2': 27, 'F3': 28, 'F4': 29, 'F5': 30,
                     'G1': 31, 'G2': 32, 'G3': 33, 'G4': 34, 'G5': 35}[sub_grade]

emp_length = st.slider("Employment Length (years)", 0, 40)
annual_inc = st.number_input("Annual Income", min_value=0.0, step=1000.0)

# Purpose needs to be converted to numeric
purpose = st.selectbox("Loan Purpose", ['credit_card', 'car', 'small_business', 'home_improvement', 'major_purchase', 'debt_consolidation'])
purpose_numeric = {'credit_card': 1, 'car': 2, 'small_business': 3, 'home_improvement': 4, 'major_purchase': 5, 'debt_consolidation': 6}[purpose]

zip_code = st.text_input("Zip Code", max_chars=6)
addr_state = st.selectbox("Address State", [
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI',
    'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 
    'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 
    'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 
    'WV', 'WI', 'WY'
])
addr_state_numeric = {state: idx for idx, state in enumerate([
    'AL', 'AK', 'AZ', 'AR', 'CA', 'CO', 'CT', 'DE', 'DC', 'FL', 'GA', 'HI',
    'ID', 'IL', 'IN', 'IA', 'KS', 'KY', 'LA', 'ME', 'MD', 'MA', 'MI', 'MN', 
    'MS', 'MO', 'MT', 'NE', 'NV', 'NH', 'NJ', 'NM', 'NY', 'NC', 'ND', 'OH', 
    'OK', 'OR', 'PA', 'RI', 'SC', 'SD', 'TN', 'TX', 'UT', 'VT', 'VA', 'WA', 
    'WV', 'WI', 'WY'
])}[addr_state]

dti = st.number_input("Debt-to-Income Ratio (DTI)", min_value=0.0, step=0.1)

# Additional required features
delinq_2yrs = st.number_input("Delinquencies in 2 Years", min_value=0)
inq_last_6mths = st.number_input("Inquiries in Last 6 Months", min_value=0)
mths_since_last_delinq = st.number_input("Months Since Last Delinquency", min_value=0)
open_acc = st.number_input("Number of Open Accounts", min_value=0)
pub_rec = st.number_input("Number of Public Records", min_value=0)
revol_bal = st.number_input("Revolving Balance", min_value=0)
revol_util = st.slider("Revolving Utilization Rate (%)", 0.0, 100.0, step=0.1)
total_acc = st.number_input("Total Accounts", min_value=0)
last_fico_range_high = st.number_input("Last FICO Range High", min_value=300, max_value=850)
last_fico_range_low = st.number_input("Last FICO Range Low", min_value=300, max_value=850)

pub_rec_bankruptcies = st.number_input("Public Record Bankruptcies", min_value=0)
fico_range_avg = st.slider("FICO Score (average)", 300, 850, step=1)
earliest_cr_line_month = st.slider("Earliest Credit Line (Month)", 1, 12)
earliest_cr_line_year = st.slider("Earliest Credit Line (Year)", 1900, 2024)
last_credit_pull_d_month = st.slider("Last Credit Pull Date (Month)", 1, 12)
last_credit_pull_d_year = st.slider("Last Credit Pull Date (Year)", 1900, 2024)

# Home Ownership options as multiple binary fields
home_ownership_MORTGAGE = st.checkbox("Home Ownership: MORTGAGE", value=False)
home_ownership_NONE = st.checkbox("Home Ownership: NONE", value=False)
home_ownership_OTHER = st.checkbox("Home Ownership: OTHER", value=False)
home_ownership_OWN = st.checkbox("Home Ownership: OWN", value=False)
home_ownership_RENT = st.checkbox("Home Ownership: RENT", value=False)

# Prepare the feature vector with numeric values for categorical features
features = np.array([
    loan_amnt, term, int_rate, installment, grade_numeric, sub_grade_numeric, emp_length, annual_inc,
    purpose_numeric, zip_code, addr_state_numeric, dti, delinq_2yrs, inq_last_6mths, mths_since_last_delinq,
    open_acc, pub_rec, revol_bal, revol_util, total_acc, last_fico_range_high,
    last_fico_range_low, pub_rec_bankruptcies, fico_range_avg, earliest_cr_line_month,
    earliest_cr_line_year, last_credit_pull_d_month, last_credit_pull_d_year,
    int(home_ownership_MORTGAGE), int(home_ownership_NONE), int(home_ownership_OTHER),
    int(home_ownership_OWN), int(home_ownership_RENT)
])

# Reshape the input to match the model's expected input format
features = features.reshape(1, -1)

# Make prediction
if st.button("Predict"):
    prediction = model.predict(features)[0]
    
    if prediction == 1:
        st.write("The person is likely to default on the loan.")
    else:
        st.write("The person is not likely to default on the loan.")