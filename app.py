import streamlit as st
import yaml
from yaml.loader import SafeLoader
import plotly.express as px
import pandas as pd
import numpy as np
from datetime import datetime
import hmac
import hashlib

# Configure the page settings
st.set_page_config(
    page_title="AI-Driven Spectrum Allocation Platform",
    page_icon="📡",
    layout="wide"
)

# Load configuration file for authentication
def load_config():
    try:
        with open('config.yaml') as file:
            config = yaml.load(file, Loader=SafeLoader)
            return config
    except FileNotFoundError:
        return None

# Simple password verification
def verify_password(password, stored_password):
    return password == stored_password

# Load the configuration
config = load_config()

# Initialize session state for authentication
if 'authenticated' not in st.session_state:
    st.session_state.authenticated = False
if 'username' not in st.session_state:
    st.session_state.username = None
if 'role' not in st.session_state:
    st.session_state.role = None

# Main application logic
if not st.session_state.authenticated:
    st.title('Login')
    username = st.text_input('Username')
    password = st.text_input('Password', type='password')
    
    if st.button('Login'):
        if config and username in config['credentials']['usernames']:
            stored_password = config['credentials']['usernames'][username]['password']
            if verify_password(password, stored_password):
                st.session_state.authenticated = True
                st.session_state.username = username
                st.session_state.role = username  # Using username as role (admin/operator/user)
                st.experimental_rerun()
            else:
                st.error('Invalid password')
        else:
            st.error('Username not found')

