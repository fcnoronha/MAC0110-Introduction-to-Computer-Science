# testa se uma sequência de números da entrada,
# terminada por 0, é ascendente.
# isso equivale a computar a expressão lógica
# (x[1]<=x[2]) and (x[2]<=x[3]) and ... and (x[n-1]<=x[n])

print("Digite os elementos da sequência, separados por <ENTER> (0 para terminar):")

# lê primeiro elemento da entrada
xatual = float(input(""))

# garante que a primeira comparação dentro do laço seja verdadeira
xanterior = xatual

# indicador de passagem
estáordenada = True

while xatual!=0:
    estáordenada = estáordenada and xanterior<=xatual
    # isso é equivalente a
    # if xatual<xanterior: estáordenada = False
    # guarda elemento atual para a próxima comparação
    xanterior = xatual
    # lê próximo elemento da entrada
    xatual = float(input(""))

if estáordenada:
    print("A sequência da entrada está em ordem crescente")
else:
    print("A sequência da entrada não está em ordem crescente")
    
