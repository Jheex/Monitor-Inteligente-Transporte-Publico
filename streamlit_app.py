import streamlit as st
import pandas as pd
import plotly.express as px
import os
import io

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Monitor de Transporte Autônomo | FIAP",
    page_icon="🌌",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. INJEÇÃO DE CSS AVANÇADO (DUOTONE: AZUL & ROXO)
# ==============================================================================
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Outfit:wght@300;400;500;700;900&display=swap');

/* --- Variáveis de Tema (Apenas Azul e Roxo) --- */
:root {
    --bg-dark: #06070D;
    --card-bg: rgba(15, 17, 28, 0.6);
    --border-color: rgba(255, 255, 255, 0.08);
    --neon-blue: #00B3FF;
    --neon-purple: #7D2AE8;
    --text-main: #F8FAFC;
    --text-muted: #8B949E;
}

/* Reset Global */
html, body, [class*="css"] {
    font-family: 'Outfit', sans-serif !important;
}

.stApp {
    background-color: var(--bg-dark) !important;
    background-image: 
        radial-gradient(circle at 10% 40%, rgba(125, 42, 232, 0.06), transparent 30%),
        radial-gradient(circle at 90% 60%, rgba(0, 179, 255, 0.06), transparent 30%);
    color: var(--text-main);
}

/* --- Animações --- */
@keyframes fadeSlideUp {
    from { opacity: 0; transform: translateY(20px); }
    to { opacity: 1; transform: translateY(0); }
}

@keyframes fadeInTab {
    from { opacity: 0; filter: blur(4px); }
    to { opacity: 1; filter: blur(0); }
}

.block-container {
    padding-top: 2rem !important;
    padding-bottom: 2rem !important;
    max-width: 96% !important;
    animation: fadeSlideUp 0.8s cubic-bezier(0.16, 1, 0.3, 1);
}

#MainMenu, footer, header { visibility: hidden; }

/* --- CARDS NATIVOS (st.metric) --- */
div[data-testid="stMetric"] {
    background: var(--card-bg) !important;
    backdrop-filter: blur(12px) !important;
    -webkit-backdrop-filter: blur(12px) !important;
    border: 1px solid var(--border-color) !important;
    border-left: 4px solid var(--neon-purple) !important;
    border-radius: 16px !important;
    padding: 20px 24px !important;
    box-shadow: 0 8px 32px rgba(0, 0, 0, 0.2) !important;
    transition: all 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275) !important;
}

div[data-testid="stMetric"]:hover {
    transform: translateY(-6px) scale(1.02) !important;
    border-left: 4px solid var(--neon-blue) !important;
    box-shadow: 0 15px 35px rgba(0, 179, 255, 0.15) !important;
    border-color: rgba(0, 179, 255, 0.3) !important;
}

div[data-testid="stMetricLabel"] p {
    font-size: 13px !important;
    font-weight: 500 !important;
    text-transform: uppercase !important;
    letter-spacing: 1.2px !important;
    color: var(--text-muted) !important;
}

