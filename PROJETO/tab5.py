import FreeSimpleGUI as sg
import json
import os
import datetime
import random

# ============================================================================
# DESIGN SYSTEM - MEDCORE ENTERPRISE
# ============================================================================
COR_SIDEBAR = '#1e272e'
COR_BG_MAIN = '#f4f6f7'
COR_CARD = '#ffffff'
COR_ACCENT = '#e67e22'  # Cor de Engenharia
COR_VERDE = '#27ae60'
COR_VERMELHO = '#c0392b'
COR_TEXTO = '#2f3640'

# ============================================================================
# LÓGICA DE DADOS (COM MAPEAMENTO DINÂMICO)
# ============================================================================
class GestorEquipamentos:
    def __init__(self):
        self.arquivo = 'equipamentos.json'
        self.dados = []
        self.carregar()

    def carregar(self):
        if os.path.exists(self.arquivo):
            f = open(self.arquivo, 'r', encoding='utf-8')
            self.dados = json.load(f)
            f.close()
        
        if len(self.dados) == 0:
            self.dados = [
                {"id": "EQ_IMG_012", "nome": "Mamógrafo Pristina", "tipo": "Imagiologia", "estado": "Operacional", "custo_reparacao": 0, "nivel": 1, "proxima_manutencao": "2026-03-01"}
            ]
            self.salvar()

    def salvar(self):
        f = open(self.arquivo, 'w', encoding='utf-8')
        json.dump(self.dados, f, indent=4)
        f.close()

    def alterar_estado(self, id_eq, novo_estado):
        for eq in self.dados:
            if eq.get('id') == id_eq:
                eq['estado'] = novo_estado
                # Lógica de custos simulada
                custo = 0
                if novo_estado == 'Avariado': custo = random.randint(800, 6000)
                eq['custo_reparacao'] = custo
        self.salvar()

    def upgrade(self, id_eq):
        for eq in self.dados:
            if eq.get('id') == id_eq:
                eq['nivel'] = eq.get('nivel', 1) + 1
        self.salvar()

    def get_tabela(self, filtro=""):
        lista = []
        f = filtro.lower()
        for eq in self.dados:
            nome = eq.get('nome', 'N/A')
            setor = eq.get('tipo', eq.get('localizacao', 'Geral'))
            if f == "" or f in nome.lower() or f in setor.lower():
                est = eq.get('estado', 'Operacional')
                icon = "🟢"
                if est == 'Avariado': icon = "🔴"
                if est == 'Em Manutenção': icon = "🟠"
                
                lista.append([eq.get('id'), nome, setor, f"{icon} {est}", f"v{eq.get('nivel', 1)}.0"])
        return lista

    def get_estatisticas(self):
        total = len(self.dados)
        operacionais = 0
        custo_total = 0
        for e in self.dados:
            if e.get('estado') == 'Operacional': operacionais = operacionais + 1
            custo_total = custo_total + e.get('custo_reparacao', 0)
        
        uptime = 0
        if total > 0: uptime = int((operacionais / total) * 100)
        return total, uptime, custo_total

# ============================================================================
# COMPONENTES DE INTERFACE
# ============================================================================
def card_estatistico(titulo, valor, cor, k):
    return sg.Column([
        [sg.Text(titulo, font=('Segoe UI', 9), text_color='gray', background_color=COR_CARD)],
        [sg.Text(valor, font=('Segoe UI', 18, 'bold'), text_color=cor, background_color=COR_CARD, key=k)]
    ], background_color=COR_CARD, size=(220, 80), pad=(10, 10))

