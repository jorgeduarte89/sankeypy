import sys
import os
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..')))

from sankeypy.plot import plot
from sankeypy.utils import gerar_df_exemplo
from sankeypy.style import default_colors

df = gerar_df_exemplo()

# Exibição simples
plot(df, title="Exibição Interativa", threshold=0.05,
     colors=default_colors, orientation='h', font_size=12)

# Exportar para HTML
plot(df, title="Exportação HTML", threshold=0.05,
     colors=default_colors, orientation='h', font_size=10,
     save_as="modular_export.html")

# Exportar para PNG
plot(df, title="Exportação PNG", threshold=0.05,
     colors=default_colors, orientation='h', font_size=10,
     save_as="modular_export.png")