div[data-testid="stMetricValue"] {
    font-size: 32px !important;
    font-weight: 900 !important;
    background: -webkit-linear-gradient(45deg, #FFF, #C4B5FD);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    letter-spacing: -1px !important;
}

/* --- ABAS (st.tabs) --- */
div[data-baseweb="tab-highlight"], div[data-baseweb="tab-border"] { display: none !important; }

.stTabs [data-baseweb="tab-list"] {
    gap: 12px !important;
    background: rgba(10, 12, 20, 0.8) !important;
    padding: 8px !important;
    border-radius: 20px !important;
    border: 1px solid var(--border-color) !important;
    margin-bottom: 30px !important;
    backdrop-filter: blur(10px);
}

.stTabs [data-baseweb="tab"] {
    height: 46px !important;
    background-color: transparent !important;
    border: none !important;
    border-radius: 14px !important;
    color: var(--text-muted) !important;
    font-weight: 600 !important;
    font-size: 14px !important;
    padding: 0 24px !important;
    transition: all 0.3s ease !important;
}

.stTabs [data-baseweb="tab"]:hover {
    color: var(--text-main) !important;
    background-color: rgba(255, 255, 255, 0.05) !important;
}

.stTabs [aria-selected="true"] {
    background: linear-gradient(135deg, var(--neon-blue) 0%, var(--neon-purple) 100%) !important;
    color: #FFFFFF !important;
    box-shadow: 0 4px 20px rgba(125, 42, 232, 0.4) !important;
}

.stTabs [data-baseweb="tab-panel"] {
    animation: fadeInTab 0.6s ease-out;
}

/* --- SIDEBAR --- */
section[data-testid="stSidebar"] {
    background-color: #07080F !important;
    border-right: 1px solid var(--border-color) !important;
}

/* --- GRÁFICOS --- */
.stPlotlyChart {
    background: var(--card-bg) !important;
    backdrop-filter: blur(8px) !important;
    border: 1px solid var(--border-color) !important;
    border-radius: 20px !important;
    padding: 15px !important;
    transition: transform 0.3s ease;
}
.stPlotlyChart:hover {
    border-color: rgba(0, 179, 255, 0.4) !important;
}

/* --- BOTÕES PREMIUM --- */
div[data-testid="stDownloadButton"] button {
    background: linear-gradient(45deg, var(--neon-blue), var(--neon-purple)) !important;
    color: white !important;
    border: none !important;
    border-radius: 30px !important;
    padding: 10px 24px !important;
    font-weight: 700 !important;
    letter-spacing: 0.5px !important;
    transition: all 0.3s ease !important;
    box-shadow: 0 4px 15px rgba(125, 42, 232, 0.2) !important;
}

div[data-testid="stDownloadButton"] button:hover {
    transform: scale(1.05) translateY(-2px) !important;
    box-shadow: 0 8px 25px rgba(0, 179, 255, 0.4) !important;
}

/* Customização de Títulos */
h1 {
    font-weight: 900 !important;
    background: -webkit-linear-gradient(45deg, var(--neon-blue), var(--neon-purple));
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}
</style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. CARREGAMENTO DA BASE DE DADOS
# ==============================================================================
@st.cache_data
def carregar_dados():
    candidatos = [
        "data/processed/base_onibus_autonomos_cidade_alfa_refinada.xlsx",
        "base_onibus_autonomos_cidade_alfa_refinada.xlsx"
    ]
    caminho = next((c for c in candidatos if os.path.exists(c)), None)
    
    if not caminho:
        st.toast("⚠️ Base não encontrada. Gerando dados simulados para visualização do design.", icon="🌌")
        df_raw = pd.DataFrame({
            'linha': ['L1', 'L2', 'L1', 'L3', 'L2'] * 20,
            'regiao': ['Norte', 'Sul', 'Leste', 'Oeste', 'Centro'] * 20,
            'status_pontualidade': ['No horário', 'Atrasada', 'Crítica', 'No horário', 'No horário'] * 20,
            'atraso_min': [0, 15, 45, 0, 0] * 20,
            'tipo_falha': ['Nenhuma', 'Nenhuma', 'Motor', 'Nenhuma', 'Sensores'] * 20,
            'nivel_trafego': ['Baixo', 'Alto', 'Moderado', 'Baixo', 'Baixo'] * 20,
            'consumo_kwh_km': [1.2, 1.8, 1.5, 1.1, 1.3] * 20,
            'velocidade_media_kmh': [45, 20, 35, 50, 40] * 20,
            'ocupacao_pct': [40, 90, 70, 30, 60] * 20,
            'passageiros_transportados': [200, 450, 350, 150, 300] * 20,
            'periodo_dia': ['Manhã', 'Tarde', 'Noite', 'Manhã', 'Tarde'] * 20,
            'intervencao_humana': ['Não', 'Não', 'Sim', 'Não', 'Não'] * 20,
            'tempo_interrupcao_min': [0, 0, 25, 0, 5] * 20,
            'id_viagem': range(100),
            'id_onibus': [f"BUS-{i}" for i in range(100)]
        })
        return df_raw
        
    df_raw = pd.read_excel(caminho, sheet_name=0)
    if 'data_hora_saida' in df_raw.columns:
        df_raw['data_hora_saida'] = pd.to_datetime(df_raw['data_hora_saida'])
    return df_raw

df = carregar_dados()


# ==============================================================================
# 4. CABEÇALHO PRINCIPAL
# ==============================================================================
st.title("Monitor Inteligente de Transporte Público")
st.markdown("<p style='color: #8B949E; font-size: 1.1rem; font-weight: 300;'>Cidade Alfa — Telemetria de Frota Autônoma, Análise de SLA e Inteligência Operacional | FIAP • FASE 5</p>", unsafe_allow_html=True)
st.divider()


# ==============================================================================
# 5. FILTROS NA SIDEBAR
# ==============================================================================
st.sidebar.markdown("### 🎛️ Filtros Globais")
st.sidebar.caption("Ajuste a amostragem da análise")

filtro_linha = st.sidebar.multiselect("Linha do Ônibus", options=sorted(df['linha'].dropna().unique()))
filtro_regiao = st.sidebar.multiselect("Região Urbana", options=sorted(df['regiao'].dropna().unique()))
filtro_status = st.sidebar.multiselect("Status SLA", options=sorted(df['status_pontualidade'].dropna().unique()))

st.sidebar.divider()
st.sidebar.markdown("### 🔥 Filtro de Exceção")
apenas_falhas = st.sidebar.checkbox("Apenas Viagens com Falhas / Críticas", value=False)

if 'nivel_trafego' in df.columns:
    st.sidebar.divider()
    st.sidebar.markdown("### 🌧️ Condições Operacionais")
    filtro_trafego = st.sidebar.multiselect("Nível de Tráfego", options=sorted(df['nivel_trafego'].dropna().unique()))
else:
    filtro_trafego = []


# ==============================================================================
# 6. APLICAÇÃO DOS FILTROS
# ==============================================================================
df_filtrado = df.copy()

if apenas_falhas:
    df_filtrado = df_filtrado[
        (df_filtrado['status_pontualidade'] == 'Crítica') | 
        (df_filtrado['tipo_falha'] != 'Nenhuma')
    ]

if filtro_linha:
    df_filtrado = df_filtrado[df_filtrado['linha'].isin(filtro_linha)]
if filtro_regiao:
    df_filtrado = df_filtrado[df_filtrado['regiao'].isin(filtro_regiao)]
if filtro_status:
    df_filtrado = df_filtrado[df_filtrado['status_pontualidade'].isin(filtro_status)]
if filtro_trafego:
    df_filtrado = df_filtrado[df_filtrado['nivel_trafego'].isin(filtro_trafego)]

if df_filtrado.empty:
    st.warning("⚠️ Nenhum registro localizado para os filtros selecionados.")
    st.stop()


# ==============================================================================
# 7. RESUMO DA AMOSTRA NA SIDEBAR
# ==============================================================================
st.sidebar.divider()
st.sidebar.metric(
    label="Registros Selecionados",
    value=f"{len(df_filtrado):,}".replace(",", "."),
    delta=f"{(len(df_filtrado)/len(df))*100:.1f}% da base original"
)


# ==============================================================================
# 8. ESTRUTURA PRINCIPAL EM ABAS
# ==============================================================================
tab_operacao, tab_telemetria, tab_falhas = st.tabs([
    "📊 1. Operação & SLA",
    "⚡ 2. Telemetria & Energia",
    "🚨 3. Confiabilidade & Falhas"
])


# ------------------------------------------------------------------------------
# ABA 1: OPERAÇÃO & SLA
# ------------------------------------------------------------------------------
with tab_operacao:
    m1, m2, m3, m4 = st.columns(4)
    
    total_viagens = len(df_filtrado)
    atraso_medio = df_filtrado['atraso_min'].mean()
    pct_no_horario = (df_filtrado['status_pontualidade'] == 'No horário').mean() * 100
    qtd_criticas = (df_filtrado['status_pontualidade'] == 'Crítica').sum()

    m1.metric("Viagens Analisadas", f"{total_viagens:,}".replace(",", "."), "Volume Processado")
    m2.metric("Atraso Médio", f"{atraso_medio:.1f} min", "Desvio Global", delta_color="off")
    m3.metric("Taxa de Sucesso (SLA)", f"{pct_no_horario:.1f}%", "No Horário", delta_color="normal")
    m4.metric("Incidentes Críticos", f"{qtd_criticas}", f"{(qtd_criticas/total_viagens)*100:.1f}% da amostragem", delta_color="inverse")

    st.write("---")

    c1, c2 = st.columns(2)

    with c1:
        df_linha = df_filtrado.groupby('linha')['atraso_min'].mean().reset_index().sort_values('atraso_min', ascending=True)
        fig_linha = px.bar(
            df_linha, y='linha', x='atraso_min', text_auto='.1f', orientation='h',
            color='atraso_min', color_continuous_scale=['#00B3FF', '#7D2AE8'],
            title="⏳ Atraso Médio por Linha (minutos)"
        )
        fig_linha.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            coloraxis_showscale=False, xaxis_title="", yaxis_title="", height=360,
            font=dict(color="#F8FAFC", family="Outfit")
        )
        st.plotly_chart(fig_linha, use_container_width=True)

    with c2:
        df_status = df_filtrado['status_pontualidade'].value_counts().reset_index()
        df_status.columns = ['Status', 'Qtd']
        fig_status = px.pie(
            df_status, values='Qtd', names='Status', hole=0.6,
            color='Status',
            # Paleta de tons da nova identidade (Azul claro p/ bom, Roxo p/ crítico)
            color_discrete_map={'No horário': '#00B3FF', 'Atrasada': '#7D2AE8', 'Crítica': '#3B0086'},
            title="🎯 Distribuição de Cumprimento do SLA"
        )
        fig_status.update_traces(textinfo='percent+label', hoverinfo='label+percent+value', textfont_size=14)
        fig_status.update_layout(
            paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
            height=360, font=dict(color="#F8FAFC", family="Outfit"), showlegend=False
        )
        st.plotly_chart(fig_status, use_container_width=True)


