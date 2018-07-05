"""
  AO PREENCHER ESSE CABEÇALHO COM O MEU NOME E O MEU NÚMERO USP, 
  DECLARO QUE SOU O ÚNICO AUTOR E RESPONSÁVEL POR ESSE PROGRAMA. 
  TODAS AS PARTES ORIGINAIS DESSE EXERCÍCIO PROGRAMA (EP) FORAM 
  DESENVOLVIDAS E IMPLEMENTADAS POR MIM SEGUINDO AS INSTRUÇÕES
  DESSE EP E QUE PORTANTO NÃO CONSTITUEM DESONESTIDADE ACADÊMICA
  OU PLÁGIO.  
  DECLARO TAMBÉM QUE SOU RESPONSÁVEL POR TODAS AS CÓPIAS
  DESSE PROGRAMA E QUE EU NÃO DISTRIBUI OU FACILITEI A
  SUA DISTRIBUIÇÃO. ESTOU CIENTE QUE OS CASOS DE PLÁGIO E
  DESONESTIDADE ACADÊMICA SERÃO TRATADOS SEGUNDO OS CRITÉRIOS
  DIVULGADOS NA PÁGINA DA DISCIPLINA.
  ENTENDO QUE EPS SEM ASSINATURA NÃO SERÃO CORRIGIDOS E,
  AINDA ASSIM, PODERÃO SER PUNIDOS POR DESONESTIDADE ACADÊMICA.

  Nome : Felipe Castro de Noronha
  NUSP : 10737032
  Turma:
  Prof.: Marcelo Queiroz
  """

import sys
import math
import pygame

from random import randint
from glob import glob
	
# o mundo não deve ser importado como módulo
if __name__!="__main__":
	print("Por favor execute o Mundo de Wumpus com o comando\n",
		  "    python3 mundo.py")
	exit()

