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
listaLinhas = object.listaTokens['linhas']

class AST():
    def __init__(self, nome, father):
         self.nome = nome;
         self.children = []
         self.father = father #cria uma referência para o pai
         self.tipo = None  #inteiro ou ponto flutuante
         self.value = None
         self.hasParenthesis = None
         
    def __str__(self, level=0):
        ret = "\t"*level+ repr(self) +"\n"
        for child in self.children:
            if (child != None):                
                ret += child.__str__(level+1) #level+1
                #print(child.__str__())
        return ret
    
    def __repr__(self):
        return self.nome
    
    def __evaluate__(self):
        print('Avaliando nó ' + str(self.nome))
        for child in self.children:
            if (child != None): 
                child.__evaluate__()
        
    def __checkTypes__(self):  
        for child in self.children:
            if (child != None): 
                child.__checkTypes__()        
        
    #code = " ";
    #for child in self.children: 
            #code += child.__codegen__();        
    #return code    
    def __codegen__(self):        
        for child in self.children: 
            print(str(child.__codegen__()))
        

"""
O cabeçalho int main() é gerado antes
"""

class Compound(AST):
    """Represents a 'BEGIN ... END' block"""
    def __init__(self,father):
        AST.__init__(self,'Block',father)
        print('Criando um nó do tipo Block.')
        #self.children = []
    def __repr__(self):
        return self.nome
    
    def __codegen__(self):
        code = " ";
        for child in self.children: 
            code += child.__codegen__();        
        return "{" + code + "}"

class Assign(AST):
    def __init__(self, left, op, right, father):
        AST.__init__(self,'Assign',father);
        print('Criando um nó do tipo Assign.')
        self.children.append(left)
        self.children.append(right)
        self.left = left
        self.token = self.op = op
        self.right = right
        self.isDecl = None
    
    def __repr__(self):
        return self.nome
    
    def __setIsDecl__(self, isDecl):
        self.isDecl = isDecl
    
    def __evaluate__(self):
        print('Avaliando atribuição.')        
        id_node = self.children[0]
        lex = id_node.token.lexema
        print('Lexema do lado esquerdo: ' + str(lex))
        #Consulta a entrada da tabela de símbolos para esse id 
        te = tabSimbolos.getEntry(lex)
        expr_value = self.children[1].__evaluate__()        
        #print('Valor da expressão no lado direito ' + str(expr_value))
        te.setRefValor(expr_value)
        id_node.value = expr_value   
        print('Valor do lexema ' + str(lex) +  ': ' + str(expr_value))
        return te.ref_valor
    
    def __codegen__(self):
        if (self.isDecl):
            id_node = self.children[0]
            te = tabSimbolos.getEntry(id_node.token.lexema)
            return typeNames[te.tipo] + " " + self.children[0].__codegen__() + " = " + self.children[1].__codegen__() + ";" 
        else:
            return self.children[0].__codegen__() + " = " + self.children[1].__codegen__() + ";" 
   
    def __checkTypes__(self): 
        if(self.children[0] != None and self.children[1] != None):
            if(self.children[0].__checkTypes__() == self.children[1].__checkTypes__()):            
                print('Tipos compatíveis.')
                return True
            elif (self.children[0].__checkTypes__() < self.children[1].__checkTypes__()):
                print('Tipos incompatíveis. Será realizada uma conversão permitida pela hierarquia de tipos.')
                self.children[0].__convertTo__(self.children[1].tipo)
                return True
            else: 
                print('Tipos incompatíveis. Será realizada uma conversão permitida pela hierarquia de tipos.')
                self.children[1].__convertTo__(self.children[0].tipo)
                return True    
        
    
class If(AST):
    def __init__(self, exp, c_true, c_false, father):
        AST.__init__(self, 'If', father)
        print('Criando um nó do tipo If.')
        self.children.append(exp)
        self.children.append(c_true)
        self.children.append(c_false)
        self.exp = exp;         
        self.c_true = c_true; 
        self.c_false = c_false; 
    
    def __repr__(self):
        return self.nome
    
class While(AST):
    def __init__(self, exp, commands, father):
        AST.__init__(self,'While', father)
        print('Criando um nó do tipo While.')
        self.children.append(exp)
        self.children.append(commands)
        self.exp = exp;
        self.commands = commands; 
    def __repr__(self):
        return self.nome
        
class Read(AST):
    def __init__(self, id_, father):
        AST.__init__(self,'Read', father)
        print('Criando um nó do tipo Read.')
        self.children.append(id_)
        self.id = id_;
    def __repr__(self):
        return self.nome
    
