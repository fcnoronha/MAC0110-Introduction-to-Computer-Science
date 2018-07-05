import sys
import math
import pygame

from random import randint
from glob import glob



# use apenas para depuração
__DEBUG__ = False
	
# o mundo não deve ser importado como módulo
if __name__!="__main__":
	print("Por favor execute o Mundo de Wumpus com o comando\n",
		  "    python3 mundo.py")
	exit()

# associa números/nomes aos 4 tipos de salas do mundo de Wumpus
LIVRE,MURO,POCO,WUMPUS = range(4)
salas = ["L","M","P","W"]

# associa números/nomes aos 5 tipos de ações possíveis
ANDAR,GIRARDIREITA,GIRARESQUERDA,ATIRAR,COMPARTILHAR = range(5)
acoes = ["A","D","E","T","C"]


class MundoDeWumpus:
	""" Classe principal: define um Mundo de Wumpus, cria personagens,
		faz a simulação e anuncia o final do jogo.
	"""
	def __init__(self):
		""" Construtor: inicializa a representação do mundo,
			inclui as personagens NUSP e dummy e passa a simular o jogo.
		"""

		self.ldp = ListaDePersonagens()
		self.P = self.nPVivas = len(self.ldp.modulo)

		sys.argv[1:] = [int(x) for x in sys.argv[1:]]

		valores = [800, 5, 0.2, 0.2, 0.9, 0.5]

		self.M, self.S, self.alfa, self.beta, self.gama, self.delta = sys.argv[1:len(sys.argv)] + valores[len(sys.argv)-1:7];

		self.N = math.ceil((self.gama * self.P / (1 - self.alfa - self.beta - self.delta)) ** 0.5)

		qtd_muros = math.floor(self.alfa * (self.N ** 2))
		qtd_pocos = math.floor(self.beta * (self.N ** 2))
		qtd_wumpus = math.floor(self.gama * self.P)

		self.nWumpus = qtd_wumpus

		self.mundo = []

		for i in range(self.N):
			lista = []
			for j in range(self.N):
				lista.append('L')
			self.mundo.append(lista)

		lista_usadas = []

		lista_elem = [[qtd_muros, 'M'], [qtd_pocos, 'P'], [qtd_wumpus, 'W']]
		for elem in lista_elem:
			while elem[0] != 0:
				i = randint(0, self.N-1)
				j = randint(0, self.N-1)
				if [i,j] not in lista_usadas:
					self.mundo[i][j] = elem[1]
					lista_usadas.append([i,j])
					elem[0] -= 1
		#self.imprimeMundo()
		
		self.ldp.iniciaPersonagens(self.N, lista_usadas)

		self.personagens = self.ldp.lista

		self.graf = interface(self.M, self.S, self.N)

		# faz o processamento do jogo
		self.processaJogo()
		# anuncia o final do jogo
		self.finalizaJogo()
	
	def processaJogo(self):
		""" Método processaJogo: controla o laço principal, processando uma
			personagem por vez, enquanto o jogo não tiver acabado.
		"""
		# inicializa flags que indicam a tentativa de andar em direção a uma
		# parede e a morte de um Wumpus.
		self.urro = False
		clock = pygame.time.Clock()
		# Repete o laço principal enquanto existirem Wumpus e personagens vivos.
		while self.nWumpus > 0 and self.nPVivas > 0:

			# código apenas para depuração: mostra o mundo a cada jogada
			if __DEBUG__:
				self.imprimeMundo()

			self.imprimeMundo()

			self.ldp.processaPercepcoes(self.mundo, self.urro)
			self.urro = False

			self.ldp.processaPlanejamentos()

			self.ldp.processaCompartilhamentos()

			self.mundo, self.nWumpus, self.urro, self.nPVivas = self.ldp.processaAcoes(self.mundo, self.nWumpus)	

			

			mundop = self.ldp.geraPosPersonagens()
			self.graf.atualizaTela(self.mundo, mundop)

			t = (1/self.graf.deltaT) * 1000
			
			clock.tick(t) 

	def finalizaJogo(self):
		""" O jogo termina quando não há mais personagens vivas,
			ou quando todos os Wumpus foram mortos.
		"""
		if __DEBUG__:
			self.imprimeMundo()
		nome = self.personagemNUSP.nome
		if self.nWumpus==0:
			print("Parabéns, "+nome+", você sobreviveu ao mundo de Wumpus!",sep="")
		x,y = self.personagemNUSP.posicao
		if self.mundo[x][y] == WUMPUS:
			print("Meus pêsames, "+nome+", você virou comida de Wumpus...",sep="")
		if self.mundo[x][y] == POCO:
			print("Meus pêsames, "+nome+", você caiu em um poço...",sep="")

	# outras funções auxiliares do processamento do mundo
	def imprimeMundo(self):
		#pos = self.personagemNUSP.posicao
		#dpos = self.dummy.posicao
		#ori = self.personagemNUSP.orientacao
		m = self.ldp.geraPosPersonagens()
		print("Estado atual do mundo (nenhuma personagem enxerga isso!):")
		for i in range(self.N):
			for j in range(self.N):
				#if pos==[i,j]:
				#	if ori==[0,-1]:
				#		print("<",end="")
				#	print("X",end="")
				#	if ori==[0,1]:
				#		print(">",end="")
				#	if ori==[1,0]:
				#		print("v",end="")
				#	if ori==[-1,0]:
				#		print("^",end="")
				#if dpos==[i,j]:
				#	print("D",end="")
				print("".join(self.mundo[i][j]),end="")
				print("".join(m[i][j]),end="\t| ")
			print("\n"+"-"*(8*self.N+1))


