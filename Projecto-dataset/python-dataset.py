import pandas as pd
from datetime import datetime, timedelta
import random

# Fixar a semente aleatória para resultados 100% reproduzíveis
random.seed(42)

# ==============================================================================
# 1. BASE DE DADOS: NIELS ELECTRONICS (100 CLIENTES)
# ==============================================================================
EMPRESA = "Niels Electronics"

# Catálogo dos 10 Electrodomésticos (Preço de Venda, Custo Unitário e Stock Inicial)
catalogo = {
    "Frigorífico": {"preco": 32000, "custo": 22000, "stock_inicial": 50},
    "Smart TV 50\"": {"preco": 24500, "custo": 17500, "stock_inicial": 50},
    "Micro-ondas": {"preco": 5200, "custo": 3600, "stock_inicial": 50},
    "Máquina de Lavar": {"preco": 21000, "custo": 15000, "stock_inicial": 50},
    "Fogão a Gás": {"preco": 14500, "custo": 10000, "stock_inicial": 50},
    "Ar Condicionado": {"preco": 28000, "custo": 19000, "stock_inicial": 50},
    "Liquidificador": {"preco": 2800, "custo": 1900, "stock_inicial": 50},
    "Aspirador de Pó": {"preco": 6500, "custo": 4500, "stock_inicial": 50},
    "Ferro de Engomar": {"preco": 1800, "custo": 1200, "stock_inicial": 50},
    "Torradeira": {"preco": 2200, "custo": 1500, "stock_inicial": 50}
}
lista_produtos = list(catalogo.keys())

# Cidades de Moçambique
cidades = [
    "Maputo", "Matola", "Beira", "Nampula", "Chimoio",
    "Quelimane", "Tete", "Pemba", "Inhambane", "Xai-Xai"
]

# Lista de 100 Clientes Únicos
primeiros_nomes = [
    "Afonso", "Nelson", "João", "Maria", "Carlos", "Ana", "Fátima", "Manuel", "Tânia", "Helena",
    "Samora", "Graça", "Celso", "Isabel", "Duarte", "Benvinda", "Edmilson", "Inês", "Salomão", "Neusa",
    "Armando", "Yara", "Zacarias", "Catarina", "Eusébio", "Lurdes", "Vicente", "Alberto", "Carla", "Rui",
    "Telma", "Paulo", "Sónia", "Danilo", "Marta", "Filipe", "Aida", "Jaime", "Lucília", "Tomás",
    "Lucas", "Beatriz", "Gabriel", "Débora", "Ricardo", "Vanessa", "Jorge", "Patrícia", "Félix", "Cláudia",
    "Bernardo", "Luísa", "Artur", "Margarida", "Sérgio", "Tatiana", "Bruno", "Ivone", "Adriano", "Jéssica",
    "Leandro", "Mércia", "Mauro", "Sheila", "Valter", "Marlene", "Hermínio", "Nádia", "Gerson", "Milena",
    "Orlando", "Célia", "Alfeu", "Belmira", "Clésio", "Denise", "Elísio", "Glória", "Hilário", "Ilda",
    "Joaquim", "Kátia", "Lázaro", "Miriam", "Norberto", "Olívia", "Pascoal", "Quitéria", "Rodolfo", "Sara",
    "Teodoro", "Úrsula", "Virgílio", "Wilma", "Xavier", "Yolanda", "Zeferino", "Zuraida", "Emílio", "Amélia"
]

sobrenomes = [
    "Domingos", "Mabunda", "Sitoe", "Langa", "Cossa", "Tembe", "Matusse", "Chissano",
    "Macamo", "Nhantumbo", "Mondlane", "Guambe", "Zandamela", "Cuamba", "Simango",
    "Bila", "Chauke", "Moiane", "Matsinhe", "Mucavele"
]

clientes_100 = [f"{primeiros_nomes[i]} {sobrenomes[i % len(sobrenomes)]}" for i in range(100)]

# Distribuição temporal das 100 compras: Julho (15), Agosto (22), Setembro (28), Outubro (35)
datas_compra = (
    [datetime(2026, 7, 1) + timedelta(days=int(i * 30 / 15)) for i in range(15)] +
    [datetime(2026, 8, 1) + timedelta(days=int(i * 30 / 22)) for i in range(22)] +
    [datetime(2026, 9, 1) + timedelta(days=int(i * 29 / 28)) for i in range(28)] +
    [datetime(2026, 10, 1) + timedelta(days=int(i * 19 / 35)) for i in range(35)]
)

