# 💜 PhonePe Transactions Dashboard

An interactive data analytics dashboard built with **Python + Streamlit + Plotly** that visualizes PhonePe transaction data — recreating the Power BI dashboard as a live web app.

🔗 **Live Demo**: [Click here to view](https://your-app-url.streamlit.app) *(update after deploying)*

---

## 📊 Dashboard Features

| Tab | What's inside |
|-----|--------------|
| **Overview** | KPI cards, monthly volume trends, status breakdown, service revenue |
| **Transactions** | Failure analysis, amount distribution, quarterly performance, recent records |
| **Users** | Age group distribution, monthly registrations, spending by age |

### Key Metrics
- **300,000** transactions across 2024
- **₹347 Cr+** total transaction volume
- **96%** success rate
- **107,658** registered users
- **4 services**: Loans, Insurance, Money Transfer, Recharge & Bills

---

## 🛠️ Tech Stack

- **Python 3.10+**
- **Streamlit** — web app framework
- **Plotly** — interactive charts
- **Pandas** — data processing
- **Power BI** — original dashboard (`.pbix` included)

---

## 🚀 Run Locally

```bash
# 1. Clone the repo
git clone https://github.com/rushikesh-k24/phonepe-dashboard.git
cd phonepe-dashboard

# 2. Install dependencies
pip install -r requirements.txt

# 3. Run the app
streamlit run app.py
```

Then open `http://localhost:8501` in your browser.

---

## 📁 Project Structure

```
phonepe-dashboard/
├── app.py                        # Streamlit dashboard
├── Phonepe-Final-Dataset.xlsx    # Dataset (2 sheets: Users + Transactions)
├── PhonePe_Dashboard.pbix        # Original Power BI dashboard
├── requirements.txt              # Python dependencies
└── README.md
```

---

## ☁️ Deploy to Streamlit Cloud (Free)

1. Push this repo to GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io)
3. Click **"New app"** → select your repo
4. Set **Main file path** to `app.py`
5. Click **Deploy** — you'll get a public URL in ~2 minutes!

---

## 👤 Author

**Rushikesh Kolhe** — Data Analyst | AI & Data Science (SPPU)

[![LinkedIn](https://img.shields.io/badge/LinkedIn-rushikeshkolhe24-blue)](https://linkedin.com/in/rushikeshkolhe24)
[![GitHub](https://img.shields.io/badge/GitHub-rushikesh--k24-black)](https://github.com/rushikesh-k24)
