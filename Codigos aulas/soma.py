# calcula a soma dos elementos de uma sequência terminada por 0

print("Digite uma sequência de números separados por <ENTER> e terminada por 0:")

# usado para testar o término da sequência
terminador = 0

# para observar a tabela com a simulação do código, troque para True:
debug = False
if debug:
    print("resposta xnovo")

# resposta guarda a soma parcial dos elementos já conhecidos
resposta = 0 # elemento neutro da soma == soma dos elementos de uma sequência vazia

# lê primeiro valor da entrada
xnovo = float(input(""))
if debug:
    print(resposta,'\t',xnovo)

# enquanto a sequência não terminou
while xnovo!=terminador:
    # adiciona o elemento novo à soma parcial
    resposta = resposta+xnovo
    if debug:
        print(resposta,'\t',xnovo)
    # lê próximo elemento da entrada
    xnovo = float(input(""))
    if debug:
        print(resposta,'\t',xnovo)

print("A soma dos elementos da sequência é:",resposta)
