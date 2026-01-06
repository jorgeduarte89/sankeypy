# generate_sankey_examples.py
import pandas as pd
from sankeypy.utils import gerar_df_exemplo
from sankeypy.style import default_colors
import os, traceback

OUT = "figs"
os.makedirs(OUT, exist_ok=True)

# helpers
def save_figure(fig, png_path, html_path):
    try:
        fig.write_image(png_path)   # tenta PNG (kaleido)
        print("Saved PNG:", png_path)
    except Exception as e:
        print("PNG failed, saving HTML instead:", e)
        fig.write_html(html_path)
        print("Saved HTML:", html_path)

# Build base dataframe
df = gerar_df_exemplo()
df.to_csv("dataset_exemplo.csv", index=False)

# Exemplo 1: Sankey básico
import plotly.graph_objects as go
def fig_basic():
    all_nodes = list(set(df['source']) | set(df['target']))
    label_to_index = {label: i for i, label in enumerate(all_nodes)}
    node_colors = default_colors[:len(all_nodes)]
    while len(node_colors) < len(all_nodes):
        node_colors.append('gray')
    sankey = go.Sankey(
        node=dict(label=all_nodes, pad=15, thickness=20, color=node_colors),
        link=dict(
            source=df['source'].map(label_to_index),
            target=df['target'].map(label_to_index),
            value=df['value'],
            customdata=df[['source','target','value']].values,
            hovertemplate='source: %{customdata[0]}<br>target: %{customdata[1]}<br>value: %{customdata[2]}<extra></extra>'
        )
    )
    fig = go.Figure(data=[sankey])
    fig.update_layout(title_text="Exemplo 1 — Sankey básico")
    return fig

save_figure(fig_basic(), os.path.join(OUT,"ex1_basic.png"), os.path.join(OUT,"ex1_basic.html"))

# Exemplo 2: Threshold (aplica agrupamento)
from sankeypy.parser import validar_dataframe, agrupar_fluxos_pequenos
df2 = validar_dataframe(df.copy(), 'source', 'target', 'value')
df_after = agrupar_fluxos_pequenos(df2, 'source', 'target', 'value', threshold=0.05)

def fig_threshold():
    all_nodes = list(set(df_after['source']) | set(df_after['target']))
    label_to_index = {label: i for i, label in enumerate(all_nodes)}
    node_colors = default_colors[:len(all_nodes)]
    while len(node_colors) < len(all_nodes):
        node_colors.append('gray')
    sankey = go.Sankey(
        node=dict(label=all_nodes, pad=15, thickness=20, color=node_colors),
        link=dict(
            source=df_after['source'].map(label_to_index),
            target=df_after['target'].map(label_to_index),
            value=df_after['value'],
            customdata=df_after[['source','target','value']].values,
            hovertemplate='source: %{customdata[0]}<br>target: %{customdata[1]}<br>value: %{customdata[2]}<extra></extra>'
        )
    )
    fig = go.Figure(data=[sankey])
    fig.update_layout(title_text="Exemplo 2 — Threshold 0.05 (agrupado)")
    return fig

save_figure(fig_threshold(), os.path.join(OUT,"ex2_threshold_after.png"), os.path.join(OUT,"ex2_threshold_after.html"))

# Exemplo 3: Paleta personalizada
def fig_colors():
    all_nodes = list(set(df['source']) | set(df['target']))
    label_to_index = {label: i for i, label in enumerate(all_nodes)}
    node_colors = ['#2E8B57', '#FFD700', '#FF6347', '#1E90FF', '#D2691E'][:len(all_nodes)]
    sankey = go.Sankey(
        node=dict(label=all_nodes, pad=15, thickness=20, color=node_colors),
        link=dict(
            source=df['source'].map(label_to_index),
            target=df['target'].map(label_to_index),
            value=df['value'],
            customdata=df[['source','target','value']].values,
            hovertemplate='source: %{customdata[0]}<br>target: %{customdata[1]}<br>value: %{customdata[2]}<extra></extra>'
        )
    )
    fig = go.Figure(data=[sankey])
    fig.update_layout(title_text="Exemplo 3 — Paleta personalizada")
    return fig

save_figure(fig_colors(), os.path.join(OUT,"ex3_colors.png"), os.path.join(OUT,"ex3_colors.html"))

# Exemplo 4: Orientação vertical
def fig_vertical():
    all_nodes = list(set(df['source']) | set(df['target']))
    label_to_index = {label: i for i, label in enumerate(all_nodes)}
    sankey = go.Sankey(orientation='v',
        node=dict(label=all_nodes, pad=15, thickness=20, color=default_colors[:len(all_nodes)]),
        link=dict(
            source=df['source'].map(label_to_index),
            target=df['target'].map(label_to_index),
            value=df['value'],
            customdata=df[['source','target','value']].values,
            hovertemplate='source: %{customdata[0]}<br>target: %{customdata[1]}<br>value: %{customdata[2]}<extra></extra>'
        )
    )
    fig = go.Figure(data=[sankey])
    fig.update_layout(title_text="Exemplo 4 — Orientação vertical")
    return fig

save_figure(fig_vertical(), os.path.join(OUT,"ex4_vertical.png"), os.path.join(OUT,"ex4_vertical.html"))

# Exemplo 5: Dados inválidos
df_bad = pd.DataFrame({
    "source": ["A", None, "B"],
    "target": ["B", "C", "D"],
    "value": [10, -5, 7]
})

# validação: guarda log
try:
    validar_dataframe(df_bad, 'source', 'target', 'value')
    with open(os.path.join(OUT,"ex5_validation_log.txt"), "w") as f:
        f.write("validar_dataframe não lançou erro — linhas válidas presentes.")
except Exception as e:
    with open(os.path.join(OUT,"ex5_validation_log.txt"), "w") as f:
        f.write("VALIDATION ERROR:\\n")
        f.write(traceback.format_exc())
    print("Validation error saved to ex5_validation_log.txt")

# gerar gráfico apenas com linhas válidas
try:
    df_valid = validar_dataframe(df_bad, 'source', 'target', 'value')
    all_nodes = list(set(df_valid['source']) | set(df_valid['target']))
    label_to_index = {label: i for i, label in enumerate(all_nodes)}
    sankey = go.Sankey(
        node=dict(label=all_nodes, pad=15, thickness=20, color=default_colors[:len(all_nodes)]),
        link=dict(
            source=df_valid['source'].map(label_to_index),
            target=df_valid['target'].map(label_to_index),
            value=df_valid['value'],
            customdata=df_valid[['source','target','value']].values,
            hovertemplate='source: %{customdata[0]}<br>target: %{customdata[1]}<br>value: %{customdata[2]}<extra></extra>'
        )
    )


    fig = go.Figure(data=[sankey])
    fig.update_layout(title_text="Exemplo 5 — Dados inválidos (linhas filtradas)")
    save_figure(fig, os.path.join(OUT,"ex5_filtered.png"), os.path.join(OUT,"ex5_filtered.html"))
except Exception as e:
    print("Não foi possível gerar gráfico reduzido:", e)

df.to_csv("data/dataset_exemplo.csv", index=False)
