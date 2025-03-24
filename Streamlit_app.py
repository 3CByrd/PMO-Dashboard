import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px

# Generate Sample Data
def generate_projects():
    stages = ["Approved", "Permitting", "Manufacturing", "Installation", "Invoicing"]
    payment_terms = [30, 45, 60]
    pm_names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    projects = []
    
    for i in range(15):
        revenue = np.random.randint(2500, 150000)
        gm = round(np.random.uniform(30, 40), 2)
        wip = np.random.randint(0, 101)
        budget_spent = wip  # Assume budget spent is proportional to WIP
        stage = np.random.choice(stages)
        due_date = pd.Timestamp.today() + pd.DateOffset(days=np.random.randint(10, 60))
        payment_term = np.random.choice(payment_terms)
        cashflow_date = due_date + pd.DateOffset(days=payment_term)
        pm = np.random.choice(pm_names)
        
        projects.append({
            "Project": f"Project {i+1}",
            "Due Date": due_date.strftime('%Y-%m-%d'),
            "Revenue": revenue,
            "GM%": gm,
            "WIP%": wip,
            "Budget Spent%": budget_spent,
            "Stage": stage,
            "PM": pm,
            "Cashflow Date": cashflow_date.strftime('%Y-%m-%d')
        })
    
    return pd.DataFrame(projects)

def generate_activity_data(num_records, start_date, end_date):
    pm_names = ["Alice", "Bob", "Charlie", "David", "Eve"]
    market_tags = ["Retail", "QSR", "Petroleum", "Wholesale", "One-off", "Service"]
    dates = pd.date_range(start=start_date, end=end_date).tolist()
    data = []
    
    for _ in range(num_records):
        data.append({
            "Creation Date": np.random.choice(dates).strftime('%Y-%m-%d'),
            "PM": np.random.choice(pm_names),
            "Market Tag": np.random.choice(market_tags),
            "Opportunity Name": f"Client ({np.random.choice(['Toronto', 'Vancouver', 'Calgary'])}, {np.random.choice(['ON', 'BC', 'AB'])}) | {np.random.choice(['New Store', 'Renovation', 'Expansion'])}"
        })
    
    return pd.DataFrame(data)

def generate_sales_orders(num_records, start_date, end_date):
    sales_data = generate_activity_data(num_records, start_date, end_date)
    sales_data["Revenue"] = np.random.randint(2500, 150000, num_records)
    sales_data["GM%"] = np.round(np.random.uniform(30, 40, num_records), 2)
    return sales_data

def generate_market_turnover(num_records, start_date, end_date):
    market_tags = ["Retail", "QSR", "Petroleum", "Wholesale", "One-off", "Service"]
    data = []
    for _ in range(num_records):
        market = np.random.choice(market_tags)
        opp_to_so = np.random.randint(5, 180)
        so_to_close = np.random.randint(30, 120)
        data.append({
            "Market Tag": market,
            "Opportunity to SO Conversion (Days)": opp_to_so,
            "SO Conversion to Closing (Days)": so_to_close,
            "Total Project Life (Days)": opp_to_so + so_to_close
        })
    
    return pd.DataFrame(data)

# Streamlit UI
st.set_page_config(layout="wide", page_title="Active Projects Dashboard")
st.title("📊 Active Projects Dashboard")

# Load Data
df = generate_projects()
opp_created = generate_activity_data(100, "2025-01-01", "2025-03-31")
opp_lost = generate_activity_data(33, "2025-01-01", "2025-03-31")
sales_orders = generate_sales_orders(90, "2025-01-01", "2025-03-31")
market_turnover = generate_market_turnover(100, "2025-01-01", "2025-03-31")

# Market Turnover Table
st.subheader("Market Turnover Table")
st.dataframe(market_turnover, use_container_width=True)

# Market Turnover Summary
turnover_summary = market_turnover.groupby("Market Tag").mean().reset_index()
st.write("### Market Turnover Summary")
st.dataframe(turnover_summary, use_container_width=True)
