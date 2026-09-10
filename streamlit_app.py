import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
import os
import io

# ==============================================================================
# 1. CONFIGURAÇÃO DA PÁGINA
# ==============================================================================
st.set_page_config(
    page_title="Control Center | Cidade Alfa",
    page_icon="⚡",
    layout="wide",
    initial_sidebar_state="expanded"
)

# ==============================================================================
# 2. DESIGN SYSTEM & CSS CUSTOMIZADO (OBSIDIAN DARK NEON)
# ==============================================================================
st.markdown("""
    <style>
    @import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');

    /* Reset global */
    html, body, [class*="css"] {
        font-family: 'Plus Jakarta Sans', -apple-system, sans-serif !important;
    }

    .stApp {
        background-color: #090D16 !important;
        color: #F1F5F9;
    }

    .block-container {
        padding-top: 1.2rem !important;
        padding-bottom: 2rem !important;
        max-width: 95% !important;
    }

    #MainMenu, footer, header { visibility: hidden; }

    /* Barra Superior Banner */
    .hero-banner {
        background: linear-gradient(135deg, rgba(15, 23, 42, 0.9) 0%, rgba(30, 27, 75, 0.7) 100%);
        border: 1px solid rgba(99, 102, 241, 0.25);
        border-radius: 16px;
        padding: 20px 24px;
        margin-bottom: 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        box-shadow: 0 10px 25px -10px rgba(0, 0, 0, 0.5);
    }

    .hero-title {
        font-size: 22px;
        font-weight: 800;
        letter-spacing: -0.5px;
        color: #F8FAFC;
        margin: 0;
        display: flex;
        align-items: center;
        gap: 10px;
    }

    .hero-subtitle {
        font-size: 13px;
        color: #94A3B8;
        margin-top: 4px;
        font-weight: 500;
    }

    .status-badge {
        background: rgba(16, 185, 129, 0.12);
        color: #34D399;
        border: 1px solid rgba(16, 185, 129, 0.3);
        padding: 6px 14px;
        border-radius: 20px;
        font-size: 11px;
        font-weight: 700;
        letter-spacing: 0.5px;
        display: inline-flex;
        align-items: center;
        gap: 6px;
    }

    .pulse-dot {
        width: 8px;
        height: 8px;
        background-color: #10B981;
        border-radius: 50%;
        box-shadow: 0 0 8px #10B981;
    }

    /* Cards de KPI Executivos */
    .kpi-container {
        background: #111827;
        border: 1px solid #1F293D;
        border-radius: 14px;
        padding: 16px 18px;
        box-shadow: 0 4px 15px rgba(0, 0, 0, 0.2);
        transition: transform 0.2s ease, border-color 0.2s ease;
    }

    .kpi-container:hover {
        border-color: #6366F1;
        transform: translateY(-2px);
    }

    .kpi-title {
        font-size: 11px;
        font-weight: 700;
        text-transform: uppercase;
        letter-spacing: 0.8px;
        color: #64748B;
        margin-bottom: 8px;
    }

    .kpi-number {
        font-size: 28px;
        font-weight: 800;
        color: #F8FAFC;
        line-height: 1;
        letter-spacing: -0.5px;
    }

    .kpi-subtext {
        font-size: 11px;
        margin-top: 8px;
        color: #94A3B8;
        font-weight: 500;
    }

    /* Container dos Gráficos Plotly */
    .stPlotlyChart {
        background: #111827;
        border: 1px solid #1F293D;
        border-radius: 14px;
        padding: 8px;
    }

    /* Customização da Sidebar */
    section[data-testid="stSidebar"] {
        background-color: #0D131F !important;
        border-right: 1px solid #1F293D;
    }

    /* Abas */
    .stTabs [data-baseweb="tab-list"] {
        gap: 8px;
        border-bottom: 1px solid #1F293D;
    }

    .stTabs [data-baseweb="tab"] {
        height: 42px;
        background-color: #111827;
        border: 1px solid #1F293D;
        border-radius: 10px;
        color: #94A3B8;
        font-weight: 600;
        font-size: 13px;
        padding: 0 18px;
    }

    .stTabs [aria-selected="true"] {
        background: #6366F1 !important;
        color: #FFFFFF !important;
        border-color: #818CF8 !important;
    }
    </style>
""", unsafe_allow_html=True)


# ==============================================================================
# 3. CARREGAMENTO DA BASE
# ==============================================================================
@st.cache_data
def carregar_dados():
    candidatos = [
        "data/processed/base_onibus_autonomos_cidade_alfa_refinada.xlsx",
        "base_onibus_autonomos_cidade_alfa_refinada.xlsx"
    ]
    caminho = next((c for c in candidatos if os.path.exists(c)), None)
    
    if not caminho:
        st.error("❌ Base de dados não encontrada.")
        st.stop()
        
    df_raw = pd.read_excel(caminho, sheet_name=0)
    if 'data_hora_saida' in df_raw.columns:
        df_raw['data_hora_saida'] = pd.to_datetime(df_raw['data_hora_saida'])
    return df_raw

