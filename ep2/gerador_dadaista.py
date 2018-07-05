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

  Referências: Com exceção das rotinas fornecidas no enunciado
  e em sala de aula, caso você tenha utilizado alguma referência,
  liste-as abaixo para que o seu programa não seja considerado
  plágio ou irregular.
 """

from random import randint

def sort(rima, anterior, uso_elem, lista, m): #funcao que sorteia elementos (verbos e substantivos)
	if(rima == True): #se e necessario ter rimas
		if(uso_elem.count(False) != 0): #se tem ao menos um elemento(verbo ou substantivo) que nao foi usado
			contador = 0
			n_sort = 0
			#ira procurar um elemento com rima M vezes, ate achar
			while(contador in range(0, m)):
				n_sort = randint(0, len(lista) - 1) #sorteia um novo elemento, no caso, o numero de um elemento na lista
				
				#pega o nucleo do elemento sorteado
				if(len(lista[n_sort].split()[0]) >  len(lista[n_sort].split()[1])):
					nucleo = lista[n_sort].split()[0]
				else:
					nucleo = lista[n_sort].split()[1]

				if(anterior == ""):
					return sort(False, "", uso_elem, lista, m)

				#checa se o elemento ainda nao foi usado e se ele tem rima
				elif(uso_elem[n_sort] == False and (nucleo[len(nucleo)-1] == anterior[len(anterior)-1]) and (nucleo[len(nucleo)-2] == anterior[len(anterior)-2])):
					uso_elem[n_sort] = True #valida o elemento como usado 
					contador += 1
					return n_sort #retorna o numero do elemento na lista
				contador += 1
			return sort(False, "", uso_elem, lista, m) #recursao, para caso ele nao ache rimas no intervalo de repetiçoes
		else: #caso todos os elementos tenham sido usados, sorteia um aleatorio
			n_sort = randint(0, len(lista) - 1)	
			return n_sort #retorna valor do elemento aleatorio		
	else: #caso nao seja necessario ter rimas
		if(uso_elem.count(False) != 0): #se tem ao menos um elemento(verbo ou substantivo) que nao foi usado
			contador = 0
			n_sort = 0
			while(uso_elem[n_sort] != False or contador == 0): #enquanto o elemento sorteado tenha sido usado, sorteia um novo
				n_sort = randint(0, len(lista) - 1) #sorteia novo elemento
				if(uso_elem[n_sort] == False): #caso o novo elemento sorteado ainda nao tenha sido usado
					uso_elem[n_sort] = True #valida o elemento como usado
					return n_sort #retorna o numero do elemento na lista
				contador += 1	
		else: #caso todos os vervos ja tenham sido usados, sorteia um aleatorio
			n_sort = randint(0, len(lista) - 1)		
			return n_sort

def declinar(pr1, pr2): #funcao criada para executar o declinio de preposiçoes
	if(pr1 == "a"):
		if(pr2 == "a"):	return "à"
		if(pr2 == "o"):	return "ao"

	elif(pr1 == "de"):
		if(pr2 == "a"):	return "da"
		if(pr2 == "o"):	return "do"

	elif(pr1 == "em"):
		if(pr2 == "a"):	return "na"
		if(pr2 == "o"):	return "no"

	elif(pr1 == "por"):
		if(pr2 == "a"):	return "pela"
		if(pr2 == "o"):	return "pelo"

	elif(pr1 == "a"):
		if(pr2 == "a"):	return "à"
		elif(pr2 == "de"):	return "da"
		elif(pr2 == "em"):	return "na"
		elif(pr2 == "por"):	return "pela"

	elif(pr1 == "o"):
		if(pr2 == "a"):	return "ao"
		elif(pr2 == "de"):	return "do"
		elif(pr2 == "em"):	return "no"
		elif(pr2 == "por"):	return "pelo"
	
	else:
		return str(pr1 + " " + pr2) #caso nao seja possivel fazer a declinacao, retorna as proprias preposicoes


def produzVersos(ls_subs, ls_verbs, n_versos, rima): #funcao que ira produzir os versos
	uso_subs = [False] * len(ls_subs) #cria lista com valores booleanos de uso de substantivos
	uso_verbs = [False] * len(ls_verbs) #cria lista com valores booleanos de uso de verbos

	#definindo uma lista de conjunçoes
	ls_conj = ["como", "enquanto", "e", "mesmo quando", "porque", "quando", "se", "toda vez que"]
	uso_conj = [False] * len(ls_conj) #cria lista com valores booleanos para o uso de conjunçoes

	m = len(ls_subs) + len(ls_verbs) #definindo a variavel m, que limita o loop do sorteio de elementos

	ele_ant = ""	
	for i in range(n_versos): #loop para a criacao de cada verso do poema, de acordo com predefinicao do 
		conj = "" #faz com que a variavel usada para conjuncao tenha sempre um valor vazio no inico do loop
		frase = str("")
		inicio = randint(1, 3) #sorteio para o uso de conjuncao no inico da frase
		if(inicio == 1): #frase comeca com conjuncao
			conj = ls_conj[sort(False, "", uso_conj, ls_conj, m)] #sorteia uma conjuncao para ser usada

		if(i%2 == 0): #reseta a rima para frases impares
			ele_ant = ""

		#sorteia o modo em que sera organizada a estrutura do verso
		estrutura = randint(0, 2)
		if(estrutura == 1): #estrututa de: sujeito + verbo + objeto
			sujeito = ls_subs[sort(False, "", uso_subs, ls_subs, m)] #atribui um suejeito sorteado
			verbo = ls_verbs[sort(False, "", uso_verbs, ls_verbs, m)] #atribui um verbo sorteado
			objeto = ls_subs[sort(rima, ele_ant, uso_subs, ls_subs, m)] #atribui um objeto sorteado

			nu_suj = sujeito.split()[1] #pega o nucleo do sujeito
			nu_obj = objeto.split()[1] #pega o nucleo do objeto
			nu_ver = verbo.split()[0] #pega o nucleo do verbo

			pr_suj = sujeito.split()[0] #pega o artigo do sujeito
			pr_obj = objeto.split()[0] #pega o artigo do objeto
			pr_ver = verbo.split()[1] #pega a preposicao do verbo

			if(pr_ver == "-"): #checa se o verbo tem ou nao preposicao
				pr_ver = "" #caso o verbo nao tenha preposicao, atribui valor vazio a variavel correspondente

			ele_ant = nu_obj #atruibui o nucleo do objeto a variavel ele_ant, que ira servir para o tratamento de rimas

			#cria uma frase, concatenando todos os elementos e tomando cuidado para tratar o espaço na declinaçao
			frase = conj + " " + pr_suj + " " + nu_suj + " " + nu_ver + " " + declinar(pr_ver, pr_obj).strip() + " " + nu_obj

		#os proximos dois casos sao analogos ao primeiro, tendo somente, variaçoes quanto a estrutura do verso
		elif(estrutura == 2): #estrutura: sujeito + objeto + verbo
			sujeito = ls_subs[sort(False, "", uso_subs, ls_subs, m)]
			objeto = ls_subs[sort(False, "", uso_subs, ls_subs, m)]
			verbo = ls_verbs[sort(rima, ele_ant, uso_verbs, ls_verbs, m)]	

			nu_suj = sujeito.split()[1]
			nu_obj = objeto.split()[1]
			nu_ver = verbo.split()[0]

			pr_suj = sujeito.split()[0]
			pr_obj = objeto.split()[0]
			pr_ver = verbo.split()[1]		

			if(pr_ver == "-"): 
				pr_ver = ""
		
			ele_ant = nu_ver

			frase = conj + " " + pr_suj + " " + nu_suj + " " + str(declinar(pr_ver, pr_obj)).strip() + " " + nu_obj + " " + nu_ver


		else: #estrutura de: verbo + objeto + sujeito
			verbo = ls_verbs[sort(False, "", uso_verbs, ls_verbs, m)]
			objeto = ls_subs[sort(False, "", uso_subs, ls_subs, m)]
			sujeito = ls_subs[sort(rima, ele_ant, uso_subs, ls_subs, m)]

			nu_suj = sujeito.split()[1]
			nu_obj = objeto.split()[1]
			nu_ver = verbo.split()[0]

			pr_suj = sujeito.split()[0]
			pr_obj = objeto.split()[0]
			pr_ver = verbo.split()[1]	

			if(pr_ver == "-"): 
				pr_ver = ""

			ele_ant = nu_suj	

			frase = conj + " " + nu_ver + " " + str(declinar(pr_ver, pr_obj)).strip() + " " + nu_obj + " " + pr_suj + " " + nu_suj
		
		if((i + 1) % 2 == 0 and i != 0): print(frase.strip().lower(), ".", sep="") #caso a frase seja par, termina com ponto
		else:
			if(i == (n_versos - 1)): print(frase.strip().capitalize(), ".", sep="") #caso seja ultimo verso e impar, termina com "."
			else: print(frase.strip().capitalize()) #caso seja so impar, começa com caixa alta

		if((i + 1) % 4 == 0): print("")	#cria estrofes com 4 versos					


def main():
	ls_subs = []
	n_subs = int(input("Quantos substantivos você deseja utilizar?\n"))
	print("Digite um substantivo (com artigo) por linha:")
	for i in range(n_subs): #loop para adicionar elementos a listagem de substantivos
		ls_subs.append(input())

	ls_verbs = []	
	n_verbs = int(input("Quantos verbos você deseja utilizar?\n"))
	print("Digite um verbo (com preposição) por linha:")
	for i in range(n_verbs): #loop para adicionar elementos a listagem de verbos
		ls_verbs.append(input(""))

	#validando se o usuario quer ou nao que o poema tenha rimas
	rima = bool(True)
	if(input("Voce deseja uma poesia com rima? Responda sim ou nao:\n") == "sim"):
		rima = True
	else:
		rima = False

	#recebendo o valor da quantidade de versos que o usuario quer que o poema tenha
	n_versos = int(input("Quantos versos voce deseja que a poesia tenha?\n"))

	produzVersos(ls_subs, ls_verbs, n_versos, rima) #invocando funcao que vai gerar o o poema em si
main()