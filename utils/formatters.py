# utils/formatters.py
def format_currency(value):
    """Formata valor monetário"""
    if value >= 1_000_000_000:
        return f'R$ {value/1_000_000_000:.2f}B'
    elif value >= 1_000_000:
        return f'R$ {value/1_000_000:.2f}M'
    elif value >= 1_000:
        return f'R$ {value/1_000:.1f}K'
    else:
        return f'R$ {value:,.2f}'

def format_percentage(value):
    """Formata porcentagem"""
    return f'{value:.2f}%'

# utils/validators.py
def validate_percentage_sum(values, target=100, tolerance=0.01):
    """Valida soma de porcentagens"""
    total = sum(values)
    return abs(total - target) <= tolerance

def validate_portfolio(portfolio):
    """Valida estrutura completa do portfólio"""
    errors = []
    
    # Valida macro alocação
    macro_total = sum(portfolio['macro'].values())
    if not validate_percentage_sum(portfolio['macro'].values()):
        errors.append(f"Alocação macro: {macro_total:.2f}% ≠ 100%")
    
    # Valida sub-alocações
    for asset_class, sub_assets in portfolio['sub'].items():
        if sub_assets:
            sub_total = sum(sub_assets.values())
            if not validate_percentage_sum(sub_assets.values()):
                errors.append(f"{asset_class}: {sub_total:.2f}% ≠ 100%")
    
    return errors