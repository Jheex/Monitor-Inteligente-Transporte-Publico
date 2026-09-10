# -*- coding: utf-8 -*-

# ============================================================
# FASE 5 - PBL
# MONITOR INTELIGENTE DE TRANSPORTE PÚBLICO
#
# 1º DESAFIO - PREPARAÇÃO E QUALIDADE DOS DADOS
# ============================================================

# ============================================================
# 1. IMPORTAÇÃO DAS BIBLIOTECAS
# ============================================================

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt

print("Bibliotecas carregadas com sucesso!")


# ============================================================
# 2. UPLOAD DO ARQUIVO
# ============================================================

print("Selecione o arquivo Excel da base.")

arquivo = input("Caminho do arquivo: ").strip().strip('"')

print()
print("Arquivo selecionado:", arquivo)


# ============================================================
# 3. LEITURA DA BASE
# ============================================================

df = pd.read_excel(
    arquivo,
    sheet_name="Base_Viagens"
)

print("Base carregada com sucesso!")


# ============================================================
# 4. CONHECENDO A BASE
# ============================================================

print("\n==============================")
print("PRIMEIROS REGISTROS")
print("==============================")

print(df.head())


print("\n==============================")
print("DIMENSÃO DA BASE")
print("==============================")

print("Linhas:", df.shape[0])
print("Colunas:", df.shape[1])


print("\n==============================")
print("NOMES DAS COLUNAS")
print("==============================")

print(df.columns.tolist())


print("\n==============================")
print("INFORMAÇÕES DA BASE")
print("==============================")

df.info()


# ============================================================
# 5. VERIFICAÇÃO DE VALORES NULOS
# ============================================================

print("\n==============================")
print("VALORES NULOS")
print("==============================")

nulos_antes = df.isnull().sum()

print(nulos_antes)

print("\nTotal de valores nulos:",
      df.isnull().sum().sum())


# ============================================================
# 6. VERIFICAÇÃO DE DUPLICIDADES
# ============================================================

print("\n==============================")
print("REGISTROS DUPLICADOS")
print("==============================")

duplicados_antes = df.duplicated().sum()

print("Quantidade de registros duplicados:",
      duplicados_antes)


# ============================================================
# 7. ESTATÍSTICA DESCRITIVA INICIAL
# ============================================================

print("\n==============================")
print("ESTATÍSTICA DESCRITIVA")
print("==============================")

print(df.describe())


# ============================================================
# 8. VERIFICAÇÃO DAS CATEGORIAS
# ============================================================

print("\n==============================")
print("CATEGORIAS - NÍVEL DE TRÁFEGO")
print("==============================")

print(df["nivel_trafego"].value_counts(dropna=False))


print("\n==============================")
print("CATEGORIAS - CHUVA")
print("==============================")

print(df["chuva"].value_counts(dropna=False))


print("\n==============================")
print("CATEGORIAS - INTERVENÇÃO HUMANA")
print("==============================")

print(df["intervencao_humana"].value_counts(dropna=False))


print("\n==============================")
print("CATEGORIAS - TIPO DE FALHA")
print("==============================")

print(df["tipo_falha"].value_counts(dropna=False))


# ============================================================
# 9. INÍCIO DAS TRATATIVAS
# ============================================================

print("\n\n############################################")
print("# INÍCIO DAS TRATATIVAS")
print("############################################")


# ============================================================
# 10. PADRONIZAÇÃO DOS NOMES DAS COLUNAS
# ============================================================

df.columns = (
    df.columns
    .str.strip()
    .str.lower()
    .str.replace(" ", "_")
)

print("\nNomes das colunas padronizados.")


# ============================================================
# 11. LIMPEZA DE ESPAÇOS DOS CAMPOS DE TEXTO
# ============================================================

colunas_texto = df.select_dtypes(
    include=["object", "string"]
).columns

for coluna in colunas_texto:

    df[coluna] = (
        df[coluna]
        .astype("string")
        .str.strip()
    )

print("Espaços extras removidos dos campos de texto.")


# ============================================================
# 12. PADRONIZAÇÃO DE CATEGORIAS
# ============================================================

# Nível de tráfego
if "nivel_trafego" in df.columns:

    df["nivel_trafego"] = (
        df["nivel_trafego"]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace({
            "baixo": "Baixo",
            "moderado": "Moderado",
            "alto": "Alto"
        })
    )