# ------------------------------------------------------------------------------
# ABA 2: TELEMETRIA & EFICIÊNCIA ENERGÉTICA
# ------------------------------------------------------------------------------
with tab_telemetria:
    e1, e2, e3, e4 = st.columns(4)

    consumo_medio = df_filtrado['consumo_kwh_km'].mean() if 'consumo_kwh_km' in df_filtrado.columns else 0
    vel_media = df_filtrado['velocidade_media_kmh'].mean() if 'velocidade_media_kmh' in df_filtrado.columns else 0
    ocupacao_media = df_filtrado['ocupacao_pct'].mean() if 'ocupacao_pct' in df_filtrado.columns else 0
    pax_total = df_filtrado['passageiros_transportados'].sum() if 'passageiros_transportados' in df_filtrado.columns else 0

    e1.metric("Consumo Médio", f"{consumo_medio:.2f} kWh/km", "Eficiência da Bateria", delta_color="off")
    e2.metric("Velocidade Média", f"{vel_media:.1f} km/h", "Fluidez nas Vias", delta_color="off")
    e3.metric("Ocupação Média", f"{ocupacao_media:.1f}%", "Capacidade Utilizada", delta_color="off")
    e4.metric("Passageiros Transp.", f"{pax_total:,.0f}".replace(",", "."), "Volume Total", delta_color="normal")

    st.write("---")

    g1, g2 = st.columns(2)

    with g1:
        if {'ocupacao_pct', 'consumo_kwh_km', 'nivel_trafego'}.issubset(df_filtrado.columns):
            fig_scat = px.scatter(
                df_filtrado, x='ocupacao_pct', y='consumo_kwh_km', color='nivel_trafego',
                color_discrete_map={'Baixo': '#00B3FF', 'Moderado': '#7D2AE8', 'Alto': '#3B0086'},
                size='consumo_kwh_km', opacity=0.8,
                title="🔋 Consumo (kWh/km) vs Ocupação (%)"
            )
            fig_scat.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)",
                xaxis_title="Ocupação (%)", yaxis_title="Consumo (kWh/km)", height=360,
                font=dict(color="#F8FAFC", family="Outfit")
            )
            st.plotly_chart(fig_scat, use_container_width=True)

    with g2:
        if {'periodo_dia', 'consumo_kwh_km'}.issubset(df_filtrado.columns):
            df_per = df_filtrado.groupby('periodo_dia')['consumo_kwh_km'].mean().reset_index()
            fig_per = px.bar(
                df_per, x='periodo_dia', y='consumo_kwh_km', text_auto='.2f',
                color='consumo_kwh_km', color_continuous_scale=['#00B3FF', '#7D2AE8'],
                title="⏱️ Eficiência Energética por Turno"
            )
            fig_per.update_layout(
                paper_bgcolor="rgba(0,0,0,0)", plot_bgcolor="rgba(0,0,0,0)", coloraxis_showscale=False,
                xaxis_title="", yaxis_title="kWh/km", height=360,
                font=dict(color="#F8FAFC", family="Outfit")
            )
            st.plotly_chart(fig_per, use_container_width=True)


