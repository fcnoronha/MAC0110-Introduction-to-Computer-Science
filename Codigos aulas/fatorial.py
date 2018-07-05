
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

