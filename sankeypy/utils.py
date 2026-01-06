import pandas as pd

def gerar_df_exemplo():
    return pd.DataFrame({
        'source': ['A', 'A', 'B', 'C', 'E'],
        'target': ['B', 'C', 'D', 'D', 'D'],
        'value':  [10, 5, 15, 5, 0.5]
    })