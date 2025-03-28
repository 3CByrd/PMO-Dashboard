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

# Streamlit UI
st.set_page_config(layout="wide", page_title="Active Projects Dashboard")
st.title("📊 Active Projects Dashboard")

# Load Data
df = generate_projects()
opp_created = generate_activity_data(100, "2025-01-01", "2025-03-31")
opp_lost = generate_activity_data(33, "2025-01-01", "2025-03-31")
sales_orders = generate_sales_orders(90, "2025-01-01", "2025-03-31")

# Display Activity KPIs
st.subheader("Activity KPIs")

st.write("### Opportunities Created")
st.dataframe(opp_created, use_container_width=True)
opp_count_pm = opp_created.groupby([pd.to_datetime(opp_created["Creation Date"]).dt.strftime('%B'), "PM"]).size().reset_index(name="Count")
fig = px.bar(opp_count_pm, x="Creation Date", y="Count", color="PM", barmode='group', title="Opportunities Created Per PM Per Month")
st.plotly_chart(fig, use_container_width=True)
opp_count_market = opp_created.groupby([pd.to_datetime(opp_created["Creation Date"]).dt.strftime('%B'), "Market Tag"]).size().reset_index(name="Count")
fig = px.bar(opp_count_market, x="Creation Date", y="Count", color="Market Tag", barmode='group', title="Opportunities Created Per Market Tag Per Month")
st.plotly_chart(fig, use_container_width=True)

st.write("### Opportunities Lost")
st.dataframe(opp_lost, use_container_width=True)
opp_lost_pm = opp_lost.groupby([pd.to_datetime(opp_lost["Creation Date"]).dt.strftime('%B'), "PM"]).size().reset_index(name="Count")
fig = px.bar(opp_lost_pm, x="Creation Date", y="Count", color="PM", barmode='group', title="Opportunities Lost Per PM Per Month")
st.plotly_chart(fig, use_container_width=True)
opp_lost_market = opp_lost.groupby([pd.to_datetime(opp_lost["Creation Date"]).dt.strftime('%B'), "Market Tag"]).size().reset_index(name="Count")
fig = px.bar(opp_lost_market, x="Creation Date", y="Count", color="Market Tag", barmode='group', title="Opportunities Lost Per Market Tag Per Month")
st.plotly_chart(fig, use_container_width=True)

st.write("### Sales Orders Created")
st.dataframe(sales_orders, use_container_width=True)
sales_revenue = sales_orders.groupby(pd.to_datetime(sales_orders["Creation Date"]).dt.strftime('%B'))["Revenue"].sum().reset_index()
fig = px.bar(sales_revenue, x="Creation Date", y="Revenue", title="Total Sales Orders Revenue Per Month", text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# Financial Compliance
st.subheader("Financial Compliance")
financial_tasks = generate_activity_data(30, "2025-01-01", "2025-03-31")
financial_tasks["Task Type"] = np.random.choice(["Invoice", "Vendor Bill", "Forecast", "Due Date", "Closing"], 30)
st.dataframe(financial_tasks, use_container_width=True)
task_summary = financial_tasks.groupby("PM").size().reset_index(name="Count")
fig = px.bar(task_summary, x="PM", y="Count", color="PM", title="Total Tasks Per PM")
st.plotly_chart(fig, use_container_width=True)
task_type_summary = financial_tasks.groupby("Task Type").size().reset_index(name="Count")
fig = px.bar(task_type_summary, x="Task Type", y="Count", color="Task Type", title="Total Tasks Per Task Type")
st.plotly_chart(fig, use_container_width=True)
