# TPC4: Aplicação para gerir um cinema

## Beatriz Sousa Neiva  A107241

## Resumo da aula
Resolução de exercícios sobre listas, listas de listas e listas de tuplos.

## Objetivos
Suponha que está a desenvolver uma aplicacão para gestão de um conjunto de salas de cinema de um centro comercial. 
Nesse centro comercial existem algumas salas de cinema (que poderão estar a exibir filmes ou não), cada sala tem uma determinada 
lotação, uma lista com a referência dos bilhetes vendidos (lugares ocupados; cada lugar é identificado por um número inteiro), e cada sala tem um filme associado.

Considera a seguinte sugestão para o modelo dos cinemas:
```
Cinema = [Sala]
Sala = [nlugares, Vendidos, filme]
nlugares = Int
filme = String 
Vendidos = [Int]
```
  
Que poderá ser usado num programa da seguinte forma:
```
sala1 = (150, [], "Twilight")
sala2 = (200, [], "Hannibal")
cinema1 = []
...
cinema1 = inserirSala(cinema1,sala1)
cinema1 = inserirSala(cinema1,sala2)
...
listar(cinema1)
...

if(disponivel(cinema1, "Twilight", 17 )):
  cinema1 = vendebilhete(cinema1, "Twilight", 17 )
...
listardisponibilidades(cinema1)
...
```

Especifique as funções utilizadas no exemplo:

1. `listar( cinema )` - que lista no monitor todos os filmes que estão em exibição nas salas do cinema passado como argumento;
2. `disponivel( cinema, filme, lugar )` - que dá como resultado **False** se o lugar lugar já estiver ocupado na sala onde o filme está a ser exibido e dará como resultado **True** se o inverso acontecer;
3. `vendebilhete( cinema, filme, lugar )` - que dá como resultado um novo cinema resultante de acrescentar o lugar à lista dos lugares ocupados, na sala onde está a ser exibido o filme;
4. `listardisponibilidades( cinema )` - que, para um dado cinema, lista no monitor para cada sala, o filme que está a ser exibido e o total de lugares disponíveis nessa sala (número de lugares na sala menos o número de lugares ocupados);
5. `inserirSala( cinema, sala )` - que acrescenta uma sala nova a um cinema (devendo verificar se a sala já existe);
6. Acrescente todas as outras funcionalidades que achar necessárias;
7. À semelhança do exercício 3, construa uma aplicação com um menu de interface para as operações.

## Resultados
``` python
def existe(cinema, filme):
    cond = False
    for sala in cinema:
        if sala[2] == filme:
            cond = True
    return cond

def listar(cinema):
    print ("-----------------Lista de Filmes---------------")
    for nlugares, vendidos, nomef in cinema:
        print(f"Filme: {nomef}       | Nº Lugares: {nlugares}")
    print("------------------------------------------------")

def disponivel(cinema, filme, lugar):
    cond = False
    for nlugares, vendidos, nomef in cinema:
        if nomef == filme and 1 <= lugar <= nlugares and lugar not in vendidos:
            cond = True
    return cond

def vendeBilhete(cinema, filme, lugar):
    mensagem = f"O lugar {lugar} para o filme {filme} não está disponível. Selecione outra opção."
    for nlugares, vendidos, nomef in cinema:
        if nomef == filme and 1 <= lugar <= nlugares and lugar not in vendidos:
            vendidos.append(lugar)
            mensagem = f"O lugar {lugar} para o filme {filme} foi adquirido com sucesso!"
    return mensagem

def listardisponibilidades(cinema):
    print("----------------Disponibilidade do Cinema----------------")
    for nlugares, vendidos, nomef in cinema:
        disponiveis = nlugares - len(vendidos)
        print(f"Nome: {nomef}      | Lugares Disponíveis: {disponiveis}")
    print("----------------------------------------------------------")

def inserirSala(cinema, sala):
    if not existe(cinema, sala[2]):
        cinema.append(sala)
        print("A sala foi adicionada!")
    else:
        print(f"A sala com o filme {sala[2]} já existe.")
    return cinema

def menu(cinema):
    cond = True
    opcoes = ("1", "2", "3", "4", "5")
    while cond:
        print("\n---------------Gestão de Salas de Cinema---------------")
        print("1 - Listar todos os filmes")
        print("2 - Listar a disponibilidade das salas dos filmes")
        print("3 - Vender bilhetes para um filme")
        print("4 - Adicionar uma nova sala de cinema")
        print("5 - Sair")
        escolha = input("Escolha a sua opção introduzindo um número da lista: ")

        if escolha in opcoes:
            if escolha == "1":
                listar(cinema)
            elif escolha == "2":
                listardisponibilidades(cinema)
            elif escolha == "3":
                filme = input("Introduza o nome do filme que deseja ver: ")
                lugar_input = input(f"Introduza o número do lugar para o filme {filme}: ")
                if lugar_input.isdigit():
                    lugar = int(lugar_input)
                    res = vendeBilhete(cinema, filme, lugar)
                    print(res)
                else:
                    print("Por favor, introduza um número válido para o lugar.")
            elif escolha == "4":
                filme = input("Introduza o nome do filme: ")
                lugares_input = input(f"Introduza o número de lugares da sala do filme {filme}: ")
                if lugares_input.isdigit():
                    nlugares = int(lugares_input)
                    novoFilme = [nlugares, [], filme]
                    cinema = inserirSala(cinema, novoFilme)
                else:
                    print("Por favor, introduza um número válido para os lugares.")
            elif escolha == "5":
                print("Escolheu a opção de sair. Até à próxima!")
                cond = False
        else:
            print("Opção inválida. Por favor, escolha outra opção.")

# Dados
sala1 = [160, [], "Morangos"]
sala2 = [180, [14, 48, 78, 162], "Carros"]
cinema = [sala1, sala2]

# Função que inicia o menu
menu(cinema)
```
