import streamlit as st
import pandas as pd

class JMeterCalculator:
    def calculate_users(self, throughput, response_time, think_time, pacing):
        cycle_time = response_time + think_time + pacing
        users = throughput * cycle_time
        return int(users)
    
    def calculate_ramp_up(self, users, speed='moderate'):
        if speed == 'fast':
            ramp_up = users / 10
        elif speed == 'moderate':
            ramp_up = users / 5
        else:
            ramp_up = users / 2
        return max(10, min(int(ramp_up), 600))
    
    def generate_options(self, target_throughput, response_time):
        users_1 = self.calculate_users(target_throughput, response_time, 0, 0)
        ramp_up_1 = self.calculate_ramp_up(users_1, 'fast')
        
        users_2 = self.calculate_users(target_throughput, response_time, 2, 0)
        ramp_up_2 = self.calculate_ramp_up(users_2, 'moderate')
        
        users_3 = self.calculate_users(target_throughput, response_time, 3, 2)
        ramp_up_3 = self.calculate_ramp_up(users_3, 'slow')
        
        return [
            {'name': 'Aggressive', 'users': users_1, 'think_time': 0, 'pacing': 0, 'ramp_up': ramp_up_1, 'desc': 'Minimum users, maximum stress'},
            {'name': 'Realistic', 'users': users_2, 'think_time': 2, 'pacing': 0, 'ramp_up': ramp_up_2, 'desc': 'Normal user behavior'},
            {'name': 'Steady', 'users': users_3, 'think_time': 3, 'pacing': 2, 'ramp_up': ramp_up_3, 'desc': 'Distributed load'}
        ]

# Web interface starts here
st.title("🚀 JMeter Configuration Calculator")
st.markdown("Get the perfect JMeter settings instantly!")

# Input boxes
col1, col2 = st.columns(2)

with col1:
    target = st.number_input("Target Throughput (req/sec)", min_value=1.0, value=100.0, step=10.0)

with col2:
    response = st.number_input("Response Time (seconds)", min_value=0.1, value=2.0, step=0.1)

# Calculate button
if st.button("Calculate Configuration", type="primary"):
    calc = JMeterCalculator()
    options = calc.generate_options(target, response)
    
    st.success("✅ Configurations ready!")
    
    # Show results in tabs
    tab1, tab2, tab3 = st.tabs(["Aggressive", "Realistic", "Steady Load"])
    
    for tab, option in zip([tab1, tab2, tab3], options):
        with tab:
            col1, col2, col3, col4 = st.columns(4)
            
            with col1:
                st.metric("👥 Users", option['users'])
            with col2:
                st.metric("⏱️ Ramp-up", f"{option['ramp_up']}s")
            with col3:
                st.metric("💭 Think Time", f"{option['think_time']}s")
            with col4:
                st.metric("⏸️ Pacing", f"{option['pacing']}s")
            
            st.info(f"**Use Case:** {option['desc']}")
            
            # JMeter config
            st.code(f"""JMeter Configuration:
Number of Threads: {option['users']}
Ramp-up Period: {option['ramp_up']} seconds
Think Time: {option['think_time']} seconds
Pacing: {option['pacing']} seconds""")

st.markdown("---")
st.markdown("💡 **Tip:** Start with 'Realistic' configuration for most tests")