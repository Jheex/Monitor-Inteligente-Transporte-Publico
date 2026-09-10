# Monitor Inteligente de Transporte Público Autônomo
### Cidade Alfa | FIAP • Fase 5 (Data Intelligence & Analytics)

[![Streamlit App](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://streamlit.io)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?style=flat&logo=python&logoColor=white)](https://www.python.org/)
[![Pandas](https://img.shields.io/badge/Pandas-Data%20Analysis-7D2AE8?style=flat&logo=pandas&logoColor=white)](https://pandas.pydata.org/)
[![Plotly](https://img.shields.io/badge/Plotly-Visualização-00B3FF?style=flat&logo=plotly&logoColor=white)](https://plotly.com/)

---

## 🌌 Sobre o Projeto
Este projeto foi desenvolvido como parte da **Fase 5 do PBL da FIAP** pelo grupo **DataBytes**. O objetivo principal é fornecer à gestão pública da **Cidade Alfa** uma ferramenta robusta de inteligência operacional, análise estatística e monitoramento em tempo real da frota de ônibus autônomos.

O sistema analisa dados de telemetria, pontualidade (SLA), eficiência energética e ocorrência de falhas técnicas, transformando dados brutos em decisões estratégicas para os níveis **Operacional, Tático e Estratégico**.

---

## 👥 Componentes do Grupo (DataBytes)

| Componente | RM |
| :--- | :--- |
| **Jhonatan Lima Coelho** | 568758 |
| **João Torres de Brito** | 571298 |
| **Kewyn Montani Zancope** | 572535 |
| **Mariana Miyasaka Maruyama** | 571761 |
| **Thiago Rodrigues Pereira Santos** | 569234 |

---

## 🎯 Principais Dores Resolvidas
1. **Baixa Visibilidade Operacional:** Monitoramento unificado do cumprimento de rotas, velocidade média e tempos de percurso.
2. **Gestão de Atrasos e SLA:** Identificação de gargalos de pontualidade por linha, região e faixa horária.
3. **Eficiencia Energética:** Análise cruzada entre o consumo de bateria (`kWh/km`), taxa de ocupação dos veículos e condições de tráfego.
4. **Confiabilidade e Falhas:** Rastreamento de incidentes mecânicos, eletrônicos e acionamentos de intervenção humana (piloto manual).

---

## 🛠️ Arquitetura e Tecnologias
O projeto foi estruturado em etapas modulares em Python:
- **Tratamento de Dados (`01_tratativas.py`):** Limpeza de nulos, remoção de duplicidades, padronização de variáveis categóricas (tráfego, chuva) e criação de colunas derivadas.
- **Análise Estatística (`02_analises_corrigido.py`):** Estatística descritiva, testes de hipóteses (ANOVA, Teste t de Welch), correlações de Pearson/Spearman e intervalos de confiança de 95%.
- **Dashboard Interativo (`streamlit_app.py`):** Desenvolvido com Streamlit, customizado com design *Glassmorphism* em paleta Duotone (Azul e Roxo), animações CSS suaves e gráficos dinâmicos em Plotly.

---

## 📂 Estrutura do Repositório

```text
📦 monitor-inteligente-transporte-publico/
├── 📄 streamlit_app.py                      # Código principal do Dashboard interativo
├── 📄 01_tratativas.py                      # Script de preparação e qualidade de dados
├── 📄 02_analises_corrigido.py              # Script de análises estatísticas e testes de hipóteses
├── 📄 requirements.txt                      # Dependências do projeto para deploy
├── 📁 data/
│   ├── 📄 base_onibus_autonomos_cidade_alfa_dados_brutos.xlsx
│   └── 📄 base_onibus_autonomos_cidade_alfa_refinada.xlsx
└── 📄 README.md                             # Documentação do projeto