#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-

import unicodedata
import re
from analex import *
object = Lexico()

object.run()

object.listaTokens = object.listaTokens['tokens']
def TabelaSimbolos():
	print object.listaTokens
	tamanho = len(object.listaTokens)
	tipo = []
	tabela = []
	for i in range(0,tamanho): 
		if((object.listaTokens[i] == 'INT' or object.listaTokens[i] == 'FLOAT') and object.listaTokens[i+1] == 'ID'):
			tipo = []
			while(object.listaTokens[i] != 'PCOMMA'):
				if(object.listaTokens[i] == 'INT' or object.listaTokens[i] == 'FLOAT'):
					tipo.append(object.listaTokens[i])
				elif(object.listaTokens[i] == 'ID'):
					tipo.append(object.listaTokens[i])
					if(object.listaTokens[i+1] == 'PCOMMA'):
						tipo.append('0')
					elif(object.listaTokens[i+1] == 'COMMA'):
						tipo.append('0')
						tabela.append(tipo)
						tipo = []
						tipo.append(tabela[len(tabela)-1][0])
					elif(object.listaTokens[i+1] == 'ATTR'):
						if(object.listaTokens[i+3] == ('PLUS' or 'MINUS' or 'DIV' or 'MULT')):
							i=i+3
						elif(object.listaTokens[i+2] == ('INTEGER_CONST' or 'FLOAT_CONST')):
							tipo.append(object.listaTokens[i+2])
							i = i + 2

				i=i+1		
			tabela.append(tipo)
			print tabela


def match(token):
	if(object.listaTokens[0] == token):
		object.listaTokens.pop(0)
		print 'Entrada correta'
	else: 
		print 'Erro sintatico'

def Programa():
	match('INT')
	match('MAIN')
	match('LBRACKET')
	match('RBRACKET')
	match('LBRACE')
	#Decl_Comando();
	match('RBRACE')
		
				
