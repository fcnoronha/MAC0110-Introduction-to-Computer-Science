# links interessantes:
# https://en.wikipedia.org/wiki/Methods_of_computing_square_roots#Babylonian_method
# https://en.wikipedia.org/wiki/Nth_root_algorithm

def raizquadrada(x):
    """Calcula a raiz quadrada de x>0
       pelo Método de Newton, através
       da sequência de aproximações
       
           y[0] = x
                    y[k]+x/y[k]
           y[k+1] = -----------
                         2
                         
       para qualquer x>0
    """

    # casos particulares...
    if x<0:
        print("Ainda não aprendi a calcular raízes de números negativos... :(")
    if x==0:
        return 0

    # caso geral
    y = x
    # condição problemática: causa loop infinito para certos x
    while y*y!=x:
        y = (y+x/y)/2
        #print(y) # uma função não deveria imprimir respostas na tela(!)
                  # mas vale a pena ver os valores intermediários para
                  # chegar na raiz quadrada de 2...

    return y

# mostra help da função recém-definida
help(raizquadrada)

# testa a raiz quadrada para x=1, 4, 9, 16, 25, 36, 49, 64, 81 e 100:
n=1
while n<=10:
    print("A raiz quadrada de",n**2,"é",raizquadrada(n**2))
    n += 1 # o mesmo que n = n+1

# calcular a raiz de 2 gera loop infinito(!!)
print("A raiz quadrada de 2 é ",end="")
print(raizquadrada(2))

