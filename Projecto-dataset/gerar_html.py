import json
import os

# Carregar dados preparados
with open('Projecto-dataset/dados.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

clientes_json = json.dumps(data['clientes'], ensure_ascii=False)
produtos_json = json.dumps(data['produtos'], ensure_ascii=False)
mensal_json = json.dumps(data['mensal'], ensure_ascii=False)

html_template = f"""<!DOCTYPE html>
<html lang="pt" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Niels Electronics — Painel Comercial & Analytics</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    /* Transições suaves ao alternar o tema */
    body, .theme-card, .theme-input, .theme-border, table, tr, th, td {{
      transition: background-color 0.25s ease, color 0.25s ease, border-color 0.25s ease;
    }}

    /* TEMA ESCURO (PRETO) */
    html.dark body {{
      background-color: #000000;
      color: #ffffff;
    }}
    html.dark .theme-header {{
      background-color: #09090b;
      border-color: #27272a;
    }}
    html.dark .theme-card {{
      background-color: #09090b;
      border-color: #27272a;
      color: #ffffff;
    }}
    html.dark .theme-subcard {{
      background-color: #121215;
      border-color: #27272a;
    }}
    html.dark .theme-input {{
      background-color: #000000;
      border-color: #27272a;
      color: #ffffff;
    }}
    html.dark .theme-input:focus {{
      border-color: #ffffff;
    }}
    html.dark .theme-muted {{
      color: #a1a1aa;
    }}
    html.dark .theme-border {{
      border-color: #27272a;
    }}
    html.dark .theme-th {{
      background-color: #09090b;
      color: #a1a1aa;
      border-color: #27272a;
    }}
    html.dark .theme-tr:hover {{
      background-color: #18181b;
    }}
    html.dark .theme-td-border {{
      border-color: #1c1c20;
    }}
    html.dark .theme-btn-primary {{
      background-color: #ffffff;
      color: #000000;
    }}
    html.dark .theme-btn-primary:hover {{
      background-color: #e4e4e7;
    }}
    html.dark .theme-btn-secondary {{
      background-color: transparent;
      border-color: #3f3f46;
      color: #d4d4d8;
    }}
    html.dark .theme-btn-secondary:hover {{
      background-color: #18181b;
      color: #ffffff;
    }}
    html.dark .theme-track {{
      background-color: #18181b;
    }}

    /* TEMA CLARO (BRANCO) */
    html.light body {{
      background-color: #f8fafc;
      color: #0f172a;
    }}
    html.light .theme-header {{
      background-color: #ffffff;
      border-color: #e2e8f0;
      box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }}
    html.light .theme-card {{
      background-color: #ffffff;
      border-color: #e2e8f0;
      color: #0f172a;
      box-shadow: 0 1px 2px 0 rgba(0, 0, 0, 0.03);
    }}
    html.light .theme-subcard {{
      background-color: #f1f5f9;
      border-color: #e2e8f0;
    }}
    html.light .theme-input {{
      background-color: #ffffff;
      border-color: #cbd5e1;
      color: #0f172a;
    }}
    html.light .theme-input:focus {{
      border-color: #0f172a;
    }}
    html.light .theme-muted {{
      color: #64748b;
    }}
    html.light .theme-border {{
      border-color: #e2e8f0;
    }}
    html.light .theme-th {{
      background-color: #f1f5f9;
      color: #475569;
      border-color: #e2e8f0;
    }}
    html.light .theme-tr:hover {{
      background-color: #f8fafc;
    }}
    html.light .theme-td-border {{
      border-color: #f1f5f9;
    }}
    html.light .theme-btn-primary {{
      background-color: #0f172a;
      color: #ffffff;
    }}
    html.light .theme-btn-primary:hover {{
      background-color: #1e293b;
    }}
    html.light .theme-btn-secondary {{
      background-color: #ffffff;
      border-color: #cbd5e1;
      color: #334155;
    }}
    html.light .theme-btn-secondary:hover {{
      background-color: #f1f5f9;
      color: #0f172a;
    }}
    html.light .theme-track {{
      background-color: #e2e8f0;
    }}

    .custom-scroll::-webkit-scrollbar {{
      width: 5px;
      height: 5px;
    }}
    .custom-scroll::-webkit-scrollbar-thumb {{
      background: #71717a;
      border-radius: 2px;
    }}
  </style>
</head>
<body class="min-h-screen p-5 md:p-10 font-sans">
  <div class="max-w-6xl mx-auto space-y-8">

    <!-- HEADER: LOGO, NOME E BOTÃO DE TROCA DE TEMA -->
    <header class="theme-header p-5 rounded-xl border flex flex-col md:flex-row md:items-center justify-between gap-5">
      <div class="flex items-center gap-3.5">
        <div id="brand-logo" class="w-10 h-10 rounded-lg flex items-center justify-center font-black text-sm tracking-wider shadow-sm transition">
          NE
        </div>
        <div>
          <div class="flex items-center gap-2.5">
            <h1 class="text-xl md:text-2xl font-bold tracking-tight uppercase">Niels Electronics</h1>
            <span class="text-xs px-2 py-0.5 border rounded-full font-mono theme-border theme-muted">100 Clientes</span>
          </div>
          <p class="text-xs theme-muted mt-1 font-mono">
            Painel Comercial &bull; Moçambique &bull; Julho a Outubro de 2026
          </p>
        </div>
      </div>

      <!-- BOTÕES DE AÇÃO: TEMA, EXPORTAR, IMPRIMIR -->
      <div class="flex flex-wrap items-center gap-2.5">
        <!-- BOTÃO TOGGLE DE TEMA BRANCO / PRETO -->
        <button id="theme-toggle-btn" onclick="toggleTheme()" class="px-3.5 py-2 theme-btn-secondary border text-xs font-mono font-medium rounded-lg transition flex items-center gap-2 cursor-pointer shadow-sm">
          <span id="theme-icon">☀️</span>
          <span id="theme-label">Tema Claro</span>
        </button>

        <a href="graficos_interativos.html" class="px-3.5 py-2 theme-btn-secondary border text-xs font-mono font-medium rounded-lg transition flex items-center gap-2 shadow-sm">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M7 12l3-3 3 3 4-4M8 21l4-4 4 4M3 4h18M4 4h16v12a1 1 0 01-1 1H5a1 1 0 01-1-1V4z"/></svg>
          Gráficos Expandidos
        </a>

        <button onclick="exportToCSV()" class="px-4 py-2 theme-btn-primary text-xs font-mono font-bold rounded-lg transition flex items-center gap-2 cursor-pointer shadow-sm">
          <svg class="w-3.5 h-3.5" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 16v1a3 3 0 003 3h10a3 3 0 003-3v-1m-4-4l-4 4m0 0l-4-4m4 4V4"/></svg>
          Exportar CSV
        </button>
      </div>
    </header>

    <!-- KPIS: CARDS MINIMALISTAS -->
    <section class="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-4 gap-4">
      <div class="theme-card p-5 border rounded-xl">
        <p class="text-[11px] uppercase font-mono tracking-wider theme-muted">Faturação Total</p>
        <h3 class="text-2xl font-bold mt-1 tracking-tight">3.563.700 <span class="text-xs font-normal theme-muted">MZN</span></h3>
        <p class="text-[11px] theme-muted mt-3 font-mono">100 transações concluídas</p>
      </div>

      <div class="theme-card p-5 border rounded-xl">
        <p class="text-[11px] uppercase font-mono tracking-wider theme-muted">Lucro Líquido</p>
        <h3 class="text-2xl font-bold mt-1 tracking-tight">1.088.000 <span class="text-xs font-normal theme-muted">MZN</span></h3>
        <p class="text-[11px] theme-muted mt-3 font-mono">Margem global: <strong>30,5%</strong></p>
      </div>

      <div class="theme-card p-5 border rounded-xl">
        <p class="text-[11px] uppercase font-mono tracking-wider theme-muted">Itens Vendidos</p>
        <h3 class="text-2xl font-bold mt-1 tracking-tight">248 <span class="text-xs font-normal theme-muted">Unidades</span></h3>
        <p class="text-[11px] theme-muted mt-3 font-mono">Média: 2,48 produtos / cliente</p>
      </div>

      <div class="theme-card p-5 border rounded-xl">
        <p class="text-[11px] uppercase font-mono tracking-wider theme-muted">Produto Principal</p>
        <h3 class="text-lg font-bold mt-1 truncate">Ar Condicionado</h3>
        <p class="text-[11px] theme-muted mt-3 font-mono">Lucro: <strong>261.000 MZN</strong></p>
      </div>
    </section>

    <!-- RESPOSTAS ÀS QUESTÕES ANALÍTICAS -->
    <section class="space-y-3">
      <div class="flex items-center justify-between border-b theme-border pb-2">
        <h2 class="text-xs font-bold uppercase tracking-wider theme-muted font-mono">
          Questões de Negócio &bull; Diagnóstico Executivo
        </h2>
      </div>

      <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-3">
        <div class="theme-card p-4 border rounded-xl space-y-1">
          <span class="text-[10px] font-mono uppercase theme-muted">01. Produto Mais Vendido</span>
          <h4 class="text-sm font-semibold">Smart TV 50" / Ar Condicionado</h4>
          <p class="text-xs theme-muted">Smart TV (30 un.). Ar Condicionado lidera faturação (812.000 MZN).</p>
        </div>

        <div class="theme-card p-4 border rounded-xl space-y-1">
          <span class="text-[10px] font-mono uppercase theme-muted">02. Produto Menos Vendido</span>
          <h4 class="text-sm font-semibold">Micro-ondas / Ferro</h4>
          <p class="text-xs theme-muted">Micro-ondas (20 un.). Ferro de Engomar teve menor receita (39.600 MZN).</p>
        </div>

        <div class="theme-card p-4 border rounded-xl space-y-1">
          <span class="text-[10px] font-mono uppercase theme-muted">03. Mês de Maior Venda</span>
          <h4 class="text-sm font-semibold">Setembro de 2026</h4>
          <p class="text-xs theme-muted">Pico de 1.084.200 MZN faturados com 77 produtos entregues a 28 clientes.</p>
        </div>

        <div class="theme-card p-4 border rounded-xl space-y-1">
          <span class="text-[10px] font-mono uppercase theme-muted">04. Tendência das Vendas</span>
          <h4 class="text-sm font-semibold">Crescimento Contínuo</h4>
          <p class="text-xs theme-muted">Evolução forte de +28,2% em Agosto e +38,0% em Setembro.</p>
        </div>

        <div class="theme-card p-4 border rounded-xl space-y-1">
          <span class="text-[10px] font-mono uppercase theme-muted">05. Rentabilidade Extrema</span>
          <h4 class="text-sm font-semibold">Ar Condicionado vs. Ferro</h4>
          <p class="text-xs theme-muted">Ar Cond. gerou 261.000 MZN de lucro. Ferro gerou 13.200 MZN.</p>
        </div>

        <div class="theme-card p-4 border rounded-xl space-y-1">
          <span class="text-[10px] font-mono uppercase theme-muted">06. Clientes Top Compradores</span>
          <h4 class="text-sm font-semibold">Família Mondlane & Tembe</h4>
          <p class="text-xs theme-muted">Telma, Samora e Bernardo gastaram 128.000 MZN cada.</p>
        </div>
      </div>
    </section>

    <!-- GRÁFICOS INTERATIVOS PLOTLY (ADAPTÁVEIS AO TEMA) -->
    <section class="space-y-4">
      <div class="flex items-center justify-between border-b theme-border pb-2">
        <h2 class="text-xs font-bold uppercase tracking-wider theme-muted font-mono">
          Visualizações Analíticas Interativas (Plotly)
        </h2>
        <span class="text-[11px] theme-muted font-mono">Passe o cursor para detalhes e zoom</span>
      </div>

      <div class="grid grid-cols-1 lg:grid-cols-2 gap-5">
        <div class="theme-card p-3 border rounded-xl">
          <div id="chart-mes" class="w-full h-[340px]"></div>
        </div>
        <div class="theme-card p-3 border rounded-xl">
          <div id="chart-prod" class="w-full h-[340px]"></div>
        </div>
        <div class="theme-card p-3 border rounded-xl">
          <div id="chart-stock" class="w-full h-[340px]"></div>
        </div>
        <div class="theme-card p-3 border rounded-xl">
          <div id="chart-cidades" class="w-full h-[340px]"></div>
        </div>
      </div>
    </section>

    <!-- TABELA DE PRODUTOS & GESTÃO DE STOCK -->
    <section class="theme-card p-5 border rounded-xl space-y-4">
      <div class="flex flex-col sm:flex-row sm:items-center justify-between gap-2 border-b theme-border pb-3">
        <div>
          <h3 class="text-sm font-bold uppercase font-mono tracking-wide">
            Controlo de Stock & Rentabilidade
          </h3>
          <p class="text-xs theme-muted mt-0.5">Catálogo de 10 electrodomésticos &bull; Base inicial de 50 unidades</p>
        </div>
        <span class="text-xs font-mono theme-muted">10 produtos</span>
      </div>
      
      <div class="overflow-x-auto custom-scroll">
        <table class="w-full text-left text-xs font-mono">
          <thead class="theme-th uppercase text-[11px] border-b">
            <tr>
              <th class="py-2.5 px-3">Produto</th>
              <th class="py-2.5 px-3">Preço Venda</th>
              <th class="py-2.5 px-3">Custo Unit.</th>
              <th class="py-2.5 px-3">Qtd Vendida</th>
              <th class="py-2.5 px-3">Stock Restante</th>
              <th class="py-2.5 px-3 text-right">Faturação</th>
              <th class="py-2.5 px-3 text-right">Lucro Total</th>
              <th class="py-2.5 px-3 text-right">Margem</th>
            </tr>
          </thead>
          <tbody id="tabela-produtos" class="divide-y theme-td-border">
            <!-- Preenchido via JavaScript -->
          </tbody>
        </table>
      </div>
    </section>

    <!-- TABELA COMPLETA DOS 100 CLIENTES -->
    <section class="theme-card p-5 border rounded-xl space-y-4">
      <div class="flex flex-col lg:flex-row lg:items-center justify-between gap-4 border-b theme-border pb-4">
        <div>
          <h3 class="text-sm font-bold uppercase font-mono tracking-wide">
            Registo das 100 Vendas & Clientes
          </h3>
          <p class="text-xs theme-muted mt-0.5">Filtre ou pesquise instantaneamente</p>
        </div>

        <!-- Filtros e Barra de Pesquisa -->
        <div class="flex flex-wrap items-center gap-2">
          <div class="relative min-w-[200px]">
            <input type="text" id="search-input" onkeyup="filtrarClientes()" placeholder="Pesquisar..." 
                   class="theme-input w-full px-3 py-1.5 pl-8 border rounded-lg text-xs placeholder-slate-400 focus:outline-none transition font-mono">
            <svg class="w-3.5 h-3.5 theme-muted absolute left-2.5 top-2" fill="none" stroke="currentColor" viewBox="0 0 24 24"><path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M21 21l-6-6m2-5a7 7 0 11-14 0 7 7 0 0114 0z"/></svg>
          </div>

          <select id="filter-cidade" onchange="filtrarClientes()" class="theme-input px-2.5 py-1.5 border rounded-lg text-xs focus:outline-none font-mono cursor-pointer">
            <option value="">Todas as Cidades</option>
            <option value="Maputo">Maputo</option>
            <option value="Matola">Matola</option>
            <option value="Beira">Beira</option>
            <option value="Nampula">Nampula</option>
            <option value="Chimoio">Chimoio</option>
            <option value="Quelimane">Quelimane</option>
            <option value="Tete">Tete</option>
            <option value="Pemba">Pemba</option>
            <option value="Inhambane">Inhambane</option>
            <option value="Xai-Xai">Xai-Xai</option>
          </select>

          <select id="filter-mes" onchange="filtrarClientes()" class="theme-input px-2.5 py-1.5 border rounded-lg text-xs focus:outline-none font-mono cursor-pointer">
            <option value="">Todos os Meses</option>
            <option value="Julho/2026">Julho/2026</option>
            <option value="Agosto/2026">Agosto/2026</option>
            <option value="Setembro/2026">Setembro/2026</option>
            <option value="Outubro/2026">Outubro/2026</option>
          </select>
        </div>
      </div>

      <div class="overflow-x-auto custom-scroll max-h-[480px]">
        <table class="w-full text-left text-xs font-mono">
          <thead class="theme-th uppercase text-[11px] sticky top-0 z-10 border-b">
            <tr>
              <th class="py-2.5 px-3">ID</th>
              <th class="py-2.5 px-3">Cliente</th>
              <th class="py-2.5 px-3">Idade</th>
              <th class="py-2.5 px-3">Cidade</th>
              <th class="py-2.5 px-3">Data</th>
              <th class="py-2.5 px-3">Mês</th>
              <th class="py-2.5 px-3">Produto</th>
              <th class="py-2.5 px-3">Preço</th>
              <th class="py-2.5 px-3 text-center">Qtd</th>
              <th class="py-2.5 px-3 text-right">Total</th>
            </tr>
          </thead>
          <tbody id="tabela-clientes" class="divide-y theme-td-border">
            <!-- Preenchido via JavaScript -->
          </tbody>
        </table>
      </div>

      <div class="pt-2 flex flex-col sm:flex-row sm:items-center justify-between text-xs theme-muted font-mono">
        <span id="contador-registos">A mostrar 100 de 100 clientes</span>
        <span id="current-theme-status">Tema: Escuro (Preto)</span>
      </div>
    </section>

    <!-- FOOTER -->
    <footer class="pt-6 pb-2 text-center text-xs theme-muted font-mono border-t theme-border">
      NIELS ELECTRONICS &copy; 2026 &bull; SISTEMA DE GESTÃO E ANALYTICS &bull; TEMA DUPLO (CLARO / ESCURO)
    </footer>

  </div>

  <!-- DADOS E JAVASCRIPT DINÂMICO -->
  <script>
    const DADOS_PRODUTOS = {produtos_json};
    const DADOS_CLIENTES = {clientes_json};
    const DADOS_MENSAL = {mensal_json};

    let currentTheme = localStorage.getItem('ne_theme') || 'dark';

    function formatMZN(val) {{
      return Number(val).toLocaleString('pt-MZ') + ' MZN';
    }}

    // Aplicação e Alternância do Tema
    function applyTheme(theme) {{
      currentTheme = theme;
      localStorage.setItem('ne_theme', theme);
      const isDark = (theme === 'dark');

      if (isDark) {{
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
        document.getElementById('theme-icon').textContent = '☀️';
        document.getElementById('theme-label').textContent = 'Tema Claro';
        document.getElementById('current-theme-status').textContent = 'Tema Ativo: Preto (Escuro)';
        
        const logo = document.getElementById('brand-logo');
        logo.className = 'w-10 h-10 rounded-lg flex items-center justify-center font-black text-sm tracking-wider shadow-sm transition bg-white text-black';
      }} else {{
        document.documentElement.classList.add('light');
        document.documentElement.classList.remove('dark');
        document.getElementById('theme-icon').textContent = '🌙';
        document.getElementById('theme-label').textContent = 'Tema Escuro';
        document.getElementById('current-theme-status').textContent = 'Tema Ativo: Branco (Claro)';
        
        const logo = document.getElementById('brand-logo');
        logo.className = 'w-10 h-10 rounded-lg flex items-center justify-center font-black text-sm tracking-wider shadow-sm transition bg-zinc-900 text-white';
      }}

      renderCharts(isDark);
    }}

    function toggleTheme() {{
      applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    }}

    // Renderização dos Gráficos Plotly com Adaptação ao Tema
    function renderCharts(isDark) {{
      const bgColor = isDark ? '#09090b' : '#ffffff';
      const textColor = isDark ? '#ffffff' : '#0f172a';
      const mutedColor = isDark ? '#a1a1aa' : '#64748b';
      const gridColor = isDark ? '#27272a' : '#e2e8f0';
      const barPrimary = isDark ? '#ffffff' : '#0f172a';
      const barSecondary = isDark ? '#71717a' : '#94a3b8';
      const barStackRest = isDark ? '#3f3f46' : '#cbd5e1';

      const baseLayout = {{
        paper_bgcolor: bgColor,
        plot_bgcolor: bgColor,
        font: {{ family: 'system-ui, sans-serif', color: textColor, size: 11 }},
        margin: {{ l: 45, r: 20, t: 40, b: 35 }},
        xaxis: {{
          gridcolor: gridColor, zerolinecolor: gridColor,
          tickfont: {{ color: mutedColor, size: 10 }},
          title_font: {{ color: textColor, size: 11 }}
        }},
        yaxis: {{
          gridcolor: gridColor, zerolinecolor: gridColor,
          tickfont: {{ color: mutedColor, size: 10 }},
          title_font: {{ color: textColor, size: 11 }}
        }},
        legend: {{
          font: {{ color: textColor, size: 10 }},
          bgcolor: isDark ? 'rgba(9, 9, 11, 0.8)' : 'rgba(255, 255, 255, 0.8)',
          bordercolor: gridColor, borderwidth: 1,
          orientation: 'h', yanchor: 'bottom', y: 1.02, xanchor: 'right', x: 1
        }},
        hoverlabel: {{
          bgcolor: isDark ? '#18181b' : '#ffffff',
          font_color: isDark ? '#ffffff' : '#0f172a',
          bordercolor: isDark ? '#52525b' : '#cbd5e1',
          font_size: 11
        }}
      }};

      const config = {{ responsive: true, displayModeBar: false }};

      // 1. Gráfico Mensal
      const dataMes = [
        {{
          x: DADOS_MENSAL.map(m => m['Mês']),
          y: DADOS_MENSAL.map(m => m['Total_Faturado_MZN']),
          name: 'Faturação', type: 'bar', marker: {{ color: barPrimary }},
          hovertemplate: '<b>%{{x}}</b><br>Faturação: %{{y:,.2f}} MZN<extra></extra>'
        }},
        {{
          x: DADOS_MENSAL.map(m => m['Mês']),
          y: DADOS_MENSAL.map(m => m['Lucro_Total_MZN']),
          name: 'Lucro Líquido', type: 'bar', marker: {{ color: barSecondary }},
          hovertemplate: '<b>%{{x}}</b><br>Lucro: %{{y:,.2f}} MZN<extra></extra>'
        }}
      ];
      Plotly.newPlot('chart-mes', dataMes, {{
        ...baseLayout,
        title: {{ text: '<b>Evolução Mensal: Faturação vs. Lucro (MZN)</b>', font: {{ size: 13, color: textColor }} }},
        barmode: 'group'
      }}, config);

      // 2. Gráfico Rentabilidade por Produto
      const sortedProd = [...DADOS_PRODUTOS].sort((a, b) => a.Faturacao_MZN - b.Faturacao_MZN);
      const dataProd = [
        {{
          y: sortedProd.map(p => p.Produto),
          x: sortedProd.map(p => p.Faturacao_MZN),
          name: 'Faturação', type: 'bar', orientation: 'h', marker: {{ color: barPrimary }},
          hovertemplate: '<b>%{{y}}</b><br>Faturação: %{{x:,.2f}} MZN<extra></extra>'
        }},
        {{
          y: sortedProd.map(p => p.Produto),
          x: sortedProd.map(p => p.Lucro_MZN),
          name: 'Lucro', type: 'bar', orientation: 'h', marker: {{ color: barSecondary }},
          hovertemplate: '<b>%{{y}}</b><br>Lucro: %{{x:,.2f}} MZN<extra></extra>'
        }}
      ];
      Plotly.newPlot('chart-prod', dataProd, {{
        ...baseLayout,
        margin: {{ l: 125, r: 20, t: 40, b: 35 }},
        title: {{ text: '<b>Rentabilidade por Produto: Faturação vs. Lucro</b>', font: {{ size: 13, color: textColor }} }},
        barmode: 'group'
      }}, config);

      // 3. Gráfico Stock (Vendido vs. Restante)
      const sortedStock = [...DADOS_PRODUTOS].sort((a, b) => a.Qtd_Vendida - b.Qtd_Vendida);
      const dataStock = [
        {{
          y: sortedStock.map(p => p.Produto),
          x: sortedStock.map(p => p.Qtd_Vendida),
          name: 'Unidades Vendidas', type: 'bar', orientation: 'h', marker: {{ color: barPrimary }},
          hovertemplate: '<b>%{{y}}</b><br>Vendido: %{{x}} un.<extra></extra>'
        }},
        {{
          y: sortedStock.map(p => p.Produto),
          x: sortedStock.map(p => p['Stock Restante']),
          name: 'Stock em Armazém', type: 'bar', orientation: 'h', marker: {{ color: barStackRest }},
          hovertemplate: '<b>%{{y}}</b><br>Disponível: %{{x}} un.<extra></extra>'
        }}
      ];
      Plotly.newPlot('chart-stock', dataStock, {{
        ...baseLayout,
        margin: {{ l: 125, r: 20, t: 40, b: 35 }},
        title: {{ text: '<b>Balanço de Stock: Vendido vs. Restante (Base 50 un.)</b>', font: {{ size: 13, color: textColor }} }},
        barmode: 'stack'
      }}, config);

      // 4. Gráfico Cidades
      const mapCidades = {{}};
      DADOS_CLIENTES.forEach(c => {{
        mapCidades[c.Cidade] = (mapCidades[c.Cidade] || 0) + c['Total Faturado (MZN)'];
      }});
      const cidadesArray = Object.keys(mapCidades).map(k => ({{ cidade: k, total: mapCidades[k] }}))
                                                  .sort((a, b) => b.total - a.total);

      const dataCidades = [{{
        x: cidadesArray.map(c => c.cidade),
        y: cidadesArray.map(c => c.total),
        type: 'bar', marker: {{ color: barSecondary }},
        hovertemplate: '<b>%{{x}}</b><br>Faturação: %{{y:,.2f}} MZN<extra></extra>'
      }}];
      Plotly.newPlot('chart-cidades', dataCidades, {{
        ...baseLayout,
        margin: {{ l: 45, r: 20, t: 40, b: 35 }},
        title: {{ text: '<b>Penetração Geográfica: Faturação por Cidade</b>', font: {{ size: 13, color: textColor }} }}
      }}, config);
    }}

    // Renderizar tabela de produtos
    function renderProdutos() {{
      const tbody = document.getElementById('tabela-produtos');
      tbody.innerHTML = '';
      
      DADOS_PRODUTOS.sort((a, b) => b.Faturacao_MZN - a.Faturacao_MZN).forEach(p => {{
        const percStock = Math.round((p['Stock Restante'] / p['Stock Inicial']) * 100);
        const tr = document.createElement('tr');
        tr.className = 'theme-tr transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 font-semibold">${{p.Produto}}</td>
          <td class="py-2.5 px-3 theme-muted">${{formatMZN(p.Preço_Venda)}}</td>
          <td class="py-2.5 px-3 theme-muted">${{formatMZN(p.Custo_Unitario)}}</td>
          <td class="py-2.5 px-3 font-bold">${{p.Qtd_Vendida}}</td>
          <td class="py-2.5 px-3">
            <div class="flex items-center gap-2">
              <div class="w-14 theme-track h-2 rounded-full overflow-hidden">
                <div class="bg-current h-full" style="width: ${{percStock}}%"></div>
              </div>
              <span class="text-[11px] theme-muted">${{p['Stock Restante']}}/50</span>
            </div>
          </td>
          <td class="py-2.5 px-3 text-right font-medium">${{formatMZN(p.Faturacao_MZN)}}</td>
          <td class="py-2.5 px-3 text-right font-medium">${{formatMZN(p.Lucro_MZN)}}</td>
          <td class="py-2.5 px-3 text-right theme-muted">${{Math.round(((p.Preço_Venda - p.Custo_Unitario) / p.Preço_Venda) * 100)}}%</td>
        `;
        tbody.appendChild(tr);
      }});
    }}

    // Renderizar tabela de clientes com filtros
    function filtrarClientes() {{
      const search = document.getElementById('search-input').value.toLowerCase();
      const cidade = document.getElementById('filter-cidade').value;
      const mes = document.getElementById('filter-mes').value;
      
      const filtrados = DADOS_CLIENTES.filter(c => {{
        const matchSearch = c.Cliente.toLowerCase().includes(search) || 
                            c.Cidade.toLowerCase().includes(search) || 
                            c.Produto.toLowerCase().includes(search) ||
                            c.ID_Cliente.toLowerCase().includes(search);
        const matchCidade = !cidade || c.Cidade === cidade;
        const matchMes = !mes || c.Mês === mes;
        return matchSearch && matchCidade && matchMes;
      }});

      const tbody = document.getElementById('tabela-clientes');
      tbody.innerHTML = '';

      filtrados.forEach(c => {{
        const tr = document.createElement('tr');
        tr.className = 'theme-tr transition';
        tr.innerHTML = `
          <td class="py-2.5 px-3 theme-muted font-mono text-[11px]">${{c.ID_Cliente}}</td>
          <td class="py-2.5 px-3 font-semibold">${{c.Cliente}}</td>
          <td class="py-2.5 px-3 theme-muted">${{c.Idade}}</td>
          <td class="py-2.5 px-3">${{c.Cidade}}</td>
          <td class="py-2.5 px-3 theme-muted">${{c['Data da Compra']}}</td>
          <td class="py-2.5 px-3 theme-muted">${{c.Mês}}</td>
          <td class="py-2.5 px-3 font-medium">${{c.Produto}}</td>
          <td class="py-2.5 px-3 theme-muted">${{formatMZN(c['Preço Venda (MZN)'] )}}</td>
          <td class="py-2.5 px-3 text-center font-bold">${{c['Qtd Comprada']}}</td>
          <td class="py-2.5 px-3 text-right font-bold">${{formatMZN(c['Total Faturado (MZN)'] )}}</td>
        `;
        tbody.appendChild(tr);
      }});

      document.getElementById('contador-registos').textContent = `A mostrar ${{filtrados.length}} de ${{DADOS_CLIENTES.length}} clientes`;
    }}

    // Exportar para CSV
    function exportToCSV() {{
      let csv = 'ID_Cliente;Cliente;Idade;Cidade;Data;Mes;Produto;Preco_MZN;Qtd;Total_MZN\\n';
      DADOS_CLIENTES.forEach(c => {{
        csv += `${{c.ID_Cliente}};"${{c.Cliente}}";${{c.Idade}};"${{c.Cidade}}";${{c['Data da Compra']}};"${{c.Mês}}";"${{c.Produto}}";${{c['Preço Venda (MZN)']}};${{c['Qtd Comprada']}};${{c['Total Faturado (MZN)']}}\\n`;
      }});
      const blob = new Blob([csv], {{ type: 'text/csv;charset=utf-8;' }});
      const url = URL.createObjectURL(blob);
      const link = document.createElement('a');
      link.setAttribute('href', url);
      link.setAttribute('download', 'niels_electronics_clientes_100.csv');
      document.body.appendChild(link);
      link.click();
      document.body.removeChild(link);
    }}

    // Inicialização ao carregar a página
    window.addEventListener('DOMContentLoaded', () => {{
      applyTheme(currentTheme);
      renderProdutos();
      filtrarClientes();
    }});
  </script>
</body>
</html>
"""

with open('index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

with open('Projecto-dataset/index.html', 'w', encoding='utf-8') as f:
    f.write(html_template)

artifact_dir = r"C:\Users\Dell\.gemini\antigravity\brain\3fce6733-d686-4d91-a0e7-108585d3892c"
with open(os.path.join(artifact_dir, 'dashboard.html'), 'w', encoding='utf-8') as f:
    f.write(html_template)

print('Dual theme index.html generated successfully!')