class Print(AST):
    def __init__(self, exp, father):
        AST.__init__(self,'Print', father)
        print('Criando um nó do tipo Print.')
        self.children.append(exp)
        self.exp = exp; 
    def __repr__(self):
        return self.nome

class BinOp(AST):
    def __init__(self, nome, left, op, right, father):
        AST.__init__(self,nome, father)
        self.children.append(left)
        self.children.append(right)
        self.left = left
        #self.token = 
        self.op = op
        self.right = right
        
    def __repr__(self):
        #self.left.repr();    
        return self.op
    
    def __evaluate__(self):
        print('Avaliando nó ' + str(self.nome))
        for child in self.children:
            if (child != None): 
                return child.__evaluate__()    

    def __checkTypes__(self): 
        if(self.children[0] != None and self.children[1] != None):
            if(self.children[0].__checkTypes__() == self.children[1].__checkTypes__()):            
                print('Tipos compatíveis.')
                return True
            elif (self.children[0].__checkTypes__() < self.children[1].__checkTypes__()):
                print('Tipos incompatíveis. Será realizada uma conversão permitida pela hierarquia de tipos.')
                self.children[0].__convertTo__(self.children[1].tipo)
                return True
            else: 
                print('Tipos incompatíveis. Será realizada uma conversão permitida pela hierarquia de tipos.')
                self.children[1].__convertTo__(self.children[0].tipo)
                return True     

    def __codegen__(self):
        return self.left.__codegen__() + self.op + self.right.__codegen__()
        
class LogicalOp(BinOp):
    def __init__(self, left, op, right, father):
        BinOp.__init__(self,'LogicalOp',left, op, right, father)
        print('Criando um nó do tipo LogicalOp com operador ' + str(op))
        

class ArithOp(BinOp):
    def __init__(self, left, op, right, father):
        BinOp.__init__(self,'ArithOp',left, op, right, father)
        print('Criando um nó do tipo ArithOp com operador ' + str(op))
        #print('Filho da esquerda: ' + str(self.children[0]))
        #print('Filho da direita: ' + str(self.children[1]))

    def __evaluate__(self):
        if(self.op == '+'):
            return self.left.__evaluate__() + self.right.__evaluate__()
        elif(self.op == '-'):
            return self.left.__evaluate__() - self.right.__evaluate__()
        elif(self.op == '*'):
            return self.left.__evaluate__() * self.right.__evaluate__()
        elif(self.op == '/'):
            return self.left.__evaluate__() / self.right.__evaluate__()        

    def __codegen__(self):
        return self.left.__codegen__() + self.op + self.right.__codegen__()

class RelOp(BinOp):
    def __init__(self, left, op, right, father):
        BinOp.__init__(self,'RelOp',left, op, right, father)
        print('Criando um nó do tipo RelOp com operador ' + str(op))

class Id(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self, token, father):
        AST.__init__(self,'Id', father)
        print('Criando um nó do tipo Id.')
        #self.children.append(token)        
        self.token = token        
        #ref para entrada da tabela de símbolos 
    
    def __repr__(self):
        #return repr(self.token)
        return self.token.lexema
    
    def __evaluate__(self):
        te = tabSimbolos.getEntry(self.token.lexema)
        print('Avaliando nó Id. Valor armazenado: ' + str(te.ref_valor))
        if (te.ref_valor != None):
            return te.ref_valor
        else: 
            return 0;
    
    def __codegen__(self): 
        #no caso do assembly, retornaria o local de memória ou registrador associado a esse identificador
        return self.token.lexema

class Num(AST):
    def __init__(self, token, father, tipo):
        AST.__init__(self,'Num', father)
        print('Criando um nó do tipo Num.')
        #self.children.append(token)   
        self.token = token
        self.value = token.lexema  #em python, não precisamos nos preocupar com o tipo de value 
        self.tipo = tipo
        
    def __repr__(self):
        #return repr(self.token)        
        return self.value
    
    def __evaluate__(self):
        return self.value
    
    def __checkTypes__(self):        
        return self.tipo
    
    def __convertTo__(self, novotipo):
        self.tipo = novotipo 
        #testa se o tipo atual é float e o novo tipo é int para realizar um truncamento ou arrendondamento 
    
    def __codegen__(self):         
        return str(self.value)


