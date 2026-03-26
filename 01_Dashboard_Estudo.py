import pandas as pd
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
from plotly.subplots import make_subplots

# ─── Configuração da Página ────────────────────────────────────────────────────
st.set_page_config(
    layout="wide",
    page_title="Dashboard Financeiro",
    page_icon="💰",
    initial_sidebar_state="expanded"
)

# ─── CSS Customizado ───────────────────────────────────────────────────────────
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Syne:wght@400;600;700;800&family=DM+Sans:wght@300;400;500&display=swap');

    html, body, [class*="css"] {
        font-family: 'DM Sans', sans-serif;
    }

    h1, h2, h3 {
        font-family: 'Syne', sans-serif !important;
    }

    .main { background-color: #0d0f14; }
    .block-container { padding: 2rem 2.5rem; }

    /* KPI Cards */
    .kpi-card {
        background: linear-gradient(135deg, #1a1d27 0%, #1e2130 100%);
        border: 1px solid #2a2d3e;
        border-radius: 16px;
        padding: 1.4rem 1.6rem;
        position: relative;
        overflow: hidden;
        transition: transform 0.2s;
    }
    .kpi-card:hover { transform: translateY(-3px); }
    .kpi-card::before {
        content: '';
        position: absolute;
        top: 0; left: 0; right: 0;
        height: 3px;
        border-radius: 16px 16px 0 0;
    }
    .kpi-card.red::before   { background: linear-gradient(90deg, #e63946, #ff6b6b); }
    .kpi-card.amber::before { background: linear-gradient(90deg, #f4a261, #e76f51); }
    .kpi-card.blue::before  { background: linear-gradient(90deg, #4361ee, #4cc9f0); }
    .kpi-card.green::before { background: linear-gradient(90deg, #2dc653, #80ed99); }

    .kpi-label {
        font-size: 0.72rem;
        font-weight: 500;
        letter-spacing: 0.12em;
        text-transform: uppercase;
        color: #6b7280;
        margin-bottom: 0.5rem;
    }
    .kpi-value {
        font-family: 'Syne', sans-serif;
        font-size: 1.75rem;
        font-weight: 700;
        color: #f0f2f5;
        line-height: 1.1;
    }
    .kpi-sub {
        font-size: 0.72rem;
        color: #6b7280;
        margin-top: 0.3rem;
    }

    /* Seção de Alerta */
    .insight-box {
        background: #1a1d27;
        border-left: 4px solid #e63946;
        border-radius: 0 12px 12px 0;
        padding: 1rem 1.2rem;
        margin: 0.5rem 0;
        color: #c9d1d9;
        font-size: 0.9rem;
    }
    .insight-box.warn { border-left-color: #f4a261; }
    .insight-box.info { border-left-color: #4361ee; }

    /* Sidebar */
    [data-testid="stSidebar"] {
        background: #0d0f14;
        border-right: 1px solid #1e2130;
    }
    [data-testid="stSidebar"] * { color: #c9d1d9 !important; }

    /* Divider */
    hr { border-color: #1e2130 !important; }

    /* Plotly background fix */
    .js-plotly-plot .plotly .bg { fill: transparent !important; }
</style>
""", unsafe_allow_html=True)

# ─── Carregamento dos Dados ────────────────────────────────────────────────────
@st.cache_data
def load_data():
    df = pd.read_excel('dados.xlsx')
    df.columns = df.columns.str.strip()
    df['DATA'] = pd.to_datetime(df['DATA'])
    cols = ['Valor Dívida', 'Juros', 'Correção', 'Valor Total da Dívida Corrigido']
    for c in cols:
        df[c] = pd.to_numeric(df[c], errors='coerce')
    df['Juros_R$'] = df['Valor Dívida'] * (df['Juros'] / 100)
    return df

df_raw = load_data()

# ─── Sidebar ──────────────────────────────────────────────────────────────────
with st.sidebar:
    st.markdown("## 💰 Filtros")
    st.markdown("---")

    devedores_opcoes = sorted(df_raw['DEVEDORES'].dropna().unique())
    devedor = st.multiselect("Devedor", devedores_opcoes, placeholder="Todos os devedores")

    datas = st.date_input(
        "Período",
        [df_raw['DATA'].min().date(), df_raw['DATA'].max().date()]
    )

    st.markdown("---")
    st.markdown(
        "<small style='color:#4b5563'>Dados carregados de <code>dados.xlsx</code></small>",
        unsafe_allow_html=True
    )

# ─── Aplicar Filtros ──────────────────────────────────────────────────────────
df = df_raw.copy()

if devedor:
    df = df[df['DEVEDORES'].isin(devedor)]

if len(datas) == 2:
    df = df[
        (df['DATA'] >= pd.to_datetime(datas[0])) &
        (df['DATA'] <= pd.to_datetime(datas[1]))
    ]

# ─── Paleta de Cores ──────────────────────────────────────────────────────────
DARK_BG     = "#0d0f14"
CARD_BG     = "#1a1d27"
BORDER      = "#2a2d3e"
RED         = "#e63946"
AMBER       = "#f4a261"
BLUE        = "#4361ee"
GREEN       = "#2dc653"
TEXT        = "#f0f2f5"
MUTED       = "#6b7280"

PLOTLY_LAYOUT = dict(
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font=dict(family="DM Sans", color=TEXT, size=12),
    margin=dict(l=20, r=20, t=40, b=20),
    xaxis=dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=MUTED)),
    yaxis=dict(gridcolor=BORDER, linecolor=BORDER, tickfont=dict(color=MUTED)),
    title_font=dict(family="Syne", size=15, color=TEXT),
    legend=dict(bgcolor="rgba(0,0,0,0)", font=dict(color=MUTED)),
    coloraxis_colorbar=dict(tickfont=dict(color=MUTED), title_font=dict(color=MUTED)),
)

# ─── KPIs ─────────────────────────────────────────────────────────────────────
total       = df['Valor Total da Dívida Corrigido'].sum()
total_juros = df['Juros_R$'].sum()
qtd         = df['DEVEDORES'].nunique()
ticket      = total / qtd if qtd > 0 else 0
total_corr  = df['Correção'].sum()

st.markdown("# Dashboard Financeiro")
st.markdown("<p style='color:#6b7280;margin-top:-0.8rem;margin-bottom:1.5rem;font-size:0.9rem;'>Gestão e Análise de Dívidas</p>", unsafe_allow_html=True)

k1, k2, k3, k4 = st.columns(4)

def kpi_card(col, label, value, sub, color_class):
    col.markdown(f"""
    <div class="kpi-card {color_class}">
        <div class="kpi-label">{label}</div>
        <div class="kpi-value">{value}</div>
        <div class="kpi-sub">{sub}</div>
    </div>
    """, unsafe_allow_html=True)

kpi_card(k1, "Total da Dívida", f"R$ {total:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), "Valor corrigido", "red")
kpi_card(k2, "Total de Juros", f"R$ {total_juros:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), "Calculado sobre principal", "amber")
kpi_card(k3, "Nº de Devedores", str(qtd), "Devedores únicos", "blue")
kpi_card(k4, "Ticket Médio", f"R$ {ticket:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."), "Dívida média por devedor", "green")

st.markdown("<br>", unsafe_allow_html=True)

# ─── Linha 1: Ranking + Composição ────────────────────────────────────────────
colA, colB = st.columns([3, 2])

# Ranking de devedores
df_group = df.groupby('DEVEDORES').agg(
    Principal=('Valor Dívida', 'sum'),
    Correção=('Correção', 'sum'),
    Total=('Valor Total da Dívida Corrigido', 'sum'),
    Juros_RS=('Juros_R$', 'sum')
).reset_index().sort_values('Total', ascending=True)

fig_rank = go.Figure()
fig_rank.add_trace(go.Bar(
    x=df_group['Total'],
    y=df_group['DEVEDORES'],
    orientation='h',
    marker=dict(
        color=df_group['Total'],
        colorscale=[[0, '#2a1a1c'], [0.5, '#9b2335'], [1, '#e63946']],
        showscale=False,
        line=dict(width=0),
    ),
    text=[f"R$ {v:,.0f}".replace(",", ".") for v in df_group['Total']],
    textposition='outside',
    textfont=dict(color=MUTED, size=11),
    hovertemplate="<b>%{y}</b><br>Total: R$ %{x:,.2f}<extra></extra>",
))
fig_rank.update_layout(**PLOTLY_LAYOUT, title="🏆 Ranking de Devedores", height=380)
fig_rank.update_xaxes(title=None)
fig_rank.update_yaxes(title=None)
colA.plotly_chart(fig_rank, use_container_width=True)

# Composição da dívida (donut)
comp = pd.DataFrame({
    'Categoria': ['Principal', 'Juros', 'Correção'],
    'Valor': [df['Valor Dívida'].sum(), total_juros, total_corr]
})

fig_pie = go.Figure(go.Pie(
    labels=comp['Categoria'],
    values=comp['Valor'],
    hole=0.62,
    marker=dict(colors=[RED, AMBER, BLUE]),
    textfont=dict(family="DM Sans", color=TEXT),
    hovertemplate="<b>%{label}</b><br>R$ %{value:,.2f}<br>%{percent}<extra></extra>",
))
fig_pie.update_layout(
    **{k: v for k, v in PLOTLY_LAYOUT.items() if k not in ('xaxis', 'yaxis', 'legend')},
    title="🧩 Composição da Dívida",
    height=380,
    annotations=[dict(
        text=f"<b style='font-size:14px'>R$ {total:,.0f}</b>".replace(",", "."),
        x=0.5, y=0.5, font_size=14, showarrow=False, font_color=TEXT
    )],
    legend=dict(
        orientation="h", yanchor="bottom", y=-0.15,
        xanchor="center", x=0.5,
        font=dict(color=MUTED)
    )
)
colB.plotly_chart(fig_pie, use_container_width=True)

# ─── Linha 2: Evolução Temporal + Tabela ──────────────────────────────────────
colC, colD = st.columns([3, 2])

# Evolução temporal
df_time = df.groupby('DATA').agg(
    Total=('Valor Total da Dívida Corrigido', 'sum'),
    Principal=('Valor Dívida', 'sum'),
    Juros=('Juros_R$', 'sum'),
).reset_index().sort_values('DATA')

fig_time = go.Figure()
fig_time.add_trace(go.Scatter(
    x=df_time['DATA'], y=df_time['Total'],
    name='Total Corrigido',
    line=dict(color=RED, width=2.5),
    fill='tozeroy',
    fillcolor='rgba(230,57,70,0.08)',
    mode='lines+markers',
    marker=dict(size=7, color=RED, line=dict(color=CARD_BG, width=2)),
    hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Total: R$ %{y:,.2f}<extra></extra>",
))
fig_time.add_trace(go.Scatter(
    x=df_time['DATA'], y=df_time['Principal'],
    name='Principal',
    line=dict(color=BLUE, width=1.5, dash='dot'),
    mode='lines',
    hovertemplate="<b>%{x|%d/%m/%Y}</b><br>Principal: R$ %{y:,.2f}<extra></extra>",
))
fig_time.update_layout(**PLOTLY_LAYOUT, title="📈 Evolução da Dívida", height=320)
fig_time.update_xaxes(title=None, tickformat="%b/%Y")
fig_time.update_yaxes(title=None, tickprefix="R$ ", tickformat=",.0f")
colC.plotly_chart(fig_time, use_container_width=True)

# Top devedores tabela
colD.markdown("### 📋 Top Devedores")
df_top = df_group.sort_values('Total', ascending=False).head(8)[['DEVEDORES', 'Principal', 'Juros_RS', 'Total']].copy()
df_top.columns = ['Devedor', 'Principal (R$)', 'Juros (R$)', 'Total (R$)']
for col_name in ['Principal (R$)', 'Juros (R$)', 'Total (R$)']:
    df_top[col_name] = df_top[col_name].apply(lambda x: f"R$ {x:,.2f}".replace(",", "X").replace(".", ",").replace("X", "."))
df_top = df_top.reset_index(drop=True)
colD.dataframe(df_top, use_container_width=True, hide_index=True)

st.markdown("---")

# ─── Insights Automáticos ─────────────────────────────────────────────────────
st.markdown("### 🚨 Insights Automáticos")
icols = st.columns(3)

if not df_group.empty:
    top = df_group.sort_values('Total', ascending=False).iloc[0]
    perc = (top['Total'] / total * 100) if total > 0 else 0
    icols[0].markdown(f"""
    <div class="insight-box">
        <b>Maior Devedor</b><br>
        <span style='font-size:1.05rem;color:#f0f2f5'>{top['DEVEDORES']}</span><br>
        Representa <b>{perc:.1f}%</b> da dívida total
    </div>""", unsafe_allow_html=True)

if len(df_time) > 1:
    inicio = df_time.iloc[0]['Total']
    fim    = df_time.iloc[-1]['Total']
    if inicio > 0:
        cresc = ((fim - inicio) / inicio) * 100
        sinal = "📈" if cresc >= 0 else "📉"
        icols[1].markdown(f"""
        <div class="insight-box warn">
            <b>Variação no Período</b><br>
            <span style='font-size:1.05rem;color:#f0f2f5'>{sinal} {cresc:+.1f}%</span><br>
            De R$ {inicio:,.0f} → R$ {fim:,.0f}
        </div>""".replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)

perc_juros = (total_juros / total * 100) if total > 0 else 0
icols[2].markdown(f"""
<div class="insight-box info">
    <b>Peso dos Juros</b><br>
    <span style='font-size:1.05rem;color:#f0f2f5'>{perc_juros:.1f}% do total</span><br>
    Equivale a R$ {total_juros:,.2f}
</div>""".replace(",", "X").replace(".", ",").replace("X", "."), unsafe_allow_html=True)