# ------------------------------------------------------------------------------
# ABA 3: CONFIABILIDADE & DIAGNÓSTICO DE FALHAS
# ------------------------------------------------------------------------------
with tab_falhas:
    f1, f2, f3 = st.columns(3)

    qtd_falhas = (df_filtrado['tipo_falha'] != 'Nenhuma').sum() if 'tipo_falha' in df_filtrado.columns else 0
    pct_intervencao = (df_filtrado['intervencao_humana'] == 'Sim').mean() * 100 if 'intervencao_humana' in df_filtrado.columns else 0
    tempo_interrupcao = df_filtrado['tempo_interrupcao_min'].mean() if 'tempo_interrupcao_min' in df_filtrado.columns else 0

    f1.metric("Ocorrências Técnicas", f"{qtd_falhas}", "Falhas Detectadas", delta_color="inverse")
    f2.metric("Intervenção Humana", f"{pct_intervencao:.1f}%", "Piloto Manual Acionado", delta_color="inverse")
    f3.metric("Downtime Médio", f"{tempo_interrupcao:.1f} min", "Tempo de Interrupção", delta_color="inverse")

    st.write("---")
    st.markdown("### 🚨 Registro Detalhado de Incidentes")
    
    cols_inc = ['id_viagem', 'id_onibus', 'linha', 'regiao', 'atraso_min', 'status_pontualidade', 'tipo_falha', 'intervencao_humana']
    cols_existentes = [c for c in cols_inc if c in df_filtrado.columns]

    df_incidentes = df_filtrado[
        (df_filtrado['status_pontualidade'] == 'Crítica') | 
        (df_filtrado['tipo_falha'] != 'Nenhuma')
    ][cols_existentes].sort_values('atraso_min', ascending=False)

    if not df_incidentes.empty:
        st.dataframe(
            df_incidentes,
            column_config={
                "id_viagem": "ID Viagem",
                "id_onibus": "ID Ônibus",
                "linha": "Linha",
                "regiao": "Região",
                "atraso_min": st.column_config.NumberColumn("Atraso", format="%d min"),
                "status_pontualidade": "Status",
                "tipo_falha": "Ocorrência",
                "intervencao_humana": "Override Manual"
            },
            use_container_width=True,
            hide_index=True,
            height=300
        )
    else:
        st.success("✅ O sistema operou de forma 100% autônoma e sem incidentes críticos no recorte selecionado.")