def print_tree(current_node, indent="", last='updown'):

    nb_children = lambda node: sum(nb_children(child) for child in node.children) + 1
    size_branch = {child: nb_children(child) for child in current_node.children}

    """ Creation of balanced lists for "up" branch and "down" branch. """
    up = sorted(current_node.children, key=lambda node: nb_children(node))
    down = []
    while up and sum(size_branch[node] for node in down) < sum(size_branch[node] for node in up):
        down.append(up.pop())

    """ Printing of "up" branch. """
    for child in up:     
        next_last = 'up' if up.index(child) is 0 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'up' in last else '│', " " * len(current_node.__repr__()))
        print_tree(child, indent=next_indent, last=next_last)

    """ Printing of current node. """
    if last == 'up': start_shape = '┌'
    elif last == 'down': start_shape = '└'
    elif last == 'updown': start_shape = ' '
    else: start_shape = '├'

    if up: end_shape = '┤'
    elif down: end_shape = '┐'
    else: end_shape = ''

    print('{0}{1}{2}{3}'.format(indent, start_shape, current_node.__repr__(), end_shape))

    """ Printing of "down" branch. """
    for child in down:
        next_last = 'down' if down.index(child) is len(down) - 1 else ''
        next_indent = '{0}{1}{2}'.format(indent, ' ' if 'down' in last else '│', " " * len(current_node.__repr__()))
        print_tree(child, indent=next_indent, last=next_last)
        

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
		print 'Entrada correta -  ' , token , 'na linha: ' , listaLinhas[0]
		listaTokens.pop(0)
		listaLexema.pop(0)
		listaLinhas.pop(0)
	else: 
		print 'Erro sintatico'
		#exit()

def Programa():
	match('INT')
	match('MAIN')
	match('LBRACKET')
	match('RBRACKET')
	match('LBRACE')
	lista = AST('decl_comando', None)    
    ast = Decl_Comando(lista);
	match('RBRACE')	
				
def Decl_Comando(lista):  
    if (listaTokens[0] == 'INT' or listaTokens[0] == 'FLOAT'):   
        lista = Declaracao(lista); 
        lista = Decl_Comando(lista);
        return lista

    elif (listaTokens[0] == 'ID' or listaTokens[0] == 'IF' or listaTokens[0] == 'WHILE' or listaTokens[0] == 'PRINT' 
          or listaTokens[0] == 'READ' or listaTokens[0] == 'LBRACE'):
       	lista = Comando(lista);
       	return Decl_Comando(lista);

    else:
    	return lista
    	


def Declaracao(lista):
	Tipo();
	match('ID')
	Decl2(lista);


def Decl2(lista):
	if(listaTokens[0] == 'COMMA'):
		match('COMMA')
		match('ID')
		Decl2(lista)

	elif(listaTokens[0] == 'PCOMMA'):
		match('PCOMMA')	
		return lista

	elif(listaTokens[0] == 'ATTR'):
		id_node = Id(listaTokens[0],None)
		match('ATTR')
		expr_node = Expressao()
		attr_node = Assign(id_node,'=',expr_node,None)
		lista.children.append(attr_node)        
        return Decl2(lista); 

  	return lista;
				

def Tipo():
	if(listaTokens[0] == 'INT'):
		match('INT')
	elif(listaTokens[0] == 'FLOAT'):
		match('FLOAT')


def Comando(lista):
	if(listaTokens[0] == 'LBRACE'):
		bloco = AST('Bloco',None)
		Bloco()
	elif(listaTokens[0] == 'ID'):
		id_node = Id(listaTokens[0],None)
		#tabela de simbolos
		Atribuicao()
	#Outra forma de fazer é criar: bloco = AST('Bloco', None); bloco.children.append(lista); return bloco;		

	elif(listaTokens[0] == 'IF'):
		if_node = AST('IF',None)
		ComandoSe()
	elif(listaTokens[0] == 'WHILE'):
		while_node = AST('WHILE',None)
		ComandoEnquanto()
	elif(listaTokens[0] == 'READ'):
		ComandoRead()
	elif(listaTokens[0] == 'PRINT'):
		ComandoPrint()

#BLOCO, EXPRESSAO

def Bloco():
	match('LBRACE')
	Comando(lista)
	match('RBRACE')

def Atribuicao():
	match('ID')
	match('ATTR')
	expr_node = Expressao()
	lista.children.append(Assign(id_node,'=',expr_node,None));
	match('PCOMMA')
	return lista


def ComandoRead():
	match('READ')
	match('ID')
	match('PCOMMA')			

