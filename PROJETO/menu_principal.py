import FreeSimpleGUI as sg
import json
import os
import datetime

# Importação direta dos módulos (assume-se que os ficheiros existem na mesma pasta)
import tab1
import tab2
import tab3
import tab4
import tab5

# ============================================================================
# DESIGN SYSTEM - MEDCORE PROFESSIONAL
# ============================================================================
COR_SIDEBAR = '#2c3e50'
COR_BG_MAIN = '#ecf0f1'
COR_CARD = '#ffffff'
COR_ACCENT = '#1abc9c'
COR_TEXTO = '#2c3e50'
COR_DANGER = '#e74c3c'
COR_SUCCESS = '#27ae60'
COR_DISABLED = '#95a5a6'

# Configuração de Utilizadores
USUARIOS = {
    "joana":  {"pass": "joana123", "nome": "Dra. Joana",      "cargo": "Diretora Clínica", "perfil": "clinico"},
    "isabel": {"pass": "isabel123", "nome": "Isabel Silva",    "cargo": "Gestora Hospitalar", "perfil": "gestao"}
}

# Definição de Permissões
PERMISSOES = {
    "clinico": ["-BTN_TAB1-", "-BTN_TAB2-"],
    "gestao":  ["-BTN_TAB3-", "-BTN_TAB4-", "-BTN_TAB5-"]
}

# ============================================================================
# FUNÇÕES DE DADOS (SEM TRY/EXCEPT)
# ============================================================================
def carregar_estatisticas():
    n_pacientes = 0
    n_medicos = 0
    
    # Verifica existência antes de abrir para evitar erro sem try/except
    if os.path.exists('pessoas.json'):
        f = open('pessoas.json', 'r', encoding='utf-8')
        dados = json.load(f)
        f.close()
        n_pacientes = len(dados)
        
    if os.path.exists('medicos.json'):
        f = open('medicos.json', 'r', encoding='utf-8')
        dados = json.load(f)
        f.close()
        n_medicos = len(dados)
        
    return n_pacientes, n_medicos

def lancar_modulo(nome_modulo):
    # Chamada direta sem tratamento de erro
    if nome_modulo == 'tab1': tab1.main()
    if nome_modulo == 'tab2': tab2.main()
    if nome_modulo == 'tab3': tab3.main()
    if nome_modulo == 'tab4': tab4.main()
    if nome_modulo == 'tab5': tab5.main()

# ============================================================================
# COMPONENTES UI
# ============================================================================
def criar_card_kpi(titulo, valor, icon, cor_texto):
    return sg.Column([
        [sg.Text(titulo, font=('Segoe UI', 8, 'bold'), text_color='gray', background_color=COR_CARD)],
        [sg.Text(valor, font=('Segoe UI', 20, 'bold'), text_color=cor_texto, background_color=COR_CARD),
         sg.Push(background_color=COR_CARD),
         sg.Text(icon, font=('Segoe UI', 20), text_color='#ecf0f1', background_color=COR_CARD)]
    ], background_color=COR_CARD, size=(200, 90), pad=(10, 10), expand_x=True)

def btn_menu(titulo, subtexto, key, icon):
    return sg.Button(f"{icon}  {titulo}\n      {subtexto}", key=key, 
                     font=('Segoe UI', 10), size=(28, 3), 
                     button_color=(COR_TEXTO, '#ffffff'),
                     mouseover_colors=(COR_TEXTO, '#dfe6e9'),
                     border_width=0, pad=(0, 5))