# Construir os 100 registos
linhas = []
for i in range(100):
    prod = lista_produtos[i % len(lista_produtos)]
    preco = catalogo[prod]["preco"]
    custo = catalogo[prod]["custo"]
    qtd = random.randint(1, 4)
    dt = datas_compra[i]

    linhas.append({
        "Empresa": EMPRESA,
        "ID_Cliente": f"CLI-{i+1:03d}",
        "Cliente": clientes_100[i],
        "Idade": random.randint(21, 59),
        "Cidade": cidades[i % len(cidades)],
        "Data": dt,
        "Data da Compra": dt.strftime("%d/%m/%Y"),
        "Produto": prod,
        "Preço Venda (MZN)": preco,
        "Custo Unitário (MZN)": custo,
        "Qtd Comprada": qtd,
        "Total Faturado (MZN)": preco * qtd,
        "Custo Total (MZN)": custo * qtd,
        "Lucro Total (MZN)": (preco - custo) * qtd,
        "Margem Lucro (%)": ((preco - custo) / preco) * 100
    })

df = pd.DataFrame(linhas)
df["Ano_Mes"] = df["Data"].dt.strftime("%Y-%m")

meses_pt = {
    "2026-07": "Julho/2026",
    "2026-08": "Agosto/2026",
    "2026-09": "Setembro/2026",
    "2026-10": "Outubro/2026"
}
df["Mês"] = df["Ano_Mes"].map(meses_pt)

# ==============================================================================
# 2. RESUMO DE STOCK POR PRODUTO
# ==============================================================================
stock_por_produto = df.groupby("Produto")["Qtd Comprada"].sum().reset_index()
stock_por_produto["Stock Inicial"] = stock_por_produto["Produto"].map(lambda p: catalogo[p]["stock_inicial"])
stock_por_produto["Stock Restante"] = stock_por_produto["Stock Inicial"] - stock_por_produto["Qtd Comprada"]

# ==============================================================================
# 3. RESPOSTAS ÀS QUESTÕES ANALÍTICAS (PAINEL GERAL)
# ==============================================================================
pd.set_option('display.max_columns', None)
pd.set_option('display.width', 1000)

print(f"=== {EMPRESA.upper()} - PAINEL ANALÍTICO COM 100 CLIENTES ===\n")
print(f"• Total de Clientes Cadastrados: {len(df)}")
print(f"• Período Analisado: {df['Data'].min().strftime('%d/%m/%Y')} a {df['Data'].max().strftime('%d/%m/%Y')}\n")

# --- 1. Produto mais vendido ---
vendas_por_produto = df.groupby("Produto")["Qtd Comprada"].sum()
faturamento_por_produto = df.groupby("Produto")["Total Faturado (MZN)"].sum()

print("1. QUAL É O PRODUTO MAIS VENDIDO / MAIS COMPRADO PELOS CLIENTES?")
print(f"   • Em Quantidade (Volume): {vendas_por_produto.idxmax()} ({vendas_por_produto.max()} unidades vendidas)")
print(f"   • Em Faturação: {faturamento_por_produto.idxmax()} ({faturamento_por_produto.max():,.2f} MZN gerados)\n")

# --- 2. Produto menos vendido ---
print("2. QUAL É O PRODUTO MENOS VENDIDO?")
print(f"   • Em Quantidade (Volume): {vendas_por_produto.idxmin()} ({vendas_por_produto.min()} unidades vendidas)")
print(f"   • Em Faturação: {faturamento_por_produto.idxmin()} ({faturamento_por_produto.min():,.2f} MZN gerados)\n")

# --- 3. Total de vendas por produto ---
print("3. QUAL É O TOTAL DE VENDAS E STOCK POR PRODUTO?")
resumo_geral_produtos = df.groupby("Produto").agg(
    Preço_Venda=("Preço Venda (MZN)", "first"),
    Custo_Unitario=("Custo Unitário (MZN)", "first"),
    Qtd_Vendida=("Qtd Comprada", "sum"),
    Faturacao_MZN=("Total Faturado (MZN)", "sum"),
    Lucro_MZN=("Lucro Total (MZN)", "sum")
).reset_index()
resumo_geral_produtos = pd.merge(resumo_geral_produtos, stock_por_produto[["Produto", "Stock Inicial", "Stock Restante"]], on="Produto")
print(resumo_geral_produtos.sort_values(by="Faturacao_MZN", ascending=False).to_string(index=False))
print()

