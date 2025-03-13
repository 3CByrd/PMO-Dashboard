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

# Streamlit UI
st.set_page_config(layout="wide", page_title="Active Projects Dashboard")
st.title("📊 Active Projects Dashboard")

# Load Data
df = generate_projects()

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
fig = px.bar(cashflow_df, x="Month", y="Revenue", title="Projected Monthly Cashflow", labels={"Revenue": "Projected Revenue ($)"})
st.plotly_chart(fig, use_container_width=True)
