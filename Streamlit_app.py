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
            "Market Tag": np.random.choice(market_tags)
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

# Filters
pm_filter = st.selectbox("Filter by Project Manager", ["All"] + df["PM"].unique().tolist())
if pm_filter != "All":
    df = df[df["PM"] == pm_filter]

# Display Project Table
st.subheader("Project Data")
st.dataframe(df, use_container_width=True)

# Display Totals & Averages
st.markdown("### Summary")
total_revenue = df["Revenue"].sum()
avg_gm = df["GM%"].mean()
avg_wip = df["WIP%"].mean()
avg_budget_spent = df["Budget Spent%"].mean()

st.write(f"**Total Revenue:** ${total_revenue:,.2f}")
st.write(f"**Average GM%:** {avg_gm:.2f}%")
st.write(f"**Average WIP%:** {avg_wip:.2f}%")
st.write(f"**Average Budget Spent%:** {avg_budget_spent:.2f}%")

# Cashflow Projection Chart
st.subheader("Cashflow Projection")
df["Cashflow Date"] = pd.to_datetime(df["Cashflow Date"])
df["Month"] = df["Cashflow Date"].dt.strftime('%Y-%m')
cashflow_df = df.groupby("Month")["Revenue"].sum().reset_index()
fig = px.bar(
    cashflow_df, x="Month", y="Revenue", title="Projected Monthly Cashflow", 
    labels={"Revenue": "Projected Revenue ($)"},
    text_auto=True
)
fig.update_traces(textfont_size=12, textposition="outside")
st.plotly_chart(fig, use_container_width=True)

# Activity Section
st.subheader("Activity KPIs")
st.write("### Opportunities Created")
st.dataframe(opp_created, use_container_width=True)
fig = px.bar(opp_created, x="Creation Date", color="PM", title="Opportunities Created Per PM Per Month")
st.plotly_chart(fig, use_container_width=True)
fig = px.bar(opp_created, x="Creation Date", color="Market Tag", title="Opportunities Created Per Market Tag Per Month")
st.plotly_chart(fig, use_container_width=True)

st.write("### Opportunities Lost")
st.dataframe(opp_lost, use_container_width=True)
fig = px.bar(opp_lost, x="Creation Date", color="PM", title="Opportunities Lost Per PM Per Month")
st.plotly_chart(fig, use_container_width=True)
fig = px.bar(opp_lost, x="Creation Date", color="Market Tag", title="Opportunities Lost Per Market Tag Per Month")
st.plotly_chart(fig, use_container_width=True)

st.write("### Sales Orders Created")
st.dataframe(sales_orders, use_container_width=True)
fig = px.bar(sales_orders, x="Creation Date", y="Revenue", title="Sales Orders Created Per Month", text_auto=True)
st.plotly_chart(fig, use_container_width=True)

# Financial Compliance Section
st.subheader("Financial Compliance")
financial_tasks = generate_activity_data(30, "2025-01-01", "2025-03-31")
financial_tasks["Task Type"] = np.random.choice(["Invoice", "Vendor Bill", "Forecast", "Due Date", "Closing"], 30)
st.dataframe(financial_tasks, use_container_width=True)
fig = px.bar(financial_tasks, x="PM", title="Total Tasks Per PM")
st.plotly_chart(fig, use_container_width=True)
fig = px.bar(financial_tasks, x="Task Type", title="Total Tasks Per Task Type")
st.plotly_chart(fig, use_container_width=True)

# Revenue Forecast Section
st.subheader("Revenue Forecast")
forecast_data = generate_sales_orders(5, "2025-03-01", "2025-03-31")
st.dataframe(forecast_data, use_container_width=True)
