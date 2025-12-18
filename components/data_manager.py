# components/data_manager.py
import streamlit as st
import pandas as pd
import json
import csv
from io import StringIO
from datetime import datetime
from utils.formatters import format_currency

class DataManager:
    @staticmethod
    def display_summary_table(portfolio, total_patrimony):
        """Exibe tabela de resumo detalhada"""
        data = []
        
        for asset_class, class_allocation in portfolio['macro'].items():
            class_value = total_patrimony * (class_allocation / 100)
            
            # Linha da classe principal
            data.append({
                'Tipo': 'Classe',
                'Nome': asset_class,
                'Alocação (%)': f"{class_allocation:.2f}%",
                'Valor (R$)': format_currency(class_value),
                'Detalhes': ''
            })
            
            # Sub-atributos
            if asset_class in portfolio['sub']:
                for sub_asset, sub_allocation in portfolio['sub'][asset_class].items():
                    sub_value = class_value * (sub_allocation / 100)
                    data.append({
                        'Tipo': 'Sub-ativo',
                        'Nome': f"  └─ {sub_asset}",
                        'Alocação (%)': f"{sub_allocation:.2f}%",
                        'Valor (R$)': format_currency(sub_value),
                        'Detalhes': f"{sub_allocation/100*class_allocation:.2f}% do total"
                    })
        
        # Criar DataFrame
        df = pd.DataFrame(data)
        
        # Exibir tabela estilizada
        st.dataframe(
            df,
            column_config={
                "Tipo": st.column_config.TextColumn("Tipo", width="small"),
                "Nome": st.column_config.TextColumn("Ativo", width="medium"),
                "Alocação (%)": st.column_config.TextColumn("Alocação", width="small"),
                "Valor (R$)": st.column_config.TextColumn("Valor", width="medium"),
                "Detalhes": st.column_config.TextColumn("Detalhes", width="medium"),
            },
            hide_index=True,
            use_container_width=True
        )
        
        # Métricas resumidas
        col1, col2, col3, col4 = st.columns(4)
        with col1:
            st.metric("Total Investido", format_currency(total_patrimony))
        with col2:
            classes_count = len(portfolio['macro'])
            st.metric("Classes de Ativos", classes_count)
        with col3:
            sub_assets_count = sum(len(subs) for subs in portfolio['sub'].values())
            st.metric("Ativos Individuais", sub_assets_count)
        with col4:
            date_str = datetime.now().strftime("%d/%m/%Y")
            st.metric("Última Atualização", date_str)
    
    @staticmethod
    def data_management_section(portfolio):
        """Seção de gerenciamento de dados"""
        st.header("💾 Gerenciamento de Dados")
        
        # Exportar para JSON
        st.subheader("Exportar Configuração")
        json_str = json.dumps(portfolio, indent=2, ensure_ascii=False)
        
        col1, col2 = st.columns(2)
        with col1:
            st.download_button(
                label="📥 Baixar JSON",
                data=json_str,
                file_name=f"diagrama_cerrado_{datetime.now().strftime('%Y%m%d_%H%M%S')}.json",
                mime="application/json"
            )
        
        with col2:
            if st.button("📋 Copiar para Clipboard"):
                st.code(json_str[:500] + "..." if len(json_str) > 500 else json_str)
                st.success("JSON copiado para clipboard!")
        
        # Importar de JSON
        st.subheader("Importar Configuração")
        uploaded_file = st.file_uploader(
            "Escolha um arquivo JSON",
            type=['json'],
            help="Faça upload de um arquivo JSON exportado anteriormente"
        )
        
        if uploaded_file is not None:
            try:
                imported_data = json.load(uploaded_file)
                
                # Validar estrutura
                if 'macro' in imported_data and 'sub' in imported_data:
                    st.success("✅ Estrutura do arquivo válida!")
                    
                    col1, col2 = st.columns(2)
                    with col1:
                        if st.button("🔄 Carregar Configuração"):
                            st.session_state.portfolio = imported_data
                            st.rerun()
                    
                    with col2:
                        if st.button("👁️ Visualizar"):
                            st.json(imported_data, expanded=False)
                else:
                    st.error("❌ Estrutura inválida. O arquivo deve conter 'macro' e 'sub'.")
            except Exception as e:
                st.error(f"Erro ao ler arquivo: {e}")
        
        # Exportar para CSV
        st.subheader("Exportar para CSV")
        
        if st.button("📊 Gerar Relatório CSV"):
            # Preparar dados para CSV
            csv_data = []
            for asset_class, class_allocation in portfolio['macro'].items():
                csv_data.append({
                    'Nível': 'Classe',
                    'Categoria': asset_class,
                    'Ativo': asset_class,
                    'Alocação (%)': class_allocation,
                    'Porcentagem do Total': class_allocation
                })
                
                if asset_class in portfolio['sub']:
                    for sub_asset, sub_allocation in portfolio['sub'][asset_class].items():
                        total_percentage = (sub_allocation / 100) * class_allocation
                        csv_data.append({
                            'Nível': 'Sub-ativo',
                            'Categoria': asset_class,
                            'Ativo': sub_asset,
                            'Alocação (%)': sub_allocation,
                            'Porcentagem do Total': total_percentage
                        })
            
            df_csv = pd.DataFrame(csv_data)
            csv_string = df_csv.to_csv(index=False)
            
            st.download_button(
                label="📥 Baixar CSV",
                data=csv_string,
                file_name=f"relatorio_alocacao_{datetime.now().strftime('%Y%m%d')}.csv",
                mime="text/csv"
            )
            
            # Pré-visualização
            st.dataframe(df_csv.head(10), use_container_width=True)
        
        # Limpar dados
        st.subheader("Manutenção")
        
        if st.button("🗑️ Limpar Todos os Dados", type="secondary"):
            st.warning("Tem certeza que deseja limpar todos os dados?")
            col1, col2, col3 = st.columns(3)
            with col1:
                if st.button("✅ Sim, limpar"):
                    for key in list(st.session_state.keys()):
                        del st.session_state[key]
                    st.rerun()
            with col2:
                if st.button("❌ Cancelar"):
                    pass
    
    @staticmethod
    def save_to_session(portfolio):
        """Salva portfólio na session_state"""
        st.session_state.portfolio = portfolio
        st.session_state.last_save = datetime.now()
    
    @staticmethod
    def load_from_session():
        """Carrega portfólio da session_state"""
        return st.session_state.get('portfolio', None)