# Chuva
if "chuva" in df.columns:

    df["chuva"] = (
        df["chuva"]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace({
            "sim": "Sim",
            "nao": "Não",
            "não": "Não"
        })
    )


# Intervenção humana
if "intervencao_humana" in df.columns:

    df["intervencao_humana"] = (
        df["intervencao_humana"]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace({
            "sim": "Sim",
            "nao": "Não",
            "não": "Não"
        })
    )


# Viagem concluída
if "viagem_concluida" in df.columns:

    df["viagem_concluida"] = (
        df["viagem_concluida"]
        .astype("string")
        .str.strip()
        .str.lower()
        .replace({
            "sim": "Sim",
            "nao": "Não",
            "não": "Não"
        })
    )


print("Categorias padronizadas.")


# ============================================================
# 13. CONVERSÃO DE COLUNAS NUMÉRICAS
# ============================================================

colunas_numericas = [
    "tempo_previsto_min",
    "tempo_real_min",
    "atraso_min",
    "distancia_km",
    "numero_paradas",
    "velocidade_media_kmh",
    "capacidade_passageiros",
    "passageiros_transportados",
    "ocupacao_pct",
    "consumo_energia_kwh",
    "consumo_kwh_km",
    "tempo_interrupcao_min"
]

for coluna in colunas_numericas:

    if coluna in df.columns:

        # Converte vírgula decimal para ponto
        df[coluna] = (
            df[coluna]
            .astype("string")
            .str.replace(",", ".", regex=False)
        )

        df[coluna] = pd.to_numeric(
            df[coluna],
            errors="coerce"
        )


print("Colunas numéricas convertidas.")


# ============================================================
# 14. CONVERSÃO DE DATA E HORA
# ============================================================

colunas_data = [
    "data_hora_saida",
    "data_hora_chegada"
]

for coluna in colunas_data:

    if coluna in df.columns:

        df[coluna] = pd.to_datetime(
            df[coluna],
            errors="coerce",
            format="mixed"
        )

print("Datas e horários padronizados.")


# ============================================================
# 15. TRATAMENTO DOS REGISTROS DUPLICADOS
# ============================================================

print("\n==============================")
print("TRATAMENTO DE DUPLICIDADES")
print("==============================")

print(
    "Duplicados antes:",
    df.duplicated().sum()
)

df = df.drop_duplicates().reset_index(drop=True)

print(
    "Duplicados depois:",
    df.duplicated().sum()
)


# ============================================================
# 16. TRATAMENTO DOS VALORES INVÁLIDOS
# ============================================================

print("\n==============================")
print("TRATAMENTO DE VALORES INVÁLIDOS")
print("==============================")


# Tempo previsto não pode ser zero ou negativo
if "tempo_previsto_min" in df.columns:

    invalidos_tempo = (
        df["tempo_previsto_min"] <= 0
    ).sum()

    print(
        "Registros com tempo previsto inválido:",
        invalidos_tempo
    )

    df = df[
        df["tempo_previsto_min"] > 0
    ]


# Tempo real não pode ser zero ou negativo
if "tempo_real_min" in df.columns:

    invalidos_real = (
        df["tempo_real_min"] <= 0
    ).sum()

    print(
        "Registros com tempo real inválido:",
        invalidos_real
    )

    df = df[
        df["tempo_real_min"] > 0
    ]


# Distância precisa ser positiva
if "distancia_km" in df.columns:

    invalidos_distancia = (
        df["distancia_km"] <= 0
    ).sum()

    print(
        "Registros com distância inválida:",
        invalidos_distancia
    )

    df = df[
        df["distancia_km"] > 0
    ]


# Número de passageiros não pode ser negativo
if "passageiros_transportados" in df.columns:

    invalidos_passageiros = (
        df["passageiros_transportados"] < 0
    ).sum()

    print(
        "Registros com passageiros inválidos:",
        invalidos_passageiros
    )

    df = df[
        df["passageiros_transportados"] >= 0
    ]


print("Valores inválidos tratados.")


# ============================================================
# 17. TRATAMENTO DOS VALORES NULOS
# ============================================================

print("\n==============================")
print("TRATAMENTO DOS VALORES NULOS")
print("==============================")


# Como no exemplo oficial do PBL,
# categorizamos a região não informada.

