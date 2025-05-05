import streamlit as st
from typing import Dict, List, Tuple, Optional, Callable, Any

def pixel_card(title: str, content_function: Callable) -> None:
    """
    Create a pixel-art styled card with title and content
    
    Args:
        title: Card title
        content_function: Function to execute inside the card
    """
    st.markdown('<div class="metric-container">', unsafe_allow_html=True)
    st.markdown(f"<h2>{title}</h2>", unsafe_allow_html=True)
    
    # Execute the content function inside the card
    content_function()
    
    st.markdown('</div>', unsafe_allow_html=True)

def achievement_badge(title: str, condition: float, threshold: float) -> bool:
    """
    Display an achievement badge if condition meets threshold
    
    Args:
        title: Achievement title
        condition: Current value
        threshold: Value required to unlock achievement
        
    Returns:
        True if achievement unlocked, False otherwise
    """
    if condition >= threshold:
        st.markdown(
            f'<div class="achievement-badge achievement-unlocked">'
            f'🏆 ACHIEVEMENT UNLOCKED: {title}'
            f'</div>',
            unsafe_allow_html=True
        )
        return True
    else:
        next_level = ""
        if condition > threshold * 0.5:
            next_level = f"You're {round((condition/threshold)*100)}% of the way there!"
        st.info(f"🔒 Next Achievement: {title} ({next_level})")
        return False

def retro_slider(label: str, min_val: float, max_val: float, default_val: float, key: str) -> float:
    """
    Create a slider with retro styling
    
    Args:
        label: Slider label
        min_val: Minimum value
        max_val: Maximum value
        default_val: Default value
        key: Unique key for the slider
        
    Returns:
        Selected value
    """
    st.markdown(f"<p>{label}</p>", unsafe_allow_html=True)
    return st.slider(
        label, 
        min_value=min_val, 
        max_value=max_val, 
        value=default_val,
        key=key,
        label_visibility="collapsed"
    )

def retro_progress_bar(label: str, value: float, max_value: float) -> None:
    """
    Create a retro-styled progress bar
    
    Args:
        label: Progress bar label
        value: Current value
        max_value: Maximum value
    """
    st.markdown(f"<p>{label}</p>", unsafe_allow_html=True)
    st.progress(min(value / max_value, 1.0))

def control_panel_section(title: str) -> None:
    """
    Create a section header for the control panel
    
    Args:
        title: Section title
    """
    st.markdown("<hr>", unsafe_allow_html=True)
    st.markdown(f"<h3>{title}</h3>", unsafe_allow_html=True)

def display_metric_value(label: str, value: Any, unit: str = "", delta: Optional[float] = None) -> None:
    """
    Display a metric value with optional delta
    
    Args:
        label: Metric label
        value: Metric value
        unit: Unit of measurement
        delta: Change in value (optional)
    """
    if delta is not None:
        if delta > 0:
            delta_html = f'<span style="color: #4CAF50; font-size: 0.8em;">▲ {delta:.1f}{unit}</span>'
        elif delta < 0:
            delta_html = f'<span style="color: #FF6F61; font-size: 0.8em;">▼ {abs(delta):.1f}{unit}</span>'
        else:
            delta_html = f'<span style="color: #AAAAAA; font-size: 0.8em;">◆ 0{unit}</span>'
    else:
        delta_html = ""
    
    st.markdown(
        f"<p>{label}<br>"
        f"<span style='font-size: 1.5em; font-family: VT323, monospace;'>{value}{unit}</span> {delta_html}</p>",
        unsafe_allow_html=True
    )

def display_achievements(achievements: List[Dict]) -> None:
    """
    Display a list of achievements
    
    Args:
        achievements: List of achievement dictionaries with title, description, icon
    """
    if not achievements:
        st.info("No achievements unlocked yet. Keep exploring!")
        return
    
    st.markdown("<h3>ACHIEVEMENTS UNLOCKED</h3>", unsafe_allow_html=True)
    
    for i, achievement in enumerate(achievements):
        st.markdown(
            f'<div class="achievement-badge achievement-unlocked" style="animation-delay: {i*0.2}s">'
            f'{achievement.get("icon", "🏆")} {achievement.get("title", "Unknown")}'
            f'</div>',
            unsafe_allow_html=True
        )
        if "description" in achievement:
            st.markdown(f"<p><small>{achievement['description']}</small></p>", unsafe_allow_html=True)

def display_decarbonization_plan(plan: Dict[str, Dict]) -> None:
    """
    Display a decarbonization plan
    
    Args:
        plan: Dictionary with short, medium, and long-term actions
    """
    if not plan:
        st.warning("Unable to generate decarbonization plan from current data.")
        return
    
    # Add tabs for timeframes
    st_tabs = st.tabs(["SHORT-TERM", "MEDIUM-TERM", "LONG-TERM"])
    
    # Short-term tab
    with st_tabs[0]:
        if plan.get("short_term"):
            for category, details in plan["short_term"].items():
                st.markdown(f"### {category}")
                st.markdown(f"**Action:** {details.get('action', 'No action specified')}")
                st.markdown(f"**Target reduction:** {details.get('target_reduction', 0)}%")
                st.markdown(f"**Emissions impact:** {details.get('emissions_impact', 0)} tCO2e")
                st.markdown("---")
        else:
            st.info("No short-term actions identified.")
    
    # Medium-term tab
    with st_tabs[1]:
        if plan.get("medium_term"):
            for category, details in plan["medium_term"].items():
                st.markdown(f"### {category}")
                st.markdown(f"**Action:** {details.get('action', 'No action specified')}")
                st.markdown(f"**Target reduction:** {details.get('target_reduction', 0)}%")
                st.markdown(f"**Emissions impact:** {details.get('emissions_impact', 0)} tCO2e")
                st.markdown("---")
        else:
            st.info("No medium-term actions identified.")
    
    # Long-term tab
    with st_tabs[2]:
        if plan.get("long_term"):
            for category, details in plan["long_term"].items():
                st.markdown(f"### {category}")
                st.markdown(f"**Action:** {details.get('action', 'No action specified')}")
                st.markdown(f"**Target reduction:** {details.get('target_reduction', 0)}%")
                st.markdown(f"**Emissions impact:** {details.get('emissions_impact', 0)} tCO2e")
                st.markdown("---")
        else:
            st.info("No long-term actions identified.")