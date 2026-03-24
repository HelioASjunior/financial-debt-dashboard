import pandas as pd
import streamlit as st
import plotly.express as px

# configurações da página
st.set_page_config(layout="wide", page_title="Dashboard Financeiro")

st.title("Dashboard Financeiro - Gestão de Dívidas")

# load DATA
df = pd.read_excel('dados.xlsx')

df.columns = df.columns.str.strip()
df['DATA'] = pd.to_datetime(df['DATA'])

cols = ['Valor Dívida', 'Juros', 'Correção', 'Valor Total da Dívida Corrigido']
for c in cols:
    df[c] = pd.to_numeric(df[c], errors='coerce')

# sidebar de filtros
st.sidebar.header("Filtros")

devedor = st.sidebar.multiselect(
    "DEVEDORES",
    df['DEVEDORES'].unique()
)

DATA_range = st.sidebar.date_input(
    "Período",
    [df['DATA'].min(), df['DATA'].max()]
)

# aplicar filtros
if devedor:
    df = df[df['DEVEDORES'].isin(devedor)]

df = df[(df['DATA'] >= pd.to_datetime(DATA_range[0])) &
        (df['DATA'] <= pd.to_datetime(DATA_range[1]))]

# kpis principais
total = df['Valor Total da Dívida Corrigido'].sum()
juros = (df['Valor Dívida'] * (df['Juros'] / 100)).sum()
qtd = df['DEVEDORES'].nunique()
ticket = total / qtd if qtd > 0 else 0

col1, col2, col3, col4 = st.columns(4)

col1.metric("Total Dívida", f"R$ {total:,.2f}")
col2.metric("Juros", f"R$ {(df['Valor Dívida'] * (df['Juros'] / 100)).sum():,.2f}")
col3.metric("DEVEDORES", qtd)
col4.metric("Ticket Médio", f"R$ {ticket:,.2f}")

# layout para gráficos
colA, colB = st.columns(2)

# gráfico 1 - ranking de DEVEDORES
df_group = df.groupby('DEVEDORES').agg({
    'Valor Dívida': 'sum',
    'Correção': 'sum',
    'Valor Total da Dívida Corrigido': 'sum',
    'Juros': lambda x: (df.loc[x.index, 'Valor Dívida'] * (x / 100)).sum()
}).reset_index()
df_group = df_group.sort_values(by='Valor Total da Dívida Corrigido', ascending=False)

fig_rank = px.bar(
    df_group,
    x='DEVEDORES',
    y='Valor Total da Dívida Corrigido',
    color='Valor Total da Dívida Corrigido',
    title="Ranking de DEVEDORES",
    color_continuous_scale='reds'
)

colA.plotly_chart(fig_rank, use_container_width=True)

# gráfico 2 - evolução temporal
df_time = df.groupby('DATA')['Valor Total da Dívida Corrigido'].sum().reset_index()

fig_time = px.line(
    df_time,
    x='DATA',
    y='Valor Total da Dívida Corrigido',
    markers=True,
    title="Evolução da Dívida"
)

colB.plotly_chart(fig_time, use_container_width=True)


# gráfico 3 - composição da dívida

st.subheader("Composição da Dívida")

comp = pd.DataFrame({
    'Categoria': ['Principal', 'Juros', 'Correção'],
    'Valor': [
        df['Valor Dívida'].sum(),
        (df['Valor Dívida'] * (df['Juros'] / 100)).sum(),
        df['Correção'].sum()
    ]
})

fig_pie = px.pie(
    comp,
    names='Categoria',
    values='Valor',
    hole=0.5
)

st.plotly_chart(fig_pie, use_container_width=True)


# insights automáticos

st.subheader("Insights Automáticos")

if not df_group.empty:
    top = df_group.iloc[0]
    perc = (top['Valor Total da Dívida Corrigido'] / total) * 100 if total > 0 else 0

    st.info(f"Maior devedor: {top['DEVEDORES']} ({perc:.1f}% da dívida total)")

if len(df_time) > 1:
    crescimento = ((df_time.iloc[-1]['Valor Total da Dívida Corrigido'] -
                    df_time.iloc[0]['Valor Total da Dívida Corrigido']) /
                   df_time.iloc[0]['Valor Total da Dívida Corrigido']) * 100

    st.warning(f"Crescimento da dívida no período: {crescimento:.1f}%")