# ============================================================================
# JANELA DE LOGIN
# ============================================================================
def janela_login():
    sg.theme('SystemDefault')
    
    layout = [
        [sg.Column([
            [sg.Text('MedCore', font=('Segoe UI', 30, 'bold'), text_color=COR_SIDEBAR, background_color=COR_CARD, pad=(0,0))],
            [sg.Text('HOSPITAL MANAGEMENT SYSTEM', font=('Segoe UI', 8, 'bold'), text_color=COR_ACCENT, background_color=COR_CARD, pad=(0,20))],
            
            [sg.Text('Utilizador', font=('Segoe UI', 9, 'bold'), background_color=COR_CARD, text_color='gray')],
            [sg.Input(key='-USER-', size=(35, 1), font=('Segoe UI', 10), border_width=1)],
            
            [sg.Text('Palavra-passe', font=('Segoe UI', 9, 'bold'), background_color=COR_CARD, text_color='gray', pad=((0,0),(10,0)))],
            [sg.Input(key='-PASS-', size=(35, 1), password_char='●', font=('Segoe UI', 10), border_width=1)],
            
            [sg.Text('', key='-MSG-', text_color=COR_DANGER, background_color=COR_CARD, size=(35, 1), justification='center')],
            
            [sg.Button('INICIAR SESSÃO', key='-LOGIN-', size=(32, 2), button_color=('white', COR_ACCENT), font=('Segoe UI', 9, 'bold'), border_width=0, pad=(0, 15))],
            [sg.Button('Cancelar e Sair', key='-CANCEL-', size=(32, 1), button_color=('gray', COR_CARD), font=('Segoe UI', 9), border_width=0)]
        ], background_color=COR_CARD, element_justification='c', pad=(40, 40))]
    ]
    
    window = sg.Window('Login', [[sg.Column(layout, background_color=COR_CARD, element_justification='c')]], 
                       no_titlebar=True, grab_anywhere=True, background_color='#bdc3c7', finalize=True)
    
    usuario_validado = None
    rodando_login = True
    
    while rodando_login:
        ev, vals = window.read()
        
        if ev == sg.WINDOW_CLOSED:
            rodando_login = False
            
        if ev == '-CANCEL-':
            rodando_login = False
            
        if ev == '-LOGIN-':
            u = vals['-USER-'].lower().strip()
            p = vals['-PASS-'].strip()
            
            if u in USUARIOS:
                # Verificação separada para evitar lógica complexa numa linha
                if USUARIOS[u]['pass'] == p:
                    usuario_validado = USUARIOS[u]
                    rodando_login = False
                else:
                    window['-MSG-'].update('Credenciais incorretas.')
            else:
                window['-MSG-'].update('Credenciais incorretas.')
                
    window.close()
    return usuario_validado