# ============================================================================
# MAIN
# ============================================================================
def main():
    sg.theme('SystemDefault')
    gestor = GestorEquipamentos()
    
    # --- SIDEBAR COM COMANDOS ---
    sidebar = [
        [sg.Text('MEDCORE ASSETS', font=('Segoe UI', 14, 'bold'), text_color='white', background_color=COR_SIDEBAR, pad=(20, 30))],
        [sg.Text('AÇÕES TÉCNICAS', font=('Segoe UI', 8, 'bold'), text_color='gray', background_color=COR_SIDEBAR, pad=(20, 5))],
        [sg.Button(' 🛠  Registar Avaria', key='-BREAK-', size=(22, 2), button_color=('white', '#34495e'), border_width=0)],
        [sg.Button(' ✅  Concluir Reparação', key='-FIX-', size=(22, 2), button_color=('white', '#34495e'), border_width=0)],
        [sg.Button(' ⬆  Upgrade Tech', key='-UPGRADE-', size=(22, 2), button_color=('white', '#34495e'), border_width=0)],
        [sg.Push(background_color=COR_SIDEBAR)],
        [sg.Button('⬅  VOLTAR AO HUB', key='-BACK-', button_color=('white', COR_VERMELHO), border_width=0, size=(22, 2), pad=(0, 20))]
    ]

    # --- ÁREA DE CONTEÚDO ---
    tot, up, custo = gestor.get_estatisticas()
    dados_tab = gestor.get_tabela()

    cabecalho = [
        [sg.Text('Engenharia Clínica & Manutenção', font=('Segoe UI', 22, 'bold'), background_color=COR_BG_MAIN, text_color=COR_TEXTO),
         sg.Push(background_color=COR_BG_MAIN),
         sg.Text('Pesquisa:', background_color=COR_BG_MAIN), sg.Input(key='-SEARCH-', size=(25,1), enable_events=True)]
    ]

    painel_resumo = [
        card_estatistico('Ativos Totais', f"{tot}", COR_SIDEBAR, '-KPI_T-'),
        card_estatistico('Disponibilidade (Uptime)', f"{up}%", COR_VERDE, '-KPI_U-'),
        card_estatistico('Encargo de Manutenção', f"{custo} €", COR_VERMELHO, '-KPI_C-')
    ]

    # Layout da Tabela e Detalhes
    col_tabela = sg.Column([
        [sg.Table(values=dados_tab, headings=['ID ATIVO', 'EQUIPAMENTO', 'SETOR/TIPO', 'ESTADO', 'VERSÃO'],
                  auto_size_columns=False, col_widths=[15, 30, 15, 15, 10],
                  justification='left', key='-TABLE-', row_height=40, num_rows=12,
                  font=('Segoe UI', 10), background_color='white', alternating_row_color='#f9f9f9',
                  enable_events=True, expand_x=True, border_width=0)]
    ], background_color=COR_BG_MAIN, pad=(0, 20))

    col_detalhes = sg.Column([
        [sg.Text('Ficha Técnica', font=('Segoe UI', 12, 'bold'), background_color=COR_CARD, text_color=COR_ACCENT)],
        [sg.HorizontalSeparator(color=COR_BG_MAIN)],
        [sg.Text('Selecione um ativo para visualizar os detalhes técnicos e histórico de intervenções.', 
                 key='-DET_TXT-', size=(25, 10), font=('Segoe UI', 10), background_color=COR_CARD, text_color='gray')]
    ], background_color=COR_CARD, size=(300, 480), pad=(20, 20))

    layout = [[
        sg.Column(sidebar, background_color=COR_SIDEBAR, size=(260, 900), expand_y=True, pad=(0,0)),
        sg.Column([cabecalho[0], painel_resumo, [col_tabela, col_detalhes]], background_color=COR_BG_MAIN, expand_x=True, expand_y=True, pad=(40, 40))
    ]]

    window = sg.Window('MedCore - Gestão de Ativos', layout, background_color=COR_BG_MAIN, finalize=True)
    window.maximize()

    rodando = True
    selecionado_id = None
    
    while rodando:
        ev, val = window.read()
        
        if ev in (sg.WINDOW_CLOSED, '-BACK-'):
            rodando = False

        if ev == '-SEARCH-':
            dados_tab = gestor.get_tabela(val['-SEARCH-'])
            window['-TABLE-'].update(values=dados_tab)

        if ev == '-TABLE-':
            if len(val['-TABLE-']) > 0:
                idx = val['-TABLE-'][0]
                selecionado_id = dados_tab[idx][0]
                
                # Busca detalhe para o painel lateral
                for item in gestor.dados:
                    if item.get('id') == selecionado_id:
                        det = f"ID: {item.get('id')}\n" \
                              f"Nome: {item.get('nome')}\n" \
                              f"Setor: {item.get('tipo', 'Geral')}\n" \
                              f"Versão: v{item.get('nivel')}.0\n" \
                              f"Manutenção: {item.get('proxima_manutencao', 'N/A')}\n\n" \
                              f"ESTADO: {item.get('estado')}\n" \
                              f"Custo Reparação: {item.get('custo_reparacao', 0)} €"
                        window['-DET_TXT-'].update(det, text_color=COR_TEXTO)

        if ev == '-BREAK-' and selecionado_id:
            gestor.alterar_estado(selecionado_id, 'Avariado')
            dados_tab = gestor.get_tabela(val['-SEARCH-'])
            window['-TABLE-'].update(values=dados_tab)
                
        if ev == '-FIX-' and selecionado_id:
            gestor.alterar_estado(selecionado_id, 'Operacional')
            dados_tab = gestor.get_tabela(val['-SEARCH-'])
            window['-TABLE-'].update(values=dados_tab)

        if ev == '-UPGRADE-' and selecionado_id:
            gestor.upgrade(selecionado_id)
            dados_tab = gestor.get_tabela(val['-SEARCH-'])
            window['-TABLE-'].update(values=dados_tab)

        # Atualização Global de KPIs
        t_n, u_n, c_n = gestor.get_estatisticas()
        window['-KPI_T-'].update(f"{t_n}")
        window['-KPI_U-'].update(f"{u_n}%")
        window['-KPI_C-'].update(f"{c_n} €")

    window.close()

if __name__ == '__main__':
    main()