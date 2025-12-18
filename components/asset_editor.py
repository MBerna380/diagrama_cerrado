# components/asset_editor.py - TEMA CLARO
"""
Editor de ativos - Versão Tema Claro
"""
import streamlit as st
import pandas as pd


def validate_percentage_sum_local(values, target=100, tolerance=0.01):
    """Valida soma de porcentagens"""
    if not values:
        return False
    total = sum(values)
    return abs(total - target) <= tolerance


class AssetEditor:
    """Editor de ativos com tema claro"""
    
    @staticmethod
    def edit_asset_class(class_name, assets_dict, class_allocation=100.0, total_patrimony=0.0):
        """Editor para classe de ativos - Tema Claro"""
        
        st.markdown(f"""
        <div style='
            background: #F8F9FA;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
            border-left: 4px solid #2E8B57;
        '>
            <h4 style='color: #2E8B57; margin: 0;'>{class_name}</h4>
        </div>
        """, unsafe_allow_html=True)
        
        # Se vazio, criar um item padrão
        if not assets_dict:
            assets_dict = {"Ativo 1": 100.0}
        
        # Informações da classe
        if total_patrimony > 0:
            class_value = total_patrimony * (class_allocation / 100)
            st.info(f"""
            **Alocação desta classe:** {class_allocation:.1f}%  
            **Valor disponível:** {format_currency(class_value)}  
            *Distribua 100% entre os ativos abaixo:*
            """)
        
        # Converter dict para DataFrame
        items_list = []
        for asset, percent in assets_dict.items():
            if total_patrimony > 0 and class_allocation > 0:
                asset_value = total_patrimony * (class_allocation / 100) * (percent / 100)
                items_list.append({
                    'Ativo': asset,
                    'Alocação (%)': percent,
                    'Valor (R$)': f"R$ {asset_value:,.2f}"
                })
            else:
                items_list.append({
                    'Ativo': asset,
                    'Alocação (%)': percent,
                    'Valor (R$)': "R$ 0,00"
                })
        
        df = pd.DataFrame(items_list)
        
        # Editor de dados
        edited_df = st.data_editor(
            df,
            column_config={
                "Ativo": st.column_config.TextColumn(
                    "Nome do Ativo",
                    width="medium",
                    required=True
                ),
                "Alocação (%)": st.column_config.NumberColumn(
                    "Percentual",
                    min_value=0.0,
                    max_value=100.0,
                    step=0.5,
                    format="%.2f"
                ),
                "Valor (R$)": st.column_config.TextColumn(
                    "Valor",
                    disabled=True
                )
            },
            num_rows="dynamic",
            use_container_width=True,
            key=f"editor_{class_name}"
        )
        
        # Botões de ação
        col1, col2, col3 = st.columns(3)
        
        with col1:
            if st.button("➕ Adicionar", 
                        key=f"add_{class_name}",
                        use_container_width=True,
                        help="Adiciona novo ativo"):
                assets_dict[f"Ativo {len(assets_dict)+1}"] = 0.0
                st.rerun()
        
        with col2:
            if st.button("🔄 Balancear", 
                        key=f"balance_{class_name}",
                        use_container_width=True,
                        help="Distribui igualmente entre ativos"):
                if assets_dict:
                    num_assets = len(assets_dict)
                    for key in assets_dict:
                        assets_dict[key] = 100.0 / num_assets
                    st.rerun()
        
        with col3:
            if st.button("✅ Validar", 
                        key=f"validate_{class_name}",
                        use_container_width=True,
                        type="primary"):
                if not edited_df.empty:
                    total = edited_df['Alocação (%)'].sum()
                    if validate_percentage_sum_local(edited_df['Alocação (%)']):
                        st.success(f"✅ Soma válida: {total:.2f}%")
                    else:
                        st.error(f"❌ Soma: {total:.2f}% ≠ 100%")
        
        # Processar edições
        if not edited_df.empty:
            valid_rows = edited_df.dropna(subset=['Ativo'])
            valid_rows = valid_rows[valid_rows['Ativo'].str.strip() != '']
            
            if not valid_rows.empty:
                new_dict = {}
                for _, row in valid_rows.iterrows():
                    asset_name = str(row['Ativo']).strip()
                    percent = float(row['Alocação (%)'])
                    new_dict[asset_name] = percent
                
                # Validar soma
                total_percent = sum(new_dict.values())
                
                if total_percent > 0:
                    # Rebalancear se necessário
                    if abs(total_percent - 100) > 0.01:
                        st.warning(f"⚠️ Rebalanceando para 100% (atual: {total_percent:.1f}%)")
                        new_dict = {k: (v / total_percent) * 100 for k, v in new_dict.items()}
                    
                    return new_dict
        
        return assets_dict
    
    @staticmethod
    def create_macro_sliders(portfolio_state):
        """Cria sliders para alocação macro"""
        st.markdown("""
        <div style='
            background: #F8F9FA;
            border-radius: 10px;
            padding: 15px;
            margin-bottom: 20px;
        '>
            <h4 style='color: #2E8B57; margin: 0;'>📊 Ajuste a Alocação Macro</h4>
            <p style='color: #666; margin: 5px 0 15px 0;'>Distribua 100% entre as classes de ativos</p>
        </div>
        """, unsafe_allow_html=True)
        
        macro_values = {}
        cols = st.columns(4)
        
        asset_classes = ['Renda Fixa', 'Ações', 'FIIs', 'Criptomoedas']
        colors = ['#2E8B57', '#1E90FF', '#FF8C00', '#9370DB']
        
        for idx, (asset_class, color) in enumerate(zip(asset_classes, colors)):
            with cols[idx]:
                # Card para cada classe
                st.markdown(f"""
                <div style='
                    background: {color}10;
                    border: 1px solid {color}30;
                    border-radius: 8px;
                    padding: 15px;
                    margin-bottom: 10px;
                '>
                    <div style='color: {color}; font-weight: 600; font-size: 14px;'>{asset_class}</div>
                """, unsafe_allow_html=True)
                
                current = portfolio_state.get('macro', {}).get(asset_class, 
                    40.0 if asset_class == 'Renda Fixa' else
                    30.0 if asset_class == 'Ações' else
                    20.0 if asset_class == 'FIIs' else 10.0)
                
                # Slider
                value = st.slider(
                    "",
                    0.0, 100.0,
                    float(current),
                    0.5,
                    key=f"macro_{asset_class}",
                    label_visibility="collapsed"
                )
                
                # Display do valor
                st.markdown(f"""
                <div style='
                    text-align: center;
                    font-size: 20px;
                    font-weight: 700;
                    color: {color};
                    margin-top: 5px;
                '>
                    {value:.1f}%
                </div>
                """, unsafe_allow_html=True)
                
                st.markdown('</div>', unsafe_allow_html=True)
                
                macro_values[asset_class] = value
        
        # Calcular e mostrar soma
        total = sum(macro_values.values())
        
        st.markdown(f"""
        <div style='
            background: {'#E8F5E9' if abs(total - 100) < 0.01 else '#FFEBEE'};
            border: 2px solid {'#2E8B57' if abs(total - 100) < 0.01 else '#F44336'};
            border-radius: 10px;
            padding: 15px;
            margin-top: 20px;
            text-align: center;
        '>
            <div style='font-size: 16px; font-weight: 600; color: {'#2E8B57' if abs(total - 100) < 0.01 else '#F44336'};'>
                {'✅' if abs(total - 100) < 0.01 else '⚠️'} Soma Total: {total:.1f}%
            </div>
            <div style='font-size: 14px; color: #666; margin-top: 5px;'>
                {'Alocação válida!' if abs(total - 100) < 0.01 else 'Ajuste para 100%'}
            </div>
        </div>
        """, unsafe_allow_html=True)
        
        return total, macro_values


def format_currency(value):
    """Função auxiliar para formatação"""
    return f"R$ {value:,.2f}"