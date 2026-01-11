import FreeSimpleGUI as sg
import random
import math
import statistics
import time
import datetime
import json
import os
import tab2

# ============================================================================
# DESIGN SYSTEM
# ============================================================================
COR_SIDEBAR = '#2c3e50'
COR_BG_MAIN = '#ecf0f1'
COR_CARD = '#ffffff'
COR_ACCENT = '#2980b9'
COR_TEXTO = '#2f3640'
COR_VERDE = '#27ae60'
COR_VERMELHO = '#e74c3c'
COR_LARANJA = '#d35400'

# ============================================================================
# CLASSE: PACIENTE
# ============================================================================
class Paciente:
    def __init__(self, id_p, tempo_chegada):
        self.id = id_p
        self.tempo_chegada = tempo_chegada
        self.inicio_atendimento = None
        self.fim_atendimento = None
        self.duracao_servico = 0

# ============================================================================
# FUNÇÕES AUXILIARES
# ============================================================================
def gerar_tempo_servico(dist, media):
    if dist == 'Exponencial':
        return random.expovariate(1.0 / media)
    elif dist == 'Normal':
        t = random.gauss(media, media * 0.2)
        return max(1, t)
    elif dist == 'Uniforme':
        return random.uniform(media * 0.5, media * 1.5)
    return media

def correr_simulacao_rapida(taxa_hora, medicos, dist, media_serv, duracao):
    t_atual = 0
    fila_q = 0
    med_livres = medicos
    prox_chegada = random.expovariate(taxa_hora/60)
    eventos = []
    soma_fila = 0
    
    while t_atual < duracao:
        if not eventos: dt = prox_chegada - t_atual
        else: dt = min(prox_chegada, eventos[0]) - t_atual
        if dt <= 0: dt = 0.001
        t_atual += dt
        soma_fila += fila_q * dt 

        if abs(t_atual - prox_chegada) < 0.001:
            if med_livres > 0:
                med_livres -= 1
                dur = gerar_tempo_servico(dist, media_serv)
                eventos.append(t_atual + dur)
                eventos.sort()
            else:
                fila_q += 1
            prox_chegada += random.expovariate(taxa_hora/60)
        
        if eventos and abs(t_atual - eventos[0]) < 0.001:
            eventos.pop(0)
            if fila_q > 0:
                fila_q -= 1
                dur = gerar_tempo_servico(dist, media_serv)
                eventos.append(t_atual + dur)
                eventos.sort()
            else:
                med_livres += 1
                
    return soma_fila / duracao if duracao > 0 else 0

