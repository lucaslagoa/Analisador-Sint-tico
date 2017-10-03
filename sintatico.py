#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-

import unicodedata
import re

def TabelaSimbolos(listaTokens,listaValor,i):

	tipo = []
	print listaTokens[i],listaValor[i]
	if(listaTokens[i] == 'INT'):
			tipo[i] = 'int'
	elif(listaTokens[i] == 'FLOAT'):
			tipo[i]	= 'float'
	print tipo[i]

	return i

def error(nome) :
	print 'Erro na função',nome


def Programa(listaTokens,i):
	if(listaTokens[i] == 'INT'):
		if(listaTokens[i+1] == 'MAIN'):
			if(listaTokens[i+2] == 'LBRACKET'):
				if(listaTokens[i+3] == 'RBRACKET'):
					if(listaTokens[i+4] == 'LBRACE'):
						i=i+4
						i = Decl_Comando(listaTokens,i);
						if(listaTokens[i] == 'RBRACE'):
							return i
						else:
							print error('programa')
							return i+1
					else: print error('Deveria aparecer um: {')
				else: print error('Deveria aparecer um: )')
			else: print error('Deveria aparecer um: (')
		else: print error('Deveria aparecer um: main')	
				
def Decl_Comando(listaTokens,i):  
    if (listaTokens[i] == 'INT' or listaTokens[i] == 'FLOAT'):   
        i = Declaracao(listaTokens,i); 
        return  Decl_Comando(listaTokens,i);
    elif (listaTokens[i] == 'ID' or listaTokens[i] == 'IF' or listaTokens[i] == 'WHILE' or listaTokens[i] == 'PRINT' 
          or listaTokens[i] == 'READ'):
        i = i + 1        
        i = Comando(listaTokens,i); 
        return i
    else:
        return i+1
        print error('decl comando')

def Declaracao(listaTokens,i):
	i = Tipo(listaTokens,i);
	if (listaTokens[i] == 'ID'):
		i=i+1
		i = Decl2(listaTokens,i);
		return i;
	else:
		return i+1
		print error('declaracao')

def Decl2(listaTokens,i):
	if(listaTokens[i] == 'COMMA'):
		i = i + 1
		if(listaTokens[i] == 'ID'):
			i = i + 1
			i = Decl2(listaTokens,i);
	elif(listaTokens[i] == 'PCOMMA'):
		i = i + 1
		return i
	elif (listaTokens[i] == 'ATTR'):
		i = i + 1
		i = Expressao(listaTokens,i)
		i = Decl2();
		return i

def Tipo(listaTokens,i):
	if(listaTokens[i] == 'INT' or listaTokens[i] == 'FLOAT'):
		i = i + 1
		return i

def Comando(listaTokens,i):
	if(listaTokens[i] == 'LBRACE'):
		i = Bloco(listaTokens,i)
		i = i + 1
		return i
	elif(listaTokens[i] == 'ID'):
		i = Atribuicao(listaTokens,i)
		i = i + 1
		return i
	elif(listaTokens[i] == 'IF'):
		i = ComandoSe(listaTokens,i)
		i = i + 1	
		return i
	elif(listaTokens[i] == 'WHILE'):
		i = ComandoEnquanto(listaTokens,i)
		i = i + 1
		return i
	elif(listaTokens[i] == 'READ'):
		i = ComandoRead(listaTokens,i)
		i = i + 1
		return i
	elif(listaTokens[i] == 'PRINT'):
		i = ComandoPrint(listaTokens,i)
		i = i + 1
		return i

def Bloco(listaTokens,i):
	if(listaTokens[i] == 'LBRACE'):
		i = Comando(listaTokens,i);
		i = i + 1;
		if(listaTokens[i] == 'RBRACE'):
			return i
		else:
			return i+1
			print error('bloco')

def Atribuicao(listaTokens,i):
	if(listaTokens[i] == 'ID'):
		if(listaTokens[i+1] == 'ATTR'):
			i = Expressao(listaTokens,i);
			i = i + 1
			if(listaTokens[i] == 'PCOMMA'):
				return i
			else:
				return i+1
				print error('atribuicao')	

def OpRel(listaTokens,i):
	if(listaTokens[i] == 'LT' or listaTokens[i] == 'LE' or listaTokens[i] == 'GT' or listaTokens[i] == 'GE'):
		i = i + 1
		return i
	else: 
		return i
		print error('OpRel')

def OpAdicao(listaTokens,i):
	if(listaTokens[i] == 'PLUS' or listaTokens[i] == 'MINUS'):
		i = i + 1
		return i
	else: 
		return i
		print error('OpAdicao')

def OpMult(listaTokens,i):
	if(listaTokens[i] == 'MULT' or listaTokens[i] == 'DIV'):
		i = i + 1
		return i
	else: 
		return i
		print error('OpMult')

def OpIgual(listaTokens,i):
	if(listaTokens[i] == 'EQ' or listaTokens[i] == 'NE'):
		i = i + 1
		return i
	else: 
		return i
		print error('OpIgual')

def ComandoRead(listaTokens,i):
	if(listaTokens[i] == 'READ'):
		i=i+1
		if(listaTokens[i] == 'ID'):
			i=i+1
			if(listaTokens[i] == 'PCOMMA'):
				i = i + 1
				return i

			else:
				return i
				print error('ComandoRead')			

