#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-

import unicodedata
import re
from analex import *
import hashlib

object = Lexico()

object.run()


listaTokens = object.listaTokens['tokens']
listaLexema = object.listaTokens['lexema']

def TabelaSimbolos():
	tamanho = len(listaTokens)
	tipo = []
	dict = {}
	dict2 = {}
	for i in range(0,tamanho): 
		if((listaTokens[i] == 'INT' or listaTokens[i] == 'FLOAT') and listaTokens[i+1] == 'ID'):
			tipo = []
			tipo.append(listaTokens[i])
			i = i+1
			while(listaTokens[i] != 'PCOMMA'):
				if(listaTokens[i] == 'ID'):
					dict[listaLexema[i]] = (tipo, 0)

				if(listaTokens[i+1] == 'PCOMMA'):
					dict2[listaLexema[i]] = (tipo, 0)
					dict.update(dict2)
				elif(listaTokens[i+1] == 'COMMA'):
					dict2[listaLexema[i]] = (tipo, 0)
					dict.update(dict2)
				elif(listaTokens[i+1] == 'ATTR'):
					if(listaTokens[i+3] == ('PLUS' or 'MINUS' or 'DIV' or 'MULT')):
						dict[listaLexema[i]] = (tipo, 0)
						i=i+3

					elif(listaTokens[i+2] == 'INTEGER_CONST' or listaTokens[i+2] == 'FLOAT_CONST'):
						dict2[listaLexema[i]] = (tipo, listaLexema[i+2])
						dict.update(dict2)
						i = i + 2
					else:
						dict[listaLexema[i]] = (tipo, 0)
				i=i+1
	print dict


def match(token):
	if(listaTokens[0] == token):
		listaTokens.pop(0)
		listaLexema.pop(0)
		print 'Entrada correta'
	else: 
		print 'Erro sintatico'

def Programa():
	match('INT')
	match('MAIN')
	match('LBRACKET')
	match('RBRACKET')
	match('LBRACE')
	Decl_Comando();
	match('RBRACE')
		
				
def Decl_Comando():  
    if (listaTokens[0] == 'INT' or listaTokens[0] == 'FLOAT'):   
        Declaracao(); 
        Decl_Comando();
        
    elif (listaTokens[0] == 'ID' or listaTokens[0] == 'IF' or listaTokens[0] == 'WHILE' or listaTokens[0] == 'PRINT' 
          or listaTokens[0] == 'READ' or listaTokens[0] == 'LBRACE'):
       	Comando();
       	Decl_Comando();

    else:
        return i

def Declaracao():
	Tipo();
	match('ID')
	Decl2();


def Decl2():
	if(listaTokens[0] == 'COMMA'):
		match('COMMA')
		match('ID')
		Decl2()
	elif(listaTokens[0] == 'PCOMMA'):
		match('PCOMMA')	
	elif(listaTokens[0] == 'ATTR'):
		match('ATTR')
		Expressao()
		Decl2()	

def Tipo():
	if(listaTokens[0] == 'INT'):
		match('INT')
	elif(listaTokens[0] == 'FLOAT'):
		match('FLOAT')

def Comando():
	if(listaTokens[0] == 'LBRACE'):
		Bloco()
	elif(listaTokens[0] == 'ID'):
		Atribuicao()
	elif(listaTokens[0] == 'IF'):
		ComandoSe()
	elif(listaTokens[0] == 'WHILE'):
		ComandoEnquanto()
	elif(listaTokens[0] == 'READ'):
		ComandoRead()
	elif(listaTokens[0] == 'PRINT'):
		ComandoPrint()

def Bloco():
	match('LBRACE')
	Comandos()
	match('RBRACE')

def Atribuicao():
	match('ID')
	match('ATTR')
	Expressao()
	match('PCOMMA')

def OpRel():
	if(listaTokens[0] == 'LT' ):
		match('LT')
	elif(listaTokens[0] == 'LE') :
		match('LE')		
	elif(listaTokens[0] == 'GT'):
		match('GT')		
	elif(listaTokens[0] == 'GE'):
		match('GE')

def OpAdicao():
	if(listaTokens[0] == 'PLUS'):
		match('PLUS')
	elif(listaTokens[0] == 'MINUS'):
		match('MINUS')


def OpMult():
	if(listaTokens[0] == 'MULT'):
		match('MULT')
	elif(listaTokens[0] == 'DIV'):
		match('DIV')

def OpIgual():
	if(listaTokens[0] == 'EQ'):
		match('EQ')
	elif(listaTokens[0] == 'NE'):
		match('NE')
	

def ComandoRead():
	match('READ')
	match('ID')
	match('PCOMMA')			

def ComandoSe():
	match('IF')
	match('LBRACKET')
	Expressao()
	match('RBRACKET')
	Comando()
	ComandoSenao()	

def ComandoSenao():
	match('ELSE')
	Comando()

	return i 			

def ComandoEnquanto():
	match('WHILE')
	match('LBRACKET')
	Expressao()
	match('RBRACKET')
	Comando()

def ComandoPrint():
	match('PRINT')
	match('LBRACKET')
	Expressao()
	match('RBRACKET')
	match('PCOMMA')		

def Expressao():
	Conjuncao()
	ExpressaoOpc()

def ExpressaoOpc():
	match('OR')
	Conjuncao()
	ExpressaoOpc()

	return i

def Conjuncao():
	Igualdade()
	ConjuncaoOpc()

def ConjuncaoOpc():
	match('AND')
	Igualdade()
	ConjuncaoOpc()

	return i

def Igualdade():
	Relacao()
	IgualdadeOpc()

def IgualdadeOpc():
	OpIgual()
	Relacao()
	IgualdadeOpc()

def Relacao():
	Adicao()
	RelacaoOpc()

def RelacaoOpc():
	OpRel()
	Adicao()
	RelacaoOpc()

	return i
	#COLOCAR VAZIO AQUI NÃO SEI COMO COLOCAR AAAAA

def Adicao():
	Termo()
	AdicaoOpc()

def AdicaoOpc():
	OpAdicao()
	Termo()
	AdicaoOpc()

	return i
	#COLOCAR VAZIO AQUI NÃO SEI COMO COLOCAR AAAAA	

def Termo():
	Fator()
	TermoOpc()

def TermoOpc():
	OpMult()
	Fator()
	TermoOpc()

	return i
	 

def Fator():
	if(listaTokens[0] == 'ID'):
		match('ID')
	elif(listaTokens[0] == 'INTEGER_CONST'):
		match('INTEGER_CONST')
	elif(listaTokens[0] == 'FLOAT_CONST'):
		match('FLOAT_CONST')
	elif(listaTokens[0] == 'LBRACKET'):
		match('LBRACKET')
		Expressao()
		match('RBRACKET')	
	