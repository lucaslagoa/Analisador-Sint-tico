from analex import *
from sintatico import *

listaTokens = lexico.listaTokens['tokens']
i=0

while (i < len(listaTokens)):
	if (listaTokens[i] == 'INT' or listaTokens[i] == 'FLOAT'):
		i = declaracao1(listaTokens,i)
		print 'Fim da analise sintatica - declaracao'
	elif(listaTokens[i] == 'WHILE'):
		i = repeticao(listaTokens,i)
		print 'Fim da analise sintatica - repeticao'
	elif(listaTokens[i] == 'INT' and listaTokens[i+1] == 'MAIN'):
		i = Programa(listaTokens,i)
		print 'Programa'