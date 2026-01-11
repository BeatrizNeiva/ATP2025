import FreeSimpleGUI as sg
import json
import os
import random
import time

# ============================================================================
# DESIGN SYSTEM - MEDCORE RH
# ============================================================================
COR_SIDEBAR = '#2c3e50'
COR_BG_MAIN = '#f4f6f7'
COR_CARD = '#ffffff'
COR_ACCENT = '#9b59b6'      # Roxo (Recursos Humanos)
COR_TEXTO = '#2f3640'
COR_VERDE = '#27ae60'
COR_AMARELO = '#f1c40f'
COR_VERMELHO = '#e74c3c'
COR_CINZA = '#95a5a6'

# ============================================================================
# LÓGICA DE DADOS (GESTOR DE RH)
# ============================================================================
class GestorRH:
    def __init__(self):
        self.arquivo = 'medicos.json'
        self.dados = []
        self.carregar()

    def carregar(self):
        if os.path.exists(self.arquivo):
            try:
                with open(self.arquivo, 'r', encoding='utf-8') as f:
                    self.dados = json.load(f)
            except:
                self.dados = []
        
        if not self.dados:
            self.gerar_dummies()
        
        self.enriquecer_dados()

    def gerar_dummies(self):
        nomes = ["Dr. António Silva", "Dra. Maria Santos", "Dr. João Costa", "Dra. Ana Pereira"]
        esps = ["Cardiologia", "Pediatria", "Neurologia", "Clínica Geral"]
        for i, (n, e) in enumerate(zip(nomes, esps)):
            self.dados.append({"id": f"m{1000+i}", "nome": n, "especialidade": e, "status": "Ativo"})

    def enriquecer_dados(self):
        """Gera dados financeiros realistas (Média ~42.000€/ano)"""
        for m in self.dados:
            if 'id' not in m or not m['id']:
                m['id'] = f"m_auto_{random.randint(10000, 99999)}"

            # Lógica de Faturação Ajustada (~42k)
            faturacao_atual = m.get('faturacao', 0)
            if faturacao_atual == 0 or faturacao_atual > 80000:
                m['faturacao'] = random.randint(30000, 54000)
                preco_medio = random.randint(60, 90)
                m['consultas_ano'] = int(m['faturacao'] / preco_medio)
            elif m.get('consultas_ano', 0) == 0:
                 preco_medio = random.randint(60, 90)
                 m['consultas_ano'] = int(m['faturacao'] / preco_medio)

            if 'rating' not in m: m['rating'] = round(random.uniform(3.5, 5.0), 1)
            if 'assiduidade' not in m: m['assiduidade'] = random.randint(90, 100)
            if 'status_pagamento' not in m: m['status_pagamento'] = 'Em Dia'

    def salvar(self):
        with open(self.arquivo, 'w', encoding='utf-8') as f:
            json.dump(self.dados, f, indent=4, ensure_ascii=False)

    def get_tabela(self, filtro=""):
        lista = []
        f = filtro.lower() if filtro else ""
        for m in self.dados:
            nome = m.get('nome', 'Sem Nome')
            esp = m.get('especialidade', 'Geral')
            if f == "" or f in nome.lower() or f in esp.lower():
                fat = f"{m.get('faturacao', 0):,.2f}€"
                lista.append([m.get('id'), nome, esp, fat, m.get('rating', 'N/A')])
        return lista

    def atualizar_medico(self, dados_novos):
        """Atualiza um médico existente ou adiciona se for novo"""
        for i, m in enumerate(self.dados):
            if m.get('id') == dados_novos.get('id'):
                self.dados[i].update(dados_novos)
                return
        self.dados.append(dados_novos)

# ============================================================================
# COMPONENTES VISUAIS
# ============================================================================
def card_stat(titulo, valor, cor_texto, bg=COR_CARD):
    return sg.Column([
        [sg.Text(titulo, font=('Segoe UI', 8, 'bold'), text_color='gray', background_color=bg)],
        [sg.Text(valor, key=f'-ST_{titulo}-', font=('Segoe UI', 16, 'bold'), text_color=cor_texto, background_color=bg)]
    ], background_color=bg, size=(140, 60), pad=(5,5))