df = carregar_dados()


# ==============================================================================
# 4. CABEÇALHO HERO BANNER
# ==============================================================================
st.markdown("""
    <div class="hero-banner">
        <div>
            <div class="hero-title">⚡ Control Center • Transporte Público Autônomo</div>
            <div class="hero-subtitle">Cidade Alfa — Telemetria de Frota, Monitoramento de SLA e Contingência em Tempo Real</div>
        </div>
        <div class="status-badge">
            <div class="pulse-dot"></div> TELEMETRIA ATIVA
        </div>
    </div>
""", unsafe_allow_html=True)


# ==============================================================================
# 5. FILTROS NA BARRA LATERAL
# ==============================================================================
with st.sidebar:
    st.markdown("### 🎛️ Filtros do Painel")
    st.caption("Refine o escopo de análise")
    st.markdown("---")

    filtro_linha = st.multiselect("Linha de Ônibus", options=sorted(df['linha'].dropna().unique()))
    filtro_regiao = st.multiselect("Região Urbano", options=sorted(df['regiao'].dropna().unique()))
    filtro_status = st.multiselect("Status do SLA", options=sorted(df['status_pontualidade'].dropna().unique()))
    filtro_falha = st.multiselect("Tipo de Ocorrência", options=sorted(df['tipo_falha'].dropna().unique()))

# Aplicação dos Filtros
df_filtrado = df.copy()
if filtro_linha: df_filtrado = df_filtrado[df_filtrado['linha'].isin(filtro_linha)]
if filtro_regiao: df_filtrado = df_filtrado[df_filtrado['regiao'].isin(filtro_regiao)]
if filtro_status: df_filtrado = df_filtrado[df_filtrado['status_pontualidade'].isin(filtro_status)]
if filtro_falha: df_filtrado = df_filtrado[df_filtrado['tipo_falha'].isin(filtro_falha)]

if df_filtrado.empty:
    st.warning("Nenhum registro localizado para a combinação de filtros aplicada.")
    st.stop()


# ==============================================================================
# 6. KPIS EXECUTIVOS (4 CARDS LIMPOS)
# ==============================================================================
total_operacoes = len(df_filtrado)
atraso_medio = df_filtrado['atraso_min'].mean()
pct_no_horario = (df_filtrado['status_pontualidade'] == 'No horário').mean() * 100
qtd_falhas = (df_filtrado['tipo_falha'] != 'Nenhuma').sum()

k1, k2, k3, k4 = st.columns(4)

with k1:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Total de Viagens</div>
            <div class="kpi-number">{total_operacoes:,.0f}</div>
            <div class="kpi-subtext">Operações registradas</div>
        </div>
    """.replace(",", "."), unsafe_allow_html=True)

with k2:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Atraso Médio</div>
            <div class="kpi-number" style="color: #F87171;">{atraso_medio:.1f} <span style="font-size:16px; color:#94A3B8;">min</span></div>
            <div class="kpi-subtext">Desvio em relação ao programado</div>
        </div>
    """, unsafe_allow_html=True)