# ============================================================================
# INTERFACE PRINCIPAL
# ============================================================================
def main():
    sg.theme('SystemDefault')
    
    # --- SIDEBAR ---
    sidebar = [
        [sg.Text('MEDCORE SIM', font=('Segoe UI', 14, 'bold'), text_color='white', background_color=COR_SIDEBAR, pad=(20, 30))],
        [sg.Text('CONTROLO', font=('Segoe UI', 8, 'bold'), text_color='#95a5a6', background_color=COR_SIDEBAR, pad=(20, 5))],
        
        [sg.Button(' ⚙️  Configurar', key='-CFG-', size=(22, 2), button_color=('white', '#34495e'), border_width=0)],
        [sg.Button(' 💾  Salvar Relatório', key='-SAVE-', size=(22, 2), button_color=('white', '#34495e'), border_width=0)],
        
        [sg.HorizontalSeparator(color='#34495e', pad=(20, 20))],
        [sg.Button(' 📊  Ir para Análise (BI)', key='-GOTO_TAB2-', size=(22, 2), button_color=('white', COR_ACCENT), border_width=0)],
        [sg.Push(background_color=COR_SIDEBAR)],
        [sg.Button('⬅  VOLTAR AO MENU', key='-BACK-', button_color=('white', COR_VERMELHO), border_width=0, size=(22, 2), pad=(0, 20))]
    ]

    # --- CONFIGURAÇÃO (Scrollable) ---
    layout_params = [
        [sg.Text('1. Parâmetros Base', font=('Segoe UI', 10, 'bold'), text_color=COR_ACCENT)],
        
        [sg.Text('Taxa Chegada (Pac/Hora):', font=('Segoe UI', 8))],
        [sg.Slider((10, 100), default_value=40, orientation='h', size=(28, 15), key='-LAMBDA-')],
        
        [sg.Text('Médicos:', font=('Segoe UI', 8)), sg.Push(), sg.Spin([i for i in range(1, 51)], initial_value=5, key='-MEDICOS-', size=(5,1))],
        [sg.Text('Média Consulta (min):', font=('Segoe UI', 8)), sg.Push(), sg.Spin([i for i in range(5, 120)], initial_value=15, key='-MEDIA_SERV-', size=(5,1))],
        [sg.Text('Duração Simulação (min):', font=('Segoe UI', 8)), sg.Push(), sg.Input('480', key='-DURACAO-', size=(5,1))],
        
        [sg.Text('Distribuição:', font=('Segoe UI', 8))],
        [sg.Combo(['Exponencial', 'Normal', 'Uniforme'], default_value='Exponencial', key='-DIST-', size=(25,1), readonly=True)],

        [sg.HorizontalSeparator(pad=(0, 10))],

        # --- NOVA SECÇÃO: AVARIA DE EQUIPAMENTOS ---
        [sg.Text('2. Avaria de Equipamentos', font=('Segoe UI', 10, 'bold'), text_color=COR_LARANJA)],
        [sg.Checkbox('Ativar Falhas de Sistema', default=False, key='-AVARIA_CHECK-', font=('Segoe UI', 9))],
        
        [sg.Text('Probabilidade Falha (%/hora):', font=('Segoe UI', 8))],
        [sg.Slider((1, 50), default_value=10, orientation='h', size=(28, 15), key='-AVARIA_PROB-')],
        
        [sg.Text('Tempo Reparação (min):', font=('Segoe UI', 8)), sg.Push(), sg.Spin([i for i in range(5, 120)], initial_value=30, key='-AVARIA_REPAIR-', size=(5,1))],
        
        [sg.Canvas(size=(0, 20))],
        [sg.Button('INICIAR SIMULAÇÃO', key='-START-', size=(25, 2), button_color=('white', COR_VERDE), font=('Segoe UI', 10, 'bold'), border_width=0)],
        [sg.Button('PARAR', key='-STOP-', size=(25, 2), button_color=('white', COR_VERMELHO), font=('Segoe UI', 10, 'bold'), border_width=0, pad=(0,10))]
    ]

    col_config = sg.Column(layout_params, background_color=COR_CARD, size=(320, 650), pad=(10, 0), expand_y=True, scrollable=True, vertical_scroll_only=True)

    # --- MONITORIZAÇÃO ---
    col_monitor = sg.Column([
        [sg.Text('Monitorização em Tempo Real', font=('Segoe UI', 12, 'bold'), text_color=COR_TEXTO, background_color=COR_CARD),
         sg.Push(background_color=COR_CARD),
         sg.Text('SISTEMA:', background_color=COR_CARD, font=('Segoe UI', 8, 'bold')),
         sg.Text(' ONLINE ', key='-STATUS_SYS-', background_color=COR_VERDE, text_color='white', font=('Segoe UI', 8, 'bold'), pad=(5,0))], # Indicador de Status
        [sg.HorizontalSeparator(pad=(0, 15))],
        
        [sg.ProgressBar(100, orientation='h', size=(20, 20), key='-PROG-', bar_color=(COR_ACCENT, '#dfe6e9'), expand_x=True)],
        [sg.Text('Status: Aguardando...', key='-STATUS-', font=('Segoe UI', 9, 'italic'), background_color=COR_CARD, text_color='gray')],
        
        [sg.Text('Fila de Espera Atual:', background_color=COR_CARD, font=('Segoe UI', 9, 'bold'))],
        [sg.Text('', key='-VISUAL_FILA-', font=('Segoe UI Symbol', 16), text_color=COR_VERMELHO, background_color=COR_CARD, size=(50, 1))],
        [sg.Text('Médicos Ocupados:', background_color=COR_CARD, font=('Segoe UI', 9, 'bold'))],
        [sg.Text('', key='-VISUAL_MED-', font=('Segoe UI Symbol', 16), text_color=COR_VERDE, background_color=COR_CARD, size=(50, 1))],

        [sg.Multiline("Log de eventos...", key='-LOG-', size=(50, 15), font=('Consolas', 9), 
                      background_color='#f8f9fa', text_color='#2d3436', border_width=1, expand_x=True, expand_y=True, autoscroll=True)],
        
        [sg.Frame(' Resultados Preliminares ', [
            [sg.Text('Fila Atual:', background_color=COR_CARD), sg.Text('0', key='-R_FILA-', font=('Segoe UI', 9, 'bold'), text_color=COR_ACCENT, background_color=COR_CARD)],
            [sg.Text('Ocupação:', background_color=COR_CARD), sg.Text('0%', key='-R_OCUP-', font=('Segoe UI', 9, 'bold'), text_color=COR_VERMELHO, background_color=COR_CARD)]
        ], background_color=COR_CARD, expand_x=True, pad=(0, 10))]

    ], background_color=COR_CARD, expand_x=True, expand_y=True, pad=(10, 0))

    layout = [[
        sg.Column(sidebar, background_color=COR_SIDEBAR, size=(260, 900), expand_y=True, pad=(0,0)),
        sg.Column([[col_config, col_monitor]], background_color=COR_BG_MAIN, expand_x=True, expand_y=True, pad=(40, 40))
    ]]

    window = sg.Window('MedCore - Simulação Clínica', layout, background_color=COR_BG_MAIN, finalize=True, resizable=True)
    window.maximize()

    # Variáveis de Estado
    rodando = True
    simulando = False
    dados_exportacao = {}

    while rodando:
        ev, val = window.read(timeout=50 if simulando else None)
        
        if ev in (sg.WINDOW_CLOSED, '-BACK-'): rodando = False

        # --- PRESETS (CONFIGURAR) ---
        if ev == '-CFG-':
            layout_cfg = [
                [sg.Text('Selecione um Cenário:', font=('Segoe UI', 10, 'bold'))],
                [sg.Combo(['Dia Normal', 'Caos: Avarias Frequentes', 'Sobrecarga de Doentes'], 
                          default_value='Dia Normal', key='-CENARIO-', size=(30, 1))],
                [sg.Button('Aplicar', key='-APPLY-', button_color=COR_ACCENT)]
            ]
            w_cfg = sg.Window('Presets', layout_cfg, modal=True, keep_on_top=True)
            e_cfg, v_cfg = w_cfg.read()
            w_cfg.close()

            if e_cfg == '-APPLY-':
                cenario = v_cfg['-CENARIO-']
                if cenario == 'Dia Normal':
                    window['-LAMBDA-'].update(40)
                    window['-MEDICOS-'].update(5)
                    window['-AVARIA_CHECK-'].update(False)
                elif cenario == 'Caos: Avarias Frequentes':
                    window['-LAMBDA-'].update(35)
                    window['-MEDICOS-'].update(5)
                    window['-AVARIA_CHECK-'].update(True)
                    window['-AVARIA_PROB-'].update(30) # 30% prob/hora
                    window['-AVARIA_REPAIR-'].update(45) # Demora muito a arranjar
                elif cenario == 'Sobrecarga de Doentes':
                    window['-LAMBDA-'].update(90)
                    window['-AVARIA_CHECK-'].update(False)
                
                sg.popup_quick_message(f"Cenário '{cenario}' aplicado!", background_color=COR_VERDE)

        # --- SALVAR (JSON) ---
        if ev == '-SAVE-':
            if not dados_exportacao:
                sg.popup_error("Sem dados para salvar!")
            else:
                filename = sg.popup_get_file('Salvar Dados', save_as=True, no_window=True, 
                                           default_extension='.json', file_types=(("JSON", "*.json"),))
                if filename:
                    try:
                        with open(filename, 'w', encoding='utf-8') as f:
                            json.dump(dados_exportacao, f, indent=4)
                        sg.popup("Salvo com sucesso!")
                    except Exception as e:
                        sg.popup_error(f"Erro: {e}")

        # --- IR PARA TAB 2 ---
        if ev == '-GOTO_TAB2-':
            if not dados_exportacao:
                sg.popup_error("Execute a simulação primeiro!")
            else:
                window.hide()
                ret = tab2.main(dados_exportacao)
                if ret == 'menu': rodando = False 
                else: window.un_hide()

        # --- START SIMULAÇÃO ---
        if ev == '-START-':
            try:
                taxa_chegada = float(val['-LAMBDA-'])
                num_medicos = int(val['-MEDICOS-'])
                dist_tipo = val['-DIST-']
                media_servico = float(val['-MEDIA_SERV-'])
                tempo_total_sim = int(val['-DURACAO-'])
                
                # Dados da Avaria
                usar_avaria = val['-AVARIA_CHECK-']
                prob_avaria_hora = float(val['-AVARIA_PROB-'])
                tempo_reparo = int(val['-AVARIA_REPAIR-'])

            except ValueError:
                sg.popup_error("Verifique os valores numéricos!")
                continue

            simulando = True
            window['-LOG-'].update(f"INÍCIO (λ={taxa_chegada}, Avaria={usar_avaria})\n" + "-"*40 + "\n")
            
            tempo_atual = 0.0
            fila = [] 
            medicos_livres = num_medicos
            proxima_chegada = random.expovariate(taxa_chegada / 60)
            eventos_saida = []

            # Estado do Equipamento
            sistema_online = True
            tempo_reparo_restante = 0

            historico_fila = []
            historico_ocupacao = []
            pacientes_atendidos = []
            contador_pacientes = 0
            tempo_sistema_online = 0.0

            while tempo_atual < tempo_total_sim and simulando:
                passo = 1.0 
                tempo_atual += passo
                
                # --- 1. LÓGICA DE AVARIA ---
                if usar_avaria:
                    if sistema_online:
                        tempo_sistema_online += passo
                        # Verifica se avaria agora (Probabilidade por minuto)
                        # A prob input é por hora, dividimos por 60 para estimar por minuto
                        chance_minuto = (prob_avaria_hora / 100.0) / 60.0
                        if random.random() < chance_minuto:
                            sistema_online = False
                            tempo_reparo_restante = tempo_reparo
                            window['-STATUS_SYS-'].update(' ERROR ', background_color=COR_VERMELHO)
                            window['-LOG-'].print(f"[{tempo_atual:.1f}m] ⚠ ALERTA: O Sistema foi abaixo! Triagem suspensa.")
                    else:
                        # Sistema está em baixo, reparar
                        tempo_reparo_restante -= passo
                        if tempo_reparo_restante <= 0:
                            sistema_online = True
                            window['-STATUS_SYS-'].update(' ONLINE ', background_color=COR_VERDE)
                            window['-LOG-'].print(f"[{tempo_atual:.1f}m] ✅ SUCESSO: Sistema recuperado. Retomando atendimento.")
                
                # --- 2. Processar Chegadas ---
                while tempo_atual >= proxima_chegada:
                    contador_pacientes += 1
                    p = Paciente(contador_pacientes, proxima_chegada)
                    
                    # Só entra em atendimento direto se houver médicos E o sistema estiver online
                    if medicos_livres > 0 and sistema_online:
                        medicos_livres -= 1
                        p.inicio_atendimento = proxima_chegada
                        p.duracao_servico = gerar_tempo_servico(dist_tipo, media_servico)
                        p.fim_atendimento = proxima_chegada + p.duracao_servico
                        eventos_saida.append(p)
                        window['-LOG-'].print(f"[{proxima_chegada:.1f}m] P{p.id} -> Consulta.")
                    else:
                        fila.append(p)
                        status_str = "FILA (Sistema OFF)" if not sistema_online else "FILA (Sem médicos)"
                        window['-LOG-'].print(f"[{proxima_chegada:.1f}m] P{p.id} -> {status_str}.")
                    
                    proxima_chegada += random.expovariate(taxa_chegada / 60)

                # --- 3. Processar Saídas (Médicos terminam consulta) ---
                eventos_saida.sort(key=lambda x: x.fim_atendimento)
                
                novos_eventos = []
                for p in eventos_saida:
                    if p.fim_atendimento <= tempo_atual:
                        medicos_livres += 1
                        pacientes_atendidos.append(p)
                        window['-LOG-'].print(f"[{p.fim_atendimento:.1f}m] P{p.id} Alta. (Dur: {p.duracao_servico:.1f}m)")
                        
                        # Tenta puxar o próximo da fila
                        # IMPORTANTE: Só puxa se o sistema estiver ONLINE
                        if fila and medicos_livres > 0 and sistema_online:
                            prox = fila.pop(0)
                            medicos_livres -= 1
                            prox.inicio_atendimento = tempo_atual
                            prox.duracao_servico = gerar_tempo_servico(dist_tipo, media_servico)
                            prox.fim_atendimento = tempo_atual + prox.duracao_servico
                            novos_eventos.append(prox)
                            window['-LOG-'].print(f"[{tempo_atual:.1f}m] P{prox.id} Saiu da Fila -> Consulta.")
                    else:
                        novos_eventos.append(p)
                eventos_saida = novos_eventos

                # --- 4. Atualizar UI ---
                ev_loop, _ = window.read(timeout=10)
                if ev_loop == '-STOP-': simulando = False

                ocupados = num_medicos - medicos_livres
                historico_fila.append((tempo_atual, len(fila)))
                historico_ocupacao.append((tempo_atual, (ocupados/num_medicos)*100))

                window['-PROG-'].update((tempo_atual/tempo_total_sim)*100)
                msg_status = f'Simulando... (Sistema: {"ON" if sistema_online else "OFF"})'
                window['-STATUS-'].update(msg_status)
                window['-R_FILA-'].update(f"{len(fila)}")
                window['-R_OCUP-'].update(f"{(ocupados/num_medicos)*100:.1f}%")
                
                # Visual bonecos (limita a 20 para não estourar o layout)
                window['-VISUAL_FILA-'].update('🚶' * min(len(fila), 20))
                window['-VISUAL_MED-'].update('👨‍⚕️' * ocupados + '⚪' * medicos_livres)

            # --- FIM SIMULAÇÃO ---
            window['-STATUS-'].update('Concluído. Gerando dados...')
            
            tempos_espera = [(p.inicio_atendimento - p.tempo_chegada) for p in pacientes_atendidos]
            media_espera = statistics.mean(tempos_espera) if tempos_espera else 0
            
            # Cálculo de dados para BI
            dados_sensibilidade = {} 
            for taxa_teste in range(10, 35, 5):
                f_media = correr_simulacao_rapida(taxa_teste, num_medicos, dist_tipo, media_servico, tempo_total_sim)
                dados_sensibilidade[taxa_teste] = f_media

            dados_exportacao = {
                'historico_fila': historico_fila,
                'historico_ocupacao': historico_ocupacao,
                'sensibilidade': dados_sensibilidade,
                'metricas': {
                    'total_pacientes': len(pacientes_atendidos),
                    'espera_media': media_espera,
                    'consulta_media': media_servico, # Adicionado para o Tab 2 usar
                    'ocupacao_media': statistics.mean([x[1] for x in historico_ocupacao]) if historico_ocupacao else 0,
                    'max_fila': max([x[1] for x in historico_fila]) if historico_fila else 0,
                    'uptime': (tempo_sistema_online / tempo_total_sim) * 100
                },
                'log_texto': window['-LOG-'].get()
            }
            
            window['-STATUS-'].update('Pronto. Pode salvar ou analisar.')
            sg.popup_quick_message("Simulação Concluída!", background_color=COR_VERDE)

    window.close()

if __name__ == '__main__':
    main()