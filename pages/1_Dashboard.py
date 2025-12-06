import streamlit as st
import pandas as pd
from app_model.cyber_incidents import get_all_cyber_incidents
from app_model.it_tickets import get_all_it_tickets
from app_model.metadatas import get_all_datasets_metadata
from app_model.db import get_connection
import plotly.express as px

st.set_page_config(
    page_title="Home Page",
    page_icon="🏠",
    layout="wide"
)

# Session check
if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False

if not st.session_state.get('logged_in'):
    st.warning("Please log in to access the Home Page.")
    if st.button("Go to Login Page"):
        st.switch_page("Home.py")
    st.stop()
else:
    st.success("Logged in successfully!")

# DB connection
conn = get_connection()

# Sidebar: Domain selection
with st.sidebar:
    st.header("Navigation")
    domain = st.selectbox("Select Domain", ["Cyber Incidents", "IT Tickets", "Metadata"])

# Load data based on domain
filtered_data = pd.DataFrame()  # default empty

if domain == "Cyber Incidents":
    data = get_all_cyber_incidents(conn)
    if 'timestamp' in data.columns:
        data['timestamp'] = pd.to_datetime(data['timestamp'])
    for col in ['severity', 'category']:
        if col in data.columns and data[col].dtype == 'object':
            data[col] = data[col].str.strip()
    severity_ = st.selectbox("Select Severity", data['severity'].unique())
    category_ = st.selectbox("Select Category", data['category'].unique())
    filtered_data = data[(data['severity'] == severity_) & (data['category'] == category_)]

elif domain == "IT Tickets":
    data = get_all_it_tickets(conn)
    for col in ['status', 'priority']:
        if col in data.columns and data[col].dtype == 'object':
            data[col] = data[col].str.strip()
    status_ = st.selectbox("Select Status", data['status'].unique())
    priority_ = st.selectbox("Select Priority", data['priority'].unique())
    filtered_data = data[(data['status'] == status_) & (data['priority'] == priority_)]

elif domain == "Metadata":
    data = get_all_datasets_metadata(conn)
    # Strip all string columns
    for col in data.select_dtypes(include='object').columns:
        data[col] = data[col].str.strip()
    # Use first two object columns for dynamic filters
    obj_cols = data.select_dtypes(include='object').columns.tolist()
    if len(obj_cols) >= 2:
        col1_filter = st.selectbox(f"Select {obj_cols[0]}", data[obj_cols[0]].unique())
        col2_filter = st.selectbox(f"Select {obj_cols[1]}", data[obj_cols[1]].unique())
        filtered_data = data[(data[obj_cols[0]] == col1_filter) & (data[obj_cols[1]] == col2_filter)]
    else:
        st.info("Not enough string columns to filter Metadata")
        filtered_data = data

# Layout columns
col1, col2 = st.columns(2)

# Plotly Charts
with col1:
    st.subheader(f"{domain} Overview")
    if not filtered_data.empty:
        # Bar chart
        if domain == "Cyber Incidents":
            bar_data = filtered_data['category'].value_counts().reset_index()
            bar_data.columns = ['Category', 'Count']
            fig = px.bar(
                bar_data, x='Category', y='Count', color='Count',
                color_continuous_scale='Viridis',
                title=f"Incidents by Category ({severity_})",
                hover_data={'Category': True, 'Count': True}
            )
        elif domain == "IT Tickets":
            bar_data = filtered_data['priority'].value_counts().reset_index()
            bar_data.columns = ['Priority', 'Count']
            fig = px.bar(
                bar_data, x='Priority', y='Count', color='Count',
                color_continuous_scale='Cividis',
                title=f"Tickets by Priority ({status_})",
                hover_data={'Priority': True, 'Count': True}
            )
        elif domain == "Metadata":
            bar_data = filtered_data[obj_cols[1]].value_counts().reset_index()
            bar_data.columns = [obj_cols[1], 'Count']
            fig = px.bar(
                bar_data, x=obj_cols[1], y='Count', color='Count',
                color_continuous_scale='Plasma',
                title=f"{obj_cols[1]} Counts for {obj_cols[0]}: {col1_filter}",
                hover_data={obj_cols[1]: True, 'Count': True}
            )
        fig.update_layout(title_x=0.5, hovermode='x')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.info("No data found for the selected filters.")

with col2:
    st.subheader(f"{domain} Trends Over Time")
    if not filtered_data.empty:
        # Only plot time-based line chart if timestamp exists
        if 'timestamp' in filtered_data.columns:
            line_fig = px.line(
                filtered_data, x='timestamp', y=filtered_data.select_dtypes(include='object').columns[0],
                markers=True,
                title=f"{domain} Trends Over Time"
            )
            line_fig.update_layout(title_x=0.5, hovermode='x unified')
            st.plotly_chart(line_fig, use_container_width=True)
        else:
            st.info("No timestamp column to plot trends.")
    else:
        st.info("No data to plot trends.")

# Show filtered data
st.subheader("Filtered Data")
st.dataframe(filtered_data)
