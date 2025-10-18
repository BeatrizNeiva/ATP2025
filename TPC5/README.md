# TPC5: Aplicação para gestão de alunos

## Beatriz Sousa Neiva  A107241

## Objetivos:

Considere que o modelo do aluno e da turma têm a seguinte estrutura:

`aluno = (nome, id, [notaTPC, notaProj, notaTeste])`

`turma = [aluno]`

* Cria uma aplicação que coloca no monitor o seguinte menu de operações:
    - 1: Criar uma turma;
    - 2: Inserir um aluno na turma;
    - 3: Listar a turma;
    - 4: Consultar um aluno por id;
    - 8: Guardar a turma em ficheiro;
    - 9: Carregar uma turma dum ficheiro;
    - 0: Sair da aplicação
* No fim de executar a operação selecionada, a aplicação deverá colocar novamente o menu e pedir ao utilizador a opção para continuar;
* Utiliza a tua aplicação para criar uma turma com 5 alunos.

* NOTA: Na pasta do TPC5, encontra-se um exemplo de ficheiro que pode ser carregado, denominado "TPC5_turmas.txt".

## Resultados
``` python

<img width="1081" height="6def mostrar_menu():
    print("\n--- Menu de Operações ---")
    print("1: Criar uma turma")
    print("2: Inserir um aluno na turma")
    print("3: Listar a turma")
    print("4: Consultar um aluno por id")
    print("8: Guardar a turma em ficheiro")
    print("9: Carregar uma turma dum ficheiro")
    print("0: Sair da aplicação")

def criar_turma():
    return []

def inserir_aluno(turma):
    nome = input("Nome do aluno: ")
    id = input("ID do aluno: ")
    notaTPC = float(input("Nota do TPC: "))
    notaProj = float(input("Nota do Projeto: "))
    notaTeste = float(input("Nota do Teste: "))
    aluno = (nome, id, [notaTPC, notaProj, notaTeste])
    turma.append(aluno)
    print("Aluno inserido com sucesso.")

def listar_turma(turma):
    if len(turma) == 0:
        print("Turma vazia.")
    else:
        print("\n--- Lista de Alunos ---")
        for aluno in turma:
            print("Nome:", aluno[0], "| ID:", aluno[1], "| Notas:", aluno[2])

def consultar_aluno(turma):
    id = input("Introduza o ID do aluno a consultar: ")
    encontrado = False
    for aluno in turma:
        if aluno[1] == id:
            print("Aluno encontrado:")
            print("Nome:", aluno[0])
            print("Notas:", aluno[2])
            encontrado = True
    if not encontrado:
        print("Aluno não encontrado.")

def guardar_turma(turma):
    nome_ficheiro = input("Nome do ficheiro para guardar (ex: TPC5_turmas.txt): ")
    ficheiro = open(nome_ficheiro, "w")
    for aluno in turma:
        linha = aluno[0] + ";" + aluno[1] + ";" + ",".join(str(n) for n in aluno[2]) + "\n"
        ficheiro.write(linha)
    ficheiro.close()
    print("Turma guardada com sucesso.")

def carregar_turma():
    nome_ficheiro = input("Nome do ficheiro a carregar (ex: TPC5_turmas.txt): ")
    turma = []
    ficheiro = open(nome_ficheiro, "r")
    linhas = ficheiro.readlines()
    for linha in linhas:
        linha = linha.strip()
        if linha != "":
            partes = linha.split(";")
            if len(partes) == 3:
                nome = partes[0]
                id = partes[1]
                notas_texto = partes[2].split(",")
                if len(notas_texto) == 3:
                    notas = [float(n) for n in notas_texto]
                    aluno = (nome, id, notas)
                    turma.append(aluno)
    ficheiro.close()
    print("Turma carregada com sucesso.")
    return turma

# Programa principal
turma = []
opcao = "início"

while opcao != "0":
    mostrar_menu()
    opcao = input("Escolha uma opção: ")

    if opcao == "1":
        turma = criar_turma()
        print("Turma criada.")
    elif opcao == "2":
        inserir_aluno(turma)
    elif opcao == "3":
        listar_turma(turma)
    elif opcao == "4":
        consultar_aluno(turma)
    elif opcao == "8":
        guardar_turma(turma)
    elif opcao == "9":
        turma = carregar_turma()
    elif opcao == "0":
        print("A sair da aplicação.")
    else:
        print("Opção inválida.")
```
