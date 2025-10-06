# TPC2: Jogo 21 fósforos

## Beatriz Sousa Neiva  A107241

## Resumo da aula TP
Resolução de exercícios que envolvem estruturas condicionais (if-elif-else) e cíclicas simples (while).
Definição e aplicção da função def.

## Objetivos
Desenvolve em Python o código necessário para o jogo dos 21 fósforos: 

### O jogo

* No início do jogo, há 21 fósforos;
* Cada jogador (computador ou utilizador), pode tirar 1, 2, 3 ou 4 fósforos quando for a sua vez de jogar;
* Os jogadores jogam alternadamente;
* **Quem tirar o último fósforo perde!**

### O programa 

* O jogo deverá ter dois modos: o jogador joga em primeiro lugar e o computador começa a jogar em segundo lugar e, no segundo modo, o computador começa em primeiro; 
* Quando o computador começa a jogar em segundo lugar, deve ganhar sempre o jogo;
* Quando o computador começa a jogar em primeiro lugar, se o utilizador cometer um erro de cálculo, o computador deverá passar para a posição de vencedor e ganhar o jogo.


## Resultados
``` python
import random
# Menu principal 

print("Jogo dos 21 fósforos")
print("Quem tirar o último fósforo perde!")
print("1 - Jogador começa")
print("2 - Computador começa")
modo = input("Escolha o modo (1 ou 2): ")

fosforos = 21
if modo == "1":
    turno = "jogador"
else:
    turno = "computador"

while fosforos > 1:
    print("\nFósforos restantes: ", fosforos)

    # Turno do jogador
    if turno == "jogador":
        escolha = int(input("Quantos fósforos quer tirar (1 a 4)? "))
        if escolha >= 1 and escolha <= 4 and escolha <= fosforos:
            fosforos = fosforos - escolha
            turno = "computador"
        else:
            print("Escolha inválida. Tente novamente.")

    # Turno do computador (Estratégia)
    else:
        
        escolha = (fosforos - 1) % 5
        if escolha == 0 or escolha > 4 or escolha > fosforos:
            if fosforos == 4:
                escolha = random.randint(1, 4)
            elif fosforos == 3:
                escolha = random.randint(1, 3)
            elif fosforos == 2:
                escolha = random.randint(1, 2)
            else:
                escolha = 1
        print("O computador tira", escolha, "fósforo(s).")
        fosforos = fosforos - escolha
        turno = "jogador"

print("\nSó resta 1 fósforo.")
if turno == "jogador":
    print("O jogador é obrigado a tirar o último fósforo. O computador ganha!")
else:
    print("O computador é obrigado a tirar o último fósforo. O jogador ganha!")
```
