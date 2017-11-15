'''
2017年11月14日23点44分
初步完成生成四元式
图形界面好写， 如果时间充足可以上pyqt5, 但是我想加入语法高亮， 不知道难不那。。。。。
目标代码：多寄存器8086汇编语言？X86？
是否转移到linux上？能否与GCC对接？


可以试试用正则表达式来做词法高亮， 而语法高亮只能是生成符号表之后了

如果成功，，，，这个算是一个扩展功能。。。。。。

2017年11月15日01点15分


目前假设目标机为32位，生成X86汇编代码（至少是X86汇编的子集）

假设数据类型所占字节长度：int: 4, float:4, double:8, short:2, long:4

@acytoo
'''
from PreDeal import *
from GrammarScanExtLib import Entry, QuatWithAct
CODE_RESULT = []
QUAT_LIST = []
SEMA_ACTION_TABLE = {}
SYMBOL_STACK = []
LAST_STACK_TOP_SYMBOL = None
CODE_SIZE = 0
current_symbol_table_pos = 0
current_symbol_index = 0
CURRENT_CONDITION_NODE = None


# program 插入的语义动作
def P11():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = 'int'
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = 4


def P12():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = 'float'
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = 4


def P13():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = 'double'
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = 8


def P14():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = 'short'
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = 2


def P15():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = 'long'
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = 4


def P21():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = \
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.children[0].attr['type']
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = \
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.children[0].attr['length']


def P22():
    global current_symbol_table_pos
    global current_symbol_index
    s = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.children[0]
    SYMBOL_TABLE.append(Entry(s.attr['type'], s.attr['length'], s.attr['name']))
    current_symbol_index += 1
    current_symbol_table_pos += s.attr['length']


def P31():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    f.attr['name'] = f.children[1].lexical_value


def P41():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    f.attr['type'] = 'int'
    f.attr['value'] = f.children[0].lexical_value


def P42():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    f.attr['type'] = 'float'
    f.attr['value'] = float(f.children[0].lexical_value)


def P43():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    f.attr['type'] = 'short'
    f.attr['value'] = f.children[0].lexical_value


def P44():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    f.attr['type'] = 'long'
    f.attr['value'] = f.children[0].lexical_value


def P51():
    pass


def P52():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father
    f.attr['type'] = f.children[0].attr['type']
    f.attr['value'] = f.children[0].attr['value']


def P61():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    if len(f.children) < 3:
        f = f.father.father.father.father

    l = f.children[0]
    r = f.children[2]

    fac = f.children[4]

    lv = search_for_symbol(l.lexical_value)
    if lv is None:
        syntax_error('undefined ' + l.lexical_value)
        return

    if lv.type != r.attr['type']:
        syntax_error('type mismatch')
        return

    result = None
    if 'op' in fac.attr:
        if fac.attr['op'] == '+':
            result = f.attr['value'] + fac.attr['factor']

        if fac.attr['op'] == '*':
            result = f.attr['value'] * fac.attr['factor']
    else:
        result = r.attr['value']
    fac.attr = {}
    code_output(lv.name + ' = ' + str(result))




    '''

    QUAT_LIST.append(QuatWithAct('=', ))


    '''


def P62():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father.father
    f.attr['type'] = f.children[2].attr['type']
    f.attr['value'] = f.children[2].attr['value']


def P71():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father
    f.attr['type'] = f.children[0].attr['type']
    f.attr['value'] = f.children[0].attr['value']


def P72():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father
    f.attr['type'] = f.children[0].attr['type']
    f.attr['value'] = f.children[0].attr['value'] + 1


def P73():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father
    f.attr['type'] = f.children[0].attr['type']
    f.attr['value'] = f.children[0].attr['value'] - 1


def P81():
    global CURRENT_CONDITION_NODE
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    CURRENT_CONDITION_NODE = f
    e = f.children[2]
    code_output('IF ' + str(e.attr['value']) + ' GOTO ' + str(CODE_SIZE + 2))
    code_output(None)
    f.attr['back'] = CODE_SIZE - 1


def P82():
    prev = CURRENT_CONDITION_NODE.attr['back']
    CODE_RESULT[prev] = 'GOTO ' + str(CODE_SIZE)


def P91():
    global CURRENT_CONDITION_NODE
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    CURRENT_CONDITION_NODE = f
    e = f.children[2]
    code_output('IF ' + str(e.attr['value']) + ' GOTO ' + str(CODE_SIZE + 2))
    code_output(None)
    f.attr['back'] = CODE_SIZE - 1


def P92():
    prev = CURRENT_CONDITION_NODE.attr['back']
    CODE_RESULT[prev] = 'GOTO ' + str(CODE_SIZE + 1)
    code_output('GOTO ' + str(prev - 1))


def P101():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father.father
    f.attr['op'] = f.children[0].lexical_value
    f.attr['factor'] = f.children[1].attr['value']


def P102():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father.father
    f.attr['op'] = f.children[0].lexical_value
    f.attr['factor'] = f.children[1].attr['value']


def no_action():
    pass


