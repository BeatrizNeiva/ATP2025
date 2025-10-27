import matplotlib.pyplot as plt


def mostrar_menu():
    print("----------Menu de Operações----------")
    print("1: Calcula Média de cada dia")
    print("2: Guardar tabela meteorológica num ficheiro de texto")
    print("3: Carregar tabela meteorológica de um ficheiro de texto")
    print("4: Temperatura mais baixa da tabela")
    print("5: Calcula a amplitude térmica de cada dia")
    print("6: Calcula o dia em que a precipitaçao foi maxima")
    print("7: Calcula os dias que a precipitaçao é maior que p")
    print("8: Calcula o numero de dias consecutivos de dias com precipitaçao abaixo do limite p")
    print("9: Recebe tabela meteorológica e desenha os graficos da Tmín., Tmax., e da pluviosidade.")
    print("0: Sair da aplicaçao.")
    print("-------------------------------------")

def medias(tabMeteo):
    res = []
    for elem in tabMeteo:
        media= (elem[1] + elem[2])/2
        data = elem[0]
        tuplo = (data, media)
        res.append(tuplo)
    return res


def guardaTabMeteo(t, fnome):
    file = open(fnome,"w")    #abrir um ficheiro

    for data, min, max, prec in t:
        ano, mes, dia = data
        registo = f"{ano}-{mes}-{dia} | {min} | {max} | {prec}\n" #\n mudar linha
        file.write(registo)
    file.close()
    return



def carregaTabMeteo(fnome):
    res = []
    file = open(fnome, "r")   # ao escrever "r" damos permissão de leitura, mas caso não se escreva nada, a permissão é "r" por defeito

    for line in file:           # line é uma string
        # line = line[:-1]
        line = line.strip()         # strip remove espaços no final ou início
        campos = line.split("|")  # o split dá sempre uma lista de strings (ou seja, assim vamos obter os tuplos da lista separados como strings)
        data, min, max, prec = campos   # ou...  data = campos[0]                 nota: data é uma string aqui
        ano, mes, dia = data.split("-") # ou... campos_data = data.split("-")
        tuplo = ((int(ano), int(mes), int(dia)), float(min), float(max), float(prec))
        res.append(tuplo)
    file.close()
    return res



def minMin(tabMeteo):
    minimo = tabMeteo[0][1]
    for data, min, *_ in tabMeteo:
        if min < minimo:
            minimo = min
    return minimo



def amplTerm(tabMeteo):
    res = []
    for elem in tabMeteo:
        amp= (elem[2] - elem[1])
        data = elem[0]
        tuplo = (data, amp)
        res.append(tuplo)
    return res



def maxChuva(tabMeteo):
    data_max = None
    valor_max = 0
    for data, Tmin, Tmax, prec in tabMeteo:
        if prec > valor_max:
            data_max = data
            valor_max = prec
    return(data_max, valor_max)



def diasChuvosos(tabMeteo, p):
    res = []
    for data, min, max, prec in tabMeteo:
        if prec > p:
            tuplo = (data, prec)
            res.append(tuplo)
    return res



def maxPeriodoCalor(tabMeteo, p):
    local_consec = 0
    global_consec = 0
    for data, min, max, prec in tabMeteo:
        if prec < p:
            local_consec = local_consec + 1
        else:
            if local_consec > global_consec:
                global_consec = local_consec
            local_consec = 0
    if local_consec > global_consec:
        global_consec = local_consec  
           
    return global_consec



def grafTabMeteo(t):
    #datas = [f"{ano}-{mes}-{dia}" for (ano,mes,dia), *_ in t]
    datas = [f"{data[0]}-{data[1]}-{data[2]}" for data, *_ in t]
    temps_min = [min for data, min, *_ in t]
    temps_max = [max for data,min, max, prec in t]
    precs = [prec for data,min, max, prec in t]

    plt.plot(datas,temps_min, label="Temp Min", color="Blue", marker="o")     #3-- para meter legenda mas depoiis tenho que adicionar plt.legendd()
    plt.plot(datas,temps_max, label="Temp Max", color="Red", marker="o")
    plt.xlabel("Data")
    plt.ylabel("Temperatura ºC")
    plt.title("Temperatura Minima")
    plt.legend()
    plt.show()

    plt.bar(datas,precs, color="b")
    plt.xlabel("Data")
    plt.ylabel("Precipitaçao mm")
    plt.title("Precipitaçao")
    plt.legend()
    plt.show()

    
    return


def main():
    tabMeteo =[]
    fnome = "meteorologia.txt"
    p = None        #não está vinculada a nenhum valor ou objeto

    while True:
        mostrar_menu()
        opcao = input("\nEscolha uma opção: ")

        if opcao == "1":
            resultado = medias(tabMeteo)
            print(f"Médias de cada dia:{resultado}")

        elif opcao == "2":
            guardaTabMeteo(t, fnome)
            print(f"Tabela guardada em {fnome}")

        elif opcao == "3":
            tabMeteo = carregaTabMeteo(fnome)
            print(f"Tabela carregada: {tabMeteo}")

        elif opcao == "4":
            resultado = minMin(tabMeteo)
            print(f"Temperatura mais baixa é {resultado}")

        elif opcao == "5":
            resultado = amplTerm(tabMeteo)
            print(f"Amplitude térmica de cada dia: {resultado}")

        elif opcao == "6":
            resultado = maxChuva(tabMeteo)
            print(f"Dia com precipitaçao máxima: {resultado}")
        
        elif opcao == "7":
            p = float(input("Introduza um valor para o limite p:"))
            resultado = diasChuvosos(tabMeteo, p)
            print(f"Dias com precipitaçao maior que p: {resultado}")
        
        elif opcao == "8":
            p = float(input("Introduza um valor para o limite p:"))
            resultado = maxPeriodoCalor(tabMeteo, p)
            print(f"Numero máximo de dias consecutivos com precipitaçao abaixo de p: {resultado}")

        elif opcao == "9":
            if tabMeteo:
                grafTabMeteo(tabMeteo)
            else:
                print("Carregue ou insira dados na tabela antes de criar graficos.")
        
        elif opcao == "0":
            print("\nSaindo da aplicação...")
            return

tabMeteo = [((2022,1,20), 2, 16, 0),((2022,1,21), 1, 13, 0.2), ((2022,1,22), 7, 17, 0.01)]  
        
main()