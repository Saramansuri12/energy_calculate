import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go

# Set page config
st.set_page_config(
    page_title="Energy Consumption Calculator",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        background: linear-gradient(90deg, #667eea 0%, #764ba2 100%);
        padding: 2rem;
        border-radius: 10px;
        margin-bottom: 2rem;
        text-align: center;
    }
    
    .main-header h1 {
        color: white;
        font-size: 3rem;
        margin-bottom: 0.5rem;
    }
    
    .main-header p {
        color: white;
        font-size: 1.2rem;
        opacity: 0.9;
    }
    
    .section-header {
        background: linear-gradient(45deg, #f093fb 0%, #f5576c 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 1rem 0;
        color: white;
        font-weight: bold;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
        padding: 1.5rem;
        border-radius: 10px;
        color: white;
        text-align: center;
        margin: 0.5rem 0;
    }
    
    .tip-card {
        background: linear-gradient(135deg, #ffecd2 0%, #fcb69f 100%);
        padding: 1.5rem;
        border-radius: 10px;
        margin: 1rem 0;
        border-left: 5px solid #ff6b6b;
    }
    
    .appliance-card {
        background: linear-gradient(135deg, #a8edea 0%, #fed6e3 100%);
        padding: 1rem;
        border-radius: 8px;
        margin: 0.5rem 0;
        border-left: 4px solid #4ecdc4;
    }
    
    .stSelectbox > div > div > div {
        background-color: #f8f9ff;
    }
    
    .stTextInput > div > div > input {
        background-color: #f8f9ff;
    }
    
    .stButton > button {
        background: linear-gradient(45deg, #667eea 0%, #764ba2 100%);
        color: white;
        border: none;
        padding: 0.75rem 2rem;
        border-radius: 25px;
        font-weight: bold;
        font-size: 1.1rem;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 5px 15px rgba(0,0,0,0.2);
    }
</style>
""", unsafe_allow_html=True)

# Modern Header
st.markdown("""
<div class="main-header">
    <h1>⚡ Energy Consumption Calculator</h1>
    <p>Smart energy management for your home</p>
</div>
""", unsafe_allow_html=True)

# Sidebar for inputs
with st.sidebar:
    st.markdown("### 👤 Personal Information")
    name = st.text_input("👨‍💼 Name", placeholder="Enter your name")
    age = st.slider("🎂 Age", min_value=18, max_value=100, value=25)
    area = st.text_input("📍 Area", placeholder="e.g., Downtown")
    city = st.text_input("🏙️ City", placeholder="e.g., Mumbai")
    
    st.markdown("### 🏠 House Details")
    home_type = st.selectbox("🏡 House Type", ["Flat", "Tenament"])
    rooms = st.selectbox("🏠 Room Configuration", ["1BHK", "2BHK", "3BHK"])
    
    st.markdown("### 📅 Day Selection")
    selected_day = st.selectbox(
        "📆 Select Day",
        ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
    )
    
    st.markdown("### 🔌 Appliances")
    
    # AC Section
    has_ac = st.toggle("❄️ Air Conditioner", value=False)
    num_ac = 0
    if has_ac:
        num_ac = st.slider("Number of ACs", min_value=1, max_value=5, value=1)
    
    # Other appliances
    has_fridge = st.toggle("🧊 Refrigerator", value=True)
    has_washing = st.toggle("👕 Washing Machine", value=False)

# Main content area
col1, col2 = st.columns([2, 1])

with col1:
    # Calculate button
    if st.button("🔍 Calculate Energy Consumption", type="primary"):
        if name and age and area and city and selected_day:
            # Initialize energy calculation
            cal_energy = 0
            
            # Set fans and lights based on room type
            rooms_lower = rooms.lower()
            if rooms_lower == "1bhk":
                fans = 2
                lights = 2
            elif rooms_lower == "2bhk":
                fans = 3
                lights = 3
            elif rooms_lower == "3bhk":
                fans = 4
                lights = 4
            
            # Day-based energy consumption multipliers
            day_multipliers = {
                "Monday": 1.0,      # Regular working day
                "Tuesday": 1.0,     # Regular working day
                "Wednesday": 1.0,   # Regular working day
                "Thursday": 1.0,    # Regular working day
                "Friday": 1.1,      # Slightly higher usage
                "Saturday": 1.3,    # Weekend - higher usage
                "Sunday": 1.2       # Weekend - moderate usage
            }
            
            # Get multiplier for selected day
            day_multiplier = day_multipliers.get(selected_day, 1.0)
            
            # Calculate base energy (fans + lights)
            base_energy = (fans * 0.4) + (lights * 0.8)
            
            # Add AC consumption
            ac_energy = 0
            if has_ac:
                ac_energy = num_ac * 3
            
            # Add fridge consumption (constant regardless of day)
            fridge_energy = 0
            if has_fridge:
                fridge_energy = 4
            
            # Add washing machine consumption
            washing_energy = 0
            if has_washing:
                washing_energy = 2
            
            # Calculate total energy with day multiplier
            cal_energy = ((base_energy + ac_energy + washing_energy) * day_multiplier) + fridge_energy
            
            # Display results with modern styling
            st.success("✅ Calculation Complete!")
            
            # User Info Card
            st.markdown("### 👤 User Profile")
            with st.container():
                info_col1, info_col2, info_col3 = st.columns(3)
                with info_col1:
                    st.metric("👨‍💼 Name", name)
                    st.metric("🎂 Age", f"{age} years")
                with info_col2:
                    st.metric("📍 Location", f"{area}, {city}")
                    st.metric("🏠 House Type", f"{home_type} - {rooms}")
                with info_col3:
                    st.metric("📅 Selected Day", selected_day)
                    st.metric("📊 Usage Factor", f"{day_multiplier}x")
            
            # Energy Consumption Metrics
            st.markdown("### ⚡ Energy Consumption Overview")
            
            metric_col1, metric_col2, metric_col3, metric_col4 = st.columns(4)
            
            with metric_col1:
                st.metric(
                    label="Today's Consumption",
                    value=f"{cal_energy:.1f} kWh",
                    delta=f"{((cal_energy - (cal_energy/day_multiplier)) if day_multiplier != 1.0 else 0):.1f} kWh"
                )
            
            with metric_col2:
                weekly_avg = cal_energy * 7 / day_multiplier
                st.metric(
                    label="Weekly Average",
                    value=f"{weekly_avg:.1f} kWh"
                )
            
            with metric_col3:
                monthly_avg = cal_energy * 30 / day_multiplier
                st.metric(
                    label="Monthly Average",
                    value=f"{monthly_avg:.1f} kWh"
                )
            
            with metric_col4:
                yearly_avg = cal_energy * 365 / day_multiplier
                st.metric(
                    label="Yearly Estimate",
                    value=f"{yearly_avg:.0f} kWh"
                )
            
            # Appliance Breakdown
            st.markdown("### 🔌 Appliance Breakdown")
            
            breakdown_data = []
            
            # Add fans
            breakdown_data.append({
                "Appliance": "💨 Fans",
                "Quantity": fans,
                "Power (kW)": 0.4,
                "Base (kWh)": fans * 0.4,
                "Today's Usage (kWh)": fans * 0.4 * day_multiplier
            })
            
            # Add lights
            breakdown_data.append({
                "Appliance": "💡 Lights",
                "Quantity": lights,
                "Power (kW)": 0.8,
                "Base (kWh)": lights * 0.8,
                "Today's Usage (kWh)": lights * 0.8 * day_multiplier
            })
            
            # Add AC if present
            if has_ac:
                breakdown_data.append({
                    "Appliance": "❄️ Air Conditioner",
                    "Quantity": num_ac,
                    "Power (kW)": 3.0,
                    "Base (kWh)": num_ac * 3,
                    "Today's Usage (kWh)": num_ac * 3 * day_multiplier
                })
            
            # Add fridge if present
            if has_fridge:
                breakdown_data.append({
                    "Appliance": "🧊 Refrigerator",
                    "Quantity": 1,
                    "Power (kW)": 4.0,
                    "Base (kWh)": 4,
                    "Today's Usage (kWh)": 4  # Constant consumption
                })
            
            # Add washing machine if present
            if has_washing:
                breakdown_data.append({
                    "Appliance": "👕 Washing Machine",
                    "Quantity": 1,
                    "Power (kW)": 2.0,
                    "Base (kWh)": 2,
                    "Today's Usage (kWh)": 2 * day_multiplier
                })
            
            # Create and display breakdown table
            df = pd.DataFrame(breakdown_data)
            st.dataframe(df, use_container_width=True)
            
            # Weekly Consumption Chart
            st.markdown("### 📊 Weekly Energy Consumption Pattern")
            
            days = ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday", "Saturday", "Sunday"]
            weekly_consumption = []
            
            for day in days:
                day_mult = day_multipliers.get(day, 1.0)
                day_energy = ((base_energy + ac_energy + washing_energy) * day_mult) + fridge_energy
                weekly_consumption.append(day_energy)
            
            # Create interactive chart
            fig = px.bar(
                x=days,
                y=weekly_consumption,
                labels={'x': 'Day of Week', 'y': 'Energy Consumption (kWh)'},
                title="Daily Energy Consumption Pattern",
                color=weekly_consumption,
                color_continuous_scale='viridis'
            )
            
            fig.update_layout(
                showlegend=False,
                xaxis_title="Day of Week",
                yaxis_title="Energy Consumption (kWh)",
                title_font_size=18,
                title_x=0.5
            )
            
            # Highlight selected day
            if selected_day in days:
                selected_index = days.index(selected_day)
                fig.update_traces(
                    marker_color=['red' if i == selected_index else 'lightblue' for i in range(len(days))]
                )
            
            st.plotly_chart(fig, use_container_width=True)
            
            # Pie chart for appliance contribution
            st.markdown("### 🥧 Energy Distribution by Appliance")
            
            appliance_names = [item["Appliance"] for item in breakdown_data]
            appliance_consumption = [item["Today's Usage (kWh)"] for item in breakdown_data]
            
            fig_pie = px.pie(
                values=appliance_consumption,
                names=appliance_names,
                title="Energy Consumption by Appliance"
            )
            
            fig_pie.update_layout(title_font_size=18, title_x=0.5)
            st.plotly_chart(fig_pie, use_container_width=True)
            
        else:
            st.error("❌ Please fill in all the required fields in the sidebar before calculating.")

with col2:
    # Energy Saving Tips
    st.markdown("### 💡 Smart Energy Tips")
    
    if selected_day in ["Saturday", "Sunday"]:
        tips = [
            "🌞 Use natural light during daytime",
            "⏰ Plan energy-intensive activities during off-peak hours",
            "🔌 Unplug unused appliances",
            "🌡️ Set AC to 24°C or higher for efficiency"
        ]
    else:
        tips = [
            "💡 Turn off lights when leaving",
            "🏠 Use smart thermostats",
            "🕐 Run appliances during off-peak hours",
            "🔋 Consider energy-efficient appliances"
        ]
    
    for tip in tips:
        st.markdown(f"""
        <div class="tip-card">
            <strong>{tip}</strong>
        </div>
        """, unsafe_allow_html=True)
    
    # Quick Stats
    st.markdown("### 📈 Quick Stats")
    
    if 'cal_energy' in locals():
        st.metric("Daily Cost Estimate", f"₹{cal_energy * 6:.0f}", help="Based on ₹6 per kWh")
        st.metric("Monthly Cost Estimate", f"₹{cal_energy * 30 * 6:.0f}")
        
        # Environmental impact
        co2_emission = cal_energy * 0.82  # kg CO2 per kWh
        st.metric("Daily CO₂ Emission", f"{co2_emission:.1f} kg", help="Carbon footprint estimate")

# Footer
st.markdown("---")
st.markdown("""
<div style="text-align: center; color: #666; font-size: 0.9rem;">
    <p>💡 This calculator provides estimates based on typical appliance power consumption.<br>
    Actual consumption may vary based on usage patterns and appliance efficiency.</p>
</div>
""", unsafe_allow_html=True)
