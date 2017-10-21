#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-

import unicodedata
import re
from analex import *
import hashlib

object1 = Lexico()

object1.run()


listaTokens = object1.listaTokens['tokens']
listaLexema = object1.listaTokens['lexema']
listaLinhas = object1.listaTokens['linhas']

id_node = None

int_type = 0
float_type = 1
dicionario = {}


class AST(object):
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
                x = child.__evaluate__()


        
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
        lex = id_node.lexema
        tipo = dicionario[lex][0]
        dict3 = {}
        expr_value = self.children[1].__evaluate__()
        dict3[lex] = (tipo, expr_value)
        dicionario.update(dict3)

       	
    
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
    
    def __init__(self,nome):
    	AST.__init__(self, nome, None)
    	
    def __repr__(self):
        return self.nome

    def __evaluate__(self):
    	print('Avaliando If.')
        valor = self.children[0].__evaluate__()
        if(valor == True):
            self.children[1].__evaluate__()
        else:
        	if(len(self.children) is not 2):
        		self.children[2].__evaluate__()    

class While(AST):
    def __init__(self, exp, commands, father):
        AST.__init__(self,'While', father)
        print('Criando um nó do tipo While.')
        self.children.append(exp)
        self.children.append(commands)
        self.exp = exp;
        self.commands = commands; 
    def __init__(self,nome):
    	AST.__init__(self, nome, None)

    def __repr__(self):
        return self.nome

    def __evaluate__(self):
    	print('Avaliando While.')
        valor = self.children[0].__evaluate__()
        while(valor == True):
        	self.children[1].__evaluate__()
        	if (self.children[1].__evaluate__() == True):
        		valor = self.children[0].__evaluate__()
        	else:
        		valor = False		

        
class Read(AST):
    def __init__(self, id_, father):
        AST.__init__(self,'Read', father)
        print('Criando um nó do tipo Read.')
        self.children.append(id_)
        self.id = id_;
    def __init__(self,nome):
    	AST.__init__(self, nome, None)    
    def __repr__(self):
        return self.nome
    
class Print(AST):
    def __init__(self, exp, father):
        AST.__init__(self,'Print', father)
        print('Criando um nó do tipo Print.')
        self.children.append(exp)
        self.exp = exp;
    def __init__(self,nome):
		AST.__init__(self, nome, None)	

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

    def __evaluate__(self):
    	print('Avaliando LogicalOp.')
    	a = self.children[0].__evaluate__()
        b = self.children[1].__evaluate__()
    	if(self.op == '&&'):
        	if(a is True and b is True):
        		c = True
        		return c
        	else:
        		c = False
        		return c
        elif(self.op == '||'):
        	if(a is True or b is True):
        		c = True
        		return c
        	else:
        		c = False
        		return c

        

class ArithOp(BinOp):
    def __init__(self, left, op, right, father):
        BinOp.__init__(self,'ArithOp',left, op, right, father)
        print('Criando um nó do tipo ArithOp com operador ' + str(op))

    def __evaluate__(self):
        a = self.children[0].__evaluate__()
        b = self.children[1].__evaluate__()
        if(self.op == '+'):
        	c = float(a) + float(b)
        	return c
        elif(self.op == '-'):
        	c = float(a) - float(b)
        	return c
        elif(self.op == '*'):
            c = float(a) * float(b)
            return c
        elif(self.op == '/'):
            c = float(a) / float(b)
            return c

    def __codegen__(self):
        return self.left.__codegen__() + self.op + self.right.__codegen__()