if "regiao" in df.columns:

    nulos_regiao = df["regiao"].isnull().sum()

    print(
        "Nulos em região antes:",
        nulos_regiao
    )

    df["regiao"] = (
        df["regiao"]
        .fillna("Não Informado")
    )

    print(
        "Nulos em região depois:",
        df["regiao"].isnull().sum()
    )


# Para categorias de falha, podemos usar "Não Informado"
if "tipo_falha" in df.columns:

    df["tipo_falha"] = (
        df["tipo_falha"]
        .fillna("Não Informado")
    )


print("Tratamento de valores nulos concluído.")


# ============================================================
# 18. VALIDAÇÃO DA OCUPAÇÃO
# ============================================================

print("\n==============================")
print("VALIDAÇÃO DA OCUPAÇÃO")
print("==============================")


if {
    "passageiros_transportados",
    "capacidade_passageiros"
}.issubset(df.columns):

    df["ocupacao_calculada_pct"] = (
        df["passageiros_transportados"]
        /
        df["capacidade_passageiros"]
    ) * 100

    df["diferenca_ocupacao_pct"] = (
        df["ocupacao_pct"]
        -
        df["ocupacao_calculada_pct"]
    )

    df["ocupacao_calculada_pct"] = (
        df["ocupacao_calculada_pct"]
        .round(2)
    )

    df["diferenca_ocupacao_pct"] = (
        df["diferenca_ocupacao_pct"]
        .round(2)
    )

    print("Indicador de ocupação calculada criado.")


# ============================================================
# 19. VALIDAÇÃO DO ATRASO
# ============================================================

print("\n==============================")
print("VALIDAÇÃO DO ATRASO")
print("==============================")


if {
    "tempo_real_min",
    "tempo_previsto_min"
}.issubset(df.columns):

    df["atraso_calculado_min"] = (
        df["tempo_real_min"]
        -
        df["tempo_previsto_min"]
    )

    df["atraso_calculado_min"] = (
        df["atraso_calculado_min"]
        .round(2)
    )

    if "atraso_min" in df.columns:

        df["diferenca_atraso_min"] = (
            df["atraso_min"]
            -
            df["atraso_calculado_min"]
        ).round(2)

    print("Indicador de atraso calculado criado.")


# ============================================================
# 20. INDICADORES DE DESEMPENHO
# ============================================================

print("\n==============================")
print("CRIAÇÃO DE INDICADORES")
print("==============================")


# Desvio percentual do tempo de viagem
if {
    "tempo_real_min",
    "tempo_previsto_min"
}.issubset(df.columns):

    df["desvio_tempo_pct"] = (
        (
            df["tempo_real_min"]
            -
            df["tempo_previsto_min"]
        )
        /
        df["tempo_previsto_min"]
    ) * 100

    df["desvio_tempo_pct"] = (
        df["desvio_tempo_pct"]
        .round(2)
    )


# Falha ocorreu
if "tipo_falha" in df.columns:

    df["falha_ocorreu"] = np.where(
        df["tipo_falha"]
        .astype("string")
        .str.lower()
        .eq("nenhuma"),
        "Não",
        "Sim"
    )


# Interrupção ocorreu
if "tempo_interrupcao_min" in df.columns:

    df["interrupcao_ocorreu"] = np.where(
        df["tempo_interrupcao_min"] > 0,
        "Sim",
        "Não"
    )


# Viagem concluída em formato binário
if "viagem_concluida" in df.columns:

    df["viagem_concluida_bin"] = np.where(
        df["viagem_concluida"] == "Sim",
        1,
        0
    )


# Intervenção humana em formato binário
if "intervencao_humana" in df.columns:

    df["intervencao_humana_bin"] = np.where(
        df["intervencao_humana"] == "Sim",
        1,
        0
    )


# Consumo energético por passageiro
if {
    "consumo_energia_kwh",
    "passageiros_transportados"
}.issubset(df.columns):

    df["consumo_kwh_por_passageiro"] = np.where(
        df["passageiros_transportados"] > 0,
        df["consumo_energia_kwh"]
        /
        df["passageiros_transportados"],
        np.nan
    )

    df["consumo_kwh_por_passageiro"] = (
        df["consumo_kwh_por_passageiro"]
        .round(3)
    )


print("Indicadores derivados criados.")


# ============================================================
# 21. INDICADORES DE DATA E PERÍODO
# ============================================================

