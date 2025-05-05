import pandas as pd
import numpy as np
from typing import Dict, List, Tuple, Optional

def calculate_reduction_scenarios(df: pd.DataFrame, reduction_values: Dict[str, float]) -> Tuple[float, float, float, Dict[str, float]]:
    """
    Calculate emissions reduction based on scenario sliders
    
    Args:
        df: DataFrame with emissions data
        reduction_values: Dictionary mapping categories to reduction percentages
        
    Returns:
        Tuple containing (current_total, new_total, reduction_percentage, category_savings)
    """
    if df.empty or 'Category' not in df.columns or 'Emissions (tCO2e)' not in df.columns:
        return 0, 0, 0, {}
    
    # Calculate current total emissions
    current_total = df['Emissions (tCO2e)'].sum()
    
    # Initialize new total with current total
    new_total = current_total
    
    # Calculate savings for each category
    category_savings = {}
    
    for category, reduction_pct in reduction_values.items():
        category_emissions = df[df['Category'] == category]['Emissions (tCO2e)'].sum()
        savings = category_emissions * (reduction_pct / 100)
        category_savings[category] = round(savings, 1)
        new_total -= savings
    
    # Calculate overall reduction percentage
    if current_total > 0:
        reduction_percentage = ((current_total - new_total) / current_total) * 100
    else:
        reduction_percentage = 0
    
    return round(current_total, 1), round(new_total, 1), round(reduction_percentage, 1), category_savings

def recommend_reduction_targets(df: pd.DataFrame) -> Dict[str, float]:
    """
    Recommend reduction targets based on emissions data
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        Dictionary mapping categories to recommended reduction percentages
    """
    if df.empty or 'Category' not in df.columns or 'Emissions (tCO2e)' not in df.columns:
        return {}
    
    # Calculate total emissions by category
    category_emissions = df.groupby('Category')['Emissions (tCO2e)'].sum()
    
    # Calculate percentage of total for each category
    total_emissions = category_emissions.sum()
    category_percentages = (category_emissions / total_emissions) * 100
    
    # Set higher reduction targets for categories with higher emissions
    reduction_targets = {}
    
    for category, percentage in category_percentages.items():
        # Base target on percentage of total emissions
        if percentage > 30:
            # Major emissions category
            reduction_targets[category] = 35
        elif percentage > 20:
            # Significant emissions category
            reduction_targets[category] = 30
        elif percentage > 10:
            # Moderate emissions category
            reduction_targets[category] = 25
        else:
            # Minor emissions category
            reduction_targets[category] = 20
    
    return reduction_targets

def calculate_cost_effectiveness(df: pd.DataFrame) -> Dict[str, float]:
    """
    Calculate cost effectiveness of reduction for each category
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        Dictionary mapping categories to cost effectiveness scores (higher is better)
    """
    # In a real scenario, this would incorporate actual cost data
    # For the sample, we'll use a simplified model based on tiers
    
    if df.empty or 'Category' not in df.columns or 'Tier' not in df.columns:
        return {}
    
    # Calculate emissions by category and tier
    cat_tier_emissions = df.groupby(['Category', 'Tier'])['Emissions (tCO2e)'].sum().reset_index()
    
    # Convert tiers to numeric values (Tier 1 = 1, Tier 2 = 2, etc.)
    cat_tier_emissions['Tier_Num'] = cat_tier_emissions['Tier'].str.extract(r'Tier (\d+)').astype(int)
    
    # Calculate weighted average tier for each category (lower is more cost-effective)
    category_weights = {}
    
    for category in cat_tier_emissions['Category'].unique():
        category_data = cat_tier_emissions[cat_tier_emissions['Category'] == category]
        total_emissions = category_data['Emissions (tCO2e)'].sum()
        
        # Weighted average tier (weighted by emissions)
        weighted_tier = (category_data['Tier_Num'] * category_data['Emissions (tCO2e)']).sum() / total_emissions
        
        # Invert so higher is better (more cost-effective)
        cost_effectiveness = 4 - weighted_tier
        
        category_weights[category] = round(cost_effectiveness, 2)
    
    return category_weights