class MundoDeWumpus:
	""" Classe principal: define um Mundo de Wumpus, cria personagens,
		faz a simulação e anuncia o final do jogo.
	"""
	def __init__(self):
		""" Construtor: inicializa a representação do mundo,inclui todos as personagens no diretorio do mundo.py.
			Responsavel pela execuçao de turnos e por finalizar o jogo.
		"""

		# Criacao de instancia para classe listaDePersonagens, que sera usada durante toda a execuçao do mundo
		self.ldp = ListaDePersonagens()
		# Recebe a quantidade de personagens lidas/encontradas
		self.P = self.nPVivas = len(self.ldp.modulo)

		# Atribuicao de valores para atributos usados para a criacao e andamento do mundo
		sys.argv[1:] = [int(x) for x in sys.argv[1:]]
		valores = [800, 5, 0.2, 0.2, 0.9, 0.5]
		self.M, self.S, self.alfa, self.beta, self.gama, self.delta = sys.argv[1:len(sys.argv)] + valores[len(sys.argv)-1:7];

		# Calcula o tamanho do toroide que recebera o mundo de Wumpus
		self.N = math.ceil((self.gama * self.P / (1 - self.alfa - self.beta - self.delta)) ** 0.5)

		# Calcula a quantidade de elementos que estarao presentes no mundo
		qtd_muros = math.floor(self.alfa * (self.N ** 2))
		qtd_pocos = math.floor(self.beta * (self.N ** 2))
		qtd_wumpus = math.floor(self.gama * self.P)

		# Instancia local do numero de wumpus
		self.nWumpus = qtd_wumpus

		# Criacao de uma matriz vazia para a alocaçao do mundo
		self.mundo = []
		for i in range(self.N):
			lista = []
			for j in range(self.N):
				lista.append('L')
			self.mundo.append(lista)


		# Lista que sera usada para o controle das salas que ja receberam alguma funcao
		lista_usadas = []

		# Lista com funcoes e marcaçoes que uma sala pode receber
		lista_elem = [[qtd_muros, 'M'], [qtd_pocos, 'P'], [qtd_wumpus, 'W']]
		# Atribui funçoes as casas do mundo
		for elem in lista_elem:
			while elem[0] != 0:
				i = randint(0, self.N-1)
				j = randint(0, self.N-1)
				if [i,j] not in lista_usadas:
					self.mundo[i][j] = elem[1]
					lista_usadas.append([i,j])
					elem[0] -= 1
		
		# Inicia personagens no mundo	
		self.ldp.iniciaPersonagens(self.N, lista_usadas)

		# Copia lista com todos os objetos personagem das classe personagem
		self.personagens = self.ldp.lista

		# Cria instancia para a interface do jogo
		self.graf = interface(self.M, self.S, self.N)

		# Faz o processamento do jogo
		self.processaJogo()

		# Anuncia o final do jogo
		self.finalizaJogo()
	
	def processaJogo(self):
		""" Método processaJogo: controla o laço principal, processando uma
			personagem por vez, enquanto o jogo não tiver acabado.
		"""
		
		# Anuncio da morte de um Wumpus
		self.urro = False
		# Instancia de relogio, que sera usada para controlar o tempo entre as rodadas
		clock = pygame.time.Clock()

		# Repete o laço principal enquanto existirem Wumpus e personagens vivos.
		while self.nWumpus > 0 and self.nPVivas > 0:

			# Roda caso o jogo nao esteja pausado
			if self.graf.pausa is not True:

				# Execuntado o metodo da classe listaDePersonagens que processa as percepcoes, passando
				# os atributos de mundo e flag do urro
				self.ldp.processaPercepcoes(self.mundo, self.urro)

				# Executa metodo da classe listaDePersonagens que processa os planjeamento das personagens
				self.ldp.processaPlanejamentos()

				# Executa metodo da classe listaDePersonagens que processa os compartilhamentos
				self.ldp.processaCompartilhamentos()

				# Atualizando atributos do mundo com o retorno da chamada do metodo de processamento de açoes
				# na classe listaDePersonagens
				self.mundo, self.nWumpus, self.urro, self.nPVivas = self.ldp.processaAcoes(self.mundo, self.nWumpus)				

			# Matriz analoga ao mundo que contem a casa com os jogares
			mundop = self.ldp.geraPosPersonagens()
			# Chamada que atualiza a representacao grafica do mundo, de acordo com as posicoes de cada personagem
			# e o mundo a cada rodada
			self.graf.atualizaTela(self.mundo, mundop)

			# Calculando o periodo que devera estar entre uma rodada e outra 
			t = (1/self.graf.deltaT) * 1000
			# Faz com que haja o 'gap' entre uma rodada e outra, sendo t o numero de rodadas por segundo
			clock.tick(t) 

	def finalizaJogo(self):
		""" O jogo termina quando não há mais personagens vivas,
			ou quando todos os Wumpus foram mortos.
		"""

		if self.nWumpus == 0:
			print("Todos os jogadores sobreviveram ao mundo de Wumpos!!")
		
		elif self.nPVivas == 0:
			print("Oh Nooo! Todos os jogadores acabaram percendo.")

