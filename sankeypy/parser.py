import pandas as pd

"""
    Valida que o DataFrame tem as colunas necessárias e remove linhas inválidas.
    Regras:
      - Assegura existência das colunas source, target e value.
      - Remove linhas com NaN nas colunas essenciais.
      - Remove linhas com value <= 0.
      - Lança ValueError se ficar vazio após limpeza.
    """



def validar_dataframe(df, source, target, value):
    for col in (source, target, value):
        if col not in df.columns:
            raise ValueError(f"Coluna '{col}' não existe no DataFrame.")

    df = df.dropna(subset=[source, target, value])
    df = df[df[value] > 0]

    if df.empty:
        raise ValueError("Não há dados válidos após remover fluxos nulos/negativos.")
    return df


"""
    Agrupa fluxos cujo valor seja inferior a (threshold * total).
    Se threshold for None, devolve o DataFrame sem alterações.
    """

def agrupar_fluxos_pequenos(df, source, target, value, threshold):
    if threshold is not None:
        total = df[value].sum()
        mask = df[value] < (threshold * total)
        if mask.any():
            agrupados = pd.DataFrame({
                source: ['Outros'] * mask.sum(),
                target: df.loc[mask, target],
                value: df.loc[mask, value]
            })
            df = pd.concat([df.loc[~mask], agrupados], ignore_index=True)
    return df