class ListaDePersonagens:

	modulo = []
	nome = []
	lista = []

	def __init__(self):
		lista = glob("personagem*.py")
		for p in lista:
			self.modulo.append(__import__(p[:-3])) # importa tirando o .py do nome
			self.nome.append(p[11:-3])

	def iniciaPersonagens(self, N, lista_usadas):
		self.N = N

		for modulo in range(len(self.modulo)):

			i = randint(0, N-1)
			j = randint(0, N-1)
			while [i, j] in lista_usadas:
				i = randint(0, N-1)
				j = randint(0, N-1)

			ori = randint(0, 3)
			orientacoes = [ [1,0], [0,1], [-1,0], [0,-1] ]

			print("nome: ", self.nome[modulo]," ori: ",orientacoes[ori], "posicao: ", [i,j])	
			self.lista.append(Personagem(self.modulo[modulo], self.nome[modulo], N, [i,j], orientacoes[ori]))

	def geraPosPersonagens(self):
		posPersonagens = []

		for i in range(self.N):
			l = []
			for j in range(self.N):
				l.append([])
			posPersonagens.append(l)

		for p in self.lista:
			if p.estaviva is True:
				pos = p.posicao
				posPersonagens[pos[0]][pos[1]].append(p.nome) 

		return posPersonagens

	def processaPercepcoes(self, mundo, urro):
		m = self.geraPosPersonagens()
		for p in self.lista:
			if p.estaviva:
				p.percepcao = p.perceber(mundo, m, urro)

	def processaPlanejamentos(self):
		for p in self.lista:
			if p.estaviva:
				p.modulo.planejar(p.percepcao)

	def processaCompartilhamentos(self):
		for p1 in self.lista:
			for p2 in self.lista:
				'''
				if p1.posicao == p2.posicao and p1.nome != p2.nome and p2.estaviva:
					comp = self.compensaRepresentacoes(p1.pos_inicial, p1.ori_inicial, p2.pos_inicial, p2.ori_inicial, p2.modulo.mundo)

					for i in range(self.N):
						for j in range(self.N):

							if 'W?' in comp[i][j] and 'W?' not in p1.modulo.mundoCompartilhado[i][j]:
								p1.modulo.mundoCompartilhado[i][j].append('W?')

							if 'W' in comp[i][j] and 'W' not in p1.modulo.mundoCompartilhado[i][j]:
								p1.modulo.mundoCompartilhado[i][j].append('W')
								if 'W?' in p1.modulo.mundoCompartilhado[i][j]:
									p1.modulo.mundoCompartilhado[i][j].remove('W?')

							if 'P?' in comp[i][j] and 'P?' not in p1.modulo.mundoCompartilhado[i][j]:
								p1.modulo.mundoCompartilhado[i][j].append('P?')		

							if 'P' in comp[i][j] and 'P' not in p1.modulo.mundoCompartilhado[i][j]:
								p1.modulo.mundoCompartilhado[i][j].append('P')
								if 'P?' in p1.modulo.mundoCompartilhado[i][j]:
									p1.modulo.mundoCompartilhado[i][j].remove('P?')

							if 'M' in comp[i][j] and 'M' not in p1.modulo.mundoCompartilhado[i][j]:
								p1.modulo.mundoCompartilhado[i][j].append('M')

							if 'I' in comp[i][j] and 'I' not in p1.modulo.mundoCompartilhado[i][j]:
								p1.modulo.mundoCompartilhado[i][j].append('I')

							if 'F' in comp[i][j] and 'F' not in p1.modulo.mundoCompartilhado[i][j]:
								p1.modulo.mundoCompartilhado[i][j].append('F')

							if 'B' in comp[i][j] and 'B' not in p1.modulo.mundoCompartilhado[i][j]:
								p1.modulo.mundoCompartilhado[i][j].append('B')

				'''
				break

	def processaAcoes(self, mundo, nw):
		N = len(mundo)
		urro = False

		mundo_apos = []
		for i in range(len(mundo)):
			c = []
			for j in range(len(mundo)):
				c.append(mundo[i][j])
			mundo_apos.append(c)

		nvivas = 0
		for p in self.lista:
			if p.estaviva:
				acao = p.modulo.agir()
				
				if 'A' in acao:
					p.impacto = False
					pos = p.posicao
					ori = p.orientacao
					# calcula a posição nova
					posnova = [(pos[0]+ori[0])%N,
							   (pos[1]+ori[1])%N]
					# se houver um muro, não dá para andar
					if mundo[posnova[0]][posnova[1]] == 'M':
						p.impacto = True

					# se houver wumpus ou poço, é game over para a personagemNUSP
					elif 'W' in mundo[posnova[0]][posnova[1]] or 'P' in mundo[posnova[0]][posnova[1]] :
						p.morrer()

					else:
						p.ande()

				elif 'E' in acao:
					p.gireEsquerda()

				elif 'D' in acao:
					p.gireDireita();

				elif 'T' in acao:
					if p.nFlechas > 0:
						# calcula destino do tiro
						pos = p.posicao
						ori = p.orientacao
						posnova = [(pos[0]+ori[0])%N,
								   (pos[1]+ori[1])%N]
						# verifica se acertou um Wumpus e atualiza o mundo

						if 'W' in mundo[posnova[0]][posnova[1]]:
							mundo_apos[posnova[0]][posnova[1]] = 'L' # atualiza a sala com Wumpus
							nw -= 1 # contabiliza a morte
							urro = True # propaga o som da morte do Wumpus

					p.atire()

				elif 'C' in acao:
					p.compartilhe()
					pass

				nvivas += 1

		return mundo_apos, nw, urro, nvivas	

	def compensaRepresentacoes(self, pos1, ori1, pos2, ori2, m2):
		#Esta errado
		oris = [[1,0], [0,-1], [-1,0], [0,1]]

		n_rot = abs(oris.index(ori2) - oris.index(ori1))

		pos3 = [0,0]

		nova = []
		for i in range(self.N):
			l = []
			for j in range(self.N):
				l.append([])
			nova.append(l)

		for r in range(n_rot):
			for i in range(self.N):
				for j in range(self.N):
					nova[i][j] = m2[self.N-j-1][i]

			for i in range(self.N):
				for j in range(self.N):
					m2[i][j] = nova[i][j]

			x = pos3[1]
			pos3[1] = -(pos3[0] + 1 - self.N)
			pos3[0] = x

		cps_col = pos2[1] - pos1[1] - pos3[1]
		cps_lin = pos2[0] - pos1[0] - pos3[0]

		for i in range(self.N):
			for j in range(self.N):
					nova[i][j] = m2[(i-cps_lin)%self.N][(j-cps_col)%self.N]

		return nova

