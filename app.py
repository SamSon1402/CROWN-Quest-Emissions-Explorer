import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import numpy as np
from PIL import Image

# Set page configuration
st.set_page_config(
    page_title="CROWN Quest: Emissions Explorer",
    page_icon="🎮",
    layout="wide",
)

# Custom CSS for retro gaming aesthetic
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=VT323&family=Space+Mono&display=swap');

:root {
    --coral-main: #FF6F61;
    --coral-dark: #E05A4F;
    --coral-light: #FF8577;
    --pixel-black: #0D1117;
    --pixel-blue: #2F3E75;
}

/* Global Styles */
.stApp {
    background-color: var(--pixel-black);
}

h1, h2, h3 {
    font-family: 'VT323', monospace !important;
    color: var(--coral-main) !important;
    text-shadow: 2px 2px 0px var(--coral-dark);
    letter-spacing: 1px;
}

p, li, .stMarkdown {
    font-family: 'Space Mono', monospace !important;
    color: #FFFFFF;
}

/* Button Styling */
.stButton>button {
    font-family: 'VT323', monospace !important;
    background-color: var(--coral-main);
    color: white;
    border: 4px solid var(--coral-dark);
    box-shadow: 4px 4px 0px var(--coral-dark);
    transition: all 0.1s ease;
}

.stButton>button:hover {
    box-shadow: 2px 2px 0px var(--coral-dark);
    transform: translate(2px, 2px);
}

/* Widget Styling */
.stSlider, .stSelectbox {
    border: 2px solid var(--coral-dark);
    padding: 4px;
}

/* Metric Card */
.metric-container {
    background-color: var(--pixel-blue);
    border: 4px solid var(--coral-main);
    padding: 20px;
    border-radius: 0px;
    box-shadow: 8px 8px 0px var(--coral-dark);
    margin-bottom: 20px;
}

/* Progress Bar */
.stProgress > div > div {
    background-color: var(--coral-main);
}

/* Divider */
hr {
    border-top: 4px dashed var(--coral-light);
}

/* Data tables */
.dataframe {
    font-family: 'Space Mono', monospace !important;
}

