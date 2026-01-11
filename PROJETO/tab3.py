import FreeSimpleGUI as sg
import json
import os
import random

# ============================================================================
# DESIGN SYSTEM - MEDCORE 360
# ============================================================================
COR_SIDEBAR = '#1e272e'
COR_BG_MAIN = '#f4f6f7'
COR_CARD = '#ffffff'
COR_ACCENT = '#0fb9b1'
COR_VERMELHO = '#e74c3c'
COR_VERDE = '#27ae60'
COR_AZUL = '#3498db'
COR_TEXTO = '#2f3640'

# ============================================================================
# LÓGICA DE DADOS
# ============================================================================
class GestorPacientes:
    def __init__(self):
        self.arquivo = 'pessoas.json'
        self.dados = []
        self.carregar()

    def carregar(self):
        if os.path.exists(self.arquivo):
            f = open(self.arquivo, 'r', encoding='utf-8')
            self.dados = json.load(f)
            f.close()

    def salvar(self):
        f = open(self.arquivo, 'w', encoding='utf-8')
        json.dump(self.dados, f, indent=4, ensure_ascii=False)
        f.close()

    def verificar_risco(self, paciente):
        idade = paciente.get('idade', 0)
        fuma = paciente.get('atributos', {}).get('fumador', False)
        if idade > 65: return "SIM", "Grupo: Geriatria (Idade > 65)"
        if fuma: return "SIM", "Grupo: Fumador (Risco Cardiovascular)"
        return "NÃO", "Baixo Risco"

    def get_tabela(self, filtro="", apenas_risco=False):
        lista = []
        f = filtro.lower()
        for p in self.dados:
            nome = p.get('nome', 'N/A')
            cc = p.get('CC', p.get('BI', '---'))
            risco_sn, _ = self.verificar_risco(p)
            if (f == "" or f in nome.lower() or f in str(cc).lower()) and (not apenas_risco or risco_sn == "SIM"):
                lista.append([p.get('id'), nome, p.get('idade'), cc, risco_sn])
        return lista

# ============================================================================
# JANELA DE FICHA TÉCNICA (LEITURA)
# ============================================================================
def janela_ficha_tecnica(p):
    morada = p.get('morada', {})
    atributos = p.get('atributos', {})
    partido = p.get('partido_politico', {})
    BG_SECTION = '#f8f9fa'
    
    def info_row(label, value):
        return [sg.Text(f"{label}:", font=('Segoe UI', 9, 'bold'), background_color=BG_SECTION, size=(15,1)),
                sg.Text(f"{value}", font=('Segoe UI', 10), background_color=BG_SECTION, text_color=COR_TEXTO)]

    layout_info = [
        [sg.Text(f"👤 {p.get('nome').upper()}", font=('Segoe UI', 16, 'bold'), text_color=COR_ACCENT)],
        [sg.Text(f"ID: {p.get('id')} | DOC: {p.get('BI', p.get('CC', '---'))}", font=('Segoe UI', 9), text_color='gray')],
        [sg.HorizontalSeparator(pad=(0, 15))],
        
        [sg.Column([
            [sg.Text('DADOS BIOGRÁFICOS', font=('Segoe UI', 8, 'bold'), text_color=COR_AZUL, background_color=BG_SECTION)],
            info_row('Idade', f"{p.get('idade')} anos"),
            info_row('Género', str(p.get('sexo')).capitalize()),
            info_row('Profissão', p.get('profissao', '---')),
            info_row('Localidade', f"{morada.get('cidade')} / {morada.get('distrito')}")
        ], background_color=BG_SECTION, pad=(0, 10), expand_x=True)],

        [sg.Column([
            [sg.Text('PERFIL SOCIAL E SAÚDE', font=('Segoe UI', 8, 'bold'), text_color=COR_AZUL, background_color=BG_SECTION)],
            info_row('Fumador', 'Sim' if atributos.get('fumador') else 'Não'),
            info_row('Religião', p.get('religiao', 'Não declarado')),
            info_row('Partido', f"{partido.get('party_name', '---')} ({partido.get('party_abbr', '')})")
        ], background_color=BG_SECTION, pad=(0, 10), expand_x=True)],

        [sg.Column([
            [sg.Text('INTERESSES', font=('Segoe UI', 8, 'bold'), text_color=COR_AZUL, background_color=BG_SECTION)],
            [sg.Text('Desportos:', font=('Segoe UI', 9, 'bold'), background_color=BG_SECTION)],
            [sg.Text(", ".join(p.get('desportos', [])), font=('Segoe UI', 9, 'italic'), background_color=BG_SECTION, size=(50, 2))],
        ], background_color=BG_SECTION, pad=(0, 10), expand_x=True)],

        [sg.Text('OBSERVAÇÕES', font=('Segoe UI', 8, 'bold'), text_color='gray')],
        [sg.Multiline(p.get('descricao', 'Sem observações.'), size=(60, 3), disabled=True, font=('Segoe UI', 9))],
        [sg.Push(), sg.Button('FECHAR', size=(12, 1), button_color=('white', COR_SIDEBAR), pad=(0, 10))]
    ]

    sg.Window('Dossiê Estruturado', layout_info, modal=True, background_color='white').read(close=True)