class Personagem:
	""" Meta-classe para processar as ações de cada personagem:
		andar, girarDireita, girarEsquerda, atirar e compartilhar.
		Essas ações são métodos da personagem que recebem também
		o objeto MundoDeWumpus, pois potencialmente podem alterar
		o estado do mundo (por exemplo, ao se matar um Wumpus).
		Essas ações devolvem True/False indicando se foram realizadas.
		Cada personagem em particular além desses métodos também
		precisa definir as funções:
			def __init__(self,N):
			def planejar(self,percepcao):
			def agir(self):
	"""
	def __init__(self, modulo, nome, N, pos, ori):
		""" Construtor da classe PersonagemNUSP
		"""	

		# inicializa a personagem
		self.modulo = modulo
		self.impacto = False
		self.percepcao = []
		self.nome = nome
		self.estaviva = True # bem-vinda ao Mundo de Wumpus, personagemNUSP!
		self.N = N # copia a dimensão do mundo, pra facilitar
		self.posicao = pos.copy() # coloca a personagemNUSP no centro do tabuleiro real...
		self.orientacao = ori.copy() # ... e olhando para a direita
		self.ori_inicial = ori.copy()
		self.pos_inicial = pos.copy()
		self.nFlechas = 1 # primeiro chá de bebê da personagemNUSP
		self.modulo.inicializa(N) # chama a inicialização do módulo
		# define os valores que a personagemNUSP conhece
		self.modulo.nFlechas = self.nFlechas # copia nFlechas para o módulo
		self.modulo.mundoCompartilhado = [] # cria matriz NxN de listas vazias
		for i in range(N):
			modulo.mundoCompartilhado.append([[]]*N)

		# Usa um vetor com as funções acima para facilitar o processamento das ações.
		# Os índices correspondem aos valores atribuídos aos símbolos respectivosande
		# ("A"<->0, "D"<->1, etc.)
		self.processe = [ self.ande, self.gireDireita, self.gireEsquerda, self.atire, self.compartilhe ]

	def ande(self):
		""" Função ande: verifica se é possível mover a personagem
			na direção indicada por sua orientação, e as consequências
			disso.
		"""

		pos = self.posicao
		ori = self.orientacao
		posnova = [(pos[0]+ori[0])%self.N, (pos[1]+ori[1])%self.N]
		pos[0],pos[1] = posnova[0],posnova[1]		

		return True

	def gireDireita(self):
		""" Corrige a orientação através de um giro no sentido horário.
		"""
		ori = self.orientacao
		if ori[1]==0:
			ori[0] = -ori[0]
		ori[0],ori[1] = ori[1],ori[0]

		return True

	def gireEsquerda(self):
		""" Corrige a orientação através de um giro no sentido anti-horário.
		"""
		ori = self.orientacao
		if ori[0]==0:
			ori[1] = -ori[1]
		ori[0],ori[1] = ori[1],ori[0]

		return True

	def atire(self):
		""" Atira uma flecha, se possível, na direção indicada pela
			orientação da personagemNUSP, e verifica se acertou um Wumpus.
		"""

		# processa o tiro
		self.nFlechas -= 1
		self.modulo.nFlechas = self.nFlechas

		return True

	def compartilhe(self):
		return True

	def perceber(self, mundo, mundop, urro):
		""" Vasculha as salas adjacentes à sala ocupada pela personagem,
			coletando as informações perceptíveis (fedor, brisa), além de
			agregar percepções decorrentes da última ação (impacto/urro),
			e de outras personagens presentes na posicao.
		"""
		self.urro = urro
		pos = self.posicao
		percepcao = []
		vizinhos = [ [(pos[0]+1)%self.N,pos[1]],
					 [(pos[0]-1)%self.N,pos[1]],
					 [pos[0],(pos[1]+1)%self.N],
					 [pos[0],(pos[1]-1)%self.N] ]
		for viz in vizinhos:
			if mundo[viz[0]][viz[1]] == 'W' and "F" not in percepcao:
				percepcao.append("F") # fedor
			if mundo[viz[0]][viz[1]] == 'P' and "B" not in percepcao:
				percepcao.append("B") # brisa
		if self.impacto:
			percepcao.append("I")
		if self.urro:
			percepcao.append("U")

		percepcao = percepcao + mundop[pos[0]][pos[1]]
		if(self.nome in percepcao):
			percepcao.remove(self.nome)
		self.impacto = False

		return percepcao

	def morrer(self):
		self.estaviva = False 	