def formulario_medico(medico=None):
    m = medico if medico else {}
    titulo = f"EDITAR: {m.get('nome')}" if medico else "NOVO MÉDICO"
    
    layout = [
        [sg.Text(titulo, font=('Segoe UI', 12, 'bold'), text_color=COR_ACCENT)],
        [sg.HorizontalSeparator()],
        [sg.Text('Nome Completo:', size=(15,1)), sg.Input(m.get('nome', ''), key='-N-', size=(30,1))],
        [sg.Text('Especialidade:', size=(15,1)), sg.Combo(['Cardiologia', 'Pediatria', 'Neurologia', 'Clínica Geral', 'Ortopedia', 'Dermatologia'], default_value=m.get('especialidade', ''), key='-E-', size=(28,1))],
        [sg.Text('Estado Atual:', size=(15,1)), sg.Combo(['Ativo', 'Férias', 'Baixa', 'Licença'], default_value=m.get('status', 'Ativo'), key='-S-', size=(28,1))],
        [sg.Canvas(size=(0, 10))],
        [sg.Button('GUARDAR', button_color=('white', COR_VERDE), size=(15,1)), sg.Button('CANCELAR', size=(10,1))]
    ]
    win = sg.Window('Editor RH', layout, modal=True, keep_on_top=True)
    ev, val = win.read()
    res = None
    if ev == 'GUARDAR':
        if not val['-N-'] or not val['-E-']:
            sg.popup_error("Nome e Especialidade são obrigatórios!")
        else:
            res = m.copy()
            res.update({'nome': val['-N-'], 'especialidade': val['-E-'], 'status': val['-S-']})
            
            # Se for novo, gera ID e dados iniciais
            if 'id' not in res: res['id'] = f"m{random.randint(2000,9999)}"
            if 'consultas_ano' not in res: res['consultas_ano'] = 0 
            if 'faturacao' not in res: res['faturacao'] = 0
            if 'rating' not in res: res['rating'] = 5.0
            if 'assiduidade' not in res: res['assiduidade'] = 100
    win.close()
    return res