with k3:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Cumprimento de SLA</div>
            <div class="kpi-number" style="color: #34D399;">{pct_no_horario:.1f}%</div>
            <div class="kpi-subtext">Viagens estritamente no horário</div>
        </div>
    """, unsafe_allow_html=True)

with k4:
    st.markdown(f"""
        <div class="kpi-container">
            <div class="kpi-title">Ocorrências Técnicas</div>
            <div class="kpi-number" style="color: #FBBF24;">{qtd_falhas}</div>
            <div class="kpi-subtext">{(qtd_falhas/total_operacoes)*100:.1f}% de taxa de incidência</div>
        </div>
    """, unsafe_allow_html=True)

st.markdown("<br>", unsafe_allow_html=True)


# ==============================================================================
# 7. HELPER DE ESTILIZAÇÃO DO PLOTLY
# ==============================================================================
def estilizar_grafico(fig, titulo=""):
    fig.update_layout(
        title=dict(text=f"<b>{titulo}</b>", font=dict(size=14, color="#F8FAFC")),
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        margin=dict(t=40, b=25, l=15, r=15),
        font=dict(color="#94A3B8"),
        xaxis=dict(showgrid=False, zeroline=False, tickfont=dict(color="#94A3B8")),
        yaxis=dict(showgrid=True, gridcolor="#1F293D", zeroline=False, tickfont=dict(color="#94A3B8")),
        legend=dict(font=dict(color="#F8FAFC"))
    )
    return fig


# ==============================================================================
# 8. ESTRUTURA PRINCIPAL EM 2 ABAS OBJETIVAS
# ==============================================================================
tab_operacao, tab_frota = st.tabs([
    "🚨 Central de Contingência & Diagnóstico",
    "🚌 Raio-X da Frota & Telemetria"
])


# ------------------------------------------------------------------------------
# TAB 1: CENTRAL DE CONTINGÊNCIA & DIAGNÓSTICO
# ------------------------------------------------------------------------------
with tab_operacao:
    col_tb, col_chart = st.columns([1.3, 1])

    with col_tb:
        st.markdown("#### 🚨 Feed de Viagens Críticas")
        st.caption("Ocorrências ordenadas por maior tempo de atraso ou falha mecânica/sensor")
        
        cols_exibir = ['id_viagem', 'id_onibus', 'linha', 'regiao', 'atraso_min', 'status_pontualidade', 'tipo_falha', 'ocupacao_pct']
        df_incidentes = df_filtrado[
            (df_filtrado['status_pontualidade'] == 'Crítica') | 
            (df_filtrado['tipo_falha'] != 'Nenhuma') |
            (df_filtrado['atraso_min'] > 15)
        ][cols_exibir].sort_values('atraso_min', ascending=False)

        if not df_incidentes.empty:
            st.dataframe(
                df_incidentes,
                column_config={
                    "id_viagem": "ID",
                    "id_onibus": "Ônibus",
                    "linha": "Linha",
                    "regiao": "Região",
                    "atraso_min": st.column_config.NumberColumn("Atraso", format="%d min"),
                    "status_pontualidade": "Status SLA",
                    "tipo_falha": "Ocorrência",
                    "ocupacao_pct": st.column_config.ProgressColumn("Ocupação", min_value=0, max_value=100, format="%d%%")
                },
                use_container_width=True,
                hide_index=True,
                height=350
            )
        else:
            st.success("✅ Nenhuma viagem crítica identificada nos parâmetros atuais.")

    with col_chart:
        df_linha = df_filtrado.groupby('linha')['atraso_min'].mean().reset_index().sort_values('atraso_min', ascending=True)
        fig_linha = px.bar(
            df_linha, y='linha', x='atraso_min', text_auto='.1f', orientation='h',
            color='atraso_min', color_continuous_scale=['#6366F1', '#EF4444']
        )
        fig_linha = estilizar_grafico(fig_linha, "Atraso Médio por Linha (minutos)")
        fig_linha.update_layout(coloraxis_showscale=False, xaxis_title=None, yaxis_title=None, height=350)
        st.plotly_chart(fig_linha, use_container_width=True)


# ------------------------------------------------------------------------------
# TAB 2: RAIO-X DA FROTA & TELEMETRIA
# ------------------------------------------------------------------------------
with tab_frota:
    f1, f2 = st.columns(2)

    with f1:
        df_falha_cat = df_filtrado['tipo_falha'].value_counts().reset_index()
        df_falha_cat.columns = ['Tipo de Falha', 'Total']
        fig_falha = px.bar(
            df_falha_cat, x='Tipo de Falha', y='Total', text_auto=True,
            color_discrete_sequence=['#818CF8']
        )
        fig_falha = estilizar_grafico(fig_falha, "Frequência por Tipo de Falha Registrar")
        fig_falha.update_layout(xaxis_title=None, yaxis_title=None, height=320)
        st.plotly_chart(fig_falha, use_container_width=True)

    with f2:
        fig_scatter = px.scatter(
            df_filtrado, x='ocupacao_pct', y='consumo_kwh_km', color='nivel_trafego',
            color_discrete_map={'Baixo': '#34D399', 'Moderado': '#FBBF24', 'Alto': '#F87171'}
        )
        fig_scatter = estilizar_grafico(fig_scatter, "Consumo Energético (kWh/km) vs Taxa de Ocupação (%)")
        fig_scatter.update_layout(xaxis_title="Ocupação (%)", yaxis_title="Consumo (kWh/km)", height=320)
        st.plotly_chart(fig_scatter, use_container_width=True)


# ==============================================================================
# 9. EXPORTAÇÃO
# ==============================================================================
st.markdown("<br>", unsafe_allow_html=True)
with st.expander("📥 Consultar Tabela Completa e Exportar Relatório"):
    buffer = io.BytesIO()
    with pd.ExcelWriter(buffer, engine='openpyxl') as writer:
        df_filtrado.to_excel(writer, sheet_name='Dados_Filtrados', index=False)
    
    st.download_button(
        label="📄 Baixar Base em Excel (.xlsx)",
        data=buffer.getvalue(),
        file_name="relatorio_cidade_alfa.xlsx",
        mime="application/vnd.openxmlformats-officedocument.spreadsheetml.sheet"
    )
    st.dataframe(df_filtrado, use_container_width=True, hide_index=True)