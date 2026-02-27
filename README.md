# Loan Default Prediction Project

[![Python 3.9+](https://img.shields.io/badge/python-3.9+-blue.svg)](https://www.python.org/downloads/)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.28+-red.svg)](https://streamlit.io/)
[![scikit-learn](https://img.shields.io/badge/scikit--learn-1.3+-orange.svg)](https://scikit-learn.org/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

## 📌 Overview

This project develops a **machine learning model to predict loan default risk** and extends it into a full-featured **interactive web application** built with Streamlit. The app not only predicts the probability of default but also provides a **loan amortization dashboard** and can send **email payment reminders** to borrowers.

The goal is to combine data science, finance, and deployment skills into a practical tool that could be used by financial institutions or individuals.

## ✨ Features

- **Loan Default Prediction** – Enter borrower details (income, credit score, loan amount, etc.) and get:
  - Probability of default
  - Risk classification (Low / Medium / High)
- **Interactive Amortization Schedule** – For a given loan amount, interest rate, and term, the app generates:
  - Monthly payment breakdown
  - Charts showing principal vs interest over time
  - Remaining balance progression
- **Email Reminders** – Send a payment reminder email via Gmail SMTP directly from the app.
- **Machine Learning Pipeline** – End-to-end preprocessing (encoding, scaling) + Logistic Regression model trained on real-world data.

## 📊 Dataset

We used a publicly available dataset from [Kaggle](https://www.kaggle.com/) containing borrower information and loan performance.

**Features:**

| Type                | Features                                                                                     |
|---------------------|----------------------------------------------------------------------------------------------|
| Numerical           | Age, Income, LoanAmount, CreditScore, MonthsEmployed, InterestRate, LoanTerm, DTIRatio, NumCreditLines |
| Categorical (Ordinal)| Education (High School < Bachelor’s < Master’s < PhD)                                        |
| Categorical (Binary) | HasMortgage, HasDependents, HasCoSigner (Yes/No → 1/0)                                       |
| Categorical (Nominal)| EmploymentType, MaritalStatus, LoanPurpose                                                   |
| Target              | `Default` (0 = Non‑default, 1 = Default)                                                     |

## 🧠 Machine Learning Pipeline

1. **Data Preprocessing**  
   - Missing value check (none critical)  
   - Ordinal encoding for `Education`  
   - Label mapping for binary Yes/No fields  
   - One‑hot encoding for nominal categoricals  
   - Standard scaling for numerical features  

2. **Model Training & Selection**  
   - Compared Logistic Regression and Random Forest.  
   - **Logistic Regression** was chosen (slightly higher ROC AUC).  
   - Train/test split: 80/20.  
   - Final model saved as `loan_default_pipeline.pkl` using `joblib`.

3. **Evaluation Metrics**  
   - ROC AUC Score  
   - Classification Report  
   - Confusion Matrix  

## 🚀 Streamlit Application

The app (`app.py`) provides three main tabs:

### 🔮 Prediction Tab
Users input borrower characteristics via sliders, dropdowns, and text fields. The model returns:
- Default probability
- Risk level (coloured badge)

### 📈 Amortization Dashboard
- Input loan amount, interest rate, and term.
- Displays monthly payment schedule table.
- Interactive charts (Plotly) for:
  - Principal vs Interest over time
  - Remaining balance

### 📧 Email Reminder
- Enter borrower's email address.
- Click “Send Reminder” to send a pre‑formatted payment reminder via Gmail SMTP (requires app password).

> **Note:** To use the email feature, you must configure your Gmail credentials in the app (see local setup).

## 🛠️ Installation

### Prerequisites
- Python 3.9 or higher
- Git

### Steps

1. **Clone the repository**
   ```bash
   git clone https://github.com/yourusername/P14_Loan_project.git
   cd P14_Loan_project
```

2. **Create and activate a virtual environment (optional but recommended)**
   ```bash
   python -m venv venv
   source venv/bin/activate   # On Windows: venv\Scripts\activate
```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
```

4. **Run the app locally**
   ```bash
   streamlit run app.py
```
### Email Configuration (optional)
To enable the email reminder feature, set the following environment variables or replace them directly in app.py (not recommended for production):

- `GMAIL_USER` – your Gmail address
- `GMAIL_APP_PASSWORD` – an App Password for Gmail

## ☁️ Deployment on Streamlit Cloud
The app is also deployed publicly via Streamlit Cloud:
https://p14loanamortization-6qu89tipcgcm3xp9nuseim.streamlit.app/

## 📚 Technologies Used
- Python – pandas, numpy, matplotlib, seaborn, scikit‑learn, joblib
- Machine Learning – Logistic Regression, Random Forest
- Web Framework – Streamlit
- Visualization – Plotly, Matplotlib
- Email – smtplib (Gmail SMTP)
- Deployment – Streamlit Cloud, GitHub
  
## 🙏 Acknowledgements
- Dataset: Kaggle – Loan Default Prediction Dataset (link if available)