class RelOp(BinOp):
    def __init__(self, left, op, right, father):
        BinOp.__init__(self,'RelOp',left, op, right, father)
        print('Criando um nó do tipo RelOp com operador ' + str(op))
    def __evaluate__(self):
    	a = self.children[0].__evaluate__()
        b = self.children[1].__evaluate__()
        if(self.op == '<'):
        	if(a < b):
        		c = True
        		return c
        	else:
        		c = False
        		return c
        elif(self.op == '<='):
        	if(a <= b):
        		c = True
        		return c
        	else:
        		c = False
        		return c
        elif(self.op == '>'):
        	if(a > b):
        		c = True
        		return c
        	else:
        		c = False
        		return c
        elif(self.op == '>='):
        	if(a >= b):
        		c = True
        		return c
        	else:
        		c = False
        		return c
        elif(self.op == '=='):
        	if(a == b):
        		c = True
        		return c
        	else:
        		c = False
        		return c
        elif(self.op == '!='):
        	if(a != b):
        		c = True
        		return c
        	else:
        		c = False
        		return c

class Id(AST):
    """The Var node is constructed out of ID token."""
    def __init__(self,token,lexema,father):
        AST.__init__(self,'Id',father)
        print('Criando um nó do tipo Id.')
        #self.children.append(token)        
        self.token = token 
        self.lexema = lexema       
        #ref para entrada da tabela de símbolos 
    
    def __repr__(self):
        #return repr(self.token)
        return self.token
    
    def __evaluate__(self):
        te = dicionario[self.lexema][1]
        if (te != None):
            return te
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
        self.value = token #em python, não precisamos nos preocupar com o tipo de value 
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
	dict2 = {}
	for i in range(0,tamanho): 
		if((listaTokens[i] == 'INT' and listaTokens[i+1] == 'ID') or (listaTokens[i] == 'FLOAT' and listaTokens[i+1] == 'ID')):
			tipo = []
			tipo.append(listaTokens[i])
			i = i+1
			while(listaTokens[i] != 'PCOMMA'):
				if(listaTokens[i] == 'ID'):
					dict2[listaLexema[i]] = (tipo, 0)
					dicionario.update(dict2)
					if(listaTokens[i+1] == 'PCOMMA'):
						dict2[listaLexema[i]] = (tipo, 0)
						dicionario.update(dict2)
					if(listaTokens[i+1] == 'ATTR' and listaTokens[i+2] == 'ID'):
						dict2[listaLexema[i]] = (tipo, 0)
						dicionario.update(dict2)	
					if((listaTokens[i+1] == 'ATTR' and listaTokens[i+2] == 'INTEGER_CONST') or (listaTokens[i+1] == 'ATTR' or listaTokens[i+2] == 'FLOAT_CONST')):
						dict2[listaLexema[i]] = (tipo, listaLexema[i+2])
						dicionario.update(dict2)
					if(listaTokens[i+1] == 'COMMA'):
						dict2[listaLexema[i]] = (tipo, 0)
						dicionario.update(dict2)
								
				i=i+1
	print dicionario
	return dicionario


def match(token):
	if(listaTokens[0] == token):
		print 'Entrada correta -  ' , token , 'na linha: ' , listaLinhas[0]
		listaTokens.pop(0)
		listaLexema.pop(0)
		listaLinhas.pop(0)
	else: 
		print 'Erro sintatico'

def Programa():
	match('INT')
	match('MAIN')
	match('LBRACKET')
	match('RBRACKET')
	match('LBRACE')
	lista = AST('decl_comando', None)    
   	ast = Decl_Comando(lista);
	match('RBRACE')
	return ast
				
def Decl_Comando(lista):  
    if (listaTokens[0] == 'INT' or listaTokens[0] == 'FLOAT'):   
        lista1 = Declaracao(lista); 
        return Decl_Comando(lista1);      
    elif (listaTokens[0] == 'ID' or listaTokens[0] == 'IF' or listaTokens[0] == 'WHILE' or listaTokens[0] == 'PRINT' 
          or listaTokens[0] == 'READ' or listaTokens[0] == 'LBRACE'):
       	lista1 = Comando(lista);
       	return Decl_Comando(lista1);
    else:
    	return lista
    	