def generate_decarbonization_plan(df: pd.DataFrame, target_reduction: float = 30.0) -> Dict[str, Dict]:
    """
    Generate a decarbonization plan based on emissions data
    
    Args:
        df: DataFrame with emissions data
        target_reduction: Overall emissions reduction target (percentage)
        
    Returns:
        Dictionary with short, medium, and long-term actions
    """
    if df.empty or 'Category' not in df.columns or 'Emissions (tCO2e)' not in df.columns:
        return {
            "short_term": {},
            "medium_term": {},
            "long_term": {}
        }
    
    # Get recommended reduction targets
    targets = recommend_reduction_targets(df)
    
    # Get cost effectiveness scores
    cost_effectiveness = calculate_cost_effectiveness(df)
    
    # Calculate total emissions by category
    category_emissions = df.groupby('Category')['Emissions (tCO2e)'].sum().to_dict()
    
    # Generate plan
    plan = {
        "short_term": {},
        "medium_term": {},
        "long_term": {}
    }
    
    for category, reduction_pct in targets.items():
        # Assign timeframe based on cost effectiveness
        effectiveness = cost_effectiveness.get(category, 2.0)
        emissions = category_emissions.get(category, 0)
        
        if effectiveness > 2.5:
            # High cost effectiveness (easy wins) - short term
            timeframe = "short_term"
            action_prefix = "Implement"
        elif effectiveness > 1.5:
            # Medium cost effectiveness - medium term
            timeframe = "medium_term"
            action_prefix = "Develop"
        else:
            # Low cost effectiveness (harder to address) - long term
            timeframe = "long_term"
            action_prefix = "Research"
        
        # Create action description
        if category == "Raw Materials":
            action = f"{action_prefix} supplier engagement program for sustainable materials"
        elif category == "Manufacturing":
            action = f"{action_prefix} energy efficiency measures in manufacturing processes"
        elif category == "Transport":
            action = f"{action_prefix} low-carbon logistics and transportation strategy"
        elif category == "Packaging":
            action = f"{action_prefix} recycled content and packaging optimization program"
        elif category == "End of Life":
            action = f"{action_prefix} product take-back and circular economy initiative"
        else:
            action = f"{action_prefix} emissions reduction program for {category}"
        
        # Add to plan
        plan[timeframe][category] = {
            "action": action,
            "target_reduction": reduction_pct,
            "emissions_impact": round(emissions * (reduction_pct / 100), 1),
            "cost_effectiveness": effectiveness
        }
    
    return plan

def calculate_abatement_curve_data(df: pd.DataFrame) -> List[Dict]:
    """
    Calculate marginal abatement cost curve data
    
    Args:
        df: DataFrame with emissions data
        
    Returns:
        List of dictionaries with abatement options
    """
    if df.empty or 'Category' not in df.columns or 'Emissions (tCO2e)' not in df.columns:
        return []
    
    # Get recommended reduction targets
    targets = recommend_reduction_targets(df)
    
    # Get cost effectiveness scores
    cost_effectiveness = calculate_cost_effectiveness(df)
    
    # Calculate total emissions by category
    category_emissions = df.groupby('Category')['Emissions (tCO2e)'].sum().to_dict()
    
    # Generate abatement options
    abatement_options = []
    
    for category in category_emissions:
        reduction_pct = targets.get(category, 20)
        effectiveness = cost_effectiveness.get(category, 2.0)
        emissions = category_emissions.get(category, 0)
        
        # Calculate abatement potential
        abatement_potential = emissions * (reduction_pct / 100)
        
        # Simulate cost (inverse of effectiveness, scaled)
        # In real application, this would be actual cost data
        cost = (3 - effectiveness) * 50  # $ per tCO2e
        
        abatement_options.append({
            "category": category,
            "abatement_potential": round(abatement_potential, 1),
            "cost_per_tco2e": round(cost, 1),
            "reduction_pct": reduction_pct
        })
    
    # Sort by cost (lowest first)
    abatement_options = sorted(abatement_options, key=lambda x: x["cost_per_tco2e"])
    
    return abatement_options