# ============================================================================
# MENU PRINCIPAL (DASHBOARD)
# ============================================================================
def janela_dashboard(user):
    sg.theme('SystemDefault')
    perfil = user['perfil']
    hoje = datetime.datetime.now().strftime("%d de %B, %Y")
    
    # Carregar dados
    n_pac, n_med = carregar_estatisticas()
    
    # 1. SIDEBAR
    col_sidebar = [
        [sg.Text('MedCore', font=('Segoe UI', 22, 'bold'), text_color='white', background_color=COR_SIDEBAR, pad=(20, 30))],
        
        [sg.Image(data=sg.DEFAULT_BASE64_ICON, background_color=COR_SIDEBAR, pad=(20,0))],
        [sg.Text(f"Olá, {user['nome']}", font=('Segoe UI', 11, 'bold'), text_color='white', background_color=COR_SIDEBAR, pad=(20, 2))],
        [sg.Text(user['cargo'], font=('Segoe UI', 9), text_color=COR_ACCENT, background_color=COR_SIDEBAR, pad=(20, (0,30)))],
        
        [sg.Text('NAVEGAÇÃO', font=('Segoe UI', 8, 'bold'), text_color='#95a5a6', background_color=COR_SIDEBAR, pad=(20, 5))],
        
        [btn_menu('Simulação', 'Gestão de Cenários', '-BTN_TAB1-', '📈')],
        [btn_menu('Business Intel.', 'Análise de Dados', '-BTN_TAB2-', '📊')],
        [btn_menu('Gestão Pacientes', 'Fichas e Triagem', '-BTN_TAB3-', '👥')],
        [btn_menu('Recursos Humanos', 'Médicos e Staff', '-BTN_TAB4-', '👨‍⚕️')],
        [btn_menu('Equipamentos', 'Manutenção Técnica', '-BTN_TAB5-', '🛠️')],
        
        [sg.Push(background_color=COR_SIDEBAR)],
        [sg.Button('TERMINAR SESSÃO', key='-LOGOUT-', button_color=('white', COR_DANGER), border_width=0, size=(25, 2), pad=(20, 30))]
    ]
    
    # 2. CONTEÚDO PRINCIPAL
    col_content = [
        [sg.Text(hoje, font=('Segoe UI', 10), text_color='gray', background_color=COR_BG_MAIN), 
         sg.Push(background_color=COR_BG_MAIN),
         sg.Text('● Sistema Online', text_color=COR_SUCCESS, font=('Segoe UI', 9, 'bold'), background_color=COR_BG_MAIN)],
        
        [sg.Text(f'Painel de Controlo - {user["cargo"]}', font=('Segoe UI', 24, 'bold'), background_color=COR_BG_MAIN, text_color=COR_TEXTO)],
        [sg.HorizontalSeparator(pad=(0, 20))],
        
        [sg.Text('ESTATÍSTICAS GERAIS', font=('Segoe UI', 10, 'bold'), background_color=COR_BG_MAIN, text_color='gray')],
        [
            criar_card_kpi('TOTAL PACIENTES', str(n_pac), '👥', COR_SIDEBAR),
            criar_card_kpi('CORPO CLÍNICO', str(n_med), '👨‍⚕️', COR_ACCENT),
            criar_card_kpi('SERVIDORES', 'Ativos', '🖥️', COR_SUCCESS)
        ],
        
        [sg.Canvas(size=(0, 20), background_color=COR_BG_MAIN)],
        
        [sg.Column([
            [sg.Text('FUNCIONALIDADES DISPONÍVEIS', font=('Segoe UI', 12, 'bold'), background_color=COR_CARD, text_color=COR_TEXTO)],
            [sg.Text('Selecione uma opção no menu lateral para aceder aos módulos.', background_color=COR_CARD, text_color='gray')],
            [sg.Multiline(
                "PERMISSÕES DE ACESSO:\n" + 
                ("✅ Simulação e BI\n❌ Dados Pessoais\n❌ Gestão Técnica" if perfil == 'clinico' else "❌ Simulação Clínica\n✅ Gestão de Utentes\n✅ RH e Equipamentos"),
                size=(50, 6), disabled=True, no_scrollbar=True, background_color='#f8f9fa', border_width=0, font=('Consolas', 10), text_color=COR_TEXTO)
            ]
        ], background_color=COR_CARD, size=(500, 200), pad=(10,0), expand_x=True)]
    ]
    
    layout = [[
        sg.Column(col_sidebar, background_color=COR_SIDEBAR, size=(280, 700), expand_y=True, pad=(0,0)),
        sg.Column(col_content, background_color=COR_BG_MAIN, expand_x=True, expand_y=True, pad=(40, 40))
    ]]
    
    window = sg.Window('MedCore - Menu Principal', layout, resizable=True, finalize=True, background_color=COR_BG_MAIN)
    window.maximize()
    
    # Bloqueio de permissões
    permitidos = []
    if perfil in PERMISSOES:
        permitidos = PERMISSOES[perfil]
    
    botoes_todos = ["-BTN_TAB1-", "-BTN_TAB2-", "-BTN_TAB3-", "-BTN_TAB4-", "-BTN_TAB5-"]
    
    for btn in botoes_todos:
        permite = False
        for p in permitidos:
            if p == btn:
                permite = True
        
        if not permite:
            window[btn].update(disabled=True, button_color=('#bdc3c7', COR_SIDEBAR))

    logout_acionado = False
    rodando_dash = True
    
    while rodando_dash:
        ev, val = window.read()
        
        if ev == sg.WINDOW_CLOSED:
            rodando_dash = False
            
        if ev == '-LOGOUT-':
            resposta = sg.popup_yes_no("Deseja realmente terminar a sessão?", title="Logout")
            if resposta == 'Yes':
                logout_acionado = True
                rodando_dash = False
        
        # Navegação
        if ev in permitidos:
            window.hide()
            mod_limpo = ev.replace('-BTN_', '').lower().replace('-', '')
            lancar_modulo(mod_limpo)
            # Recarregar stats
            n_p, n_m = carregar_estatisticas()
            window.un_hide()
            
    window.close()
    return logout_acionado

# ============================================================================
# MAIN LOOP
# ============================================================================
def main():
    app_ativa = True
    
    while app_ativa:
        usuario = janela_login()
        
        if usuario:
            logout = janela_dashboard(usuario)
            if not logout:
                app_ativa = False
        else:
            app_ativa = False

if __name__ == '__main__':
    main()