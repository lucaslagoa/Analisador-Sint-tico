from analex import *
from sintatico import *

print 'Tabela de Simbolos'
TabelaSimbolos()

while(len(listaTokens)>0):

	root = Programa()
	root.__evaluate__()
	print "Variaveis pos-programa: "
	print dicionario