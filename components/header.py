# components/header.py
import streamlit as st

def setup_theme():
    """Configura tema escuro personalizado"""
    st.set_page_config(
        page_title="Diagrama do Cerrado",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS personalizado
    st.markdown("""
    <style>
    /* Tema escuro personalizado */
    :root {
        --primary-color: #2E8B57;
        --secondary-color: #1E90FF;
        --background-color: #0E1117;
        --card-background: #262730;
        --text-color: #FAFAFA;
    }
    
    .stApp {
        background: linear-gradient(135deg, #0c0c0c 0%, #1a1a1a 100%);
    }
    
    /* Cards */
    .stCard {
        background-color: var(--card-background);
        border-radius: 10px;
        padding: 1.5rem;
        border-left: 4px solid var(--primary-color);
    }
    
    /* Títulos */
    h1, h2, h3 {
        color: var(--text-color) !important;
        font-weight: 600;
    }
    
    h1 {
        border-bottom: 2px solid var(--primary-color);
        padding-bottom: 0.5rem;
    }
    
    /* Sliders personalizados */
    .stSlider > div > div > div {
        background-color: var(--primary-color);
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(90deg, var(--primary-color), #32CD32);
        color: white;
        border: none;
        border-radius: 5px;
        padding: 0.5rem 1rem;
        font-weight: 500;
        transition: all 0.3s ease;
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 139, 87, 0.4);
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #1a1a1a;
        color: white;
        border: 1px solid #444;
    }
    
    /* Data Editor */
    .dataframe {
        background-color: #1a1a1a !important;
        color: white !important;
    }
    
    /* Metric cards */
    [data-testid="stMetric"] {
        background-color: var(--card-background);
        padding: 1rem;
        border-radius: 10px;
    }
    
    [data-testid="stMetricValue"] {
        color: var(--primary-color) !important;
        font-size: 1.8rem !important;
    }
    
    </style>
    """, unsafe_allow_html=True)

def create_header():
    """Cria cabeçalho personalizado"""
    col1, col2, col3 = st.columns([1, 2, 1])
    
    with col1:
        st.image("https://via.placeholder.com/100/2E8B57/FFFFFF?text=DC", 
                width=80)
    
    with col2:
        st.title("🌿 Diagrama do Cerrado")
        st.markdown("*Planejamento Patrimonial Inteligente*")
    
    with col3:
        total_patrimony = st.session_state.get('total_patrimony', 0)
        st.metric("Patrimônio Total", 
                 f"R$ {total_patrimony:,.2f}", 
                 delta=None)