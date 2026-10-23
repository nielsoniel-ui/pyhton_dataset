import json
import os

with open('Projecto-dataset/dados.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

clientes_json = json.dumps(data['clientes'], ensure_ascii=False)
produtos_json = json.dumps(data['produtos'], ensure_ascii=False)
mensal_json = json.dumps(data['mensal'], ensure_ascii=False)

html_graficos = f"""<!DOCTYPE html>
<html lang="pt" class="dark">
<head>
  <meta charset="UTF-8">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Niels Electronics — Gráficos Analíticos Interativos (Tema Duplo)</title>
  <script src="https://cdn.plot.ly/plotly-2.35.2.min.js"></script>
  <script src="https://www.gstatic.com/antigravity/web/dev/tailwindcss.min.js"></script>
  <style>
    body, .theme-card, .theme-border, button {{
      transition: background-color 0.25s ease, color 0.25s ease, border-color 0.25s ease;
    }}
    html.dark body {{
      background-color: #000000;
      color: #ffffff;
    }}
    html.dark .theme-header, html.dark .theme-card {{
      background-color: #09090b;
      border-color: #27272a;
    }}
    html.dark .theme-muted {{
      color: #a1a1aa;
    }}
    html.dark .theme-border {{
      border-color: #27272a;
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

    html.light body {{
      background-color: #f8fafc;
      color: #0f172a;
    }}
    html.light .theme-header, html.light .theme-card {{
      background-color: #ffffff;
      border-color: #e2e8f0;
      box-shadow: 0 1px 3px 0 rgba(0, 0, 0, 0.05);
    }}
    html.light .theme-muted {{
      color: #64748b;
    }}
    html.light .theme-border {{
      border-color: #e2e8f0;
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
  </style>
</head>
<body class="min-h-screen p-5 md:p-10 font-sans">
  <div class="max-w-6xl mx-auto space-y-8">
    
    <!-- HEADER -->
    <header class="theme-header p-5 rounded-xl border flex flex-col sm:flex-row sm:items-center justify-between gap-4">
      <div class="flex items-center gap-3">
        <a href="index.html" class="w-9 h-9 rounded-lg flex items-center justify-center font-black text-xs tracking-wider transition bg-white text-black" id="brand-logo">
          NE
        </a>
        <div>
          <h1 class="text-lg md:text-xl font-bold uppercase tracking-tight">Gráficos Analíticos Interativos &bull; Plotly</h1>
          <p class="text-xs theme-muted font-mono">Niels Electronics &bull; Zoom, Seleção de Séries, Tooltips e Exportação</p>
        </div>
      </div>

      <div class="flex items-center gap-2.5">
        <button id="theme-toggle-btn" onclick="toggleTheme()" class="px-3.5 py-1.5 theme-btn-secondary border text-xs font-mono font-medium rounded-lg transition flex items-center gap-2 cursor-pointer shadow-sm">
          <span id="theme-icon">☀️</span>
          <span id="theme-label">Tema Claro</span>
        </button>
        <a href="index.html" class="px-3.5 py-1.5 theme-btn-secondary border text-xs font-mono rounded-lg transition">
          &larr; Voltar ao Painel Geral
        </a>
      </div>
    </header>

    <!-- GRÁFICOS INTERATIVOS -->
    <div class="grid grid-cols-1 gap-6">
      <div class="theme-card p-4 border rounded-xl">
        <div id="chart-mes" class="w-full h-[380px]"></div>
      </div>
      <div class="theme-card p-4 border rounded-xl">
        <div id="chart-prod" class="w-full h-[400px]"></div>
      </div>
      <div class="theme-card p-4 border rounded-xl">
        <div id="chart-stock" class="w-full h-[400px]"></div>
      </div>
      <div class="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div class="theme-card p-4 border rounded-xl">
          <div id="chart-cidades" class="w-full h-[380px]"></div>
        </div>
        <div class="theme-card p-4 border rounded-xl">
          <div id="chart-clientes" class="w-full h-[380px]"></div>
        </div>
      </div>
    </div>

    <footer class="pt-6 pb-2 text-center text-xs theme-muted font-mono border-t theme-border">
      NIELS ELECTRONICS &copy; 2026 &bull; VISUALIZAÇÕES INTERATIVAS COM SUPORTE A TEMA CLARO E ESCURO
    </footer>
  </div>

  <script>
    const DADOS_PRODUTOS = {produtos_json};
    const DADOS_CLIENTES = {clientes_json};
    const DADOS_MENSAL = {mensal_json};

    let currentTheme = localStorage.getItem('ne_theme') || 'dark';

    function applyTheme(theme) {{
      currentTheme = theme;
      localStorage.setItem('ne_theme', theme);
      const isDark = (theme === 'dark');

      if (isDark) {{
        document.documentElement.classList.add('dark');
        document.documentElement.classList.remove('light');
        document.getElementById('theme-icon').textContent = '☀️';
        document.getElementById('theme-label').textContent = 'Tema Claro';
        const logo = document.getElementById('brand-logo');
        logo.className = 'w-9 h-9 rounded-lg flex items-center justify-center font-black text-xs tracking-wider transition bg-white text-black';
      }} else {{
        document.documentElement.classList.add('light');
        document.documentElement.classList.remove('dark');
        document.getElementById('theme-icon').textContent = '🌙';
        document.getElementById('theme-label').textContent = 'Tema Escuro';
        const logo = document.getElementById('brand-logo');
        logo.className = 'w-9 h-9 rounded-lg flex items-center justify-center font-black text-xs tracking-wider transition bg-zinc-900 text-white';
      }}

      renderCharts(isDark);
    }}

    function toggleTheme() {{
      applyTheme(currentTheme === 'dark' ? 'light' : 'dark');
    }}

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
        margin: {{ l: 45, r: 20, t: 45, b: 35 }},
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

      const config = {{ responsive: true, displayModeBar: true }};

      // 1. Mensal
      const dataMes = [
        {{
          x: DADOS_MENSAL.map(m => m['Mês']),
          y: DADOS_MENSAL.map(m => m['Total_Faturado_MZN']),
          name: 'Faturação Bruta', type: 'bar', marker: {{ color: barPrimary }},
          hovertemplate: '<b>%{{x}}</b><br>Faturação: %{{y:,.2f}} MZN<extra></extra>'
        }},
        {{
          x: DADOS_MENSAL.map(m => m['Mês']),
          y: DADOS_MENSAL.map(m => m['Lucro_Total_MZN']),
          name: 'Lucro Líquido', type: 'bar', marker: {{ color: barSecondary }},
          hovertemplate: '<b>%{{x}}</b><br>Lucro Líquido: %{{y:,.2f}} MZN<extra></extra>'
        }}
      ];
      Plotly.newPlot('chart-mes', dataMes, {{
        ...baseLayout,
        title: {{ text: '<b>Evolução Mensal: Faturação vs. Lucro Líquido (MZN)</b>', font: {{ size: 14, color: textColor }} }},
        barmode: 'group'
      }}, config);

      // 2. Produto
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
        margin: {{ l: 135, r: 20, t: 45, b: 35 }},
        title: {{ text: '<b>Rentabilidade por Produto: Faturação vs. Lucro Total</b>', font: {{ size: 14, color: textColor }} }},
        barmode: 'group'
      }}, config);

      // 3. Stock
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
        margin: {{ l: 135, r: 20, t: 45, b: 35 }},
        title: {{ text: '<b>Balanço de Stock: Unidades Vendidas vs. Stock Restante (Base 50 un.)</b>', font: {{ size: 14, color: textColor }} }},
        barmode: 'stack'
      }}, config);

      // 4. Cidades
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
        margin: {{ l: 45, r: 20, t: 45, b: 35 }},
        title: {{ text: '<b>Faturação por Cidade (Moçambique)</b>', font: {{ size: 14, color: textColor }} }}
      }}, config);

      // 5. Clientes
      const dataClientes = [{{
        x: DADOS_CLIENTES.map(c => c.Idade),
        y: DADOS_CLIENTES.map(c => c['Total Faturado (MZN)']),
        mode: 'markers',
        marker: {{
          size: DADOS_CLIENTES.map(c => c['Qtd Comprada'] * 4 + 5),
          color: barPrimary,
          line: {{ width: 1, color: isDark ? '#71717a' : '#475569' }},
          opacity: 0.85
        }},
        text: DADOS_CLIENTES.map(c => `<b>${{c.Cliente}}</b> (${{c.Cidade}})<br>Idade: ${{c.Idade}} anos<br>Comprou: ${{c['Qtd Comprada']}}x ${{c.Produto}}<br>Total: ${{formatMZN(c['Total Faturado (MZN)'] )}}`),
        hoverinfo: 'text'
      }}];
      Plotly.newPlot('chart-clientes', dataClientes, {{
        ...baseLayout,
        margin: {{ l: 55, r: 20, t: 45, b: 35 }},
        title: {{ text: '<b>Perfil dos Clientes: Idade vs. Gasto (MZN)</b>', font: {{ size: 14, color: textColor }} }}
      }}, config);
    }}

    window.addEventListener('DOMContentLoaded', () => {{
      applyTheme(currentTheme);
    }});
  </script>
</body>
</html>
"""

with open('graficos_interativos.html', 'w', encoding='utf-8') as f:
    f.write(html_graficos)

with open('Projecto-dataset/graficos_interativos.html', 'w', encoding='utf-8') as f:
    f.write(html_graficos)

print('Updated graficos_interativos.html with dual theme support!')
