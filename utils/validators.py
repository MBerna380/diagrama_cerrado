# utils/validators.py
"""
Validações para o Diagrama do Cerrado
"""

def validate_percentage_sum(values, target=100, tolerance=0.01):
    """
    Valida se a soma dos valores é igual ao target
    
    Args:
        values: Lista ou iterável de valores
        target: Valor alvo (default: 100)
        tolerance: Tolerância permitida (default: 0.01)
    
    Returns:
        bool: True se válido, False caso contrário
    """
    if not values:
        return False
    
    total = sum(values)
    return abs(total - target) <= tolerance


class PortfolioValidator:
    """Classe para validações do portfólio"""
    
    @staticmethod
    def validate_macro_allocation(macro_allocation):
        """Valida a alocação macro"""
        total = sum(macro_allocation.values())
        if not validate_percentage_sum(macro_allocation.values()):
            return False, f"Soma das alocações macro: {total:.2f}% (deve ser 100%)"
        return True, "✅ Alocação macro válida"
    
    @staticmethod
    def validate_sub_allocations(portfolio):
        """Valida todas as sub-alocações"""
        errors = []
        
        for asset_class, sub_assets in portfolio['sub'].items():
            if sub_assets:  # Se houver sub-atributos
                total = sum(sub_assets.values())
                if not validate_percentage_sum(sub_assets.values()):
                    errors.append(f"{asset_class}: {total:.2f}% ≠ 100%")
        
        if errors:
            return False, " | ".join(errors)
        return True, "✅ Todas sub-alocações válidas"
    
    @staticmethod
    def validate_asset_names(portfolio):
        """Valida nomes dos ativos"""
        empty_names = []
        
        for asset_class, sub_assets in portfolio['sub'].items():
            for asset_name in sub_assets.keys():
                if not asset_name or str(asset_name).strip() == '':
                    empty_names.append(f"{asset_class}: Nome vazio")
        
        if empty_names:
            return False, "Nomes de ativos vazios encontrados"
        return True, "✅ Todos os nomes são válidos"
    
    @staticmethod
    def validate_negative_values(portfolio):
        """Valida valores negativos"""
        negative_found = []
        
        # Verificar macro
        for asset_class, value in portfolio['macro'].items():
            if value < 0:
                negative_found.append(f"{asset_class} macro: {value}")
        
        # Verificar sub
        for asset_class, sub_assets in portfolio['sub'].items():
            for asset_name, value in sub_assets.items():
                if value < 0:
                    negative_found.append(f"{asset_class}/{asset_name}: {value}")
        
        if negative_found:
            return False, f"Valores negativos: {', '.join(negative_found)}"
        return True, "✅ Todos os valores são positivos"
    
    @staticmethod
    def full_portfolio_validation(portfolio):
        """Executa todas as validações"""
        results = []
        
        # 1. Validação macro
        valid_macro, msg_macro = PortfolioValidator.validate_macro_allocation(portfolio['macro'])
        results.append(("Alocação Macro", valid_macro, msg_macro))
        
        # 2. Validação sub
        valid_sub, msg_sub = PortfolioValidator.validate_sub_allocations(portfolio)
        results.append(("Sub-alocações", valid_sub, msg_sub))
        
        # 3. Validação nomes
        valid_names, msg_names = PortfolioValidator.validate_asset_names(portfolio)
        results.append(("Nomes dos Ativos", valid_names, msg_names))
        
        # 4. Validação negativos
        valid_values, msg_values = PortfolioValidator.validate_negative_values(portfolio)
        results.append(("Valores Negativos", valid_values, msg_values))
        
        return results