# ============================================================================
# FORMULÁRIO DE EDIÇÃO (COM VALIDAÇÃO)
# ============================================================================
def janela_formulario(paciente=None):
    p = paciente if paciente else {"nome": "", "idade": "", "CC": "", "profissao": "", "morada": {"cidade": ""}, "atributos": {"fumador": False}}
    
    layout = [
        [sg.Text('EDITOR DE UTENTE', font=('Segoe UI', 12, 'bold'), text_color=COR_ACCENT)],
        [sg.Text('Nome:'), sg.Input(p.get('nome'), key='-N-')],
        [sg.Text('Idade:'), sg.Input(p.get('idade'), key='-I-', size=(5,1)), sg.Text('CC/BI:'), sg.Input(p.get('CC', p.get('BI', '')), key='-C-')],
        [sg.Text('Cidade:'), sg.Input(p.get('morada',{}).get('cidade'), key='-CID-')],
        [sg.Checkbox('Fumador Ativo', default=p.get('atributos',{}).get('fumador'), key='-FUM-')],
        [sg.Button('GUARDAR', button_color=('white', COR_VERDE)), sg.Button('CANCELAR', button_color=('white', COR_VERMELHO))]
    ]
    
    win = sg.Window('Editor', layout, modal=True)
    
    res = None
    rodando_form = True
    
    while rodando_form:
        ev, vals = win.read()
        
        if ev in (sg.WINDOW_CLOSED, 'CANCELAR'):
            rodando_form = False
            
        if ev == 'GUARDAR':
            # --- VALIDAÇÕES ---
            
            # 1. Validação da Idade: Apenas números
            idade_input = str(vals['-I-']).strip()
            if not idade_input.isdigit():
                sg.popup_error('A idade deve conter apenas números inteiros.', title='Erro de Validação')
                continue # Volta ao loop, não fecha a janela
            
            # 2. Validação da Cidade: Não pode conter números
            cidade_input = str(vals['-CID-'])
            if any(char.isdigit() for char in cidade_input):
                sg.popup_error('O nome da cidade não pode conter números.', title='Erro de Validação')
                continue
            
            # 3. Validação do Nome: Não pode conter números (aplicado à lógica de "número e cidade")
            nome_input = str(vals['-N-'])
            if any(char.isdigit() for char in nome_input):
                sg.popup_error('O nome não pode conter números.', title='Erro de Validação')
                continue

            # Se passou nas validações, guarda os dados
            res = p.copy()
            res.update({"nome": nome_input, "idade": int(idade_input), "CC": vals['-C-']})
            
            if 'morada' not in res: res['morada'] = {}
            res['morada']['cidade'] = cidade_input
            
            if 'atributos' not in res: res['atributos'] = {}
            res['atributos']['fumador'] = vals['-FUM-']
            
            if not p.get('id'): res['id'] = f"p{random.randint(1000, 9999)}"
            
            rodando_form = False
            
    win.close()
    return res

