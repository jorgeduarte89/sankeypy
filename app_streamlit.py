# app_streamlit.py
"""
Streamlit demo para SankeyPy
- Upload CSV
- Seleção de colunas (source/target/value)
- Slider threshold (agrupamento de fluxos pequenos)
- Gerar Sankey interativamente
- Download em HTML
"""

import os
import tempfile
import pandas as pd
import streamlit as st
import plotly.graph_objects as go

# Importa módulos da tua biblioteca
from sankeypy.parser import validar_dataframe, agrupar_fluxos_pequenos
from sankeypy.style import default_colors


# =========================
# CONFIGURAÇÃO DA PÁGINA
# =========================
st.set_page_config(page_title="SankeyPy — Demo", layout="wide")

st.title("📊 SankeyPy — Demonstração Interativa")
st.markdown(
    "Esta aplicação permite carregar um CSV, escolher colunas e gerar um diagrama de Sankey "
    "utilizando a biblioteca **SankeyPy**."
)


# =========================
# SIDEBAR — UPLOAD E OPÇÕES
# =========================
st.sidebar.header("Opções")

uploaded_file = st.sidebar.file_uploader("Carregar CSV", type=["csv", "txt"])
use_example = st.sidebar.button("Usar dataset de exemplo")

threshold = st.sidebar.slider(
    "Threshold (proporção para agrupar 'Outros')",
    min_value=0.0, max_value=0.5, value=0.05, step=0.01
)

orientation = st.sidebar.selectbox(
    "Orientação do Sankey",
    options=["h", "v"], index=0
)

font_size = st.sidebar.slider(
    "Tamanho da fonte",
    min_value=8, max_value=20, value=11
)


# =========================
# 1 — CARREGAR DATAFRAME
# =========================


# -----------------------------
df = None

if uploaded_file:
    # tenta ler com header normal
    try:
        df = pd.read_csv(uploaded_file)
    except Exception as e:
        st.sidebar.error(f"Erro a ler o ficheiro: {e}")
        df = None

    # Caso o CSV esteja sem cabeçalho (ex.: A,B,10) e tenha exactamente 3 colunas,
    # re-lê com header=None e atribui nomes standard.
    if df is not None:
        needed = {"source", "target", "value"}
        cols = set(df.columns.astype(str))
        if not needed.issubset(cols) and df.shape[1] == 3:
            # re-leitura forçada com header=None
            uploaded_file.seek(0)  # volta ao início do buffer
            df = pd.read_csv(uploaded_file, header=None)
            df.columns = ["source", "target", "value"]
            st.sidebar.warning("CSV sem cabeçalho detectado: atribuí 'source,target,value' automaticamente.")

    # limpeza de tipos: normalizar strings e converter coluna value para numérica
    if df is not None:
        # remover espaços em cabeçalhos e valores de strings
        df.columns = [str(c).strip() for c in df.columns]

        # normalizar a coluna 'value' se existir
        if "value" in df.columns:
            # converter a coluna para string, substituir vírgulas por pontos, tirar espaços
            df["value"] = df["value"].astype(str).str.strip().str.replace(",", ".", regex=False)
            # converter para numérico (coerce => NaN onde não converter)
            df["value"] = pd.to_numeric(df["value"], errors="coerce")
            # retirar linhas com value inválido
            before = len(df)
            df = df.dropna(subset=["value"])
            after = len(df)
            if before != after:
                st.sidebar.info(f"{before-after} linha(s) removida(s) por 'value' inválido(a).")
        else:
            st.sidebar.error("A coluna 'value' não foi encontrada no CSV após limpeza.")
            df = None

elif use_example:
    df = pd.DataFrame({
        "source": ["A", "A", "B", "C", "E"],
        "target": ["B", "C", "D", "D", "D"],
        "value": [10, 5, 15, 5, 0.5]
    })
    st.sidebar.success("Dataset de exemplo carregado.")

if df is None:
    st.info("Carrega um CSV através do menu à esquerda ou usa o dataset de exemplo.")
    st.stop()


# Preview do DataFrame
st.subheader("Pré-visualização do dataset")
st.dataframe(df.head(6))


# =========================
# 2 — SELEÇÃO DE COLUNAS
# =========================

cols = list(df.columns)

source_col = st.selectbox("Coluna para 'source'", options=cols)
target_col = st.selectbox("Coluna para 'target'", options=cols)
value_col = st.selectbox("Coluna para 'value'", options=cols)

st.write("---")

btn_generate = st.button("Gerar Sankey")
export_html = st.checkbox("Permitir download em HTML", value=True)


# =========================
# FUNÇÃO DE CONSTRUÇÃO DO SANKEY
# =========================

def build_sankey(df_in, source, target, value, threshold=None, orientation='h', font_size=10):
    """
    Cria um Figure Plotly com base nos dados do SankeyPy.
    """
    # 1) validar dados
    df_val = validar_dataframe(df_in.copy(), source, target, value)

    # 2) aplicar threshold
    df_proc = agrupar_fluxos_pequenos(df_val.copy(), source, target, value, threshold)

    # 3) extrair nós
    nodes = list(dict.fromkeys(list(df_proc[source]) + list(df_proc[target])))
    label_to_id = {label: i for i, label in enumerate(nodes)}

    # 4) cores
    colors = default_colors[:len(nodes)]

    # 5) construir objeto Sankey
    sankey = go.Sankey(
        orientation=orientation,
        node=dict(
            label=nodes,
            color=colors,
            pad=15,
            thickness=20,
        ),
        link=dict(
            source=df_proc[source].map(label_to_id),
            target=df_proc[target].map(label_to_id),
            value=df_proc[value],
        )
    )

    fig = go.Figure(sankey)
    fig.update_layout(title="SankeyPy — Demo", font_size=font_size)

    return fig


# =========================
# 3 — GERAR SANKEY
# =========================

if btn_generate:
    try:
        fig = build_sankey(
            df,
            source_col,
            target_col,
            value_col,
            threshold=threshold,
            orientation=orientation,
            font_size=font_size
        )

        st.success("Sankey gerado com sucesso!")
        st.plotly_chart(fig, use_container_width=True)

        # Download HTML
        if export_html:
            tmp = tempfile.NamedTemporaryFile(delete=False, suffix=".html")
            tmp.close()
            fig.write_html(tmp.name)

            with open(tmp.name, "rb") as f:
                st.download_button(
                    "Descarregar HTML",
                    data=f,
                    file_name="sankeypy_output.html",
                    mime="text/html"
                )

            os.unlink(tmp.name)

    except Exception as e:
        st.error(f"Erro ao gerar Sankey: {e}")
