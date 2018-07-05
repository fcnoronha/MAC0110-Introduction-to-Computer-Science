def Fibonacci(m):
    """ Gerador de números de Fibonacci
        gera o valor F(m) da sequência
        definida por F(0)=0, F(1)=1 e
        F(n)=F(n-1)+F(n-2) para n>1
    """

    # testa os casos iniciais (m=0,1)
    if m==0 or m==1:
        return m

    # funciona assim também (mas não contem pra ninguém!)
    # return Fibonacci(m-1)+Fibonacci(m-2)
    
    # prepara Fatual = F(1) e Fultimo = F(0)
    Fultimo = 0
    Fatual = 1

    # contador n percorre os valores n=1,2,...,m
    n = 1
    while n<m:
        # atualiza contador
        n = n+1
        # guarda valores antigos de
        # Fpenultimo==F(n-2) e Fultimo=F(n-1)
        Fpenultimo = Fultimo
        Fultimo = Fatual
        # gera termo Fatual==F(n) de Fibonacci
        Fatual = Fultimo+Fpenultimo

    # devolve valor e F(m)
    return Fatual

# imprime o help da função recém-definida (whaaaaat??????)
help(Fibonacci)

# código de teste da função
contador = 0
while contador<=30:
    print("F(",contador,")=",Fibonacci(contador),sep="")
    contador += 1 # o mesmo que contador = contador+1
