from random import randint

def distribuicao(N): #define um valor aleatorio para cada casa decimal de 10^(n-1), ou seja, os pesos
	contador = 0 
	dist = ""
	while (contador < N): #loop que criar um valor numerico(peso) para cada N
		p = randint(0,9)
		p = str(p)
		dist = str(dist) + p #forma 'peculiar' de criar um numero, alternativa ao uso de exponencial
		contador += 1
	dist = int(dist)
	assert dist in range(10**N)
	return dist

def sorteia(N, dist): #Devolve o resultado de um sorteio enviesado dentre os inteiros de 0 a N-1 de acordo com a distribuição dist
	dist1 = dist2 = dist #clonando a variavel inicial, para futura manipulaçao
	x = S = n = 0
	sorteio = 1

	while(x <= N): #loop que conta a soma de todos os digitos de dist
		S += (dist1%10)
		dist1 = dist1//10
		x += 1

	s = randint(0, (S-1)) #realiza um sorteio aleatorio entre 0 e s-1

	while(sorteio <= N): #realiza um sorteio final, levando em conta os pesos
		n += (dist2%10)
		dist2 = dist2//10		
		if((S - s) <= n): 
			return(N - sorteio)
		sorteio += 1

def jogada(N, jogador, lanceanterior): #recebe os valores das jogadas
	if(jogador == "humano"):
		lance = int(input("É a sua vez de jogar:"))
		while((lance == lanceanterior) or (lance < 0 or lance >= N)): #verifica consistencia de dados
			if(lance < 0 or lance >= N):
				lance = int(input("Por favor digite outro número:"))

			if(lance == lanceanterior):
				lance = int(input("A mesa já escolheu esse número.\nPor favor digite outro número:"))
	else:
		lance = randint(0, N-1)
		while(lance == lanceanterior):
			lance = randint(0, N-1) #gera o valor da mesa
		print("É a vez da mesa jogar.\nA mesa escolhe o número", lance, ".")

	assert lance in range(N) and lance != lanceanterior
	return lance
	   
def jogar(): #que realiza o jogo
	global pontoh #definindo o uso de variaveis globais
	global pontoc
	global rodada

	print("\nRodada", rodada, "\nEscolhendo jogador inicial...", sep="")

	jog = randint(0, 1) #realiza o sorteio, a fim de verificar quem vai jogar primeiro

	if(jog == 0): #caso em que o usuario(humano) joga primeiro e a masa(computador) joga depois
		jogador1 = "humano"
		jogador2 = "computador"
		jh = jogada(N, jogador1, -1) #variavel jh(jogada humana) recebe valores
		jc = jogada(N, jogador2, jh) #variavel jc(jogada computador) recebe valores

	elif(jog == 1): #analogo ao anterior
		jogador1 = "computador"
		jogador2 = "humano"
		jc = jogada(N, jogador1, -1)
		jh = jogada(N, jogador2, jc)

	sorteio = sorteia(N, dist) #realizaçao de um sorteio enviesado
	print("Sorteio = ", sorteio, ".", sep="")

	#as condiçoes seguintes definem a pontuaçao do jogo
	if(jh == sorteio): #quando o jogador acerta em cheio
		pontoh += 100
		pontoc -= 100
		print("Você ganhou!\nPontuação: Jogador = ", pontoh, ", Mesa = ", pontoc, sep="")

	elif(jc == sorteio): #quuando o computador acerta em cheio
		pontoc += 100
		pontoh -= 100
		print("A mesa ganhou!\nPontuação: Jogador = ", pontoh, ", Mesa = ", pontoc, sep="")

	#quando o computador tem o resultado mais aproximado, levando em coonta a circularidade da roleta
	elif(min((jc-sorteio)%N , (sorteio-jc)%N ) < min((sorteio-jh)%N , (jh-sorteio)%N )): 
		pontoc += 10
		pontoh -= 10
		print("A mesa ganhou!\nPontuação: Jogador = ", pontoh, ", Mesa = ", pontoc, sep ="")

	#quando o humano tem o resultado mais aproximado, levando em coonta a circularidade da roleta
	elif(min((jc-sorteio)%N , (sorteio-jc)%N ) > min((sorteio-jh)%N , (jh-sorteio)%N )):
		pontoh += 10
		pontoc -= 10
		print("Você ganhou!\nPontuação: Jogador = ", pontoh, ", Mesa = ", pontoc, sep="")

	#quando humano e computador tem a mesma proximidade, o humano recebe os pontos
	elif(min((jc-sorteio)%N , (sorteio-jc)%N ) == min((sorteio-jh)%N , (jh-sorteio)%N )):
		pontoh += 10
		pontoc -= 10
		print("Você ganhou!\nPontuação: Jogador = ", pontoh, ", Mesa = ", pontoc, sep="")

	decisao = input("Deseja continuar jogando (S/N):") #checa se o jgador deseja continuar jogadno

	if(decisao == "S"):
		rodada += 1
		jogar() #repete o jogo

	else:
		if(pontoh >= 0):
			print("\nVocê deve receber", pontoh, "da mesa!\nObrigado por jogar a roleta maluca!")
		else:
			print("\nVocê deve pagar", pontoc, "para a mesa!\nObrigado por jogar a roleta maluca!")

#inicializaçao
print("Bem-vind@ à roleta maluca!")
N = input("Por favor digite a quantidade de elementos da roleta (entre 2 e 100):")
while(not N.isdecimal() or int(N) < 2 or int(N) > 100): #checa se N e decimal == consistencia
	N = input("Por favor digite um inteiro entre 2 e 100: ")
N = int(N)
print("A roleta possui os números 0...", N-1, "\nAguarde enquanto envieso a roleta...", sep="")

dist = distribuicao(N) #define dist
rodada = 1
pontoh = pontoc = 0 

jogar() #realiza a funcao da jogada