import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# Load the dataset
@st.cache
def load_data():
    return pd.read_csv('tva_project_data.csv')

# Function to format the dataframe for display
def format_df(df):
    return df.style.format({
        'Cost': '${:,.2f}',
        'Start Date': lambda x: pd.to_datetime(x).strftime('%Y-%m-%d'),
        'End Date': lambda x: pd.to_datetime(x).strftime('%Y-%m-%d')
    })

# Home Page with more detailed introduction and project summary
def home():
    st.title("Project Overview")
    st.write("Welcome to the Tennessee Valley Authority IT Modernization Dashboard.")
    st.markdown("""
    - **Replace Older IT Systems**: To introduce scalability, flexibility, and operational efficiency.
    - **Integrate Data and Management**: For optimized decision-making.
    - **Effective Change Management**: Ensure seamless technology adaptation.
    """)
    st.image("https://via.placeholder.com/800x300.png", caption='Project Visualization')

# Detailed Project Phases and Tasks with Filters and Visuals
def project_details():
    st.title("Project Phases and Tasks")
    data = load_data()
    phase = st.selectbox("Select Phase:", ['All'] + list(data['Phase'].unique()))
    if phase != 'All':
        data = data[data['Phase'] == phase]
    
    status = st.multiselect("Filter by Status:", options=data['Status'].unique(), default=data['Status'].unique())
    filtered_data = data[data['Status'].isin(status)]
    
    st.dataframe(format_df(filtered_data))
    st.markdown("### Phase Cost Breakdown")
    fig, ax = plt.subplots()
    filtered_data.groupby('Status')['Cost'].sum().plot(kind='barh', ax=ax)
    st.pyplot(fig)

# Financial Overview with Enhanced Visualizations
def financial_overview():
    st.title("Financial Overview")
    data = load_data()
    total_cost = data['Cost'].sum()
    st.write("Total Estimated Cost: ${:,.2f}".format(total_cost))
    
    st.markdown("### Cost Distribution by Phase")
    cost_by_phase = data.groupby('Phase')['Cost'].sum().sort_values()
    st.bar_chart(cost_by_phase)

    st.markdown("### Detailed Cost Analysis")
    st.dataframe(data.groupby(['Phase', 'Status'])['Cost'].describe())

# Progress Tracker with Status and Timeline Visuals
def project_status():
    st.title("Project Status")
    data = load_data()
    status_counts = data['Status'].value_counts()
    st.write("Status Overview:")
    st.bar_chart(status_counts)
    
    st.markdown("### Detailed Status by Phase")
    status_by_phase = pd.crosstab(data['Phase'], data['Status'])
    st.bar_chart(status_by_phase)

# Main app configuration
def main():
    st.sidebar.title("Navigation")
    page = st.sidebar.radio("Go to", ['Home', 'Project Details', 'Financial Overview', 'Project Status'])

    if page == 'Home':
        home()
    elif page == 'Project Details':
        project_details()
    elif page == 'Financial Overview':
        financial_overview()
    elif page == 'Project Status':
        project_status()

if __name__ == "__main__":
    main()
