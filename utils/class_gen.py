'''
class Person:
  def __init__(mysillyobject, name, age):
    mysillyobject.name = name
    mysillyobject.age = age

  def myfunc(abc):
    print("Hello my name is " + abc.name)
'''
from utils import price_fetch

class Symbol:
    def __init__(self,symbol):
        self.name = symbol
        self.symHistory = price_fetch.yahoo(symbol)
        self.lastClose = self.symHistory['Close'].iloc[-1]
