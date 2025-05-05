import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

def load_emissions_data(file_path: str) -> pd.DataFrame:
    """
    Load and clean emissions data from CSV file
    
    Args:
        file_path: Path to the CSV file
        
    Returns:
        DataFrame with cleaned emissions data
    """
    try:
        df = pd.read_csv(file_path)
        
        # Basic cleaning
        df.columns = df.columns.str.strip()
        
        # Convert emissions to numeric
        if 'Emissions (tCO2e)' in df.columns:
            df['Emissions (tCO2e)'] = pd.to_numeric(df['Emissions (tCO2e)'], errors='coerce')
        
        # Convert data quality to numeric
        if 'Data Quality Score' in df.columns:
            df['Data Quality Score'] = pd.to_numeric(df['Data Quality Score'], errors='coerce')
        
        # Fill missing values with column mean
        df = df.fillna(df.mean(numeric_only=True))
        
        return df
    except Exception as e:
        print(f"Error loading data: {e}")
        return pd.DataFrame()

def calculate_data_quality_score(df: pd.DataFrame) -> float:
    """
    Calculate data quality score based on completeness and consistency
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        Quality score from 0-5
    """
    if df.empty:
        return 0
    
    # Calculate completeness (percentage of non-null values)
    completeness = 1 - (df.isna().sum().sum() / (df.shape[0] * df.shape[1]))
    
    # Calculate consistency (standard deviation of values normalized)
    if 'Emissions (tCO2e)' in df.columns:
        emissions_std = df['Emissions (tCO2e)'].std()
        emissions_mean = df['Emissions (tCO2e)'].mean()
        if emissions_mean > 0:  # Avoid division by zero
            consistency = 1 - min(emissions_std / emissions_mean, 1)
        else:
            consistency = 1
    else:
        consistency = 1
    
    # If we have actual data quality scores, incorporate them
    if 'Data Quality Score' in df.columns:
        reported_quality = df['Data Quality Score'].mean() / 5  # Normalize to 0-1
        quality_score = (0.4 * completeness + 0.3 * consistency + 0.3 * reported_quality) * 5
    else:
        quality_score = (0.7 * completeness + 0.3 * consistency) * 5
    
    return round(quality_score, 1)

def get_reduction_potential(df: pd.DataFrame, category: str, reduction_percentage: float) -> float:
    """
    Calculate potential emissions reduction for a category
    
    Args:
        df: DataFrame with emissions data
        category: Emissions category to calculate reduction for
        reduction_percentage: Percentage reduction to apply (0-100)
        
    Returns:
        Potential emissions reduction in tCO2e
    """
    if df.empty or 'Category' not in df.columns or 'Emissions (tCO2e)' not in df.columns:
        return 0
    
    category_emissions = df[df['Category'] == category]['Emissions (tCO2e)'].sum()
    potential_reduction = category_emissions * (reduction_percentage / 100)
    
    return round(potential_reduction, 1)

def calculate_category_breakdown(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate emissions breakdown by category
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        Dictionary of categories and their emissions values
    """
    if df.empty or 'Category' not in df.columns or 'Emissions (tCO2e)' not in df.columns:
        return {}
    
    category_emissions = df.groupby('Category')['Emissions (tCO2e)'].sum()
    return category_emissions.to_dict()

def calculate_tier_breakdown(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate emissions breakdown by tier
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        Dictionary of tiers and their emissions values
    """
    if df.empty or 'Tier' not in df.columns or 'Emissions (tCO2e)' not in df.columns:
        return {}
    
    tier_emissions = df.groupby('Tier')['Emissions (tCO2e)'].sum()
    return tier_emissions.to_dict()

def get_tier_category_flow(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get emissions flow from tiers to categories for Sankey diagram
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        DataFrame with tier, category, and emissions values
    """
    if df.empty or 'Tier' not in df.columns or 'Category' not in df.columns:
        return pd.DataFrame()
    
    tier_cat = df.groupby(['Tier', 'Category'])['Emissions (tCO2e)'].sum().reset_index()
    return tier_cat

def get_data_quality_by_category(df: pd.DataFrame) -> pd.DataFrame:
    """
    Get data quality scores by category
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        DataFrame with categories and their quality scores
    """
    if df.empty or 'Category' not in df.columns or 'Data Quality Score' not in df.columns:
        return pd.DataFrame()
    
    quality_by_category = df.groupby('Category')['Data Quality Score'].mean().reset_index()
    return quality_by_category

def generate_achievements(df: pd.DataFrame, reduction_percentage: float) -> List[Dict]:
    """
    Generate achievements based on data quality and reduction targets
    
    Args:
        df: DataFrame with emissions data
        reduction_percentage: Overall reduction percentage achieved
        
    Returns:
        List of achievement dictionaries with title and description
    """
    achievements = []
    
    # Data quality achievements
    data_quality = calculate_data_quality_score(df)
    if data_quality >= 4.5:
        achievements.append({
            "title": "Data Quality Master",
            "description": "Achieved excellent data quality across all categories",
            "icon": "🏆"
        })
    elif data_quality >= 3.5:
        achievements.append({
            "title": "Data Quality Expert",
            "description": "Achieved good data quality across most categories",
            "icon": "🥇"
        })
    
    # Reduction achievements
    if reduction_percentage >= 50:
        achievements.append({
            "title": "Climate Champion",
            "description": "Achieved 50%+ emissions reduction across supply chain",
            "icon": "🌍"
        })
    elif reduction_percentage >= 30:
        achievements.append({
            "title": "Sustainability Leader",
            "description": "Achieved 30%+ emissions reduction across supply chain",
            "icon": "🌱"
        })
    elif reduction_percentage >= 15:
        achievements.append({
            "title": "Carbon Reducer",
            "description": "Achieved 15%+ emissions reduction across supply chain",
            "icon": "♻️"
        })
    
    return achievements