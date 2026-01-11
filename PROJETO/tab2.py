import FreeSimpleGUI as sg
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import json
import statistics

# ============================================================================
# DESIGN SYSTEM
# ============================================================================
COR_SIDEBAR = '#2c3e50'
COR_BG_MAIN = '#ecf0f1'
COR_ACCENT = '#2980b9'
COR_TEXTO = '#2f3640'
COR_VERDE = '#27ae60'
COR_ROXO = '#8e44ad'
COR_ALERT = '#c0392b' # Vermelho para alertas

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================
def desenhar_figura(canvas, figure):
    """Insere o gráfico do Matplotlib dentro do Canvas do FreeSimpleGUI"""
    if not hasattr(canvas, 'children'): return None
    figure_canvas_agg = FigureCanvasTkAgg(figure, canvas)
    figure_canvas_agg.draw()
    figure_canvas_agg.get_tk_widget().pack(side='top', fill='both', expand=1)
    return figure_canvas_agg

def carregar_dados_json(caminho):
    """Lê o ficheiro JSON gerado pelo tab1"""
    try:
        with open(caminho, 'r', encoding='utf-8') as f:
            return json.load(f)
    except Exception as e:
        sg.popup_error(f"Erro ao ler JSON: {e}")
        return None

# ============================================================================
# INTERFACE TAB 2 (BUSINESS INTELLIGENCE)
# ============================================================================
def main(dados_memoria=None):
    sg.theme('SystemDefault')

    # --- SIDEBAR ---
    sidebar = [
        [sg.Text('DASHBOARD', font=('Segoe UI', 14, 'bold'), text_color='white', background_color=COR_SIDEBAR, pad=(20, 30))],
        [sg.Text('ANÁLISE DE DADOS', font=('Segoe UI', 8), text_color='#bdc3c7', background_color=COR_SIDEBAR, pad=(20, 0))],
        
        [sg.Button(' 📂 Carregar Dados (.json)', key='-LOAD_FILE-', size=(22, 2), button_color=('white', '#d35400'), border_width=0, pad=(20, 20))],
        
        [sg.HorizontalSeparator(color='#34495e', pad=(20, 10))],
        [sg.Text('Fonte dos Dados:', text_color='#bdc3c7', background_color=COR_SIDEBAR, font=('Segoe UI', 8), pad=(20, 0))],
        [sg.Text('Aguardando...', key='-SOURCE-', text_color='white', background_color=COR_SIDEBAR, font=('Segoe UI', 9, 'bold'), pad=(20, 5))],
        
        [sg.Push(background_color=COR_SIDEBAR)],
        [sg.Button('⬅  VOLTAR', key='-BACK-', button_color=('white', '#c0392b'), border_width=0, size=(22, 2), pad=(0, 20))]
    ]

    # --- CARDS DE KPI ---
    def criar_card(titulo, key_valor, unidade, cor_texto=COR_ACCENT):
        return sg.Column([
            [sg.Text(titulo, font=('Segoe UI', 8), text_color='gray', background_color='white')],
            [sg.Text('-', key=key_valor, font=('Segoe UI', 14, 'bold'), text_color=cor_texto, background_color='white'),
             sg.Text(unidade, font=('Segoe UI', 9), text_color=cor_texto, background_color='white')]
        ], background_color='white', size=(190, 60), pad=(5, 5), element_justification='c')

    # Linha 1: Foco no Paciente e Tempos
    layout_kpis_linha1 = [
        criar_card('Total Pacientes', '-KPI_TOTAL-', ''),
        criar_card('Tempo Médio Consulta', '-KPI_CONSULTA-', 'min'),
        criar_card('Tempo Médio Espera', '-KPI_ESPERA-', 'min'),
        criar_card('Tempo Total na Clínica', '-KPI_CLINICA-', 'min', COR_ROXO)
    ]

    # Linha 2: Foco na Fila e Recursos (COM O NOVO CARD DE UPTIME)
    layout_kpis_linha2 = [
        criar_card('Disponibilidade Equip.', '-KPI_UPTIME-', '%', COR_VERDE), # <--- NOVO BLOCO
        criar_card('Ocupação Média Médicos', '-KPI_OCUP-', '%'),
        criar_card('Tamanho Médio Fila', '-KPI_FILA_MED-', 'pac'),
        criar_card('Tamanho Máximo Fila', '-KPI_FILA_MAX-', 'pac', COR_ALERT)
    ]

    # --- ÁREA PRINCIPAL ---
    col_main = sg.Column([
        [sg.Text('Indicadores de Performance Clínica', font=('Segoe UI', 16, 'bold'), background_color=COR_BG_MAIN, text_color=COR_TEXTO)],
        [sg.HorizontalSeparator()],
        
        [sg.Column([layout_kpis_linha1], background_color=COR_BG_MAIN, element_justification='c')],
        [sg.Column([layout_kpis_linha2], background_color=COR_BG_MAIN, element_justification='c')],
        
        # Área do Gráfico (Canvas)
        [sg.Canvas(key='-CANVAS-', size=(800, 500), background_color='white', expand_x=True, expand_y=True)]
    
    ], background_color=COR_BG_MAIN, expand_x=True, expand_y=True, pad=(20, 20))

    layout = [[sg.Column(sidebar, background_color=COR_SIDEBAR, expand_y=True, pad=(0,0)), col_main]]

    # Criação da Janela
    window = sg.Window('MedCore Analytics', layout, finalize=True, resizable=True, background_color=COR_BG_MAIN)
    window.maximize()

    figure_agg = None

    # --- FUNÇÃO DE ATUALIZAÇÃO ---
    def atualizar_dashboard(dados, origem_texto):
        nonlocal figure_agg
        
        if not dados: return
        
        metricas = dados.get('metricas', {})
        hist_fila = dados.get('historico_fila', [])
        
        # --- CÁLCULOS ---
        fila_media = 0
        if hist_fila:
            valores_fila = [p[1] for p in hist_fila]
            fila_media = statistics.mean(valores_fila) if valores_fila else 0

        tempo_consulta_medio = metricas.get('consulta_media', 15.0) 
        tempo_espera = metricas.get('espera_media', 0)
        tempo_total_clinica = tempo_espera + tempo_consulta_medio

        # Novo: Uptime (Se não existir no JSON, assume 100%)
        uptime = metricas.get('uptime', 100.0)

        # --- ATUALIZAÇÃO DA UI ---
        window['-KPI_TOTAL-'].update(metricas.get('total_pacientes', 0))
        window['-KPI_CONSULTA-'].update(f"{tempo_consulta_medio:.1f}")
        window['-KPI_ESPERA-'].update(f"{tempo_espera:.1f}")
        window['-KPI_CLINICA-'].update(f"{tempo_total_clinica:.1f}")
        
        # Atualiza Uptime com cor dinâmica (Vermelho se < 90%)
        cor_uptime = COR_VERDE if uptime >= 90 else COR_ALERT
        window['-KPI_UPTIME-'].update(f"{uptime:.1f}", text_color=cor_uptime)

        window['-KPI_OCUP-'].update(f"{metricas.get('ocupacao_media', 0):.1f}")
        window['-KPI_FILA_MED-'].update(f"{fila_media:.1f}")
        window['-KPI_FILA_MAX-'].update(metricas.get('max_fila', 0))

        window['-SOURCE-'].update(origem_texto)

        # --- GERAÇÃO DOS GRÁFICOS ---
        if figure_agg:
            figure_agg.get_tk_widget().forget()
            plt.close('all')

        fig, axs = plt.subplots(2, 2, figsize=(10, 8), constrained_layout=True)
        
        # Gráfico 1: Evolução Fila
        if hist_fila:
            t_f, y_f = zip(*hist_fila)
            axs[0, 0].plot(t_f, y_f, color='#e74c3c')
            axs[0, 0].fill_between(t_f, y_f, color='#e74c3c', alpha=0.1)
            axs[0, 0].axhline(y=fila_media, color='black', linestyle='--', alpha=0.5, label='Média')
            axs[0, 0].set_title('Evolução da Fila (Tempo Real)')
            axs[0, 0].legend()
        else:
            axs[0, 0].text(0.5, 0.5, 'Sem dados', ha='center')
        
        # Gráfico 2: Evolução Ocupação
        hist_ocup = dados.get('historico_ocupacao', [])
        if hist_ocup:
            t_o, y_o = zip(*hist_ocup)
            axs[0, 1].plot(t_o, y_o, color='#2980b9')
            axs[0, 1].fill_between(t_o, y_o, color='#2980b9', alpha=0.1)
            axs[0, 1].set_title('Taxa de Ocupação (%)')
            axs[0, 1].set_ylim(0, 105)

        # Gráfico 3: Sensibilidade
        sens = dados.get('sensibilidade', {})
        if sens:
            dados_ordenados = sorted([(int(k), v) for k, v in sens.items()])
            sx = [d[0] for d in dados_ordenados]
            sy = [d[1] for d in dados_ordenados]
            axs[1, 0].plot(sx, sy, marker='o', color='#f39c12')
            axs[1, 0].set_title('Sensibilidade: Fila vs Taxa Chegada')
            axs[1, 0].set_xlabel('Taxa (λ)')
        else:
            axs[1, 0].text(0.5, 0.5, 'Sem dados de sensibilidade', ha='center')

        # Gráfico 4: Pizza
        labels = ['Espera', 'Consulta']
        sizes = [tempo_espera, tempo_consulta_medio]
        if sum(sizes) > 0:
            axs[1, 1].pie(sizes, labels=labels, autopct='%1.1f%%', colors=['#e74c3c', '#27ae60'], startangle=90)
        else:
            axs[1, 1].text(0.5, 0.5, 'Sem dados de tempo', ha='center')
        axs[1, 1].set_title('Distribuição do Tempo do Paciente')

        figure_agg = desenhar_figura(window['-CANVAS-'].TKCanvas, fig)

    if dados_memoria:
        atualizar_dashboard(dados_memoria, "Simulação Recente (Memória)")

    while True:
        event, values = window.read()
        if event in (sg.WINDOW_CLOSED, '-BACK-'): break

        if event == '-LOAD_FILE-':
            filepath = sg.popup_get_file('Selecione arquivo .json', file_types=(("Arquivos JSON", "*.json"),), no_window=True)
            if filepath:
                dados_json = carregar_dados_json(filepath)
                if dados_json:
                    atualizar_dashboard(dados_json, "Arquivo JSON")

    window.close()
    return 'voltar'