
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

st.set_page_config(
    page_title="Online Retail Dashboard",
    layout="wide"
)

df = pd.read_csv("cleaned_online_retail.csv")

df['InvoiceDate'] = pd.to_datetime(df['InvoiceDate'])

st.title("Online Retail Revenue Dashboard")
st.write("Revenue Analysis and Customer Behavior")

# Calculate KPIs
total_revenue = df['TotalRevenue'].sum()
total_orders = df['InvoiceNo'].nunique()
total_customers = df['CustomerID'].nunique()
aov = total_revenue / total_orders

# Display KPIs
st.subheader("Business Performance")

col1, col2, col3, col4 = st.columns(4)

col1.write("Total Revenue")
col1.write(round(total_revenue, 2))

col2.write("Total Orders")
col2.write(total_orders)

col3.write("Total Customers")
col3.write(total_customers)

col4.write("Average Order Value")
col4.write(round(aov, 2))

# Monthly Revenue
st.subheader("Monthly Revenue Trend")

monthly_revenue = df.groupby(
    df['InvoiceDate'].dt.to_period('M')
)['TotalRevenue'].sum()

fig, ax = plt.subplots(figsize=(12, 5))
monthly_revenue.index = monthly_revenue.index.astype(str)
monthly_revenue.plot(kind='line', ax=ax)

ax.set_xlabel("Month")
ax.set_ylabel("Revenue")
ax.set_title("Monthly Revenue Trend")
plt.xticks(rotation=45)
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

# Top Products
st.subheader("Top 10 Products")

top_products = (
    df.groupby('Description')['TotalRevenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10, 6))
top_products.sort_values().plot(kind='barh', ax=ax)
ax.set_xlabel("Revenue")
ax.set_ylabel("Product")
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

# Country Revenue
st.subheader("Country-wise Revenue")

country_revenue = (
    df.groupby('Country')['TotalRevenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

fig, ax = plt.subplots(figsize=(10, 6))
country_revenue.sort_values().plot(kind='barh', ax=ax)
ax.set_xlabel("Revenue")
ax.set_ylabel("Country")
plt.tight_layout()

st.pyplot(fig)
plt.close(fig)

# Customer Behaviour
st.subheader("Top 10 Customers")

# Convert CustomerID into numeric format
df['CustomerID'] = pd.to_numeric(
    df['CustomerID'],
    errors='coerce'
)

# Remove missing CustomerID values
customer_df = df.dropna(subset=['CustomerID'])

# Calculate Top 10 Customers
top_customers = (
    customer_df.groupby('CustomerID')['TotalRevenue']
    .sum()
    .sort_values(ascending=False)
    .head(10)
)

# Display customer data
if not top_customers.empty:

    st.write("Top 10 Customer Revenue Details")

    st.dataframe(
        top_customers.reset_index()
    )

    fig, ax = plt.subplots(figsize=(10, 6))

    top_customers.sort_values().plot(
        kind='barh',
        ax=ax
    )

    ax.set_xlabel("Revenue")
    ax.set_ylabel("Customer ID")
    ax.set_title("Top 10 Customers by Revenue")

    plt.tight_layout()

    st.pyplot(fig)
    plt.close(fig)

else:
    st.warning("No Customer Data Available!")
    st.write("Total Customer Records:", len(customer_df))
