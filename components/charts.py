# components/charts.py
import plotly.graph_objects as go
import plotly.express as px
from plotly.subplots import make_subplots
from utils.formatters import format_currency, format_percentage

class ChartBuilder:
    def __init__(self, total_patrimony):
        self.total_patrimony = total_patrimony
    
    def create_sunburst_chart(self, portfolio_data):
        """Cria gráfico sunburst com valores em R$"""
        labels = []
        parents = []
        values = []
        text = []
        
        # Nível 1: Classes de ativos
        for asset_class, allocation in portfolio_data['macro'].items():
            labels.append(asset_class)
            parents.append("")
            value_brl = self.total_patrimony * (allocation / 100)
            values.append(value_brl)
            text.append(f"{allocation}%<br>{format_currency(value_brl)}")
            
            # Nível 2: Sub-ativos
            if asset_class in portfolio_data['sub']:
                for sub_asset, sub_allocation in portfolio_data['sub'][asset_class].items():
                    labels.append(sub_asset)
                    parents.append(asset_class)
                    sub_value_brl = value_brl * (sub_allocation / 100)
                    values.append(sub_value_brl)
                    text.append(f"{sub_allocation}%<br>{format_currency(sub_value_brl)}")
        
        fig = go.Figure(go.Sunburst(
            labels=labels,
            parents=parents,
            values=values,
            branchvalues="total",
            text=text,
            textinfo="text",
            hovertemplate="<b>%{label}</b><br>" +
                         "Alocação: %{text}<br>" +
                         "Valor Absoluto: %{value:,.2f}<br>" +
                         "<extra></extra>",
            marker=dict(
                colors=px.colors.qualitative.Set3,
                line=dict(width=2, color='#1a1a1a')
            ),
            maxdepth=2
        ))
        
        fig.update_layout(
            title="Diagrama de Alocação Patrimonial",
            template="plotly_dark",
            margin=dict(t=40, l=0, r=0, b=0),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)',
            font=dict(color='white')
        )
        
        return fig
    
    def create_horizontal_bar_chart(self, portfolio_data):
        """Gráfico de barras horizontal"""
        categories = []
        percentages = []
        values_brl = []
        
        for asset_class, allocation in portfolio_data['macro'].items():
            categories.append(asset_class)
            percentages.append(allocation)
            values_brl.append(self.total_patrimony * (allocation / 100))
        
        fig = go.Figure()
        
        fig.add_trace(go.Bar(
            y=categories,
            x=percentages,
            orientation='h',
            text=[f"{p}%<br>{format_currency(v)}" 
                  for p, v in zip(percentages, values_brl)],
            textposition='auto',
            hoverinfo='text',
            marker=dict(
                color=['#2E8B57', '#1E90FF', '#FF8C00', '#9370DB'],
                line=dict(color='#1a1a1a', width=1)
            )
        ))
        
        fig.update_layout(
            title="Alocação por Classe",
            xaxis_title="Percentual (%)",
            template="plotly_dark",
            height=400,
            showlegend=False,
            xaxis=dict(range=[0, 100]),
            paper_bgcolor='rgba(0,0,0,0)',
            plot_bgcolor='rgba(0,0,0,0)'
        )
        
        return fig