def ComandoSe(listaTokens,i):
	if(listaTokens[i] == 'IF'):
		i=i+1
		if(listaTokens[i] == 'LBRACKET'):
			i=i+1
			i=Expressao(listaTokens,i)
			#i=i+1
			if(listaTokens[i] == 'RBRACKET'):
				i=i+1
				i = Comando(listaTokens,i)
				#i=i+1
				i = ComandoSenao(listaTokens,i)
				return i
			else: 
				return i+1
				print error('ComandoSe')	

def ComandoSenao(listaTokens,i):
	if(listaTokens[i] == 'ELSE'):
		i=i+1
		i = Comando(listaTokens,i)
		return i 
	else: 
		return i+1				

def ComandoEnquanto(listaTokens,i):
	if(listaTokens[i] == 'WHILE'):
		i=i+1
		if(listaTokens[i] == 'LBRACKET'):
			i=i+1
			i = Expressao(listaTokens,i)
			if(listaTokens[i] == 'RBRACKET'):
				i = i + 1
				i = Expressao(listaTokens,i)
				return i
			else:
				return i + 1
				print error('ComandoEnquanto')

def ComandoPrint(listaTokens,i):
	if(listaTokens[i] == 'PRINT'):
		i=i+1
		if(listaTokens[i] == 'LBRACKET'):
			i=i+1
			i = Expressao(listaTokens,i)
			if(listaTokens[i] == 'RBRACKET'):
				i=i+1
				if(listaTokens[i] == 'PCOMMA'):
					i=i+1
					return i
	else:
		return i+1
		print error('ComandoPrint')		

def Expressao(listaTokens,i):
	i = Conjuncao(listaTokens,i)
	i = i + 1
	i = ExpressaoOpc(listaTokens,i)
	i = i + 1 
	return i

def ExpressaoOpc(listaTokens,i):
	if(listaTokens[i] == 'OR'):
		i = i + 1
		i = Conjuncao(listaTokens,i)
		i = i + 1
		i = ExpressaoOpc(listaTokens,i)
		return i
	else:	
		return i + 1

def Conjuncao(listaTokens,i):
	i = Igualdade(listaTokens,i)
	i = i + 1
	i = ConjuncaoOpc(listaTokens,i)
	i = i + 1
	return i

def ConjuncaoOpc(listaTokens,i):
	if(listaTokens[i] == 'AND'):
		i = i + 1
		i = Igualdade(listaTokens,i)
		i = i + 1
		i = ConjuncaoOpc(listaTokens,i)
		i = i + 1
		return i
	else: 
		return i + 1

def Igualdade(listaTokens,i):
	i = Relacao(listaTokens,i)
	i = i + 1
	i = IgualdadeOpc(listaTokens,i)
	i = i + 1
	return i 

def IgualdadeOpc(listaTokens,i):
	i = OpIgual(listaTokens,i)
	i = i + 1
	i = Relacao(listaTokens,i)
	i = i + 1
	i = RelacaoOpc(listaTokens,i)
	i = i + 1
	return i
	#COLOCAR VAZIO AQUI NÃO SEI COMO COLOCAR AAAAA

def Relacao(listaTokens,i):
	i = Adicao(listaTokens,i)
	i = i + 1
	i = RelacaoOpc(listaTokens,i)	
	i = i + 1
	return i 

def RelacaoOpc(listaTokens,i):
	i = OpRel(listaTokens,i)
	i = i + 1
	i = Adicao(listaTokens,i)
	i = i + 1
	i = RelacaoOpc(listaTokens,i)
	i = i + 1
	return i
	#COLOCAR VAZIO AQUI NÃO SEI COMO COLOCAR AAAAA

def Adicao(listaTokens,i):
	i = Termo(listaTokens,i)
	i = i + 1
	i = AdicaoOpc(listaTokens,i)
	i = i + 1
	return i

def AdicaoOpc(listaTokens,i):
	i = OpAdicao(listaTokens,i)
	i = i + 1
	i = Termo(listaTokens,i)
	i = i + 1
	i = AdicaoOpc(listaTokens,i)
	i = i + 1
	return i
	#COLOCAR VAZIO AQUI NÃO SEI COMO COLOCAR AAAAA	

def Termo(listaTokens,i):
	i = Fator(listaTokens,i)
	i = i + 1
	i = TermoOpc(listaTokens,i)
	i = i + i
	return i

def TermoOpc(listaTokens,i):
	i = OpMult(listaTokens,i)
	i = i + 1
	i = Fator(listaTokens,i)
	i = i + 1
	i = TermoOpc(listaTokens,i)
	i = i + 1
	return i 
	#COLOCAR VAZIO AQUI NÃO SEI COMO COLOCAR 

def Fator(listaTokens,i):
	if(listaTokens[i] == 'ID'):
		i = i + 1
	elif(listaTokens[i] == 'INTEGER_CONST'):
		i = i + 1
	elif(listaTokens[i] == 'FLOAT_CONST'):
		i = i + 1
	elif(listaTokens[i] == 'LBRACKET'):
		i = i + 1
		i = Expressao(listaTokens,i)
		i = i + 1
		if(listaTokens[i] == 'RBRACKET'):
			i = i + 1
			return i 
		else:
			return i + 1
			print error('fator')	