class interface:
	def __init__(self, m, s, N):
		pygame.init()

		self.N = N

		self.I0, self.J0 = 0,0

		self.deltaT = 1000

		self.imagens = []
		self.imagens.append(pygame.image.load("poco.jpeg"))
		self.imagens.append(pygame.image.load("wumpus.jpg"))
		self.imagens.append(pygame.image.load("personagem.jpg"))
		self.imagens.append(pygame.image.load("livre.jpg"))
		self.imagens.append(pygame.image.load("muro.jpg"))


		pygame.display.set_caption("Mundo de Wumpus")

		self.M = m
		self.tela = pygame.display.set_mode((self.M, self.M))
		self.S = s

		#while self.rodando:
			#for evento in pygame.event.get():
				#self.processaComando(evento)

	def atualizaTela(self, mundo, mundoP):
		tamBloco = int(self.M / self.S)

		for i in range(self.N):
			print(mundoP[i])

		i = 0
		while i*tamBloco <= self.M: 
			j = 0
			while j*tamBloco <= self.M: 
				lin = (i + self.I0) % self.N
				col = (j + self.J0) % self.N
				if len(mundoP[lin][col]) > 0:
					self.tela.blit(pygame.transform.smoothscale( self.imagens[2], (tamBloco, tamBloco)), (j*tamBloco, i*tamBloco))
				else:
					if 'W' in mundo[lin][col]:
						self.tela.blit(pygame.transform.smoothscale(self.imagens[1], (tamBloco, tamBloco)), (j*tamBloco, i*tamBloco))
					elif 'P' in mundo[lin][col]:
						self.tela.blit(pygame.transform.smoothscale(self.imagens[0], (tamBloco, tamBloco)), (j*tamBloco, i*tamBloco))
					elif 'M' in mundo[lin][col]:
						self.tela.blit(pygame.transform.smoothscale(self.imagens[4], (tamBloco, tamBloco)), (j*tamBloco, i*tamBloco))
					elif 'L' in mundo[lin][col]:
						self.tela.blit(pygame.transform.smoothscale(self.imagens[3], (tamBloco, tamBloco)), (j*tamBloco, i*tamBloco))
				j += 1			
			i += 1

		pygame.display.flip()

		for evento in pygame.event.get([pygame.QUIT, pygame.KEYDOWN]):
			self.processaComando(evento)
			
	def processaComando(self, evento):
		if evento.type == pygame.QUIT:
				rodando = False
				pygame.quit()
				exit()

		elif evento.type == pygame.KEYDOWN:
			if evento.key == pygame.K_ESCAPE:
				rodando = False
				pygame.quit()
				exit()
			
			elif evento.key == pygame.K_BACKSPACE:
				self.rodando = not self.rodando

			elif evento.key == pygame.K_EQUALS:
				if self.S > 1:
					self.S -= 1

			elif evento.key == pygame.K_MINUS:
				if self.S < 50:
					self.S += 1

			elif evento.key == pygame.K_UP:
				self.I0 -= 1
				self.I0 = self.I0 % self.N

			elif evento.key == pygame.K_DOWN:
				self.I0 += 1
				self.I0 = self.I0 % self.N

			elif evento.key == pygame.K_RIGHT:	
				self.J0 += 1
				self.J0 = self.J0 % self.N

			elif evento.key == pygame.K_LEFT:	
				self.J0 -= 1
				self.J0 = self.J0 % self.N

			elif evento.key == pygame.K_PERIOD:	
				self.deltaT = int(self.deltaT*1.5)
				self.deltaT = min(self.deltaT, 10000)

			elif evento.key == pygame.K_COMMA:	
				self.deltaT = int(self.deltaT/1.5)
				self.deltaT = max(self.deltaT, 100)

# Chamada principal... é aqui que toda a mágica acontece!
m = MundoDeWumpus()
