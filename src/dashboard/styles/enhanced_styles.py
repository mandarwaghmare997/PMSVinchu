"""
Enhanced UI/UX Styling Module for PMS Intelligence Hub
Professional styling with modern design principles and animations
Author: Vulnuris Development Team
"""

import streamlit as st
from typing import Dict, List, Optional

class EnhancedUIStyles:
    """
    Enhanced UI styling with modern design principles
    """
    
    def __init__(self):
        self.color_scheme = {
            # Primary colors
            'primary': '#1e3a8a',
            'primary_light': '#3b82f6',
            'primary_dark': '#1e40af',
            
            # Secondary colors
            'secondary': '#059669',
            'secondary_light': '#10b981',
            'secondary_dark': '#047857',
            
            # Accent colors
            'accent': '#f59e0b',
            'accent_light': '#fbbf24',
            'accent_dark': '#d97706',
            
            # Neutral colors
            'background': '#f8fafc',
            'surface': '#ffffff',
            'surface_dark': '#f1f5f9',
            'text_primary': '#1e293b',
            'text_secondary': '#64748b',
            'text_muted': '#94a3b8',
            
            # Status colors
            'success': '#059669',
            'warning': '#f59e0b',
            'error': '#dc2626',
            'info': '#0ea5e9',
            
            # Chart colors
            'chart_1': '#3b82f6',
            'chart_2': '#10b981',
            'chart_3': '#f59e0b',
            'chart_4': '#ef4444',
            'chart_5': '#8b5cf6',
            'chart_6': '#06b6d4',
            'chart_7': '#84cc16',
            'chart_8': '#f97316'
        }
        
        self.gradients = {
            'primary': 'linear-gradient(135deg, #1e3a8a 0%, #3b82f6 100%)',
            'secondary': 'linear-gradient(135deg, #059669 0%, #10b981 100%)',
            'accent': 'linear-gradient(135deg, #f59e0b 0%, #fbbf24 100%)',
            'success': 'linear-gradient(135deg, #059669 0%, #34d399 100%)',
            'warning': 'linear-gradient(135deg, #f59e0b 0%, #fcd34d 100%)',
            'error': 'linear-gradient(135deg, #dc2626 0%, #f87171 100%)',
            'neutral': 'linear-gradient(135deg, #f1f5f9 0%, #ffffff 100%)'
        }
    
    def inject_global_styles(self):
        """
        Inject global CSS styles with modern design and animations
        """
        st.markdown(f"""
        <style>
        /* Import Google Fonts */
        @import url('https://fonts.googleapis.com/css2?family=Inter:wght@300;400;500;600;700&display=swap');
        
        /* Global Variables */
        :root {{
            --primary-color: {self.color_scheme['primary']};
            --primary-light: {self.color_scheme['primary_light']};
            --secondary-color: {self.color_scheme['secondary']};
            --accent-color: {self.color_scheme['accent']};
            --background-color: {self.color_scheme['background']};
            --surface-color: {self.color_scheme['surface']};
            --text-primary: {self.color_scheme['text_primary']};
            --text-secondary: {self.color_scheme['text_secondary']};
            --success-color: {self.color_scheme['success']};
            --warning-color: {self.color_scheme['warning']};
            --error-color: {self.color_scheme['error']};
            --border-radius: 12px;
            --shadow-sm: 0 1px 2px 0 rgba(0, 0, 0, 0.05);
            --shadow-md: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
            --shadow-lg: 0 10px 15px -3px rgba(0, 0, 0, 0.1);
            --shadow-xl: 0 20px 25px -5px rgba(0, 0, 0, 0.1);
        }}
        
        /* Global Styles */
        .main .block-container {{
            padding-top: 2rem;
            padding-bottom: 2rem;
            max-width: 1200px;
        }}
        
        /* Typography */
        .main {{
            font-family: 'Inter', -apple-system, BlinkMacSystemFont, sans-serif;
            color: var(--text-primary);
            background: var(--background-color);
        }}
        
        h1, h2, h3, h4, h5, h6 {{
            font-family: 'Inter', sans-serif;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 1rem;
        }}
        
        /* Enhanced Header */
        .main-header {{
            background: {self.gradients['primary']};
            padding: 2rem 0;
            margin: -2rem -1rem 2rem -1rem;
            border-radius: 0 0 var(--border-radius) var(--border-radius);
            box-shadow: var(--shadow-lg);
            position: relative;
            overflow: hidden;
        }}
        
        .main-header::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            bottom: 0;
            background: url('data:image/svg+xml,<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 100 100"><defs><pattern id="grid" width="10" height="10" patternUnits="userSpaceOnUse"><path d="M 10 0 L 0 0 0 10" fill="none" stroke="rgba(255,255,255,0.1)" stroke-width="0.5"/></pattern></defs><rect width="100" height="100" fill="url(%23grid)"/></svg>');
            opacity: 0.3;
        }}
        
        .main-header h1 {{
            color: white;
            text-align: center;
            font-size: 2.5rem;
            font-weight: 700;
            margin: 0;
            position: relative;
            z-index: 1;
            text-shadow: 0 2px 4px rgba(0,0,0,0.3);
        }}
        
        /* Enhanced Metrics Cards */
        .metric-card {{
            background: var(--surface-color);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(0,0,0,0.05);
            transition: all 0.3s cubic-bezier(0.4, 0, 0.2, 1);
            position: relative;
            overflow: hidden;
        }}
        
        .metric-card::before {{
            content: '';
            position: absolute;
            top: 0;
            left: 0;
            right: 0;
            height: 4px;
            background: {self.gradients['primary']};
            transform: scaleX(0);
            transition: transform 0.3s ease;
        }}
        
        .metric-card:hover {{
            transform: translateY(-4px);
            box-shadow: var(--shadow-xl);
        }}
        
        .metric-card:hover::before {{
            transform: scaleX(1);
        }}
        
        .metric-value {{
            font-size: 2.5rem;
            font-weight: 700;
            color: var(--primary-color);
            margin: 0.5rem 0;
            line-height: 1;
        }}
        
        .metric-label {{
            font-size: 0.875rem;
            font-weight: 500;
            color: var(--text-secondary);
            text-transform: uppercase;
            letter-spacing: 0.05em;
            margin-bottom: 0.5rem;
        }}
        
        .metric-change {{
            font-size: 0.875rem;
            font-weight: 600;
            display: flex;
            align-items: center;
            gap: 0.25rem;
        }}
        
        .metric-change.positive {{
            color: var(--success-color);
        }}
        
        .metric-change.negative {{
            color: var(--error-color);
        }}
        
        /* Enhanced Sidebar */
        .css-1d391kg {{
            background: var(--surface-color);
            border-right: 1px solid rgba(0,0,0,0.1);
        }}
        
        .sidebar-content {{
            padding: 1rem;
        }}
        
        .filter-section {{
            background: var(--surface-color);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            margin-bottom: 1rem;
            box-shadow: var(--shadow-sm);
            border: 1px solid rgba(0,0,0,0.05);
        }}
        
        .filter-section h3 {{
            color: var(--text-primary);
            font-size: 1.125rem;
            font-weight: 600;
            margin-bottom: 1rem;
            padding-bottom: 0.5rem;
            border-bottom: 2px solid var(--primary-color);
        }}
        
        /* Enhanced Charts */
        .chart-container {{
            background: var(--surface-color);
            border-radius: var(--border-radius);
            padding: 1.5rem;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(0,0,0,0.05);
            margin-bottom: 2rem;
            transition: all 0.3s ease;
        }}
        
        .chart-container:hover {{
            box-shadow: var(--shadow-lg);
        }}
        
        .chart-title {{
            font-size: 1.25rem;
            font-weight: 600;
            color: var(--text-primary);
            margin-bottom: 1rem;
            display: flex;
            align-items: center;
            gap: 0.5rem;
        }}
        
        .chart-title::before {{
            content: '';
            width: 4px;
            height: 1.5rem;
            background: {self.gradients['primary']};
            border-radius: 2px;
        }}
        
        /* Enhanced Buttons */
        .stButton > button {{
            background: {self.gradients['primary']};
            color: white;
            border: none;
            border-radius: var(--border-radius);
            padding: 0.75rem 1.5rem;
            font-weight: 600;
            font-size: 0.875rem;
            transition: all 0.3s ease;
            box-shadow: var(--shadow-sm);
            text-transform: uppercase;
            letter-spacing: 0.05em;
        }}
        
        .stButton > button:hover {{
            transform: translateY(-2px);
            box-shadow: var(--shadow-md);
        }}
        
        .stButton > button:active {{
            transform: translateY(0);
        }}
        
        /* Enhanced File Uploader */
        .uploadedFile {{
            background: var(--surface-color);
            border-radius: var(--border-radius);
            border: 2px dashed var(--primary-light);
            padding: 2rem;
            text-align: center;
            transition: all 0.3s ease;
        }}
        
        .uploadedFile:hover {{
            border-color: var(--primary-color);
            background: rgba(59, 130, 246, 0.05);
        }}
        
        /* Enhanced Tables */
        .dataframe {{
            border-radius: var(--border-radius);
            overflow: hidden;
            box-shadow: var(--shadow-md);
            border: 1px solid rgba(0,0,0,0.05);
        }}
        
        .dataframe thead th {{
            background: {self.gradients['primary']};
            color: white;
            font-weight: 600;
            padding: 1rem;
            border: none;
        }}
        
        .dataframe tbody td {{
            padding: 0.75rem 1rem;
            border-bottom: 1px solid rgba(0,0,0,0.05);
        }}
        
        .dataframe tbody tr:hover {{
            background: rgba(59, 130, 246, 0.05);
        }}
        
        /* Enhanced Selectbox */
        .stSelectbox > div > div {{
            background: var(--surface-color);
            border-radius: var(--border-radius);
            border: 1px solid rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .stSelectbox > div > div:focus-within {{
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}
        
        /* Enhanced Number Input */
        .stNumberInput > div > div {{
            background: var(--surface-color);
            border-radius: var(--border-radius);
            border: 1px solid rgba(0,0,0,0.1);
            transition: all 0.3s ease;
        }}
        
        .stNumberInput > div > div:focus-within {{
            border-color: var(--primary-color);
            box-shadow: 0 0 0 3px rgba(59, 130, 246, 0.1);
        }}
        
        /* Enhanced Slider */
        .stSlider > div > div > div {{
            background: var(--primary-color);
        }}
        
        /* Loading Animation */
        .loading-spinner {{
            display: inline-block;
            width: 20px;
            height: 20px;
            border: 3px solid rgba(59, 130, 246, 0.3);
            border-radius: 50%;
            border-top-color: var(--primary-color);
            animation: spin 1s ease-in-out infinite;
        }}
        
        @keyframes spin {{
            to {{ transform: rotate(360deg); }}
        }}
        
        /* Success/Error Messages */
        .success-message {{
            background: rgba(5, 150, 105, 0.1);
            border: 1px solid var(--success-color);
            border-radius: var(--border-radius);
            padding: 1rem;
            color: var(--success-color);
            font-weight: 500;
        }}
        
        .error-message {{
            background: rgba(220, 38, 38, 0.1);
            border: 1px solid var(--error-color);
            border-radius: var(--border-radius);
            padding: 1rem;
            color: var(--error-color);
            font-weight: 500;
        }}
        
        /* Responsive Design */
        @media (max-width: 768px) {{
            .main .block-container {{
                padding-left: 1rem;
                padding-right: 1rem;
            }}
            
            .main-header h1 {{
                font-size: 2rem;
            }}
            
            .metric-value {{
                font-size: 2rem;
            }}
        }}
        
        /* Animation Classes */
        .fade-in {{
            animation: fadeIn 0.6s ease-in-out;
        }}
        
        @keyframes fadeIn {{
            from {{ opacity: 0; transform: translateY(20px); }}
            to {{ opacity: 1; transform: translateY(0); }}
        }}
        
        .slide-in-left {{
            animation: slideInLeft 0.6s ease-in-out;
        }}
        
        @keyframes slideInLeft {{
            from {{ opacity: 0; transform: translateX(-30px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        .slide-in-right {{
            animation: slideInRight 0.6s ease-in-out;
        }}
        
        @keyframes slideInRight {{
            from {{ opacity: 0; transform: translateX(30px); }}
            to {{ opacity: 1; transform: translateX(0); }}
        }}
        
        /* Custom Scrollbar */
        ::-webkit-scrollbar {{
            width: 8px;
        }}
        
        ::-webkit-scrollbar-track {{
            background: var(--background-color);
        }}
        
        ::-webkit-scrollbar-thumb {{
            background: var(--primary-light);
            border-radius: 4px;
        }}
        
        ::-webkit-scrollbar-thumb:hover {{
            background: var(--primary-color);
        }}
        </style>
        """, unsafe_allow_html=True)
    
    def create_metric_card(self, title: str, value: str, change: str = None, 
                          change_type: str = "positive", icon: str = None) -> str:
        """
        Create an enhanced metric card with animations
        """
        change_class = f"metric-change {change_type}" if change else ""
        change_html = f'<div class="{change_class}">{change}</div>' if change else ""
        icon_html = f'<span style="font-size: 1.5rem; margin-right: 0.5rem;">{icon}</span>' if icon else ""
        
        return f"""
        <div class="metric-card fade-in">
            <div class="metric-label">{icon_html}{title}</div>
            <div class="metric-value">{value}</div>
            {change_html}
        </div>
        """
    
    def create_section_header(self, title: str, subtitle: str = None, icon: str = None) -> str:
        """
        Create an enhanced section header
        """
        icon_html = f'<span style="margin-right: 0.5rem;">{icon}</span>' if icon else ""
        subtitle_html = f'<p style="color: var(--text-secondary); margin: 0.5rem 0 0 0; font-size: 1rem;">{subtitle}</p>' if subtitle else ""
        
        return f"""
        <div class="chart-title fade-in">
            {icon_html}{title}
        </div>
        {subtitle_html}
        """
    
    def create_status_badge(self, text: str, status: str = "info") -> str:
        """
        Create a status badge with appropriate styling
        """
        color_map = {
            "success": self.color_scheme['success'],
            "warning": self.color_scheme['warning'],
            "error": self.color_scheme['error'],
            "info": self.color_scheme['info']
        }
        
        color = color_map.get(status, self.color_scheme['info'])
        
        return f"""
        <span style="
            background: {color}15;
            color: {color};
            padding: 0.25rem 0.75rem;
            border-radius: 9999px;
            font-size: 0.75rem;
            font-weight: 600;
            text-transform: uppercase;
            letter-spacing: 0.05em;
            border: 1px solid {color}30;
        ">{text}</span>
        """
    
    def create_progress_bar(self, value: float, max_value: float = 100, 
                           color: str = None, height: str = "8px") -> str:
        """
        Create an animated progress bar
        """
        percentage = min((value / max_value) * 100, 100)
        bar_color = color or self.color_scheme['primary']
        
        return f"""
        <div style="
            width: 100%;
            background: rgba(0,0,0,0.1);
            border-radius: 9999px;
            height: {height};
            overflow: hidden;
            margin: 0.5rem 0;
        ">
            <div style="
                width: {percentage}%;
                height: 100%;
                background: {bar_color};
                border-radius: 9999px;
                transition: width 1s ease-in-out;
                animation: progressFill 1.5s ease-in-out;
            "></div>
        </div>
        <style>
        @keyframes progressFill {{
            from {{ width: 0%; }}
            to {{ width: {percentage}%; }}
        }}
        </style>
        """
    
    def create_loading_spinner(self, text: str = "Loading...") -> str:
        """
        Create a loading spinner with text
        """
        return f"""
        <div style="
            display: flex;
            align-items: center;
            justify-content: center;
            gap: 0.75rem;
            padding: 2rem;
            color: var(--text-secondary);
            font-weight: 500;
        ">
            <div class="loading-spinner"></div>
            {text}
        </div>
        """
    
    def create_info_box(self, title: str, content: str, box_type: str = "info") -> str:
        """
        Create an information box with appropriate styling
        """
        type_styles = {
            "info": {
                "bg": f"{self.color_scheme['info']}15",
                "border": self.color_scheme['info'],
                "icon": "ℹ️"
            },
            "success": {
                "bg": f"{self.color_scheme['success']}15",
                "border": self.color_scheme['success'],
                "icon": "✅"
            },
            "warning": {
                "bg": f"{self.color_scheme['warning']}15",
                "border": self.color_scheme['warning'],
                "icon": "⚠️"
            },
            "error": {
                "bg": f"{self.color_scheme['error']}15",
                "border": self.color_scheme['error'],
                "icon": "❌"
            }
        }
        
        style = type_styles.get(box_type, type_styles["info"])
        
        return f"""
        <div style="
            background: {style['bg']};
            border: 1px solid {style['border']}30;
            border-left: 4px solid {style['border']};
            border-radius: var(--border-radius);
            padding: 1rem;
            margin: 1rem 0;
        ">
            <div style="
                font-weight: 600;
                color: {style['border']};
                margin-bottom: 0.5rem;
                display: flex;
                align-items: center;
                gap: 0.5rem;
            ">
                {style['icon']} {title}
            </div>
            <div style="color: var(--text-primary);">
                {content}
            </div>
        </div>
        """