def Declaracao(lista):
	global id_node
	Tipo();
	if(listaTokens[0] == 'ID'):
		id_node = Id(listaTokens[0],listaLexema[0],None)
		match('ID')

	return Decl2(lista);

def Decl2(lista):
	global id_node

	if(listaTokens[0] == 'COMMA'):
		match('COMMA')
		match('ID')
		return Decl2(lista)

	elif(listaTokens[0] == 'PCOMMA'):
		match('PCOMMA')	
		return lista

	elif(listaTokens[0] == 'ATTR'):
		match('ATTR')
		expr_node = Expressao()
		attr_node = Assign(id_node,'=',expr_node,None)
		attr_node.__setIsDecl__(True)
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
		return Bloco(lista)
	elif(listaTokens[0] == 'ID'):
		return Atribuicao(lista)
	elif(listaTokens[0] == 'IF'):
		return ComandoSe(lista)
	elif(listaTokens[0] == 'WHILE'):
		return ComandoEnquanto(lista)
	elif(listaTokens[0] == 'READ'):
		return ComandoRead(lista)
	elif(listaTokens[0] == 'PRINT'):
		return ComandoPrint(lista)

def Bloco(lista):
	bloco = AST('Bloco',None)
	match('LBRACE')
	retorno = Decl_Comando(bloco)
	match('RBRACE')	
	lista.children.append(retorno)

	return lista

def Atribuicao(lista):
	id_node = Id(listaTokens[0],listaLexema[0],None)
	print listaLexema[0], "lista lexema"
	match('ID')
	match('ATTR')
	expr_node = Expressao()
	lista.children.append(Assign(id_node,'=',expr_node,None));
	match('PCOMMA')
	return lista


def ComandoRead(lista):
	read_node = Read('READ')
	match('READ')
	id_node = Id(listaTokens[0],listaLexema[0],None)
	read_node.children.append(id_node)
	match('ID')
	match('PCOMMA')	
	lista.children.append(read_node)		
	return lista

def ComandoSe(lista):
	if_node = If('IF')
	match('IF')
	match('LBRACKET')
	expr_node = Expressao()
	if_node.children.append(expr_node)
	match('RBRACKET')
	c_true = AST('C_TRUE',None)
	retorno = Comando(c_true)
	if_node.children.append(retorno)
	ComandoSenao(if_node)	
	lista.children.append(if_node)
	return lista

def ComandoSenao(if_node):
	if(listaTokens[0] == 'ELSE'):
		c_false = AST('C_FALSE',None)
		match('ELSE')
		retorno = Comando(c_false)
		if_node.children.append(retorno)
		return if_node
	else :
		return if_node

def ComandoEnquanto(lista):
	while_node = While('WHILE')
	match('WHILE')
	match('LBRACKET')
	expr_node = Expressao()
	while_node.children.append(expr_node)
	match('RBRACKET')
	c_true = AST('C_TRUE',None)
	retorno = Comando(c_true)
	while_node.children.append(retorno)
	lista.children.append(while_node)
	return lista

def ComandoPrint(lista):
	print_node = Print('PRINT')
	match('PRINT')
	match('LBRACKET')
	expr = Expressao()
	print_node.children.append(expr)
	match('RBRACKET')
	match('PCOMMA')	
	lista.children.append(print_node)	
	return lista


def Expressao(): #expressao        
    expr = Conjuncao();
    return ExpressaoOpc(expr);

def ExpressaoOpc(expr):
	if(listaTokens[0] == 'OR'):
		match('OR')
		expr2 = Conjuncao()
		or_node = LogicalOp(expr,'||',expr2,None)
		expr2 = ExpressaoOpc(or_node)		
		return expr2
	else: 
		return expr

def Conjuncao():
	expr = Igualdade()
	return ConjuncaoOpc(expr)


def ConjuncaoOpc(expr):
	if(listaTokens[0] == 'AND'):
		match('AND')
		expr2= Igualdade()
		and_node = LogicalOp(expr,'&&',expr2,None)
		expr2 = ConjuncaoOpc(and_node)		
		return expr2
	else :
		return expr