</style>
""", unsafe_allow_html=True)

# App Header with pixel art title
st.markdown("<h1 style='text-align: center; font-size: 52px;'>🎮 CROWN QUEST: EMISSIONS EXPLORER 🎮</h1>", unsafe_allow_html=True)

# Simulated data loading
@st.cache_data
def load_data():
    # This would be replaced with actual data loading in a real scenario
    categories = ['Raw Materials', 'Manufacturing', 'Transport', 'Packaging', 'End of Life']
    tiers = ['Tier 1', 'Tier 2', 'Tier 3']
    regions = ['Europe', 'North America', 'Asia', 'South America', 'Africa']
    
    # Create sample dataframe
    data = []
    for category in categories:
        for tier in tiers:
            for region in regions:
                emissions = np.random.randint(50, 500)
                data_quality = np.random.randint(1, 6)
                data.append({
                    'Category': category,
                    'Tier': tier,
                    'Region': region,
                    'Emissions (tCO2e)': emissions,
                    'Data Quality Score': data_quality
                })
    
    return pd.DataFrame(data)

df = load_data()

# Sidebar with game controller aesthetic
with st.sidebar:
    st.markdown("<h2>CONTROL PANEL</h2>", unsafe_allow_html=True)
    st.markdown("<hr>", unsafe_allow_html=True)
    
    # Filters
    st.markdown("<h3>SELECT YOUR DATA</h3>", unsafe_allow_html=True)
    selected_tiers = st.multiselect("Supply Chain Tiers", options=df['Tier'].unique(), default=df['Tier'].unique())
    selected_regions = st.multiselect("Regions", options=df['Region'].unique(), default=df['Region'].unique())
    
    # Filter the data
    filtered_df = df[(df['Tier'].isin(selected_tiers)) & (df['Region'].isin(selected_regions))]
    
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown("<h3>DATA QUEST PROGRESS</h3>", unsafe_allow_html=True)
    
    # Data quality metrics styled as quest progress
    data_quality_avg = filtered_df['Data Quality Score'].mean()
    st.markdown(f"<p>Data Quality Level:</p>", unsafe_allow_html=True)
    st.progress(data_quality_avg/5)
    
    # Achievement section
    if data_quality_avg > 3:
        st.success("🏆 ACHIEVEMENT UNLOCKED: High Quality Data Master")
    else:
        st.info("🔒 Next Achievement: Reach average data quality score of 4")

# Main content area split into two columns
col1, col2 = st.columns(2)

with col1:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown("<h2>EMISSIONS BY CATEGORY</h2>", unsafe_allow_html=True)
    
    # Category bar chart with custom pixel-art inspired theme
    cat_emissions = filtered_df.groupby('Category')['Emissions (tCO2e)'].sum().reset_index()
    fig_cat = px.bar(
        cat_emissions, 
        x='Category', 
        y='Emissions (tCO2e)',
        color='Emissions (tCO2e)',
        color_continuous_scale=['#FF6F61', '#FF8577', '#FFA799', '#FFCCC2', '#FFE1DE'],
        template='plotly_dark'
    )
    fig_cat.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    st.plotly_chart(fig_cat, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Interactive heat map
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown("<h2>EMISSIONS HEAT MAP</h2>", unsafe_allow_html=True)
    
    # Create pivot table for heatmap
    heatmap_data = filtered_df.pivot_table(
        index='Region', 
        columns='Category',
        values='Emissions (tCO2e)',
        aggfunc='sum'
    )
    
    fig_heatmap = px.imshow(
        heatmap_data,
        color_continuous_scale=['#2F3E75', '#3F5294', '#FF6F61', '#E05A4F', '#C8412E'],
        aspect="auto"
    )
    fig_heatmap.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    st.plotly_chart(fig_heatmap, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

with col2:
    # Sankey diagram with pixel styling
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown("<h2>EMISSIONS FLOW MAP</h2>", unsafe_allow_html=True)
    
    # Create data for Sankey diagram
    tier_cat = filtered_df.groupby(['Tier', 'Category'])['Emissions (tCO2e)'].sum().reset_index()
    
    # Create lists for Sankey diagram
    label_list = list(tier_cat['Tier'].unique()) + list(tier_cat['Category'].unique())
    
    # Create source, target and value lists
    source_list = []
    target_list = []
    value_list = []
    
    # Map tiers to their indices
    tier_indices = {tier: idx for idx, tier in enumerate(tier_cat['Tier'].unique())}
    # Map categories to their indices (offset by number of tiers)
    cat_indices = {cat: idx + len(tier_indices) for idx, cat in enumerate(tier_cat['Category'].unique())}
    
    # Create the links
    for _, row in tier_cat.iterrows():
        source_list.append(tier_indices[row['Tier']])
        target_list.append(cat_indices[row['Category']])
        value_list.append(row['Emissions (tCO2e)'])
    
    # Create Sankey diagram
    fig_sankey = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label_list,
            color=['#FF6F61', '#FF8577', '#FFA799'] + ['#E05A4F', '#C8412E', '#A73229', '#892920', '#6F2018'][:len(cat_indices)]
        ),
        link=dict(
            source=source_list,
            target=target_list,
            value=value_list,
            color=['rgba(255, 111, 97, 0.4)'] * len(value_list)
        )
    )])
    
    fig_sankey.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    
    st.plotly_chart(fig_sankey, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)
    
    # Data quality section
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown("<h2>DATA QUALITY RADAR</h2>", unsafe_allow_html=True)
    
    quality_by_category = filtered_df.groupby('Category')['Data Quality Score'].mean().reset_index()
    
    # Create radar chart for data quality
    categories = quality_by_category['Category'].tolist()
    values = quality_by_category['Data Quality Score'].tolist()
    
    fig_radar = go.Figure()
    
    fig_radar.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(255, 111, 97, 0.5)',
        line=dict(color='#FF6F61', width=3)
    ))
    
    fig_radar.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5]
            )
        ),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    
    st.plotly_chart(fig_radar, use_container_width=True)
    st.markdown('</div>', unsafe_allow_html=True)

# Decarbonization scenario section
st.markdown("<h2>DECARBONIZATION SCENARIO SIMULATOR</h2>", unsafe_allow_html=True)
st.markdown("<p>Adjust the sliders to simulate different reduction strategies and see their impact</p>", unsafe_allow_html=True)

col3, col4 = st.columns(2)

with col3:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    
    # Category reduction sliders
    reduction_values = {}
    for category in df['Category'].unique():
        reduction_values[category] = st.slider(
            f"{category} Emissions Reduction (%)", 
            min_value=0, 
            max_value=100, 
            value=20,
            key=f"slider_{category}"
        )
    
    # Calculate new emissions with reductions
    current_total = filtered_df['Emissions (tCO2e)'].sum()
    
    new_total = current_total
    category_savings = {}
    
    for category in reduction_values:
        category_emissions = filtered_df[filtered_df['Category'] == category]['Emissions (tCO2e)'].sum()
        savings = category_emissions * (reduction_values[category] / 100)
        category_savings[category] = savings
        new_total -= savings
    
    st.markdown('</div>', unsafe_allow_html=True)

with col4:
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    
    # Results display
    reduction_percentage = ((current_total - new_total) / current_total) * 100
    
    st.markdown(f"<h3>EMISSIONS REDUCTION RESULTS</h3>", unsafe_allow_html=True)
    st.markdown(f"<p>Current Emissions: {current_total:.1f} tCO2e</p>", unsafe_allow_html=True)
    st.markdown(f"<p>New Emissions: {new_total:.1f} tCO2e</p>", unsafe_allow_html=True)
    st.markdown(f"<p>Total Reduction: {current_total - new_total:.1f} tCO2e ({reduction_percentage:.1f}%)</p>", unsafe_allow_html=True)
    
    # Create data for reduction visualization
    categories = list(category_savings.keys())
    savings = list(category_savings.values())
    
    fig_savings = px.bar(
        x=categories, 
        y=savings,
        labels={"x": "Category", "y": "Emissions Savings (tCO2e)"},
        color=savings,
        color_continuous_scale=['#FF6F61', '#E05A4F', '#C8412E'],
        template='plotly_dark'
    )
    
    fig_savings.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    
    st.plotly_chart(fig_savings, use_container_width=True)
    
    # Achievement system
    if reduction_percentage > 30:
        st.success("🏆 ACHIEVEMENT UNLOCKED: Carbon Reduction Champion")
    elif reduction_percentage > 20:
        st.success("🏆 ACHIEVEMENT UNLOCKED: Climate Defender")
    elif reduction_percentage > 10:
        st.success("🏆 ACHIEVEMENT UNLOCKED: Emission Cutter")
    
    st.markdown('</div>', unsafe_allow_html=True)

# Footer section
st.markdown("<hr>", unsafe_allow_html=True)
st.markdown(
    "<p style='text-align: center;'>Created for Crown Holdings - Sustainability Data Analyst Internship</p>", 
    unsafe_allow_html=True
)