# ============================================================================
# MAIN
# ============================================================================
def main():
    sg.theme('SystemDefault')
    gestor = GestorRH()
    
    # --- SIDEBAR ---
    sidebar = [
        [sg.Text('MEDCORE RH', font=('Segoe UI', 14, 'bold'), text_color='white', background_color=COR_SIDEBAR, pad=(20, 30))],
        [sg.Button(' ➕  Novo Médico', key='-ADD-', size=(22, 2), button_color=('white', '#34495e'), border_width=0)],
        [sg.Button(' 📝  Editar Ficha', key='-EDIT-', size=(22, 2), button_color=('white', '#34495e'), border_width=0)],
        [sg.Canvas(size=(0, 10), background_color=COR_SIDEBAR)],
        [sg.Button(' 💰  Processar Salários', key='-PAY-', size=(22, 2), button_color=('white', COR_VERDE), border_width=0)],
        [sg.Push(background_color=COR_SIDEBAR)],
        [sg.Button(' 🗑️  Remover', key='-DEL-', size=(22, 2), button_color=('white', COR_VERMELHO), border_width=0)],
        [sg.Button('⬅  VOLTAR', key='-BACK-', button_color=('white', COR_VERMELHO), border_width=0, size=(22, 2), pad=(0, 20))]
    ]

    # --- LISTA ---
    dados_tab = gestor.get_tabela()
    col_lista = sg.Column([
        [sg.Text('Corpo Clínico', font=('Segoe UI', 18, 'bold'), background_color=COR_BG_MAIN), 
         sg.Push(background_color=COR_BG_MAIN),
         sg.Input(key='-SEARCH-', size=(20,1), enable_events=True), sg.Text('🔍', background_color=COR_BG_MAIN)],
        
        [sg.Table(values=dados_tab, headings=['ID', 'NOME', 'ESPECIALIDADE', 'FATURAÇÃO (Ano)', 'RATING'], 
                  auto_size_columns=False, col_widths=[6, 25, 15, 15, 8],
                  key='-TABLE-', row_height=35, num_rows=14, justification='left',
                  font=('Segoe UI', 10), enable_events=True, expand_x=True,
                  alternating_row_color='#f9f9f9', select_mode=sg.TABLE_SELECT_MODE_BROWSE)]
    ], background_color=COR_BG_MAIN, expand_x=True, expand_y=True)

    # --- DETALHE ---
    col_detalhe = sg.Column([
        [sg.Text('PERFIL PROFISSIONAL', font=('Segoe UI', 12, 'bold'), text_color=COR_ACCENT, background_color=COR_CARD)],
        [sg.HorizontalSeparator(pad=(0,15))],
        
        [sg.Text('Selecione um médico...', key='-D_NOME-', font=('Segoe UI', 16, 'bold'), background_color=COR_CARD)],
        [sg.Text('-', key='-D_SPEC-', font=('Segoe UI', 10), text_color='gray', background_color=COR_CARD)],
        
        [sg.Canvas(size=(0, 20), background_color=COR_CARD)],
        
        [sg.Frame(' PERFORMANCE ANUAL ', [
            [card_stat('CONSULTAS', '-', COR_SIDEBAR), card_stat('FATURAÇÃO', '-', COR_VERDE)],
            [card_stat('AVALIAÇÃO', '-', COR_AMARELO), card_stat('ASSIDUIDADE', '-', COR_ACCENT)]
        ], background_color=COR_CARD, border_width=1, expand_x=True)],
        
        [sg.Canvas(size=(0, 20), background_color=COR_CARD)],
        
        [sg.Text('Status Contratual:', font=('Segoe UI', 9, 'bold'), background_color=COR_CARD)],
        [sg.Text('-', key='-D_STATUS-', background_color='#ecf0f1', size=(30, 1), pad=(0,5))],
        
    ], background_color=COR_CARD, size=(350, 600), pad=(20, 0), expand_y=True)

    layout = [[
        sg.Column(sidebar, background_color=COR_SIDEBAR, size=(260, 900), expand_y=True, pad=(0,0)),
        sg.Column([[col_lista, col_detalhe]], background_color=COR_BG_MAIN, expand_x=True, expand_y=True, pad=(40, 40))
    ]]

    window = sg.Window('MedCore - Recursos Humanos', layout, background_color=COR_BG_MAIN, finalize=True)
    window.maximize()

    selecionado = None

    while True:
        ev, val = window.read()
        if ev in (sg.WINDOW_CLOSED, '-BACK-'): break

        # PESQUISA
        if ev == '-SEARCH-':
            dados_tab = gestor.get_tabela(val['-SEARCH-'])
            window['-TABLE-'].update(values=dados_tab)

        # SELEÇÃO NA TABELA
        if ev == '-TABLE-' and val['-TABLE-']:
            idx = val['-TABLE-'][0]
            if idx < len(dados_tab):
                mid = dados_tab[idx][0]
                selecionado = next((m for m in gestor.dados if m.get('id') == mid), None)
                
                if selecionado:
                    window['-D_NOME-'].update(selecionado.get('nome', 'Sem Nome'))
                    window['-D_SPEC-'].update(selecionado.get('especialidade', '-'))
                    window['-D_STATUS-'].update(selecionado.get('status', 'Ativo'))
                    
                    window['-ST_CONSULTAS-'].update(selecionado.get('consultas_ano', 0))
                    window['-ST_FATURAÇÃO-'].update(f"{selecionado.get('faturacao', 0):,.2f}€")
                    window['-ST_AVALIAÇÃO-'].update(f"{selecionado.get('rating', 0)}/5.0")
                    window['-ST_ASSIDUIDADE-'].update(f"{selecionado.get('assiduidade', 0)}%")

        # ➕ ADICIONAR
        if ev == '-ADD-':
            res = formulario_medico(None) # None = Novo
            if res:
                gestor.atualizar_medico(res)
                gestor.enriquecer_dados()
                gestor.salvar()
                dados_tab = gestor.get_tabela(val['-SEARCH-'])
                window['-TABLE-'].update(values=dados_tab)
                sg.popup_quick_message("Médico adicionado!", text_color='white', background_color=COR_VERDE)

        # 📝 EDITAR
        if ev == '-EDIT-':
            if selecionado:
                res = formulario_medico(selecionado) # Passa o selecionado
                if res:
                    gestor.atualizar_medico(res)
                    gestor.salvar()
                    
                    # Atualiza tabela e detalhe visual
                    dados_tab = gestor.get_tabela(val['-SEARCH-'])
                    window['-TABLE-'].update(values=dados_tab)
                    
                    # Atualiza o detalhe imediatamente
                    window['-D_NOME-'].update(res.get('nome'))
                    window['-D_SPEC-'].update(res.get('especialidade'))
                    window['-D_STATUS-'].update(res.get('status'))
                    selecionado = res # Atualiza a referência local
                    
                    sg.popup_quick_message("Dados atualizados!", text_color='white', background_color=COR_ACCENT)
            else:
                sg.popup("Por favor, selecione um médico na tabela primeiro.", title="Seleção Necessária")

        # 💰 PROCESSAR SALÁRIOS
        if ev == '-PAY-':
            if not gestor.dados:
                sg.popup_error("Não existem médicos para processar.")
            else:
                total_estimado = sum([m.get('faturacao', 0)/12 for m in gestor.dados]) * 0.7 # Ex: 70% da faturação mensal é salário
                confirm = sg.popup_ok_cancel(f"Processar salários para {len(gestor.dados)} médicos?\n\nTotal Estimado (Mês): {total_estimado:,.2f}€", title="Folha de Pagamentos")
                
                if confirm == 'OK':
                    # Simulação visual de processamento
                    sg.popup_quick_message("A contactar sistema bancário...", background_color=COR_SIDEBAR)
                    time.sleep(1.5)
                    
                    # Atualiza status de pagamento
                    for m in gestor.dados:
                        m['status_pagamento'] = 'Pago'
                    gestor.salvar()
                    
                    sg.popup(f"Sucesso! Pagamentos processados.", title="Concluído")

        # 🗑️ REMOVER
        if ev == '-DEL-':
            if selecionado:
                if sg.popup_yes_no(f"Tem a certeza que deseja remover:\n{selecionado.get('nome')}?", title="Confirmar Remoção") == 'Yes':
                    gestor.dados = [m for m in gestor.dados if m.get('id') != selecionado.get('id')]
                    gestor.salvar()
                    
                    dados_tab = gestor.get_tabela(val['-SEARCH-'])
                    window['-TABLE-'].update(values=dados_tab)
                    
                    # Limpa detalhes
                    selecionado = None
                    window['-D_NOME-'].update('Selecione um médico...')
                    window['-D_SPEC-'].update('-')
                    window['-D_STATUS-'].update('-')
                    window['-ST_FATURAÇÃO-'].update('-')
            else:
                sg.popup("Selecione um médico para remover.")

    window.close()

if __name__ == '__main__':
    main()