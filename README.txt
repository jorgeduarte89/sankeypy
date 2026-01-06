# SankeyPy

SankeyPy é uma biblioteca Python para criação de **Sankey Diagrams** de forma simples e intuitiva, com integração direta com **Pandas DataFrames**.

O objetivo da biblioteca é reduzir a complexidade normalmente associada à criação de Sankey diagrams em bibliotecas como Matplotlib ou Plotly, fornecendo uma API de alto nível orientada a dados tabulares.

Este projeto foi desenvolvido como **Projeto Final da Licenciatura em Engenharia Informática**.

---

## ✨ Principais características

- Integração direta com `pandas.DataFrame`
- API simples: `plot(df)`
- Geração automática de nós e fluxos
- Estilos configuráveis (cores, espaçamentos, labels)
- Compatível com Matplotlib
- Aplicação de demonstração com Streamlit

---

## 📦 Instalação

Clonar o repositório:

```bash
git clone https://github.com/jorgeduarte89/sankeypy.git
cd sankeypy

Estrutura:

sankeypy/
│
├── plot.py        # Função principal de visualização
├── parser.py      # Interpretação do DataFrame
├── utils.py       # Funções auxiliares
├── style.py       # Configuração visual e estilos
├── examples/      # Exemplos de utilização
│
├── app_streamlit.py   # Aplicação de demonstração



