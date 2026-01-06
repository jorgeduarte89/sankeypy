import plotly.graph_objects as go
import pandas as pd
from .parser import validar_dataframe, agrupar_fluxos_pequenos

def plot(df, source='source', target='target', value='value',
         title=None, threshold=None,
         colors=None, orientation='h', font_size=10,
         save_as=None):
    """
    Gera um Sankey Diagram com personalização visual e exportação opcional.
    """

    df = validar_dataframe(df, source, target, value)
    df = agrupar_fluxos_pequenos(df, source, target, value, threshold)

    all_nodes = list(set(df[source]) | set(df[target]))
    label_to_index = {label: i for i, label in enumerate(all_nodes)}

    node_colors = None
    if colors:
        node_colors = colors[:len(all_nodes)]
        while len(node_colors) < len(all_nodes):
            node_colors.append('gray')

    sankey_data = go.Sankey(
        orientation=orientation,
        node=dict(
            label=all_nodes,
            pad=15,
            thickness=20,
            color=node_colors
        ),
        link=dict(
            source=df[source].map(label_to_index),
            target=df[target].map(label_to_index),
            value=df[value],
            customdata=df[[source, target, value]].values,
            hovertemplate='source: %{customdata[0]}<br>target: %{customdata[1]}<br>value: %{customdata[2]}<extra></extra>'
        )
    )

    fig = go.Figure(data=[sankey_data])
    fig.update_layout(
        title_text=title or "Sankey Diagram",
        font_size=font_size,
        hoverlabel=dict(namelength=-1)
    )

    if save_as:
        if save_as.endswith(".html"):
            fig.write_html(save_as)
            print(f"[✔] Gráfico exportado para {save_as}")
        elif save_as.endswith((".png", ".jpg", ".jpeg", ".svg", ".pdf")):
            try:
                fig.write_image(save_as)
                print(f"[✔] Imagem exportada para {save_as}")
            except Exception as e:
                print(f"[✖] Falha na exportação para imagem: {e}")
        else:
            print("[!] Extensão de ficheiro não suportada para exportação.")
    else:
        fig.show()
