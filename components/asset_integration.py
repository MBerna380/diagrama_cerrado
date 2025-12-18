# components/asset_integration.py
import requests
import streamlit as st
from PIL import Image
from io import BytesIO
import base64
import yfinance as yf
import pandas as pd

class AssetIntegration:
    def __init__(self):
        self.cache = {}
        
    def get_stock_logo(self, ticker):
        """Obtém logo de ação/FII da B3"""
        cache_key = f"stock_{ticker}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # Usando yfinance para dados básicos
            stock = yf.Ticker(f"{ticker}.SA")
            info = stock.info
            
            if 'logo_url' in info:
                self.cache[cache_key] = info['logo_url']
                return info['logo_url']
            
            # Fallback para APIs públicas
            b3_logo = self._get_b3_logo(ticker)
            if b3_logo:
                self.cache[cache_key] = b3_logo
                return b3_logo
                
        except Exception as e:
            st.warning(f"Não foi possível obter logo para {ticker}: {e}")
        
        # Retorna placeholder
        return f"https://via.placeholder.com/40/2E8B57/FFFFFF?text={ticker[:3]}"
    
    def get_crypto_logo(self, symbol):
        """Obtém logo de criptomoeda"""
        cache_key = f"crypto_{symbol}"
        
        if cache_key in self.cache:
            return self.cache[cache_key]
        
        try:
            # CoinGecko API (gratuita)
            url = f"https://api.coingecko.com/api/v3/coins/{symbol.lower()}"
            response = requests.get(url, timeout=5)
            
            if response.status_code == 200:
                data = response.json()
                logo = data['image']['small']
                self.cache[cache_key] = logo
                return logo
        except:
            pass
        
        # CryptoIcons fallback
        return f"https://cryptoicons.org/api/icon/{symbol.lower()}/40"
    
    def display_asset_with_logo(self, asset_name, allocation, value_brl):
        """Exibe ativo com logo e informações"""
        col1, col2, col3 = st.columns([1, 3, 2])
        
        with col1:
            # Identificar tipo de ativo
            if any(x in asset_name.upper() for x in ['PETR', 'VALE', 'ITUB', 'B3']):
                logo_url = self.get_stock_logo(asset_name)
            elif 'BTC' in asset_name.upper() or 'ETH' in asset_name.upper():
                logo_url = self.get_crypto_logo(asset_name)
            else:
                logo_url = "https://via.placeholder.com/40/808080/FFFFFF?text=?"
            
            st.image(logo_url, width=40)
        
        with col2:
            st.write(f"**{asset_name}**")
        
        with col3:
            st.write(f"**{allocation:.1f}%**")
            st.caption(f"R$ {value_brl:,.2f}")
    
    def get_asset_price(self, ticker, asset_type):
        """Obtém preço atual do ativo"""
        try:
            if asset_type in ['Ações', 'FIIs']:
                stock = yf.Ticker(f"{ticker}.SA")
                return stock.info.get('regularMarketPrice', 0)
            elif asset_type == 'Criptomoedas':
                # Simulação - implementar API real
                return 0
        except:
            return 0