# --- 4. Valor total das vendas por mês ---
print("4. QUAL É O VALOR TOTAL DAS VENDAS POR MÊS?")
vendas_mensais = df.groupby(["Ano_Mes", "Mês"]).agg(
    Clientes_Atendidos=("Cliente", "count"),
    Unidades_Vendidas=("Qtd Comprada", "sum"),
    Total_Faturado_MZN=("Total Faturado (MZN)", "sum"),
    Lucro_Total_MZN=("Lucro Total (MZN)", "sum")
).reset_index()

for _, row in vendas_mensais.iterrows():
    print(f"   • {row['Mês']}: {row['Total_Faturado_MZN']:,.2f} MZN | Lucro: {row['Lucro_Total_MZN']:,.2f} MZN ({row['Unidades_Vendidas']} unid., {row['Clientes_Atendidos']} clientes)")
print()

# --- 5. Em que mês a empresa vende mais? ---
mes_top = vendas_mensais.loc[vendas_mensais["Total_Faturado_MZN"].idxmax()]
print("5. EM QUE MÊS A EMPRESA VENDE MAIS?")
print(f"   • {mes_top['Mês']}, atingindo {mes_top['Total_Faturado_MZN']:,.2f} MZN faturados ({mes_top['Unidades_Vendidas']} unidades vendidas e {mes_top['Clientes_Atendidos']} clientes).\n")

# --- 6. As vendas estão a aumentar ou a diminuir? ---
vendas_mensais["Crescimento_%"] = vendas_mensais["Total_Faturado_MZN"].pct_change() * 100
print("6. AS VENDAS ESTÃO A AUMENTAR OU A DIMINUIR?")
print("   • Resposta: As vendas mostram tendência de crescimento contínuo ao longo dos meses:")
for i in range(1, len(vendas_mensais)):
    m_ant = vendas_mensais.iloc[i-1]["Mês"]
    m_atu = vendas_mensais.iloc[i]["Mês"]
    pct = vendas_mensais.iloc[i]["Crescimento_%"]
    v_ant = vendas_mensais.iloc[i-1]["Total_Faturado_MZN"]
    v_atu = vendas_mensais.iloc[i]["Total_Faturado_MZN"]
    print(f"     - De {m_ant} ({v_ant:,.2f} MZN) para {m_atu} ({v_atu:,.2f} MZN): {pct:+.1f}%")
print()

# --- 7. Produto com MAIS e MENOS lucro ---
lucro_por_prod = df.groupby("Produto")["Lucro Total (MZN)"].sum()
print("7. QUAL É O PRODUTO QUE GERA MAIS E MENOS LUCRO?")
print(f"   • MAIS LUCRO: {lucro_por_prod.idxmax()} ({lucro_por_prod.max():,.2f} MZN de lucro total)")
print(f"   • MENOS LUCRO: {lucro_por_prod.idxmin()} ({lucro_por_prod.min():,.2f} MZN de lucro total)\n")

# --- 8. Quem são os clientes que mais compram? ---
top_clientes = df.sort_values(by="Total Faturado (MZN)", ascending=False)[
    ["Cliente", "Cidade", "Produto", "Qtd Comprada", "Total Faturado (MZN)", "Data da Compra"]
]

print("8. QUEM SÃO OS CLIENTES QUE MAIS COMPRAM (TOP 5 CLIENTES VIP)?")
for i, (_, row) in enumerate(top_clientes.head(5).iterrows(), 1):
    print(f"   {i}º {row['Cliente']} ({row['Cidade']}): {row['Total Faturado (MZN)']:,.2f} MZN ({row['Qtd Comprada']}x {row['Produto']}) em {row['Data da Compra']}")

print("\n" + "=" * 90)
print(f"TOTAL GERAL FATURADO: {df['Total Faturado (MZN)'].sum():,.2f} MZN")
print(f"LUCRO LÍQUIDO GLOBAL: {df['Lucro Total (MZN)'].sum():,.2f} MZN")
print(f"TOTAL DE ITENS VENDIDOS: {df['Qtd Comprada'].sum()} unidades")
print("=" * 90)

# Visualizar as primeiras e últimas linhas do dataset
print("\n[Amostra dos 5 Primeiros Clientes do Dataset de 100 Clientes]")
print(df[["ID_Cliente", "Cliente", "Cidade", "Data da Compra", "Produto", "Qtd Comprada", "Total Faturado (MZN)"]].head(5).to_string(index=False))

print("\n[Amostra dos 5 Últimos Clientes do Dataset de 100 Clientes]")
print(df[["ID_Cliente", "Cliente", "Cidade", "Data da Compra", "Produto", "Qtd Comprada", "Total Faturado (MZN)"]].tail(5).to_string(index=False))