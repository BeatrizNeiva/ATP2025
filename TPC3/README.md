# TPC3: Aplicação para manipulação de listas de inteiros

## Beatriz Sousa Neiva  A107241

## Resumo da aula TP
Algoritmos sobre listas.

## Objetivos 
- Crie uma aplicação em Python que coloca no monitor o seguinte menu:
    * (1) Criar Lista 
    * (2) Ler Lista
    * (3) Soma
    * (4) Média
    * (5) Maior
    * (6) Menor
    * (7) estaOrdenada por ordem crescente
    * (8) estaOrdenada por ordem decrescente
    * (9) Procura um elemento
    * (0) Sair
- O utilizador irá escolher uma das opções introduzindo o número correspondente;
- Se a opção não for sair, a aplicação executa a operação pretendida, apresenta o resultado e a seguir apresenta de novo o menu;
- Se a opção for sair, a aplicação termina colocando uma mensagem no monitor.

* No desenvolvimento da aplicação deverá ter em atenção o seguinte:
    - A aplicação terá uma variável interna para guardar uma lista de números;
    - Na opção 1, deverá ser criada uma lista de números aleatórios entre 1 e 100 que será guardada na variável interna;
    - Na opção 2, deverá ser criada uma lista com números introduzidos pelo utilizador, que será guardada na variável interna;
    - Nestas primeiras opções, se a variável interna já tiver uma lista, esta será sobreposta/apagada pela nova lista;
    - Na opção 3, será calculada a soma dos elementos na lista no momento;
    - Na opção 4, será calculada a média dos elementos na lista no momento;
    - Na opção 5, será calculado o maior elemento da lista no momento;
    - Na opção 6, será calculado o menor elemento da lista no momento;
    - Na opção 7, a aplicação deverá indicar (Sim/Não) se a lista está ordenada por ordem crescente;
    - Na opção 8, a aplicação deverá indicar (Sim/Não) se a lista está ordenada por ordem decrescente;
    - Na opção 9, a aplicação irá procurar um elemento na lista, se o encontrar deverá devolver a sua posição, devolverá -1 se o elemento não estiver na lista;
    - Se o utilizador selecionar a opção 0, a aplicação deverá terminar mostrando a lista que está nesse momento guardada.
 
## Resultados

``` python
# Função para criar lista com os números escolhidos pelo utilizador
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
```

