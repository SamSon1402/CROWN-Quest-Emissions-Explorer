import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import Dict, List, Tuple, Optional

# Color constants
COLORS = {
    'main': '#FF6F61',
    'dark': '#E05A4F',
    'light': '#FF8577',
    'background': '#0D1117',
    'blue': '#2F3E75',
    'white': '#FFFFFF'
}

CORAL_PALETTE = ['#FF6F61', '#FF8577', '#FFA799', '#FFCCC2', '#FFE1DE']
CORAL_DARK_PALETTE = ['#E05A4F', '#C8412E', '#A73229', '#892920', '#6F2018']

def create_emissions_bar_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create bar chart showing emissions by category
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        Plotly figure object
    """
    if df.empty or 'Category' not in df.columns or 'Emissions (tCO2e)' not in df.columns:
        # Return empty figure if no data
        return go.Figure()
    
    # Group by category
    cat_emissions = df.groupby('Category')['Emissions (tCO2e)'].sum().reset_index()
    
    # Create bar chart with retro coral color scheme
    fig = px.bar(
        cat_emissions, 
        x='Category', 
        y='Emissions (tCO2e)',
        color='Emissions (tCO2e)',
        color_continuous_scale=CORAL_PALETTE,
        template='plotly_dark'
    )
    
    # Apply retro styling
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    
    # Add pixel-like border to bars
    fig.update_traces(
        marker_line_width=1,
        marker_line_color=COLORS['dark']
    )
    
    return fig

def create_heatmap(df: pd.DataFrame) -> go.Figure:
    """
    Create emissions heat map by region and category
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        Plotly figure object
    """
    if df.empty or 'Region' not in df.columns or 'Category' not in df.columns:
        return go.Figure()
    
    # Create pivot table for heatmap
    heatmap_data = df.pivot_table(
        index='Region', 
        columns='Category',
        values='Emissions (tCO2e)',
        aggfunc='sum'
    )
    
    # Create heatmap with custom color scale
    fig = px.imshow(
        heatmap_data,
        color_continuous_scale=[COLORS['blue'], '#3F5294', COLORS['main'], COLORS['dark'], '#C8412E'],
        aspect="auto"
    )
    
    # Apply retro styling
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    
    # Add pixel-like borders
    fig.update_traces(
        xgap=3,  # Add gap between cells
        ygap=3
    )
    
    return fig

def create_sankey_diagram(df: pd.DataFrame) -> go.Figure:
    """
    Create Sankey diagram showing emissions flow from tiers to categories
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        Plotly figure object
    """
    if df.empty or 'Tier' not in df.columns or 'Category' not in df.columns:
        return go.Figure()
    
    # Group by tier and category
    tier_cat = df.groupby(['Tier', 'Category'])['Emissions (tCO2e)'].sum().reset_index()
    
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
    
    # Calculate number of tiers and categories for color allocation
    num_tiers = len(tier_indices)
    
    # Create node colors: corals for tiers, darker corals for categories
    tier_colors = CORAL_PALETTE[:num_tiers] if num_tiers <= len(CORAL_PALETTE) else [CORAL_PALETTE[i % len(CORAL_PALETTE)] for i in range(num_tiers)]
    cat_colors = CORAL_DARK_PALETTE[:len(cat_indices)] if len(cat_indices) <= len(CORAL_DARK_PALETTE) else [CORAL_DARK_PALETTE[i % len(CORAL_DARK_PALETTE)] for i in range(len(cat_indices))]
    node_colors = tier_colors + cat_colors
    
    # Create Sankey diagram with retro colors
    fig = go.Figure(data=[go.Sankey(
        node=dict(
            pad=15,
            thickness=20,
            line=dict(color="black", width=0.5),
            label=label_list,
            color=node_colors
        ),
        link=dict(
            source=source_list,
            target=target_list,
            value=value_list,
            color=['rgba(255, 111, 97, 0.4)'] * len(value_list)
        )
    )])
    
    # Apply retro styling
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    
    return fig

def create_data_quality_radar(quality_df: pd.DataFrame) -> go.Figure:
    """
    Create radar chart showing data quality by category
    
    Args:
        quality_df: DataFrame with categories and quality scores
        
    Returns:
        Plotly figure object
    """
    if quality_df.empty or 'Category' not in quality_df.columns or 'Data Quality Score' not in quality_df.columns:
        return go.Figure()
    
    categories = quality_df['Category'].tolist()
    values = quality_df['Data Quality Score'].tolist()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatterpolar(
        r=values,
        theta=categories,
        fill='toself',
        fillcolor='rgba(255, 111, 97, 0.5)',
        line=dict(color=COLORS['main'], width=3)
    ))
    
    fig.update_layout(
        polar=dict(
            radialaxis=dict(
                visible=True,
                range=[0, 5],
                tickvals=[1, 2, 3, 4, 5],
                ticktext=['1', '2', '3', '4', '5'],
                tickangle=0,
                gridcolor='rgba(255, 255, 255, 0.2)',
                linecolor='rgba(255, 255, 255, 0.2)'
            ),
            angularaxis=dict(
                gridcolor='rgba(255, 255, 255, 0.2)',
                linecolor='rgba(255, 255, 255, 0.2)'
            ),
            bgcolor='rgba(0,0,0,0)'
        ),
        showlegend=False,
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    
    return fig

def create_reduction_results_chart(category_savings: Dict[str, float]) -> go.Figure:
    """
    Create bar chart showing emissions savings by category
    
    Args:
        category_savings: Dictionary mapping categories to savings values
        
    Returns:
        Plotly figure object
    """
    if not category_savings:
        return go.Figure()
    
    # Convert dictionary to lists
    categories = list(category_savings.keys())
    savings = list(category_savings.values())
    
    # Create DataFrame for plotting
    savings_df = pd.DataFrame({
        'Category': categories,
        'Emissions Savings (tCO2e)': savings
    })
    
    # Sort by savings amount for better visualization
    savings_df = savings_df.sort_values('Emissions Savings (tCO2e)', ascending=False)
    
    # Create bar chart
    fig = px.bar(
        savings_df, 
        x='Category', 
        y='Emissions Savings (tCO2e)',
        color='Emissions Savings (tCO2e)',
        color_continuous_scale=CORAL_PALETTE,
        template='plotly_dark'
    )
    
    # Apply retro styling
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    
    # Add pixel-like border to bars
    fig.update_traces(
        marker_line_width=1,
        marker_line_color=COLORS['dark']
    )
    
    return fig

def create_regional_emissions_chart(df: pd.DataFrame) -> go.Figure:
    """
    Create bar chart showing emissions by region
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        Plotly figure object
    """
    if df.empty or 'Region' not in df.columns or 'Emissions (tCO2e)' not in df.columns:
        return go.Figure()
    
    # Group by region
    region_emissions = df.groupby('Region')['Emissions (tCO2e)'].sum().reset_index()
    
    # Sort by emissions amount
    region_emissions = region_emissions.sort_values('Emissions (tCO2e)', ascending=False)
    
    # Create bar chart
    fig = px.bar(
        region_emissions, 
        x='Region', 
        y='Emissions (tCO2e)',
        color='Emissions (tCO2e)',
        color_continuous_scale=CORAL_PALETTE,
        template='plotly_dark'
    )
    
    # Apply retro styling
    fig.update_layout(
        plot_bgcolor='rgba(0,0,0,0)',
        paper_bgcolor='rgba(0,0,0,0)',
        font=dict(family='VT323', size=14),
        margin=dict(l=40, r=40, t=10, b=10),
    )
    
    # Add pixel-like border to bars
    fig.update_traces(
        marker_line_width=1,
        marker_line_color=COLORS['dark']
    )
    
    return fig