class ListaDePersonagens:
	"""	Classe para coordenar a coreografia de todos as personagens. Mantem uma lista com todos os objetos
		do tipo personagem, percorrendo cada um deles ao realizar suas funcoes.
	"""

	modulo = [] # Lista contendo o modulo - ou mente, de cada personagem 
	nome = [] # Lista contendo o nome de cada personagem
	lista = [] # Lista contendo os objetos da classe personagem, ou seja, todo aspecto fisico e metafisico

	def __init__(self):
		# Inicializando a busca no diretorio, adicionando modulos e nomes nas respectivas listas
		lista = glob("personagem*.py")
		for p in lista:
			self.modulo.append(__import__(p[:-3])) # importa tirando o .py do nome
			self.nome.append(p[11:-3])

	def iniciaPersonagens(self, N, lista_usadas):
		self.N = N # Tamanho do mundo

		# Iterando entre todos os modulos adquiridos
		for modulo in range(len(self.modulo)):

			# Gera um valor aleatorio para servir como posicao da personagem
			i = randint(0, N-1)
			j = randint(0, N-1)
			# Se atentando para a personagem num ser inicializa em um poço, muro ou Wumpos
			while [i, j] in lista_usadas:
				i = randint(0, N-1)
				j = randint(0, N-1)

			# Gerando uma orientacao aleatoria
			ori = randint(0, 3)
			orientacoes = [ [1,0], [0,1], [-1,0], [0,-1] ]

			# Atribuindo objetos Personagem a lista
			self.lista.append(Personagem(self.modulo[modulo], self.nome[modulo], N, [i,j], orientacoes[ori]))

	def geraPosPersonagens(self):
		# Metodo para gerar matriz com o tamanho do mundo, mas que contem a posicao de cada personagem
		posPersonagens = []
		for i in range(self.N):
			l = []
			for j in range(self.N):
				l.append([])
			posPersonagens.append(l)

		# Percorre a lista de personagens, checa se a personagem esta viva, e caso ela eteja, coloca seu nome na
		# matriz, na posicao analoga a que ela esta no mundo
		for p in self.lista:
			if p.estaviva is True:
				pos = p.posicao
				posPersonagens[pos[0]][pos[1]].append(p.nome) 

		return posPersonagens

	def processaPercepcoes(self, mundo, urro):
		# Percorre a lista de personagens, e faz com que as personagens vivas tenham suas percepçoes
		m = self.geraPosPersonagens()
		for p in self.lista:
			if p.estaviva:
				p.percepcao = p.perceber(mundo, m, urro)

	def processaPlanejamentos(self):
		# Percorre a lista de personagens, e faz com que as personagens vivas se planejem de acorod com suas percepçoes
		for p in self.lista:
			if p.estaviva:
				p.modulo.planejar(p.percepcao)

	def processaCompartilhamentos(self):
		# Metodo incompleto. Tinha como objetivo, para cada personagem em uma sala com mais de duas personagens, atribuir
		# ao mundo compartilhado de cada uma, a visao de mundo de suas companheiras de sala. Para isso, utilizaria o metodo 
		# compensaRepresentaçoes() para fazer com que as orientacoes do mundo de uma sirvam para a outra.

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
		# Processa o açao tomada por cada personagem, tomando cuidado para que seja posivel realizar determinda açao
		
		N = self.N 
		urro = False

		# Inicializao de uma matriz que e a copia do mundo passado ao metodo. Sua funçao e ser retornada a classe mundo,
		# atualizando esta caso algum wumpus tenha sido morto.
		mundo_apos = []
		for i in range(len(mundo)):
			c = []
			for j in range(len(mundo)):
				c.append(mundo[i][j])
			mundo_apos.append(c)

		nvivas = 0 # Numero de personagens vivas
		for p in self.lista: # Percorrendo a lista de objetos Personagem
			if p.estaviva: # Promovendo açao somente com as que estao vivas
				acao = p.modulo.agir() # Chama o metodo da personagem responsavel por tomar açoes, armazenando a açao
				
				if 'A' in acao: 
					# Se a açao tomada for andar, ira checar se e possivel realizar este movimento
					p.impacto = False
					pos = p.posicao # Colhe a posicao da personagem
					ori = p.orientacao # Colhe a orientaçao da personagem
					# calcula a posição nova
					posnova = [(pos[0]+ori[0])%N,
							   (pos[1]+ori[1])%N]
					# se houver um muro, não dá para andar
					if mundo[posnova[0]][posnova[1]] == 'M':
						p.impacto = True
					# se houver wumpus ou poço, é game over para a personagem
					elif 'W' in mundo[posnova[0]][posnova[1]] or 'P' in mundo[posnova[0]][posnova[1]] :
						p.morrer()
					# Caso contrario, a personagem pode andar
					else:
						p.andar()

				elif 'E' in acao: # Rotaciona a orientaçao da personagem para a esquerda
					p.girarEsquerda()

				elif 'D' in acao: # Rotaciona a orientaçao da personagem para a direita
					p.girarDireita();

				elif 'T' in acao: # Açao de atirar
					if p.nFlechas > 0: # Checa se a personagem possui fflechas
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
					# Caso o compartilhamento estivesse funcioando, chamaria esta funçao 
					#p.compartilhe()
					pass

				nvivas += 1 # Incrementa 1 ao numero de personagens vivas

		# Retorna atributos que serao utilizados no proximo turno
		return mundo_apos, nw, urro, nvivas	

	def compensaRepresentacoes(self, pos1, ori1, pos2, ori2, m2):
		# Metodo para 'alinhar' duas representaçoes de mundo, rotacionando uma das duas e depois realocando
		# elementos para que eles partissem de um unico ponto fixo. Depois, retorna uma matriz, o resultado
		# deste 'alinhamento'.

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
	""" Meta-classe para processar as ações de cada personagem:	andar, girarDireita, girarEsquerda, atirar e compartilhar.
		Essas ações devolvem True/False indicando se foram realizadas. Cada personagem em particular além desses métodos também
		precisa definir as funções de inicializaçao, percepçao e morte.
	"""
	def __init__(self, modulo, nome, N, pos, ori):

		# inicializa a personagem e seus atributos
		self.modulo = modulo # Recebe o mudulo da personagem
		self.impacto = False # Inicializa sua percepçao de impacto
		self.percepcao = [] # Inicializa sua lista de percepçoes
		self.nome = nome # Define o seu nome
		self.estaviva = True # Bem-vinda ao Mundo de Wumpus!
		self.N = N # copia a dimensão do mundo, pra facilitar
		self.posicao = pos.copy() # Coloca a personagem na posiçao definida 
		self.orientacao = ori.copy() # Orienta a personagem de acordo com a orientaçao definida
		self.ori_inicial = ori.copy() # Orientaçao inicial, usada no 'alinhamento' de percepçoes
		self.pos_inicial = pos.copy() # Posiçao inicial, usada no 'alinhamento' de percepçoes
		self.nFlechas = 1 # Tem 1 fflecha
		self.modulo.inicializa(N) # chama a inicialização do módulo
		self.modulo.nFlechas = self.nFlechas # copia nFlechas para o módulo
		self.modulo.mundoCompartilhado = [] # cria matriz NxN de listas vazias
		for i in range(N):
			modulo.mundoCompartilhado.append([[]]*N)

		# Usa um vetor com as funções acima para facilitar o processamento das ações.
		# Os índices correspondem aos valores atribuídos aos símbolos respectivosandar
		# ("A"<->0, "D"<->1, etc.)
		self.processe = [ self.andar, self.girarDireita, self.girarEsquerda, self.atire, self.compartilhe ]

	def andar(self):
		# Move a personagem
		pos = self.posicao
		ori = self.orientacao
		posnova = [(pos[0]+ori[0])%self.N, (pos[1]+ori[1])%self.N]
		pos[0],pos[1] = posnova[0],posnova[1]		

		return True

	def girarDireita(self):
		# Gira a personagem para a direita
		ori = self.orientacao
		if ori[1]==0:
			ori[0] = -ori[0]
		ori[0],ori[1] = ori[1],ori[0]

		return True

	def girarEsquerda(self):
		# Gira a personagem para a esquerda
		ori = self.orientacao
		if ori[0]==0:
			ori[1] = -ori[1]
		ori[0],ori[1] = ori[1],ori[0]

		return True

	def atire(self):
		# Processa o tiro
		self.nFlechas -= 1
		self.modulo.nFlechas = self.nFlechas

		return True

	def compartilhe(self):
		return True

	def perceber(self, mundo, mundop, urro):
		""" Vasculha as salas adjacentes à sala ocupada pela personagem coletando as informações perceptíveis (fedor, brisa), 
			além de	agregar percepções decorrentes da última ação (impacto/urro), e de outras personagens presentes na posicao. 
			Retornando uma lista com a percepçao.
		"""
		self.urro = urro # Recebendo a propagaçao do urro
		pos = self.posicao
		percepcao = []
		# Lista usada para verificar as casas adjacentes
		vizinhos = [ [(pos[0]+1)%self.N,pos[1]],
					 [(pos[0]-1)%self.N,pos[1]],
					 [pos[0],(pos[1]+1)%self.N],
					 [pos[0],(pos[1]-1)%self.N] ]
		# Verifica as casas adjacentes a personagem, em busca das percepçoes
		for viz in vizinhos:
			if mundo[viz[0]][viz[1]] == 'W' and "F" not in percepcao:
				percepcao.append("F") # fedor
			if mundo[viz[0]][viz[1]] == 'P' and "B" not in percepcao:
				percepcao.append("B") # brisa
		if self.impacto: # Caso tenha havido a percepçao de impacto
			percepcao.append("I")
		if self.urro: # Caso tenha tido propagaçao de urro
			percepcao.append("U")

		# Adicionando a percepçao de outras personagens na mesma sala
		percepcao = percepcao + mundop[pos[0]][pos[1]]
		if(self.nome in percepcao):
			percepcao.remove(self.nome)
		self.impacto = False # Ressetando a percepçao de impacto para o proximo turno

		return percepcao

	def morrer(self):
		# Coloca a personagem como morta
		self.estaviva = False 	