def Igualdade():
	expr = Relacao()
	return IgualdadeOpc(expr)

def IgualdadeOpc(expr):
	if(listaTokens[0] == 'EQ'):
		OpIgual()
		expr2 = Relacao()
		igual_node = RelOp(expr,'==',expr2,None)
		return IgualdadeOpc(igual_node)

	elif(listaTokens[0] == 'NE'):
		OpIgual()
		expr2 = Relacao()
		diferente_node = RelOp(expr,'!=',expr2,None)
		return IgualdadeOpc(diferente_node)

	else : 
		return expr

def OpIgual():
	if(listaTokens[0] == 'EQ'):
		match('EQ')
	elif(listaTokens[0] == 'NE'):
		match('NE')	

def Relacao():
	expr = Adicao()
	return RelacaoOpc(expr)

def RelacaoOpc(expr):
	if(listaTokens[0] == 'LT'):
		OpRel()
		expr2 = Adicao()
		menor_node = RelOp(expr,'<',expr2,None)
		return RelacaoOpc(menor_node)
	elif(listaTokens[0] == 'LE'):
		OpRel()
		expr2 = Adicao()
		menorigual_node = RelOp(expr,'<=',expr2,None)
		return RelacaoOpc(menorigual_node)
	elif(listaTokens[0] == 'GT'):
		OpRel()
		expr2 = Adicao()
		maior_node = RelOp(expr,'>',expr2,None)
		return RelacaoOpc(maior_node)
	elif(listaTokens[0] == 'GE'):
		OpRel()
		expr2 = Adicao()
		maiorigual_node = RelOp(expr,'>=',expr2,None)
		return RelacaoOpc(maiorigual_node)
	else : 
		return expr	

	

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
	expr = Termo()
	return AdicaoOpc(expr)

def AdicaoOpc(expr):
	if(listaTokens[0] == 'PLUS'):
		OpAdicao()
		expr2 = Termo()
		plus_node = ArithOp(expr,'+',expr2,None)
		return AdicaoOpc(plus_node)

	elif(listaTokens[0] == 'MINUS'):
		OpAdicao()
		expr2 = Termo()
		minus_node = ArithOp(expr,'-',expr2,None)
		return AdicaoOpc(minus_node)

	else: 
		return expr

def OpAdicao():
	if(listaTokens[0] == 'PLUS'):
		match('PLUS')
	elif(listaTokens[0] == 'MINUS'):
		match('MINUS')

def Termo():
	expr = Fator()
	return TermoOpc(expr)

def TermoOpc(expr):
	if(listaTokens[0] == 'MULT'):
		OpMult()
		expr2 = Fator()
		mult_node = ArithOp(expr,'*',expr2,None)
		return TermoOpc(mult_node)

	elif(listaTokens[0] == 'DIV'):
		OpMult()
		expr2 = Fator()
		div_node = ArithOp(expr,'/',expr2,None)
		return TermoOpc(div_node)	
	else: 
		return expr	
	 
def OpMult():
	if(listaTokens[0] == 'MULT'):
		match('MULT')
	elif(listaTokens[0] == 'DIV'):
		match('DIV')	 

def Fator():
	if(listaTokens[0] == 'ID'):
		id_node = Id(listaTokens[0],listaLexema[0],None)
		print listaLexema[0], "lista lexema"
		match('ID')
		return id_node
	elif(listaTokens[0] == 'INTEGER_CONST'):
		num_node = Num(listaLexema[0],None,int_type)
		match('INTEGER_CONST')
		return num_node
	elif(listaTokens[0] == 'FLOAT_CONST'):
		num_node = Num(listaLexema[0],None,float_type)
		match('FLOAT_CONST')
		return num_node
	elif(listaTokens[0] == 'LBRACKET'):
		match('LBRACKET')
		expr = Expressao()
		match('RBRACKET')	
		return expr	
