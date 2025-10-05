# criar lista com números do usuário
def criar_lista_usuario():
    lista = []
    n = int(input("Quantos números deseja adicionar à lista? "))
    for i in range(n):
        numero = int(input(f"Digite o {i+1}º número: "))
        lista.append(numero)
    return lista

# Função para somar os elementos da lista
def somaLista(lista):
    soma = 0
    i = 1
    while i < len(lista):
        soma = soma + lista[i]
        i = i + 1
    return soma

# Função para calcular a média dos elementos da lista
def mediaLista(lista):
    soma = 0
    i = 1
    while i < len(lista):
        soma = soma + lista[i]
        i = i + 1
    media = soma / len(lista)
    return media

# Função para encontrar o maior elemento da lista
def maiorLista(lista):
    lista.sort()
    return lista[-1:]

# Função para encontrar o menor elemento da lista
def menorLista(lista):
    menor = float('inf')
    for num in lista:
        if num < menor:
            menor = num
    return menor

# Função para saber se a lista está ordenada de forma crescente
def estaOrdenadaC(lista):
    maior = float('inf')
    i = len(lista) - 1
    while i >= 0 and lista[i] <= maior:
        maior = lista[i]
        i = i - 1
    return i == -1

# Função para saber se a lista está ordenada de forma decrescente
def estaOrdenadaD(lista):
    menor = float('-inf')
    i = len(lista) - 1
    while i >= 0 and lista[i] >= menor:
        menor = lista[i]
        i = i - 1
    return i == -1

# Função para procurar um elemento na lista
def indice(lista, elemento):
    for i in range(len(lista)):
        if lista[i] == elemento:
            return i
    return -1




# exibir o menu e as opções
def menu():
    lista = []
    continuar = True
    while continuar:
        print("\nMenu:")
        print("(1) Criar Lista")
        print("(2) Ler Lista")
        print("(3) Soma")
        print("(4) Média")
        print("(5) Maior")
        print("(6) Menor")
        print("(7) Está Ordenada Crescente")
        print("(8) Está Ordenada Decrescente")
        print("(9) Procurar Elemento")
        print("(0) Sair")
        
        escolha = int(input("Escolha uma opção: "))
        if escolha == 1:
            lista = criar_lista_usuario()
            print("Lista criada:", lista)
        elif escolha == 2:
            print("Lista atual:", lista)
        elif escolha == 3:
            print("Soma:", somaLista(lista))
        elif escolha == 4:
            print("Média:", mediaLista(lista) if lista else "Lista vazia")
        elif escolha == 5:
            print("Maior:", maiorLista(lista) if lista else "Lista vazia")
        elif escolha == 6:
            print("Menor:", menorLista(lista) if lista else "Lista vazia")
        elif escolha == 7:
            print("Está ordenada de forma crescente?", "Sim" if estaOrdenadaC(lista) else "Não")
        elif escolha == 8:
            print("Está ordenada de forma decrescente?", "Sim" if estaOrdenadaD(lista) else "Não")
        elif escolha == 9:
            elemento = int(input("Digite o número a procurar: "))
            print("Elemento encontrado na posição:", indice(lista, elemento))
        elif escolha == 0:
            print("A sair. Lista final:", lista)
            continuar = False  # sair do loop
        else:
            print("Opção inválida!")


menu()

