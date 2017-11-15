'''
改写Scaner中产生式，符号表等为类， 方便打印， 实际作用没变， 如果时间来不及马上回退到11.11版本
11.13.2017
@acytoo
'''
class Formula():
    def __init__(self, left, right, select=None):
        self.left = left
        self.right = right
        self.select = set()

    def __str__(self):
        return self.left + ' -> ' + str(self.right) + ' Select: ' + str(self.select)

class Symbol():
    '''
    一个总的符号类
    '''
    def __init__(self, symbol, first_set=None, follow_set=None, sym_type='N'):
        self.symbol = symbol
        self.first_set = first_set
        self.follow_set = follow_set
        self.sym_type = sym_type
        self.is_nullable = False
        self.attr = {}
        self.father = None
        self.children = []
        self.lexical_value = None

    def __str__(self):
        return self.symbol + ' Derive_empty:' + str(self.is_nullable) + ' First:' + str(self.first_set) + ' Follow:' + str(self.follow_set)

    def is_terminal(self):
        return self.sym_type == 'T'


class Entry():
    def __init__(self, type, length, name):
        self.type = type
        self.length = length
        self.name = name

    def __str__(self):
        return self.name + ' ' + self.type + ' ' + str(self.length)

class QuatWithAct():
    '''
    带有活动信息的四元式
    (op, dest(Activity), source(Activity), res(Activity))
    '''
    def __init__(self, op, d, da=True, s, sa=True, r, ra=True):
        self.op = op
        self.destination = d
        self.destActivity = da
        self.source = s
        self.sourceActivity = sa
        self.result = r
        self.resActivity = ra
    def __str__(self):
        return '( '+ str(self.op)+ str(self.destination)+ str(self.source)+ str(self.result)+ ')'