if "data_hora_saida" in df.columns:

    df["data"] = (
        df["data_hora_saida"]
        .dt.date
    )

    df["hora_saida"] = (
        df["data_hora_saida"]
        .dt.hour
    )

    df["dia_semana"] = (
        df["data_hora_saida"]
        .dt.day_name()
    )

    # Traduzir dias da semana para português
    df["dia_semana"] = (
        df["dia_semana"]
        .replace({
            "Monday": "Segunda-feira",
            "Tuesday": "Terça-feira",
            "Wednesday": "Quarta-feira",
            "Thursday": "Quinta-feira",
            "Friday": "Sexta-feira",
            "Saturday": "Sábado",
            "Sunday": "Domingo"
        })
    )

    df["fim_de_semana"] = np.where(
        df["data_hora_saida"].dt.dayofweek >= 5,
        "Sim",
        "Não"
    )

    df["periodo_dia"] = pd.cut(
        df["hora_saida"],
        bins=[-1, 5, 11, 17, 23],
        labels=[
            "Madrugada",
            "Manhã",
            "Tarde",
            "Noite"
        ]
    )

    print("Indicadores temporais criados.")


# ============================================================
# 22. ORDENAÇÃO DA BASE
# ============================================================

if "id_viagem" in df.columns:

    df = df.sort_values(
        by="id_viagem"
    )


df = df.reset_index(drop=True)


# ============================================================
# 23. VERIFICAÇÃO FINAL DE QUALIDADE
# ============================================================

print("\n\n############################################")
print("# VERIFICAÇÃO FINAL")
print("############################################")


print("\n==============================")
print("DIMENSÃO FINAL")
print("==============================")

print("Linhas:", df.shape[0])
print("Colunas:", df.shape[1])


print("\n==============================")
print("NULOS APÓS O TRATAMENTO")
print("==============================")

print(df.isnull().sum())


print("\nTotal de valores nulos:",
      df.isnull().sum().sum())


print("\n==============================")
print("DUPLICIDADES APÓS O TRATAMENTO")
print("==============================")

print(
    "Duplicados:",
    df.duplicated().sum()
)


print("\n==============================")
print("ESTATÍSTICA DESCRITIVA FINAL")
print("==============================")

print(df.describe())


# ============================================================
# 24. VERIFICAR AS PRINCIPAIS CATEGORIAS
# ============================================================

print("\n==============================")
print("NÍVEL DE TRÁFEGO")
print("==============================")

print(
    df["nivel_trafego"]
    .value_counts(dropna=False)
)


print("\n==============================")
print("STATUS DE PONTUALIDADE")
print("==============================")

print(
    df["status_pontualidade"]
    .value_counts(dropna=False)
)


print("\n==============================")
print("TIPO DE FALHA")
print("==============================")

print(
    df["tipo_falha"]
    .value_counts(dropna=False)
)


# ============================================================
# 25. RELATÓRIO DE QUALIDADE
# ============================================================

relatorio_qualidade = pd.DataFrame({
    "coluna": df.columns,
    "tipo": [
        str(df[col].dtype)
        for col in df.columns
    ],
    "registros_preenchidos": [
        int(df[col].notna().sum())
        for col in df.columns
    ],
    "valores_nulos": [
        int(df[col].isnull().sum())
        for col in df.columns
    ],
    "percentual_nulos": [
        round(
            df[col].isnull().mean() * 100,
            2
        )
        for col in df.columns
    ],
    "valores_unicos": [
        int(df[col].nunique(dropna=True))
        for col in df.columns
    ]
})


# ============================================================
# 26. EXPORTAR A BASE REFINADA
# ============================================================

nome_saida = (
    "base_onibus_autonomos_cidade_alfa_refinada.xlsx"
)

with pd.ExcelWriter(
    nome_saida,
    engine="openpyxl"
) as writer:

    # Base principal refinada
    df.to_excel(
        writer,
        sheet_name="Base_Refinada",
        index=False
    )

    # Relatório de qualidade
    relatorio_qualidade.to_excel(
        writer,
        sheet_name="Qualidade_Dados",
        index=False
    )

print("\n==============================")
print("EXPORTAÇÃO")
print("==============================")

print(
    "Arquivo gerado:",
    nome_saida
)


# ============================================================
# 27. DOWNLOAD DO ARQUIVO
# ============================================================

print("\nProcesso concluído!")
print("A base refinada está pronta para o 2º Desafio.")