#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-

import unicodedata
import re

def declaracao1(listaTokens, i):
	if((listaTokens[i] == 'INT') or (listaTokens[i]=='FLOAT')):
		if(listaTokens[i+1] != 'MAIN'):
			i=i+1
			i = identificador(listaTokens,i)
			i = atribuicao1(listaTokens,i)
			i = numeral(listaTokens,i)
			return i	
		else:
			return i+1

def identificador(listaTokens, i):
	if(listaTokens[i] != 'ID' ):
		print 'O token deve ser um identificador !'
		error('identificador')
		return i
	else: 
		return i+1

def atribuicao1(listaTokens,i):
	if(listaTokens[i] != 'ATTR' and listaTokens[i] != 'COMMA' and listaTokens[i] != 'PCOMMA'):
		print 'O token deve ser um = ou , ou ;'
		error('atribuicao')
		return i
	else:
		return i+1

def numeral(listaTokens,i):
	if(listaTokens[i] != 'INTEGER_CONST' and listaTokens[i] != 'FLOAT_CONST'):
		print 'erro'
		error('numeral')
	else: 
		return i+1	

def error(nome) :
	print 'Erro na função',nome

def repeticao(listaTokens,i):
	if(listaTokens[i] == 'WHILE'):
		i=i+1
	return i

def Programa(listaTokens,i):
	if(listaTokens[i] == 'INT'):
		if(listaTokens[i+1] == 'MAIN'):
			if(listaTokens[i+2] == 'LBRACKET'):
				if(listaTokens[i+3] == 'RBRACKET'):
					if(listaTokens[i+4] == 'LBRACE'):
						i=i+4
						i = Decl_Comando(listaTokens,i);
						print i
						if(listaTokens[i] == 'RBRACE'):
							return i
						else:
							print error('programa')
							return i+1

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
		i = Decl2();
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