class interface:
	""" Classe que define a visulizaçao do mundo de Wumpus, aceitando comandos por teclado que afetam a 
		visulizaçao do usuario.
	"""
	def __init__(self, m, s, N):
		""" Metodo de inicializaçao, que abre a janela em que sera mostrado o mundo e que carrega as imagens.
		"""

		pygame.init() # Inicializaçao do modulo pygame
		self.N = N # Atribuiçao do tamanho do mundo, para facilitar

		self.I0, self.J0 = 0,0 # Coeficientes que definem a posiçao do mundo mostrado
		self.deltaT = 1000 # Coeficiente do tempo de cada turno

		# Carregando lista com imagens que serao utilizadas na representaçao
		self.imagens = []
		self.imagens.append(pygame.image.load("poco.jpeg"))
		self.imagens.append(pygame.image.load("wumpus.jpg")) # Muito fofo
		self.imagens.append(pygame.image.load("personagem.jpg"))
		self.imagens.append(pygame.image.load("livre.jpg"))
		self.imagens.append(pygame.image.load("muro.jpg"))

		self.pausa = False # Flag usada para pausar o jogo

		pygame.display.set_caption("Mundo de Wumpus") # Define titulo da janela em que ocorre a representaçao

		self.M = m # Numero de pixels altura X largula da janela
		self.tela = pygame.display.set_mode((self.M, self.M)) # Dimensiona a janela
		self.S = s # Numero de casas que devem ser mostradas em uma linha/coluna

	def atualizaTela(self, mundo, mundoP):
		""" Metodo chamado a cada turno, que constroi uma nova reprentaçao do mundo, de acordo com a movimentaçao
			das personagens e a possivel morte de um wumpus.
		"""
		tamBloco = int(self.M / self.S) # Tamanho em pixels de cada bloco mostrado na tela

		# Loops para criar uma visao do toroide, o qual nao tem bordas
		i = 0
		while i*tamBloco <= self.M: 
			j = 0
			while j*tamBloco <= self.M: 
				lin = (i + self.I0) % self.N # Linha referente ao mundo
				col = (j + self.J0) % self.N # Coluna referente ao mundo
				if len(mundoP[lin][col]) > 0: # Caso haja um personagem em determinda sala, define aquele bloco com a imagem 
					self.tela.blit(pygame.transform.smoothscale( self.imagens[2], (tamBloco, tamBloco)), (j*tamBloco, i*tamBloco))
				else:
					if 'W' in mundo[lin][col]: # Atribui imagem de wumpus a sala que tem wumpus
						self.tela.blit(pygame.transform.smoothscale(self.imagens[1], (tamBloco, tamBloco)), (j*tamBloco, i*tamBloco))
					elif 'P' in mundo[lin][col]: # Atribui imagem de poço a sala que tem poço
						self.tela.blit(pygame.transform.smoothscale(self.imagens[0], (tamBloco, tamBloco)), (j*tamBloco, i*tamBloco))
					elif 'M' in mundo[lin][col]: # Atribui imagem de muro a sala que tem muro
						self.tela.blit(pygame.transform.smoothscale(self.imagens[4], (tamBloco, tamBloco)), (j*tamBloco, i*tamBloco))
					elif 'L' in mundo[lin][col]: # Atribui imagem de sala livre a sala que esta livre
						self.tela.blit(pygame.transform.smoothscale(self.imagens[3], (tamBloco, tamBloco)), (j*tamBloco, i*tamBloco))
				j += 1			
			i += 1

		pygame.display.flip() # Atualiza a janela

		# Recebe eventos de QUIT(fechar janela) e KEYDOWN(tecla pressionada)
		for evento in pygame.event.get([pygame.QUIT, pygame.KEYDOWN]):
			self.processaComando(evento)
			
	def processaComando(self, evento):
		""" Funçao que processas os eventos recebidos e os traduz como alteraçoes nos coeficientes que definem
			a forma de representaçao do mundo.
		"""
		# Fecha a janela e termina a execuçao do jogo
		if evento.type == pygame.QUIT:
				rodando = False
				pygame.quit()
				exit()

		# Lidando com eventos de pressionamento de teclas
		elif evento.type == pygame.KEYDOWN:
			# Tecla ESC, fecha o jogo
			if evento.key == pygame.K_ESCAPE:
				rodando = False
				pygame.quit()
				exit()
			
			# Tecla ESPAÇO, pausa o jogo
			elif evento.key == pygame.K_SPACE:
				self.pausa = True

			# Tecla '=', aumenta o zoom da visualizaçao do mundo
			elif evento.key == pygame.K_EQUALS:
				if self.S > 1:
					self.S -= 1

			# Tecla '-', diminui o zoom da representaçao do mundo
			elif evento.key == pygame.K_MINUS:
				if self.S < 50:
					self.S += 1

			# Tecla UP, rola a visualizaçao para cima
			elif evento.key == pygame.K_UP:
				self.I0 -= 1
				self.I0 = self.I0 % self.N

			# Tecla DOWN, roda a visulizaçao para baixo
			elif evento.key == pygame.K_DOWN:
				self.I0 += 1
				self.I0 = self.I0 % self.N

			# Tecla RIGHT, rola a visualizaçao para a direita
			elif evento.key == pygame.K_RIGHT:	
				self.J0 += 1
				self.J0 = self.J0 % self.N

			# Tecla LEFT, rola a visualizaçao para esquerda
			elif evento.key == pygame.K_LEFT:	
				self.J0 -= 1
				self.J0 = self.J0 % self.N

			# Tecla '.', acelera a simulaçao
			elif evento.key == pygame.K_PERIOD:	
				self.deltaT = int(self.deltaT*1.5)
				self.deltaT = min(self.deltaT, 10000) # Define valor maximo de tempo de cada turno

			# Tecla ',', desacelera a simulaçao
			elif evento.key == pygame.K_COMMA:	
				self.deltaT = int(self.deltaT/1.5)
				self.deltaT = max(self.deltaT, 100) # Define valor minimo de tempo para cada turno

# Chamada principal... é aqui que toda a mágica acontece!
m = MundoDeWumpus()