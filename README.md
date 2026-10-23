# Niels Electronics — Dataset & Commercial Analytics

Sistema de Gestão Comercial, Controlo de Stock e Análise de Vendas da **Niels Electronics** desenvolvido em Python com Pandas, Plotly e Interface Web HTML interativa com tema duplo (Claro / Escuro).

---

## 📌 Conteúdo do Projeto

* **`Projecto-dataset/python-dataset.py`**: Script principal com a base de dados de 100 clientes, catálogo de 10 electrodomésticos, controlo de stock e respostas automatizadas a todas as questões de negócio (produto mais/menos vendido, mês com maior faturação, tendências de vendas, lucratividade e ranking VIP de clientes).
* **`Projecto-dataset/dados.json`**: Base de dados estruturada em formato JSON.
* **`Projecto-dataset/gerar_html.py`**: Gerador do painel web interativo (`index.html`).
* **`Projecto-dataset/gerar_graficos_plotly.py`**: Gerador dos gráficos analíticos interativos usando Plotly.
* **`index.html`**: Painel comercial completo com KPIs, respostas de negócio, gráficos interativos Plotly, controlo de stock, tabela com pesquisa em tempo real, filtros por cidade/mês e exportação para CSV.
* **`graficos_interativos.html`**: Vista expandida das visualizações analíticas interativas (Evolução Mensal, Rentabilidade, Balanço de Stock, Penetração Geográfica e Dispersão Demográfica).
* **`2-INSTALAÇÃO E CONFIGURAÇÃO DO AMBIENTE.pdf`**: Material didático de apoio para configuração do ambiente de Data Science.

---

## 🚀 Tecnologias Utilizadas

* **Python 3**
* **Pandas**: Manipulação e análise estruturada de dados.
* **Plotly**: Visualizações e gráficos analíticos interativos.
* **HTML5, Tailwind CSS & JavaScript**: Interface web minimalista com tema duplo (Preto / Branco) e exportação de relatórios.

---

## 💻 Como Executar

### 1. Instalar as dependências
```bash
pip install pandas plotly
```

### 2. Executar a análise de dados no terminal
```bash
python Projecto-dataset/python-dataset.py
```

### 3. Gerar/Atualizar a interface e gráficos
```bash
python Projecto-dataset/gerar_html.py
python Projecto-dataset/gerar_graficos_plotly.py
```

### 4. Visualizar o Painel
Basta abrir o ficheiro `index.html` ou `graficos_interativos.html` no seu navegador (Google Chrome, Microsoft Edge, Firefox, etc.).
