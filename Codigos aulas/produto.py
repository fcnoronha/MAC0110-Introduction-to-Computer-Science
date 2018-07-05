# calcula o produto dos elementos de uma sequência terminada por 0

print("Digite uma sequência de números separados por <ENTER> e terminada por 0:")

# usado para testar o término da sequência
terminador = 0

# para observar a tabela com a simulação do código, troque para True:
debug = False
if debug:
    print("resposta xnovo")

# resposta guarda o produto parcial dos elementos já conhecidos
resposta = 1 # elemento neutro do produto == produto dos elementos de uma sequência vazia

# lê primeiro valor da entrada
xnovo = float(input(""))
if debug:
    print(resposta,'\t',xnovo)

# enquanto a sequência não terminou
while xnovo!=terminador:
    # multiplica o elemento novo ao produto parcial
    resposta = resposta*xnovo
    if debug:
        print(resposta,'\t',xnovo)
    # lê próximo elemento da entrada
    xnovo = float(input(""))
    if debug:
        print(resposta,'\t',xnovo)

print("O produto dos elementos da sequência é:",resposta)
