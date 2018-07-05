nome = input("Prezado Sr./Sra. usuári@, qual é o nome de vossa senhoria? ")

print("Muito prazer, Sr./Sra.",nome,"! Sabia que seu nome tem",len(nome),"letras?")

idade = int(input("Qual é a vossa idade? "))

resposta = input("Vossa senhoria já fez aniversário esse ano? Responda S ou N: ")

if resposta=="S":
    anodenascimento = 2018-idade
else:
    anodenascimento = 2018-idade-1

if (anodenascimento>=0):
    acdc="d.c.?"
else:
    acdc="a.c.?"

print("Sabia que vossa senhoria nasceu no ano de",anodenascimento,acdc)

print("Tenha um bom dia!")