# ============================================================================
# MAIN INTERFACE
# ============================================================================
def main():
    sg.theme('SystemDefault')
    gestor = GestorPacientes()
    
    sidebar = [
        [sg.Text('MEDCORE 360', font=('Segoe UI', 14, 'bold'), text_color='white', background_color=COR_SIDEBAR, pad=(20, 30))],
        [sg.Button(' ➕  Novo Utente', key='-ADD-', size=(22, 2), button_color=('white', '#34495e'), border_width=0)],
        [sg.Button(' 📝  Editar Dados', key='-EDIT-', size=(22, 2), button_color=('white', '#34495e'), border_width=0)],
        [sg.Button(' 🔍  Ficha Técnica', key='-FICHA-', size=(22, 2), button_color=('white', '#34495e'), border_width=0)],
        [sg.Canvas(size=(0, 10), background_color=COR_SIDEBAR)],
        [sg.Button(' 🩺  Triagem Rápida', key='-TRIAGEM-', size=(22, 2), button_color=('white', '#f39c12'), border_width=0)],
        [sg.Button(' 📑  Ver Todos', key='-RESET-', size=(22, 2), button_color=('white', COR_AZUL), border_width=0)],
        [sg.Push(background_color=COR_SIDEBAR)],
        [sg.Button(' 🗑️  Remover', key='-DEL-', size=(22, 2), button_color=('white', COR_VERMELHO), border_width=0)],
        [sg.Button('⬅  VOLTAR', key='-BACK-', button_color=('white', COR_VERMELHO), border_width=0, size=(22, 2), pad=(0, 20))]
    ]

    dados_tab = gestor.get_tabela()

    col_diretorio = sg.Column([
        [sg.Text('Diretório de Utentes', font=('Segoe UI', 18, 'bold'), background_color=COR_BG_MAIN), 
         sg.Push(background_color=COR_BG_MAIN), 
         sg.Input(key='-SEARCH-', size=(20,1), enable_events=True), sg.Text('🔍', background_color=COR_BG_MAIN)],
        [sg.Table(values=dados_tab, headings=['ID', 'NOME', 'IDADE', 'DOC. ID', 'RISCO'], 
                  auto_size_columns=False, col_widths=[8, 30, 6, 15, 8], 
                  key='-TABLE-', row_height=35, num_rows=15, 
                  font=('Segoe UI', 10), enable_events=True, expand_x=True)]
    ], background_color=COR_BG_MAIN, expand_x=True, expand_y=True)

    col_perfil = sg.Column([
        [sg.Text('RESUMO DO PERFIL', font=('Segoe UI', 12, 'bold'), text_color=COR_ACCENT, background_color=COR_CARD)],
        [sg.HorizontalSeparator(color=COR_BG_MAIN, pad=(0,10))],
        [sg.Text('Selecione um utente...', key='-DET_NOME-', font=('Segoe UI', 11, 'bold'), background_color=COR_CARD, size=(25, 2))],
        [sg.Text('Profissão:', font=('Segoe UI', 9, 'bold'), background_color=COR_CARD), sg.Text('-', key='-DET_PROF-', background_color=COR_CARD)],
        [sg.Text('Cidade:', font=('Segoe UI', 9, 'bold'), background_color=COR_CARD), sg.Text('-', key='-DET_MOR-', background_color=COR_CARD)],
        [sg.Frame(' STATUS DE RISCO ', [
            [sg.Text('-', key='-DET_RISCO_SN-', font=('Segoe UI', 12, 'bold'), background_color='#fff5f5')],
            [sg.Text('-', key='-DET_RISCO_TIPO-', font=('Segoe UI', 8, 'italic'), size=(25, 2), background_color='#fff5f5', text_color=COR_VERMELHO)]
        ], background_color='#fff5f5', border_width=1, expand_x=True)],
    ], background_color=COR_CARD, size=(300, 480), pad=(20, 20))

    layout = [[sg.Column(sidebar, background_color=COR_SIDEBAR, size=(260, 900), expand_y=True, pad=(0,0)),
               sg.Column([[col_diretorio, col_perfil]], background_color=COR_BG_MAIN, expand_x=True, expand_y=True, pad=(40, 40))]]

    window = sg.Window('MedCore Admin', layout, finalize=True)
    window.maximize()

    selecionado = None
    rodando = True
    
    while rodando:
        ev, val = window.read()
        if ev in (sg.WINDOW_CLOSED, '-BACK-'): rodando = False

        if ev in ('-SEARCH-', '-RESET-'):
            if ev == '-RESET-': window['-SEARCH-'].update('')
            dados_tab = gestor.get_tabela(window['-SEARCH-'].get())
            window['-TABLE-'].update(values=dados_tab)

        if ev == '-TRIAGEM-':
            dados_tab = gestor.get_tabela(window['-SEARCH-'].get(), apenas_risco=True)
            window['-TABLE-'].update(values=dados_tab)

        if ev == '-TABLE-':
            if len(val['-TABLE-']) > 0:
                idx = val['-TABLE-'][0]
                if idx < len(dados_tab):
                    pid = dados_tab[idx][0]
                    selecionado = next((p for p in gestor.dados if p['id'] == pid), None)
                    if selecionado:
                        window['-DET_NOME-'].update(f"{selecionado['nome']}")
                        window['-DET_PROF-'].update(selecionado.get('profissao', '---'))
                        window['-DET_MOR-'].update(selecionado.get('morada', {}).get('cidade', '---'))
                        sn, tipo = gestor.verificar_risco(selecionado)
                        window['-DET_RISCO_SN-'].update(sn, text_color=COR_VERMELHO if sn == "SIM" else COR_VERDE)
                        window['-DET_RISCO_TIPO-'].update(tipo)

        if ev == '-FICHA-' and selecionado:
            janela_ficha_tecnica(selecionado)

        if ev == '-EDIT-' and selecionado:
            res = janela_formulario(selecionado)
            if res:
                for i, p in enumerate(gestor.dados):
                    if p['id'] == selecionado['id']: gestor.dados[i] = res
                gestor.salvar()
                dados_tab = gestor.get_tabela(val['-SEARCH-'])
                window['-TABLE-'].update(values=dados_tab)

        if ev == '-ADD-':
            res = janela_formulario()
            if res:
                gestor.dados.append(res)
                gestor.salvar()
                dados_tab = gestor.get_tabela()
                window['-TABLE-'].update(values=dados_tab)
                
        if ev == '-DEL-' and selecionado:
            if sg.popup_yes_no(f"Remover utente {selecionado['nome']}?") == 'Yes':
                gestor.dados = [p for p in gestor.dados if p['id'] != selecionado['id']]
                gestor.salvar()
                dados_tab = gestor.get_tabela()
                window['-TABLE-'].update(values=dados_tab)
                selecionado = None

    window.close()

if __name__ == '__main__': main()