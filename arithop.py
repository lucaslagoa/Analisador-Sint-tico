#!/usr/bin/env python2.7.12
#-*- coding: utf-8 -*-

class Tree :
  def __init__(self, cargo, left=None, right=None) :
    self.cargo = cargo
    self.left  = left
    self.right = right

  def __str__(self) :
    return str(self.cargo)

def printTreePostorder(tree) :
  if tree == None : return
  printTreePostorder(tree.left)
  printTreePostorder(tree.right)
  print tree.cargo,

def getToken(tokenList, expected) :
  if tokenList[0] == expected :
    tokenList[0:1] = []   # remove the token
    return 1
  else :
    return 0
    
def getProduct(tokenList) :
  a = getNumber(tokenList)
  if getToken(tokenList, '*') :
    b = getProduct(tokenList)        # this line changed
    return Tree('*', a, b)
  else :
    return a

def getSum(tokenList) :
  a = getProduct(tokenList)
  if getToken(tokenList, '+') :
    b = getSum(tokenList)
    return Tree('+', a, b)
  else :
    return a

def getNumber(tokenList) :
  if getToken(tokenList, '(') :
    x = getSum(tokenList)      
    getToken(tokenList, ')')    
    return x
  else :
    x = tokenList[0]
    if type(x) != type(0) : return None
    tokenList[0:1] = []   
    return Tree(x, None, None)    

tokenList = [9, '*', '(', 11, '+', 5, ')', '*', 7, 'end']
tree = getSum(tokenList)
printTreePostorder(tree)

