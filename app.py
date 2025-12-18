# app.py - TEMA CLARO
"""
Diagrama do Cerrado - Tema Claro Moderno
"""
import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import json
from datetime import datetime

# Importações locais
try:
    from components.asset_editor import AssetEditor
    ASSET_EDITOR_OK = True
except ImportError as e:
    st.error(f"Erro ao importar AssetEditor: {e}")
    ASSET_EDITOR_OK = False


def format_currency(value):
    """Formata valor monetário"""
    return f"R$ {value:,.2f}"


def setup_light_theme():
    """Configura tema claro moderno"""
    st.set_page_config(
        page_title="Diagrama do Cerrado",
        page_icon="🌿",
        layout="wide",
        initial_sidebar_state="expanded"
    )
    
    # CSS - TEMA CLARO E MODERNO
    st.markdown("""
    <style>
    /* Tema claro moderno */
    .stApp {
        background-color: #FFFFFF;
        color: #1A1A1A;
    }
    
    /* Títulos */
    h1, h2, h3, h4 {
        color: #2E8B57 !important;
        font-weight: 700;
        font-family: 'Segoe UI', 'Arial', sans-serif;
    }
    
    h1 {
        border-bottom: 3px solid #2E8B57;
        padding-bottom: 10px;
        margin-bottom: 30px;
    }
    
    /* Cards e containers */
    .main-card {
        background: linear-gradient(135deg, #FFFFFF 0%, #F8F9FA 100%);
        border-radius: 12px;
        border: 1px solid #E0E0E0;
        padding: 20px;
        box-shadow: 0 4px 6px rgba(0, 0, 0, 0.05);
        margin-bottom: 20px;
    }
    
    .metric-card {
        background: linear-gradient(135deg, #2E8B57 0%, #3CB371 100%);
        color: white;
        padding: 15px;
        border-radius: 10px;
        text-align: center;
        box-shadow: 0 4px 8px rgba(46, 139, 87, 0.2);
    }
    
    /* Botões */
    .stButton > button {
        background: linear-gradient(90deg, #2E8B57, #3CB371);
        color: white;
        border: none;
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
        font-size: 14px;
        transition: all 0.3s ease;
        box-shadow: 0 2px 4px rgba(46, 139, 87, 0.2);
    }
    
    .stButton > button:hover {
        transform: translateY(-2px);
        box-shadow: 0 4px 12px rgba(46, 139, 87, 0.3);
        background: linear-gradient(90deg, #3CB371, #2E8B57);
    }
    
    /* Sliders */
    .stSlider > div > div > div {
        background: linear-gradient(90deg, #2E8B57, #3CB371) !important;
    }
    
    .stSlider > div > div {
        background-color: #E8F5E9 !important;
    }
    
    /* Sidebar */
    [data-testid="stSidebar"] {
        background-color: #F8F9FA;
        border-right: 1px solid #E0E0E0;
    }
    
    /* Tabs */
    .stTabs [data-baseweb="tab-list"] {
        gap: 2px;
        background-color: #F8F9FA;
        padding: 8px;
        border-radius: 10px;
    }
    
    .stTabs [data-baseweb="tab"] {
        border-radius: 8px;
        padding: 10px 20px;
        font-weight: 600;
    }
    
    .stTabs [aria-selected="true"] {
        background-color: #2E8B57 !important;
        color: white !important;
    }
    
    /* Inputs */
    .stTextInput > div > div > input,
    .stNumberInput > div > div > input {
        background-color: #FFFFFF;
        color: #1A1A1A;
        border: 2px solid #E0E0E0;
        border-radius: 8px;
        padding: 8px 12px;
    }
    
    .stTextInput > div > div > input:focus,
    .stNumberInput > div > div > input:focus {
        border-color: #2E8B57;
        box-shadow: 0 0 0 1px #2E8B57;
    }
    
    /* Expanders */
    .streamlit-expanderHeader {
        background-color: #F8F9FA;
        border: 1px solid #E0E0E0;
        border-radius: 8px;
        font-weight: 600;
    }
    
    /* Divider */
    hr {
        border-color: #E0E0E0;
        margin: 20px 0;
    }
    
    /* Badges */
    .badge {
        display: inline-block;
        background: #E8F5E9;
        color: #2E8B57;
        padding: 4px 12px;
        border-radius: 20px;
        font-size: 12px;
        font-weight: 600;
        margin: 2px;
    }
    
    /* Tooltips */
    .tooltip {
        position: relative;
        display: inline-block;
        cursor: help;
    }
    
    /* Responsividade */
    @media (max-width: 768px) {
        .main-card {
            padding: 15px;
        }
        
        h1 {
            font-size: 24px;
        }
    }
    </style>
    """, unsafe_allow_html=True)
    
    # Custom HTML para header
    st.markdown("""
    <div style='text-align: center; padding: 20px 0;'>
        <h1 style='color: #2E8B57; margin-bottom: 10px;'>🌿 Diagrama do Cerrado</h1>
        <p style='color: #666; font-size: 16px; font-weight: 500;'>Planejamento Patrimonial Inteligente</p>
    </div>
    """, unsafe_allow_html=True)


