import streamlit as st
import pandas as pd
import plotly.express as px

# 1. Configuração da Página
st.set_page_config(
    page_title="Monitor Inteligente de Transporte Público",
    page_icon="🚌",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# 2. Estilização CSS Avançada
st.markdown("""
    <style>
    /* Reduzir espaçamentos do Streamlit para caber em uma tela */
    .block-container {
        padding-top: 1rem !important;
        padding-bottom: 0rem !important;
        max-width: 98% !important;
    }
    header {visibility: hidden;} /* Remove a barra superior padrão */
    
    /* Centralizar textos (labels) dos filtros */
    div[data-testid="stSelectbox"] label p {
        text-align: center;
        font-size: 14px;
        width: 100%;
    }

    /* Ajustes de Título e Emoji */
    .titulo-dash { 
        font-size: 40px !important; /* O !important força a mudança */
        font-weight: bold; 
        margin-bottom: 0px; 
        padding-bottom: 0px;
        display: flex;
        align-items: center;
    }
    .titulo-emoji { 
        font-size: 65px !important; 
        margin-right: 12px; 
    }
    .subtitulo-dash { font-size: 15px; opacity: 0.8; margin-top: 5px; margin-bottom: 15px;}
    
    /* Estilo dos Cards Customizados */
    .metric-card {
        background-color: var(--secondary-background-color);
        border-radius: 12px;
        padding: 15px 20px;
        display: flex;
        align-items: center;
        box-shadow: 0 4px 6px rgba(0,0,0,0.05);
        border: 1px solid rgba(128,128,128,0.2);
        margin-bottom: 10px;
    }
    .icon-wrapper {
        width: 55px;
        height: 55px;
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        font-size: 28px;
        margin-right: 15px;
    }
    
    .icon-blue { background-color: rgba(52, 152, 219, 0.2); color: #3498db; }
    .icon-red { background-color: rgba(231, 76, 60, 0.2); color: #e74c3c; }
    .icon-green { background-color: rgba(46, 204, 113, 0.2); color: #2ecc71; }
    .icon-purple { background-color: rgba(155, 89, 182, 0.2); color: #9b59b6; }
    
    .metric-info {
        display: flex;
        flex-direction: column;
    }
    .metric-label {
        font-size: 14px;
        font-weight: 600;
        opacity: 0.8;
        margin-bottom: 4px;
    }
    .metric-value {
        font-size: 26px;
        font-weight: bold;
        line-height: 1;
    }
    </style>
""", unsafe_allow_html=True)

# Função auxiliar para gerar os cards HTML
def render_card(icon, color_class, label, value):
    return f"""
    <div class="metric-card">
        <div class="icon-wrapper {color_class}">{icon}</div>
        <div class="metric-info">
            <div class="metric-label">{label}</div>
            <div class="metric-value">{value}</div>
        </div>
    </div>
    """

# 3. Carregamento dos Dados
@st.cache_data
def carregar_dados():
    return pd.read_excel("base_onibus_autonomos_cidade_alfa_refinada.xlsx")

df = carregar_dados()

# 4. Cabeçalho
col_titulo, col_data = st.columns([4, 1])
with col_titulo:
    # Trocado de <p> para <div> para garantir que o tamanho não seja bloqueado pelo Streamlit
    st.markdown('<div class="titulo-dash"><span class="titulo-emoji">🚌</span> Monitor Inteligente de Transporte Público</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitulo-dash">Cidade Alfa — Desempenho operacional e eficiência da frota</div>', unsafe_allow_html=True)
with col_data:
    st.markdown('<div style="text-align: right; font-size: 12px; margin-top: 10px; opacity: 0.7;">Última atualização<br><b>09 de set. de 2026</b></div>', unsafe_allow_html=True)

# 5. Filtros
col_f1, col_f2, col_f3, col_f4, col_f5 = st.columns(5)

with col_f1:
    filtro_linha = st.selectbox("Linha", ["Todos"] + list(df['linha'].dropna().unique()))
with col_f2:
    filtro_regiao = st.selectbox("Região", ["Todos"] + list(df['regiao'].dropna().unique()))
with col_f3:
    filtro_trafego = st.selectbox("Nível de tráfego", ["Todos"] + list(df['nivel_trafego'].dropna().unique()))
with col_f4:
    filtro_chuva = st.selectbox("Chuva", ["Todos"] + list(df['chuva'].dropna().unique()))
with col_f5:
    filtro_periodo = st.selectbox("Período do dia", ["Todos"] + list(df['periodo_dia'].dropna().unique()))

# Aplicando os filtros no DataFrame
df_filtrado = df.copy()
if filtro_linha != "Todos": df_filtrado = df_filtrado[df_filtrado['linha'] == filtro_linha]
if filtro_regiao != "Todos": df_filtrado = df_filtrado[df_filtrado['regiao'] == filtro_regiao]
if filtro_trafego != "Todos": df_filtrado = df_filtrado[df_filtrado['nivel_trafego'] == filtro_trafego]
if filtro_chuva != "Todos": df_filtrado = df_filtrado[df_filtrado['chuva'] == filtro_chuva]
if filtro_periodo != "Todos": df_filtrado = df_filtrado[df_filtrado['periodo_dia'] == filtro_periodo]

# 6. Visão Geral (Cards Customizados)
if df_filtrado.empty:
    st.warning("Nenhum dado encontrado para os filtros selecionados.")
else:
    col_k1, col_k2, col_k3, col_k4 = st.columns(4)
    
    total_viagens = len(df_filtrado)
    atraso_medio = df_filtrado['atraso_min'].mean()
    ocupacao_media = df_filtrado['ocupacao_pct'].mean()
    consumo_medio = df_filtrado['consumo_kwh_km'].mean()

    col_k1.markdown(render_card("🚌", "icon-blue", "Total de Viagens", f"{total_viagens:,.0f}".replace(",", ".")), unsafe_allow_html=True)
    col_k2.markdown(render_card("🕒", "icon-red", "Atraso Médio (min)", f"{atraso_medio:.1f}".replace(".", ",")), unsafe_allow_html=True)
    col_k3.markdown(render_card("👥", "icon-green", "Ocupação Média", f"{ocupacao_media:.1f}%".replace(".", ",")), unsafe_allow_html=True)
    col_k4.markdown(render_card("⚡", "icon-purple", "Consumo Médio (kWh/km)", f"{consumo_medio:.2f}".replace(".", ",")), unsafe_allow_html=True)

    # 7. Gráficos
    col_g1, col_g2 = st.columns(2)
    
    altura_grafico = 270 
    margem_grafico = dict(t=30, b=10, l=10, r=10)

    with col_g1:
        # Atraso Médio por Nível de Tráfego
        df_trafego = df_filtrado.groupby('nivel_trafego')['atraso_min'].mean().reset_index()
        df_trafego['ordem'] = df_trafego['nivel_trafego'].map({'Baixo': 1, 'Moderado': 2, 'Alto': 3})
        df_trafego = df_trafego.sort_values('ordem')
        
        fig1 = px.bar(
            df_trafego, x='nivel_trafego', y='atraso_min', text_auto='.1f', title="<b>Atraso Médio por Nível de Tráfego</b>",
            color='nivel_trafego', color_discrete_map={'Baixo': '#27ae60', 'Moderado': '#f1c40f', 'Alto': '#e74c3c'}
        )
        fig1.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Atraso médio (min)", height=altura_grafico, margin=margem_grafico)
        st.plotly_chart(fig1, use_container_width=True)

        # Impacto da Chuva no Atraso
        df_chuva = df_filtrado.groupby('chuva')['atraso_min'].mean().reset_index()
        fig3 = px.bar(
            df_chuva, x='chuva', y='atraso_min', text_auto='.1f', title="<b>Impacto da Chuva no Atraso</b>",
            color='chuva', color_discrete_map={'Não': '#5dade2', 'Sim': '#21618c'}
        )
        fig3.update_layout(showlegend=False, xaxis_title=None, yaxis_title="Atraso médio (min)", height=altura_grafico, margin=margem_grafico)
        st.plotly_chart(fig3, use_container_width=True)

    with col_g2:
        # Atraso Médio por Linha
        df_linha = df_filtrado.groupby('linha')['atraso_min'].mean().reset_index().sort_values('atraso_min', ascending=True)
        fig2 = px.bar(
            df_linha, y='linha', x='atraso_min', text_auto='.1f', orientation='h', title="<b>Atraso Médio por Linha</b>",
            color_discrete_sequence=['#3498db']
        )
        fig2.update_layout(xaxis_title="Atraso médio (min)", yaxis_title=None, height=altura_grafico, margin=margem_grafico)
        st.plotly_chart(fig2, use_container_width=True)

        # Status de Pontualidade (Cores estilo Semáforo)
        df_status = df_filtrado['status_pontualidade'].value_counts().reset_index()
        df_status.columns = ['Status', 'Contagem']
        
        fig4 = px.pie(
            df_status, values='Contagem', names='Status', hole=0.5, title="<b>Status de Pontualidade</b>",
            color='Status', color_discrete_map={'No horário': '#27ae60', 'Atrasada': '#f1c40f', 'Crítica': '#e74c3c'}
        )
        fig4.update_traces(textinfo='percent', textfont_size=14)
        fig4.add_annotation(text=f"<b>{total_viagens:,.0f}</b><br>viagens".replace(",", "."), x=0.5, y=0.5, font_size=16, showarrow=False)
        fig4.update_layout(height=altura_grafico, margin=margem_grafico, legend=dict(orientation="v", yanchor="middle", y=0.5, xanchor="left", x=1))
        st.plotly_chart(fig4, use_container_width=True)