"""def Decl_Comando():  
    if (object.listaTokens[i] == 'INT' or object.listaTokens[i] == 'FLOAT'):   
        i = Declaracao(); 
        return  Decl_Comando();
    elif (object.listaTokens[i] == 'ID' or object.listaTokens[i] == 'IF' or object.listaTokens[i] == 'WHILE' or object.listaTokens[i] == 'PRINT' 
          or object.listaTokens[i] == 'READ'):
        i = i + 1        
        i = Comando(i); 
        return i
    else:
        return i+1
        print error('decl comando')

def Declaracao():
	Tipo();
	if (object.listaTokens[i] == 'ID'):
		i=i+1
		i = Decl2();
		return i;
	else:
		return i+1
		print error('declaracao')

def Decl2(object.listaTokens,i):
	if(object.listaTokens[i] == 'COMMA'):
		i = i + 1
		if(object.listaTokens[i] == 'ID'):
			i = i + 1
			i = Decl2(object.listaTokens,i);
	elif(object.listaTokens[i] == 'PCOMMA'):
		i = i + 1
		return i
	elif (object.listaTokens[i] == 'ATTR'):
		i = i + 1
		i = Expressao(object.listaTokens,i)
		i = Decl2();
		return i

def Tipo(object.listaTokens,i):
	if(object.listaTokens[i] == 'INT' or object.listaTokens[i] == 'FLOAT'):
		i = i + 1
		return i

def Comando(object.listaTokens,i):
	if(object.listaTokens[i] == 'LBRACE'):
		i = Bloco(object.listaTokens,i)
		i = i + 1
		return i
	elif(object.listaTokens[i] == 'ID'):
		i = Atribuicao(object.listaTokens,i)
		i = i + 1
		return i
	elif(object.listaTokens[i] == 'IF'):
		i = ComandoSe(object.listaTokens,i)
		i = i + 1	
		return i
	elif(object.listaTokens[i] == 'WHILE'):
		i = ComandoEnquanto(object.listaTokens,i)
		i = i + 1
		return i
	elif(object.listaTokens[i] == 'READ'):
		i = ComandoRead(object.listaTokens,i)
		i = i + 1
		return i
	elif(object.listaTokens[i] == 'PRINT'):
		i = ComandoPrint(object.listaTokens,i)
		i = i + 1
		return i

def Bloco(object.listaTokens,i):
	if(object.listaTokens[i] == 'LBRACE'):
		i = Decl_Comando(object.listaTokens,i);
		i = i + 1;
		if(object.listaTokens[i] == 'RBRACE'):
			return i
		else:
			return i+1
			print error('bloco')

def Atribuicao(object.listaTokens,i):
	if(object.listaTokens[i] == 'ID'):
		if(object.listaTokens[i+1] == 'ATTR'):
			i = Expressao(object.listaTokens,i);
			i = i + 1
			if(object.listaTokens[i] == 'PCOMMA'):
				return i
			else:
				return i+1
				print error('atribuicao')	

def OpRel(object.listaTokens,i):
	if(object.listaTokens[i] == 'LT' or object.listaTokens[i] == 'LE' or object.listaTokens[i] == 'GT' or object.listaTokens[i] == 'GE'):
		i = i + 1
		return i
	else: 
		return i
		print error('OpRel')

def OpAdicao(object.listaTokens,i):
	if(object.listaTokens[i] == 'PLUS' or object.listaTokens[i] == 'MINUS'):
		i = i + 1
		return i
	else: 
		return i
		print error('OpAdicao')

def OpMult(object.listaTokens,i):
	if(object.listaTokens[i] == 'MULT' or object.listaTokens[i] == 'DIV'):
		i = i + 1
		return i
	else: 
		return i
		print error('OpMult')

def OpIgual(object.listaTokens,i):
	if(object.listaTokens[i] == 'EQ' or object.listaTokens[i] == 'NE'):
		i = i + 1
		return i
	else: 
		return i
		print error('OpIgual')

def ComandoRead(object.listaTokens,i):
	if(object.listaTokens[i] == 'READ'):
		i=i+1
		if(object.listaTokens[i] == 'ID'):
			i=i+1
			if(object.listaTokens[i] == 'PCOMMA'):
				i = i + 1
				return i

			else:
				return i
				print error('ComandoRead')			

def ComandoSe(object.listaTokens,i):
	if(object.listaTokens[i] == 'IF'):
		i=i+1
		if(object.listaTokens[i] == 'LBRACKET'):
			i=i+1
			i=Expressao(object.listaTokens,i)
			#i=i+1
			if(object.listaTokens[i] == 'RBRACKET'):
				i=i+1
				i = Comando(object.listaTokens,i)
				#i=i+1
				i = ComandoSenao(object.listaTokens,i)
				return i
			else: 
				return i+1
				print error('ComandoSe')	

def ComandoSenao(object.listaTokens,i):
	if(object.listaTokens[i] == 'ELSE'):
		i=i+1
		i = Comando(object.listaTokens,i)
		return i 
	else: 
		return i+1				

def ComandoEnquanto(object.listaTokens,i):
	if(object.listaTokens[i] == 'WHILE'):
		i=i+1
		if(object.listaTokens[i] == 'LBRACKET'):
			i=i+1
			i = Expressao(object.listaTokens,i)
			if(object.listaTokens[i] == 'RBRACKET'):
				i = i + 1
				i = Expressao(object.listaTokens,i)
				return i
			else:
				return i + 1
				print error('ComandoEnquanto')

def ComandoPrint(object.listaTokens,i):
	if(object.listaTokens[i] == 'PRINT'):
		i=i+1
		if(object.listaTokens[i] == 'LBRACKET'):
			i=i+1
			i = Expressao(object.listaTokens,i)
			if(object.listaTokens[i] == 'RBRACKET'):
				i=i+1
				if(object.listaTokens[i] == 'PCOMMA'):
					i=i+1
					return i
	else:
		return i+1
		print error('ComandoPrint')		

def Expressao(object.listaTokens,i):
	i = Conjuncao(object.listaTokens,i)
	i = i + 1
	i = ExpressaoOpc(object.listaTokens,i)
	i = i + 1 
	return i

def ExpressaoOpc(object.listaTokens,i):
	if(object.listaTokens[i] == 'OR'):
		i = i + 1
		i = Conjuncao(object.listaTokens,i)
		i = i + 1
		i = ExpressaoOpc(object.listaTokens,i)
		return i
	else:	
		return i + 1

def Conjuncao(object.listaTokens,i):
	i = Igualdade(object.listaTokens,i)
	i = i + 1
	i = ConjuncaoOpc(object.listaTokens,i)
	i = i + 1
	return i

def ConjuncaoOpc(object.listaTokens,i):
	if(object.listaTokens[i] == 'AND'):
		i = i + 1
		i = Igualdade(object.listaTokens,i)
		i = i + 1
		i = ConjuncaoOpc(object.listaTokens,i)
		i = i + 1
		return i
	else: 
		return i + 1

def Igualdade(object.listaTokens,i):
	i = Relacao(object.listaTokens,i)
	i = i + 1
	i = IgualdadeOpc(object.listaTokens,i)
	i = i + 1
	return i 

def IgualdadeOpc(object.listaTokens,i):
	i = OpIgual(object.listaTokens,i)
	i = i + 1
	i = Relacao(object.listaTokens,i)
	i = i + 1
	i = RelacaoOpc(object.listaTokens,i)
	i = i + 1
	return i
	#COLOCAR VAZIO AQUI NÃO SEI COMO COLOCAR AAAAA

def Relacao(object.listaTokens,i):
	i = Adicao(object.listaTokens,i)
	i = i + 1
	i = RelacaoOpc(object.listaTokens,i)	
	i = i + 1
	return i 

def RelacaoOpc(object.listaTokens,i):
	i = OpRel(object.listaTokens,i)
	i = i + 1
	i = Adicao(object.listaTokens,i)
	i = i + 1
	i = RelacaoOpc(object.listaTokens,i)
	i = i + 1
	return i
	#COLOCAR VAZIO AQUI NÃO SEI COMO COLOCAR AAAAA

def Adicao(object.listaTokens,i):
	i = Termo(object.listaTokens,i)
	i = i + 1
	i = AdicaoOpc(object.listaTokens,i)
	i = i + 1
	return i

def AdicaoOpc(object.listaTokens,i):
	i = OpAdicao(object.listaTokens,i)
	i = i + 1
	i = Termo(object.listaTokens,i)
	i = i + 1
	i = AdicaoOpc(object.listaTokens,i)
	i = i + 1
	return i
	#COLOCAR VAZIO AQUI NÃO SEI COMO COLOCAR AAAAA	

def Termo(object.listaTokens,i):
	i = Fator(object.listaTokens,i)
	i = i + 1
	i = TermoOpc(object.listaTokens,i)
	i = i + i
	return i

def TermoOpc(object.listaTokens,i):
	i = OpMult(object.listaTokens,i)
	i = i + 1
	i = Fator(object.listaTokens,i)
	i = i + 1
	i = TermoOpc(object.listaTokens,i)
	i = i + 1
	return i 
	#COLOCAR VAZIO AQUI NÃO SEI COMO COLOCAR 

def Fator(object.listaTokens,i):
	if(object.listaTokens[i] == 'ID'):
		i = i + 1
	elif(object.listaTokens[i] == 'INTEGER_CONST'):
		i = i + 1
	elif(object.listaTokens[i] == 'FLOAT_CONST'):
		i = i + 1
	elif(object.listaTokens[i] == 'LBRACKET'):
		i = i + 1
		i = Expressao(object.listaTokens,i)
		i = i + 1
		if(object.listaTokens[i] == 'RBRACKET'):
			i = i + 1
			return i 
		else:
			return i + 1
			print error('fator') """	