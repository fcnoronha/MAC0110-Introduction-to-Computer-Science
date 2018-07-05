

def fatorial(n):
    """ fatorial(n) é calculado iterativamente
        através do produto parcial 1*2*...*k
        para k=0,1,...n
    """
    fat = 1 # elemento neutro do produto
    for i in range(n):
        # multiplica os fatores 1, 2, ..., n
        fat = fat*(i+1)
    return fat

def cosseno(x):
    """ Implementação ruim: calcula explicitamente
        os expoentes e fatoriais exatamente como
        na fórmula de Taylor
        referência: https://en.wikipedia.org/wiki/Taylor_series
    """
    cos = 0
    n = 0
    eps = 1e-16
    # força a entrada no laço, sem afetar as contas:
    termo = 1
    # acrescenta termos enquanto eles não
    # estiverem no intervalo [-eps,+eps]
    while termo<-eps or termo>eps:
        # calcula novo termo
        termo = (-1)**n * x**(2*n) / fatorial(2*n)
        cos = cos+termo
        n = n+1
    return cos

# testa o cosseno de múltiplos de pi
# observe como o resultado se deteriora
# até se tornar inviável
pi = 3.141592653589793
for n in range(20):
    print("cosseno(",n,"*pi)=",cosseno(n*pi),sep="")
# se quiser refazer o gráfico do cosseno
# com os erros numéricos, veja a receita
# no arquivo cosseno-v1.py
