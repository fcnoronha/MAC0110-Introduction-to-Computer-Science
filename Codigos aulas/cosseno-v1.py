
def cosseno(x):
    """ Implementação melhor: calcula termos
        iterativamente, explorando a relação
        termo(n) = -x**2*termo(n-1)/(2n*(2n-1)),
        e corrige x para o intervalo [0,2*pi]
        para diminuir erros numéricos
    """
    # traz x para o intervalo [0,2*pi] (usando modulo)
    pi = 3.141592653589793
    x = x % (2*pi)
    # obs: em muitas outras linguagens de programação
    # não existe modulo com valores fracionários.
    # nesses casos uma solução simples é converter diretamente:
    # if x>=0: x = x - 2*pi*int(x/(2*pi))
    # else: x = x - 2*pi*(int(x/(2*pi))-1)
    cos = 0
    n = 0
    eps = 1e-16
    termo = 1 # primeiro termo da série
    while termo<-eps or termo>eps:
        cos = cos+termo
        n = n+1
        # calcula novo termo de forma iterativa
        termo = -x*x*termo/((2*n)*(2*n-1))
    return cos

# testa código gerando um gráfico de cosseno(x)
# para x no intervalo [0, 20*pi]
pi = 3.141592653589793
x = -2*pi
while x<20*pi:
    print(x,"\t",cosseno(x))
    x += 0.01

# Para visualizar o gráfico, salve a saída do
# seu programa em um arquivo rodando (no terminal)
# python3 cosseno-v1.py > cosseno.txt
# e depois use o comando graph (do pacote plotutils):
# graph -T X < cosseno.txt
# (em X-Window) ou
# graph -T svg < cosseno.txt > cosseno.svg
# para salvar em arquivo.
# Para instalar o pacote plotutils em Linux
# basta rodar
# sudo apt install plotutils
# para outros sistemas, veja a página
# https://www.gnu.org/software/plotutils/