def ComandoSe():
	match('IF')
	match('LBRACKET')
	expr_node = Expressao()
	if_node.children.append(expr_node)
	match('RBRACKET')
	c_true = AST('C_TRUE',None)
	if_node.children.append(c_true)
	Comando(c_true)
	ComandoSenao()

def ComandoSenao():
	if(listaTokens[0] == 'ELSE'):
		match('ELSE')
		c_false = AST('C_FALSE',None)
		if_node.children.append(c_false)
		Comando(c_false)
	else :
		return if_node

def ComandoEnquanto():
	match('WHILE')
	match('LBRACKET')
	expr_node = Expressao()
	while_node.children.append(expr_node)
	match('RBRACKET')
	c_true = AST('C_TRUE',None)
	while_node.children.append(c_true)
	Comando(c_true)
	return while_node

def ComandoPrint():
	match('PRINT')
	match('LBRACKET')
	Expressao()
	match('RBRACKET')
	match('PCOMMA')		

def Expressao(): #expressao
    global token, tabSimbolos, currentType, currentTableEntry, currentToken;    
    #ast_node = AST('ast_node', None)
    if (token.type == ID or token.type == INTEGER_CONST or 
        token.type == FLOAT_CONST or token.type == LBRACKET):        
        expr1 = T();
        expr2 = E_(expr1);
        if(expr2 != None):                    
            #ast_node.children.append(expr2)
            return expr2
        else:             
            #ast_node.children.append(expr1)
            return expr1   

def Expressao():
	Conjuncao()
	ExpressaoOpc()

def ExpressaoOpc():
	if(listaTokens[0] == 'OR'):
		match('OR')
		Conjuncao()
		ExpressaoOpc()
	else: 
		return None

def Conjuncao():
	Igualdade()
	ConjuncaoOpc()
	#todo opc precisa de parametro

def ConjuncaoOpc():
	if(listaTokens[0] == 'AND'):
		match('AND')
		Igualdade()
		ConjuncaoOpc()
	else :
		return None

def Igualdade():
	Relacao()
	IgualdadeOpc()

def IgualdadeOpc():
	if(listaTokens[0] == 'EQ' or listaTokens[0] == 'NE'):
		OpIgual()
		Relacao()
		IgualdadeOpc()
	else : 
		return None

def OpIgual():
	if(listaTokens[0] == 'EQ'):
		match('EQ')
	elif(listaTokens[0] == 'NE'):
		match('NE')	

def Relacao():
	Adicao()
	RelacaoOpc()

def RelacaoOpc():
	if(listaTokens[0] == 'LT' or listaTokens[0] == 'LE' or listaTokens[0] == 'GT' or listaTokens[0] == 'GE'):
		OpRel()
		Adicao()
		RelacaoOpc()
	else : 
		return None	

	

def OpRel():
	if(listaTokens[0] == 'LT' ):
		match('LT')
	elif(listaTokens[0] == 'LE') :
		match('LE')		
	elif(listaTokens[0] == 'GT'):
		match('GT')		
	elif(listaTokens[0] == 'GE'):
		match('GE')

def Adicao():
	Termo()
	AdicaoOpc()

def AdicaoOpc():
	if(listaTokens[0] == 'PLUS' or listaTokens[0] == 'MINUS'):
		OpAdicao()
		Termo()
		AdicaoOpc()

	else: 
		return None

def OpAdicao():
	if(listaTokens[0] == 'PLUS'):
		match('PLUS')
	elif(listaTokens[0] == 'MINUS'):
		match('MINUS')

def Termo():
	Fator()
	TermoOpc()

def TermoOpc():
	if(listaTokens[0] == 'MULT' or listaTokens[0] == 'DIV'):
		OpMult()
		Fator()
		TermoOpc()
	else: 
		return None	
	 
def OpMult():
	if(listaTokens[0] == 'MULT'):
		match('MULT')
	elif(listaTokens[0] == 'DIV'):
		match('DIV')	 

def Fator():
	if(listaTokens[0] == 'ID'):
		id_node = Id(listaTokens[0],None)
		match('ID')
		return id_node
	elif(listaTokens[0] == 'INTEGER_CONST'):
		num_node = Num(listaTokens[0],None,int_type)
		match('INTEGER_CONST')
		return num_node
	elif(listaTokens[0] == 'FLOAT_CONST'):
		num_node = Num(listaToken[0],None,float_type)
		match('FLOAT_CONST')
		return num_node
	elif(listaTokens[0] == 'LBRACKET'):
		match('LBRACKET')
		expr = Expressao()
		match('RBRACKET')	
		return expr	