if st.session_state.authenticated:
    # Sidebar for navigation
    st.sidebar.title(f'Welcome {config["credentials"]["usernames"][st.session_state.username]["name"]}')
    
    # Role-based navigation options
    if st.session_state.role == 'admin':
        pages = ['Dashboard', 'Spectrum Analysis', 'Allocation Management', 'Reports', 'User Management']
    elif st.session_state.role == 'operator':
        pages = ['Dashboard', 'Spectrum Analysis', 'Allocation Management', 'Reports']
    else:  # user role
        pages = ['Dashboard', 'Spectrum Analysis', 'Reports']
    
    page = st.sidebar.selectbox('Navigation', pages)
    
    if st.sidebar.button('Logout'):
        st.session_state.authenticated = False
        st.session_state.username = None
        st.session_state.role = None
        st.experimental_rerun()
    
    if page == 'Dashboard':
        st.title('Spectrum Allocation Dashboard')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Current Spectrum Usage')
            data = np.random.rand(10, 10)
            fig = px.imshow(data,
                           labels=dict(x="Frequency", y="Time", color="Usage"),
                           title="Spectrum Usage Heatmap")
            st.plotly_chart(fig, use_container_width=True)
        
        with col2:
            st.subheader('Usage Trends')
            dates = pd.date_range(start='2023-01-01', end='2023-12-31', freq='M')
            values = np.random.randn(len(dates)).cumsum()
            df = pd.DataFrame({'Date': dates, 'Usage': values})
            fig = px.line(df, x='Date', y='Usage', title='Historical Spectrum Usage')
            st.plotly_chart(fig, use_container_width=True)
        
        st.subheader('Recent Alerts')
        alerts = [
            {'time': '2023-12-01 10:30', 'type': 'Congestion', 'message': 'High usage detected in Band A'},
            {'time': '2023-12-01 09:15', 'type': 'Interference', 'message': 'Potential interference in Band B'}
        ]
        for alert in alerts:
            st.warning(f"[{alert['time']}] {alert['type']}: {alert['message']}")
    
    elif page == 'Spectrum Analysis':
        st.title('AI-Powered Spectrum Analysis')
        
        # AI Analysis Tools
        analysis_type = st.selectbox(
            'Select Analysis Type',
            ['Interference Detection', 'Usage Prediction', 'Optimization Recommendations']
        )
        
        if analysis_type == 'Interference Detection':
            st.subheader('Interference Detection')
            # Simulated interference detection
            interference_data = np.random.rand(24)
            fig = px.line(x=range(24), y=interference_data,
                         labels={'x': 'Hour', 'y': 'Interference Level'},
                         title='24-Hour Interference Analysis')
            st.plotly_chart(fig)
            
            if st.button('Run Deep Analysis') and st.session_state.role != 'user':
                st.info('Running deep analysis...')
                st.success('Analysis complete! No critical interference detected.')
        
        elif analysis_type == 'Usage Prediction':
            st.subheader('Usage Prediction')
            days = st.slider('Prediction Window (Days)', 1, 30, 7)
            confidence = st.slider('Confidence Level (%)', 50, 95, 80)
            
            if st.button('Generate Prediction'):
                # Simulated AI prediction with confidence intervals
                dates = pd.date_range(start='2024-01-01', periods=days)
                base_predictions = np.random.randn(days).cumsum()
                
                # Generate confidence intervals
                confidence_range = (100 - confidence) / 100
                lower_bound = base_predictions - np.random.rand(days) * confidence_range * 10
                upper_bound = base_predictions + np.random.rand(days) * confidence_range * 10
                
                # Create prediction DataFrame
                pred_df = pd.DataFrame({
                    'Date': dates,
                    'Predicted Usage': base_predictions,
                    'Lower Bound': lower_bound,
                    'Upper Bound': upper_bound
                })
                
                # Plot with confidence intervals
                fig = px.line(pred_df, x='Date', y=['Predicted Usage', 'Lower Bound', 'Upper Bound'],
                             labels={'value': 'Usage', 'variable': 'Prediction Type'},
                             title=f'Usage Prediction with {confidence}% Confidence Interval')
                st.plotly_chart(fig)
                
                # Add prediction insights
                avg_prediction = np.mean(base_predictions)
                trend = 'increasing' if base_predictions[-1] > base_predictions[0] else 'decreasing'
                st.info(f'Average predicted usage: {avg_prediction:.2f} with a {trend} trend')
    
    elif page == 'Allocation Management' and st.session_state.role != 'user':
        st.title('Spectrum Allocation Management')
        
        col1, col2 = st.columns(2)
        
        with col1:
            st.subheader('Allocation Request')
            frequency_band = st.selectbox('Frequency Band', ['Band A', 'Band B', 'Band C'])
            bandwidth = st.slider('Bandwidth (MHz)', 1, 100, 10)
            duration = st.selectbox('Duration', ['1 hour', '1 day', '1 week', '1 month'])
            
            if st.button('Submit Request'):
                st.success('Allocation request submitted successfully!')
        
        with col2:
            st.subheader('Active Allocations')
            allocations = pd.DataFrame({
                'Band': ['A', 'B', 'C'],
                'Usage (%)': [75, 45, 90],
                'Status': ['Active', 'Active', 'Near Capacity']
            })
            st.dataframe(allocations)
    
    elif page == 'Reports':
        st.title('Regulatory Reports')
        
        report_type = st.selectbox(
            'Report Type',
            ['Usage Summary', 'Compliance Report', 'Interference Report']
        )
        
        date_range = st.date_input(
            'Select Date Range',
            [datetime.now(), datetime.now()]
        )
        
        if st.button('Generate Report'):
            st.subheader(f'{report_type} - {date_range[0]} to {date_range[1]}')
            
            if report_type == 'Usage Summary':
                # Simulated usage data
                usage_data = pd.DataFrame({
                    'Band': ['A', 'B', 'C'] * 4,
                    'Usage': np.random.rand(12) * 100,
                    'Date': pd.date_range(start=date_range[0], periods=4).repeat(3)
                })
                fig = px.line(usage_data, x='Date', y='Usage', color='Band',
                             title='Band Usage Over Time')
                st.plotly_chart(fig)
            
            st.download_button(
                'Download Report',
                'Report data would be here in real implementation',
                'report.csv'
            )
    
    elif page == 'User Management' and st.session_state.role == 'admin':
        st.title('User Management')
        
        st.subheader('Add New User')
        new_username = st.text_input('Username')
        new_role = st.selectbox('Role', ['user', 'operator', 'admin'])
        new_email = st.text_input('Email')
        
        if st.button('Add User'):
            st.success(f'User {new_username} added successfully!')
        
        st.subheader('Existing Users')
        users_df = pd.DataFrame({
            'Username': list(config['credentials']['usernames'].keys()),
            'Role': list(config['credentials']['usernames'].keys()),
            'Email': [user['email'] for user in config['credentials']['usernames'].values()]
        })
        st.dataframe(users_df)