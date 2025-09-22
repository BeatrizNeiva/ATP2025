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