# ==============================================================================
# 9. CENTRAL DE EXPORTAÇÃO
# ==============================================================================
st.write("<br><br>", unsafe_allow_html=True)
st.markdown("### 📥 Central de Exportação de Dados")
st.caption(f"Base filtrada contendo {len(df_filtrado):,} linhas operacionais prontas para download.")

col_exp_1, col_exp_2 = st.columns(2)

buffer_excel = io.BytesIO()
with pd.ExcelWriter(buffer_excel, engine='openpyxl') as writer:
    df_filtrado.to_excel(writer, sheet_name='Dataset_Export', index=False)
bytes_excel = buffer_excel.getvalue()
bytes_csv = df_filtrado.to_csv(index=False).encode('utf-8-sig')

with col_exp_1:
    st.download_button(
        label="🟣 EXPORTAR RELATÓRIO EXCEL (.xlsx)",
        data=bytes_excel,
        file_name="relatorio_autonomo_fiap.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet",
        use_container_width=True
    )

with col_exp_2:
    st.download_button(
        label="🔵 EXPORTAR DATASET RAW (.csv)",
        data=bytes_csv,
        file_name="dados_autonomos_fiap.csv",
        mime="text/csv",
        use_container_width=True
    )

with st.expander("🔍 Inspecionar Base de Dados Completa"):
    st.dataframe(
        df_filtrado,
        use_container_width=True,
        hide_index=True,
        column_config={
            "ocupacao_pct": st.column_config.ProgressColumn("Ocupação", min_value=0, max_value=100, format="%d%%"),
            "atraso_min": st.column_config.NumberColumn("Atraso (min)", format="%d"),
            "consumo_kwh_km": st.column_config.NumberColumn("Consumo", format="%.2f kWh")
        } if 'ocupacao_pct' in df_filtrado.columns else None
    )