SEMA_ACTION_TABLE['P11'] = P11
SEMA_ACTION_TABLE['P12'] = P12
SEMA_ACTION_TABLE['P13'] = P13
SEMA_ACTION_TABLE['P14'] = P14
SEMA_ACTION_TABLE['P15'] = P15
SEMA_ACTION_TABLE['P21'] = P21
SEMA_ACTION_TABLE['P22'] = P22
SEMA_ACTION_TABLE['P31'] = P31
SEMA_ACTION_TABLE['P41'] = P41
SEMA_ACTION_TABLE['P42'] = P42
SEMA_ACTION_TABLE['P43'] = P43
SEMA_ACTION_TABLE['P44'] = P44
SEMA_ACTION_TABLE['P51'] = P51
SEMA_ACTION_TABLE['P52'] = P52
SEMA_ACTION_TABLE['P61'] = P61
SEMA_ACTION_TABLE['P62'] = P62
SEMA_ACTION_TABLE['P71'] = P71
SEMA_ACTION_TABLE['P72'] = P72
SEMA_ACTION_TABLE['P73'] = P73
SEMA_ACTION_TABLE['P81'] = P81
SEMA_ACTION_TABLE['P82'] = P82
SEMA_ACTION_TABLE['P91'] = P91
SEMA_ACTION_TABLE['P92'] = P92
SEMA_ACTION_TABLE['P101'] = P101
SEMA_ACTION_TABLE['P102'] = P102
SEMA_ACTION_TABLE['null'] = no_action

def search_for_symbol(name):
    for e in SYMBOL_TABLE:
        if e.name == name:
            return e


def next_token():
    r = Lexer.scanner()
    while r is None:
        r = Lexer.scanner()
    return r

def control():
    global LAST_STACK_TOP_SYMBOL
    SYMBOL_STACK.append('#')
    SYMBOL_STACK.append('<s>')  # 《program》

    token_tuple = next_token()

    formulas = open('formulas.txt', 'w')
    stack = open('stack.txt', 'w')
    while len(SYMBOL_STACK) > 0:
        stack_top_symbol = SYMBOL_STACK[-1]
        while stack_top_symbol == 'null':
            SYMBOL_STACK.pop()
            stack_top_symbol = SYMBOL_STACK[-1]

        if stack_top_symbol.startswith('P'):        # 语义动作
            do_sema_actions(stack_top_symbol)
            SYMBOL_STACK.pop()
            stack.write(str(SYMBOL_STACK) + '\n')
            continue

        current_token = token_tuple[0]
        if current_token == 'OP' or current_token == 'SEP':
            current_token = token_tuple[1]

        if current_token == 'EOF':
            current_token = '#'

        if stack_top_symbol == 'null':
            LAST_STACK_TOP_SYMBOL = SYMBOL_STACK.pop()
            continue

        if stack_top_symbol == '#':
            break

        if not is_terminal(stack_top_symbol):
            try:
                p = Analysis_Table[stack_top_symbol][current_token]
            except KeyError:
                # Stack top symbol unmatched, ignore it
                syntax_error('unmatched')
                token_tuple = next_token()
                continue

            if p == 'SYNC':
                # SYNC recognized, pop Stack
                syntax_error("sync symbol, recovering")
                LAST_STACK_TOP_SYMBOL = SYMBOL_STACK.pop()
                stack.write(str(SYMBOL_STACK) + '\n')
                formulas.write(str(p) + '\n')
                continue

            stack.write(str(SYMBOL_STACK) + '\n')
            formulas.write(str(p) + '\n')
            LAST_STACK_TOP_SYMBOL = SYMBOL_STACK.pop()
            SYMBOL_STACK.extend(reversed(p.right))
            symbol_for_str((LAST_STACK_TOP_SYMBOL)).children = []
            for symbol in p.right:
                if symbol.startswith('P'):
                    symbol_for_str(LAST_STACK_TOP_SYMBOL).children.append(symbol)
                    continue

                if symbol == 'null':
                    continue
                t = symbol_for_str(symbol)
                symbol_for_str(LAST_STACK_TOP_SYMBOL).children.append(t)
                t.father = symbol_for_str(LAST_STACK_TOP_SYMBOL)


        else:
            symbol_for_str(stack_top_symbol).lexical_value = token_tuple[1]
            LAST_STACK_TOP_SYMBOL = SYMBOL_STACK.pop()
            stack.write(str(SYMBOL_STACK) + '\n')
            token_tuple = next_token()

    formulas.close()
    stack.close()
def code_output(code):
    global CODE_SIZE
    CODE_SIZE += 1
    CODE_RESULT.append(code)

def print_code_result():
    for r in CODE_RESULT:
        print(str(CODE_RESULT.index(r)) + ': ' + r)

def syntax_error(msg, row=None, column=None):
    if row is None:
        row = Lexer.current_row + 1
    if column is None:
        column = Lexer.current_column + 1
    print('在%d行%d列出现了%s的语法错误' % (row, column, msg))

def do_sema_actions(symbol):
    SEMA_ACTION_TABLE[symbol]()


if __name__ == '__main__':
    Pre_Deal()      # 读取文法， 可以考虑将扫描的文法分析表保存， 以欧化结构， 加快速度
    Lexer.read_source_file('1.c')   # 读取要分析的文件
    control()
    print("符号表")
    print("------------")
    print_symbol_table()
    print('\n')
    print("中间代码")
    print("------------")
    print_code_result()
    print('Withour Deal\n\n')
    print(CODE_RESULT)
    #prettyprint_parsing_table()