def main():
    """Função principal"""
    
    # Configurar tema
    setup_light_theme()
    
    # Inicializar session_state - COM VALORES FLOAT!
    if 'portfolio' not in st.session_state:
        st.session_state.portfolio = {
            'macro': {
                'Renda Fixa': 40.0,
                'Ações': 30.0,
                'FIIs': 20.0,
                'Criptomoedas': 10.0
            },
            'sub': {
                'Renda Fixa': {'Tesouro Selic': 100.0},
                'Ações': {'PETR4': 50.0, 'VALE3': 30.0, 'ITUB4': 20.0},
                'FIIs': {'MXRF11': 60.0, 'HGLG11': 40.0},
                'Criptomoedas': {'Bitcoin': 70.0, 'Ethereum': 30.0}
            }
        }
    
    if 'total_patrimony' not in st.session_state:
        st.session_state.total_patrimony = 100000.0
    
    # Sidebar - Moderna
    with st.sidebar:
        # Logo e título da sidebar
        st.markdown("""
        <div style='text-align: center; padding: 20px 0;'>
            <h3 style='color: #2E8B57;'>⚙️ Controle</h3>
            <p style='color: #666; font-size: 14px;'>Ajuste sua alocação</p>
        </div>
        """, unsafe_allow_html=True)
        
        # Patrimônio total
        with st.container():
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            total = st.number_input(
                "💰 **Patrimônio Total (R$)**",
                min_value=0.0,
                value=float(st.session_state.total_patrimony),
                step=1000.0,
                format="%.2f",
                help="Valor total do seu patrimônio"
            )
            st.session_state.total_patrimony = total
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Alocação macro
        with st.container():
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            st.subheader("📈 Alocação Macro")
            
            macro_total = 0.0
            
            # Cores para cada classe
            colors = {
                'Renda Fixa': '#2E8B57',
                'Ações': '#1E90FF', 
                'FIIs': '#FF8C00',
                'Criptomoedas': '#9370DB'
            }
            
            for asset_class in st.session_state.portfolio['macro']:
                current = float(st.session_state.portfolio['macro'][asset_class])
                
                # Slider com cor personalizada
                value = st.slider(
                    f"**{asset_class}**",
                    min_value=0.0,
                    max_value=100.0,
                    value=current,
                    step=0.5,
                    key=f"slider_{asset_class}",
                    help=f"Alocação para {asset_class}"
                )
                
                st.session_state.portfolio['macro'][asset_class] = float(value)
                macro_total += float(value)
                
                # Barra de progresso simples
                progress_html = f"""
                <div style='margin: 5px 0 15px 0;'>
                    <div style='display: flex; justify-content: space-between; font-size: 12px; color: #666;'>
                        <span>0%</span>
                        <span>{value:.1f}%</span>
                        <span>100%</span>
                    </div>
                    <div style='background: #E0E0E0; height: 4px; border-radius: 2px;'>
                        <div style='background: {colors[asset_class]}; width: {value}%; height: 100%; border-radius: 2px;'></div>
                    </div>
                </div>
                """
                st.markdown(progress_html, unsafe_allow_html=True)
            
            # Status da soma
            if abs(macro_total - 100.0) < 0.01:
                st.success(f"✅ **Soma:** {macro_total:.1f}%")
            else:
                st.error(f"⚠️ **Soma:** {macro_total:.1f}% ≠ 100%")
                # Auto-correção
                if st.button("🔧 Auto-corrigir", use_container_width=True):
                    if macro_total > 0:
                        for key in st.session_state.portfolio['macro']:
                            st.session_state.portfolio['macro'][key] = (
                                st.session_state.portfolio['macro'][key] / macro_total * 100
                            )
                    st.rerun()
            
            st.markdown('</div>', unsafe_allow_html=True)
        
        # Botões de ação
        with st.container():
            st.markdown('<div class="main-card">', unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                if st.button("🔄 Resetar", use_container_width=True, type="secondary"):
                    st.session_state.portfolio = {
                        'macro': {
                            'Renda Fixa': 40.0,
                            'Ações': 30.0,
                            'FIIs': 20.0,
                            'Criptomoedas': 10.0
                        },
                        'sub': {}
                    }
                    st.rerun()
            with col2:
                if st.button("💾 Salvar", use_container_width=True, type="primary"):
                    st.success("✅ Configuração salva!")
            st.markdown('</div>', unsafe_allow_html=True)
    
    # Layout principal com abas
    tab1, tab2, tab3 = st.tabs(["📊 **Dashboard**", "📝 **Editar Ativos**", "💾 **Exportar**"])
    
    with tab1:
        # Cards de métricas no topo
        col1, col2, col3, col4 = st.columns(4)
        
        with col1:
            st.markdown("""
            <div class="metric-card">
                <div style="font-size: 12px; opacity: 0.9;">PATRIMÔNIO</div>
                <div style="font-size: 24px; font-weight: 700;">R$ {:,}</div>
            </div>
            """.format(int(total)), unsafe_allow_html=True)
        
        with col2:
            total_assets = sum(len(st.session_state.portfolio['sub'].get(cls, {})) 
                             for cls in st.session_state.portfolio['macro'])
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 12px; opacity: 0.9;">TOTAL DE ATIVOS</div>
                <div style="font-size: 24px; font-weight: 700;">{total_assets}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col3:
            classes = len(st.session_state.portfolio['macro'])
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 12px; opacity: 0.9;">CLASSES</div>
                <div style="font-size: 24px; font-weight: 700;">{classes}</div>
            </div>
            """, unsafe_allow_html=True)
        
        with col4:
            date_str = datetime.now().strftime("%d/%m")
            st.markdown(f"""
            <div class="metric-card">
                <div style="font-size: 12px; opacity: 0.9;">ATUALIZADO</div>
                <div style="font-size: 24px; font-weight: 700;">{date_str}</div>
            </div>
            """, unsafe_allow_html=True)
        
        st.divider()
        
        # Gráfico principal
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader("📈 Visão Geral da Alocação")
        
        fig = go.Figure()
        
        labels = list(st.session_state.portfolio['macro'].keys())
        values = list(st.session_state.portfolio['macro'].values())
        
        # Cores modernas
        colors = ['#2E8B57', '#1E90FF', '#FF8C00', '#9370DB']
        
        fig.add_trace(go.Pie(
            labels=labels,
            values=values,
            hole=0.4,
            textinfo='label+percent',
            textposition='outside',
            marker=dict(colors=colors, line=dict(color='white', width=2)),
            hoverinfo='label+percent+value',
            textfont=dict(size=14, color='black')
        ))
        
        fig.update_layout(
            title=dict(
                text="Distribuição do Patrimônio",
                font=dict(size=20, color='#1A1A1A')
            ),
            showlegend=True,
            legend=dict(
                font=dict(color='#1A1A1A'),
                bgcolor='rgba(255,255,255,0.8)',
                bordercolor='#E0E0E0'
            ),
            height=500,
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        st.plotly_chart(fig, use_container_width=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Tabela de resumo
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.subheader("📋 Resumo Detalhado")
        
        # Criar tabela de resumo
        summary_data = []
        for asset_class, allocation in st.session_state.portfolio['macro'].items():
            class_value = total * (float(allocation) / 100.0)
            
            summary_data.append({
                'Classe': asset_class,
                'Alocação': f"{allocation:.1f}%",
                'Valor': format_currency(class_value),
                'Cor': colors[list(st.session_state.portfolio['macro'].keys()).index(asset_class)]
            })
        
        # Exibir como cards
        cols = st.columns(4)
        for idx, item in enumerate(summary_data):
            with cols[idx]:
                st.markdown(f"""
                <div style='
                    background: linear-gradient(135deg, {item['Cor']}20, {item['Cor']}10);
                    border-left: 4px solid {item['Cor']};
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 10px;
                '>
                    <div style='font-weight: 600; color: {item['Cor']}; font-size: 14px;'>{item['Classe']}</div>
                    <div style='font-size: 20px; font-weight: 700; color: #1A1A1A; margin: 5px 0;'>{item['Alocação']}</div>
                    <div style='font-size: 12px; color: #666;'>{item['Valor']}</div>
                </div>
                """, unsafe_allow_html=True)
        
        # Detalhes expandíveis
        for asset_class, allocation in st.session_state.portfolio['macro'].items():
            class_value = total * (float(allocation) / 100.0)
            
            with st.expander(f"🔍 Detalhes de {asset_class} ({allocation:.1f}%)", expanded=False):
                if asset_class in st.session_state.portfolio['sub']:
                    assets = st.session_state.portfolio['sub'][asset_class]
                    if assets:
                        # Tabela interna
                        for asset_name, asset_percent in assets.items():
                            asset_percent_float = float(asset_percent)
                            asset_value = class_value * (asset_percent_float / 100.0)
                            
                            col1, col2, col3 = st.columns([3, 1, 2])
                            with col1:
                                st.write(f"**{asset_name}**")
                            with col2:
                                st.metric("", f"{asset_percent_float:.1f}%")
                            with col3:
                                st.metric("", format_currency(asset_value))
                    else:
                        st.info("Nenhum sub-ativo definido. Use a aba 'Editar Ativos' para adicionar.")
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    with tab2:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.header("📝 Edição de Sub-Ativos")
        st.markdown("Defina os ativos específicos dentro de cada classe de investimento.")
        st.markdown('</div>', unsafe_allow_html=True)
        
        if ASSET_EDITOR_OK:
            for asset_class, class_allocation in st.session_state.portfolio['macro'].items():
                if asset_class not in st.session_state.portfolio['sub']:
                    st.session_state.portfolio['sub'][asset_class] = {}
                
                # Card para cada classe
                st.markdown(f"""
                <div class="main-card">
                    <h4 style='color: #2E8B57;'>{asset_class}</h4>
                    <p style='color: #666; font-size: 14px; margin-bottom: 20px;'>
                        Alocação total da classe: <strong>{class_allocation:.1f}%</strong> 
                        ({format_currency(total * (float(class_allocation) / 100.0))})
                    </p>
                """, unsafe_allow_html=True)
                
                edited = AssetEditor.edit_asset_class(
                    class_name=asset_class,
                    assets_dict=st.session_state.portfolio['sub'][asset_class],
                    class_allocation=float(class_allocation),
                    total_patrimony=float(total)
                )
                
                if edited is not None:
                    st.session_state.portfolio['sub'][asset_class] = edited
                
                st.markdown('</div>', unsafe_allow_html=True)
                st.write("")  # Espaço
        else:
            st.warning("⚠️ Editor de ativos não disponível")
    
    with tab3:
        st.markdown('<div class="main-card">', unsafe_allow_html=True)
        st.header("💾 Exportar Dados")
        st.markdown("Salve ou compartilhe sua configuração de portfólio.")
        
        col1, col2 = st.columns(2)
        
        with col1:
            # Exportar JSON
            portfolio_json = json.dumps(st.session_state.portfolio, indent=2, ensure_ascii=False)
            
            st.download_button(
                label="📥 **Baixar como JSON**",
                data=portfolio_json,
                file_name=f"diagrama_cerrado_{datetime.now().strftime('%Y%m%d_%H%M')}.json",
                mime="application/json",
                use_container_width=True,
                help="Baixa a configuração completa do portfólio"
            )
            
            # Exportar CSV
            csv_data = []
            for asset_class, allocation in st.session_state.portfolio['macro'].items():
                class_value = total * (float(allocation) / 100.0)
                csv_data.append([asset_class, "", allocation, class_value])
                
                if asset_class in st.session_state.portfolio['sub']:
                    for asset_name, asset_percent in st.session_state.portfolio['sub'][asset_class].items():
                        asset_value = class_value * (float(asset_percent) / 100.0)
                        csv_data.append(["", asset_name, asset_percent, asset_value])
            
            df_csv = pd.DataFrame(csv_data, columns=["Classe", "Ativo", "Alocação (%)", "Valor (R$)"])
            csv_string = df_csv.to_csv(index=False)
            
            st.download_button(
                label="📊 **Baixar como CSV**",
                data=csv_string,
                file_name=f"relatorio_portfolio_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv",
                use_container_width=True,
                help="Baixa um relatório em formato de planilha"
            )
        
        with col2:
            # Visualizar dados
            if st.button("👁️ **Visualizar Dados**", use_container_width=True):
                with st.expander("📋 Dados do Portfólio", expanded=True):
                    st.json(st.session_state.portfolio)
            
            # Copiar para clipboard
            if st.button("📋 **Copiar JSON**", use_container_width=True, type="secondary"):
                st.code(portfolio_json[:300] + "..." if len(portfolio_json) > 300 else portfolio_json)
                st.success("JSON copiado para a área de transferência!")
        
        # Resumo de exportação
        st.divider()
        st.subheader("📊 Estatísticas da Exportação")
        
        col1, col2, col3 = st.columns(3)
        with col1:
            st.metric("Classes", len(st.session_state.portfolio['macro']))
        with col2:
            total_assets = sum(len(st.session_state.portfolio['sub'].get(cls, {})) 
                             for cls in st.session_state.portfolio['macro'])
            st.metric("Ativos", total_assets)
        with col3:
            st.metric("Data", datetime.now().strftime("%d/%m/%Y"))
        
        st.markdown('</div>', unsafe_allow_html=True)


if __name__ == "__main__":
    main()