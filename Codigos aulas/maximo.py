# calcula o máximo dos elementos de uma sequência terminada por 0

print("Digite uma sequência de números separados por <ENTER> e terminada por 0:")

# usado para testar o término da sequência
terminador = 0

# para observar a tabela com a simulação do código, troque para True:
debug = False
if debug:
    print("resposta xnovo")

# lê primeiro valor da entrada
xnovo = float(input(""))

# resposta guarda sempre o maior elemento já conhecido
resposta = xnovo
if debug:
    print(resposta,'\t',xnovo)

# enquanto a sequência não terminou
while xnovo!=terminador:
    # guarda xnovo se ele for o maior elemento até agora
    if xnovo > resposta:
        resposta = xnovo
    # ou equivalentemente ao if acima...
    # resposta = max(resposta,xnovo)
    if debug:
        print(resposta,'\t',xnovo)

    # lê próximo elemento da entrada
    xnovo = float(input(""))
    if debug:
        print(resposta,'\t',xnovo)

# testa se a sequência é vazia ou não
if resposta==terminador:
    print("O máximo de uma sequência vazia não está definido.")
else:
    print("O máximo dos elementos da sequência é:",resposta)
