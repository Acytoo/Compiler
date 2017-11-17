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

本文汇编代码“样式”来自图书馆的一本叫做    《现代X86汇编语言程序设计》 的书。

作者美国人Daniel Kusswurm, 张银奎、罗冰、宋维、张佩等译

2017年11月16日16点37分

修改了汇编代码的生成， 先看界面了， 可以试试以前学QT时的框架， 明天
最后一天至少要完善界面

2017年11月16日20点43分

@acytoo
'''
from PreDeal import *
from Lexer import ERR_MSG
from GrammarScanExtLib import INFO, QuatWithAct
CODE_RESULT = []
'''
保存四元式的结构换成字典， key为四元式出现顺序
'''
QUAT_DICT = {}
SEMA_ACTION_TABLE = {}
SYMBOL_STACK = []
LAST_STACK_TOP_SYMBOL = None
CODE_SIZE = 0
current_symbol_table_pos = 0
current_symbol_index = 0
CURRENT_CONDITION_NODE = None
SYMBOL_TABLE = []
index = 0
ASSEMBLY_CODE = []
data_fir_flag = True
code_fir_flag = True
variable_names = []

# program 插入的语义动作
def A11():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = 'int'
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = 4


def A12():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = 'float'
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = 4


def A13():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = 'double'
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = 8


def A14():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = 'short'
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = 2


def A15():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = 'long'
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = 4


def A21():
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['type'] = \
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.children[0].attr['type']
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.attr['length'] = \
    symbol_for_str(LAST_STACK_TOP_SYMBOL).father.children[0].attr['length']


def A22():
    '''
    current_symbol_table_pos 记录着在数据块中的起始地址信息
    '''
    global data_fir_flag
    global current_symbol_table_pos
    global current_symbol_index
    s = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.children[0]
    # print('in the A22 ', s)
    if s.attr['name'] not in variable_names:
        variable_names.append(s.attr['name'])
        SYMBOL_TABLE.append(INFO(s.attr['type'], s.attr['length'], s.attr['name'], current_symbol_table_pos))
        current_symbol_index += 1
        current_symbol_table_pos += s.attr['length']
        # print('current_symbol_table_pos', current_symbol_table_pos)
        if data_fir_flag:
            data_fir_flag = False
            ASSEMBLY_CODE.append('\n\t.data')
        ASSEMBLY_CODE.append(s.attr['name']+'\t'+'db'+'\t'+str(s.attr['length'])+' dup(0)')
    else:
        syntax_error('重定义: '+s.attr['name'], Lexer.current_row, Lexer.current_column)


def A31():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    f.attr['name'] = f.children[1].lexical_value
    # print('\nLAST_STACK_TOP_SYMBOL ', LAST_STACK_TOP_SYMBOL)
    # print('What the fuck is F', f)

    # print('HERE, IN A31', f.children[1].lexical_value)


def A41():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    f.attr['type'] = 'int'
    f.attr['value'] = f.children[0].lexical_value


def A42():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    f.attr['type'] = 'float'
    f.attr['value'] = float(f.children[0].lexical_value)


def A43():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    f.attr['type'] = 'short'
    f.attr['value'] = f.children[0].lexical_value


def A44():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    f.attr['type'] = 'long'
    f.attr['value'] = f.children[0].lexical_value


def A51():
    pass


def A52():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father
    f.attr['type'] = f.children[0].attr['type']
    f.attr['value'] = f.children[0].attr['value']


def A61():
    global index
    global code_fir_flag
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    if len(f.children) < 3:
        f = f.father.father.father.father

    l = f.children[0]
    r = f.children[2]

    fac = f.children[4]

    lv = search_for_symbol(l.lexical_value)
    if lv is None:
        syntax_error('未定义的 ' + l.lexical_value)
        return

    if lv.type != r.attr['type']:
        syntax_error('类型不匹配')
        return

    result = None
    if 'op' in fac.attr:
        if fac.attr['op'] == '+':
            result = f.attr['value'] + fac.attr['factor']
        elif fac.attr['op'] == '*':
            result = f.attr['value'] * fac.attr['factor']
        elif fac.attr['op'] == '-':
            result = f.attr['value'] - fac.attr['factor']
        elif fac.attr['op'] == '/':
            result = f.attr['value'] / fac.attr['factor']
    else:
        result = r.attr['value']
    fac.attr = {}
    code_output(lv.name + ' = ' + str(result))
    if code_fir_flag:
        code_fir_flag = False
        ASSEMBLY_CODE.append('\n\t.code\n')
    ASSEMBLY_CODE.append('mov\t'+lv.name+'\t'+str(result))
    QUAT_DICT[index]=QuatWithAct('=', str(result), '_', lv.name)
    index += 1



def A62():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father.father
    try:
        f.attr['type'] = f.children[2].attr['type']
        f.attr['value'] = f.children[2].attr['value']
    except KeyError:
        syntax_error('暂时不支持的操作')

def A71():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father
    try:
        f.attr['type'] = f.children[0].attr['type']
        f.attr['value'] = f.children[0].attr['value']
    except KeyError:
        syntax_error('暂时不支持的操作')
        return


def A72():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father
    f.attr['type'] = f.children[0].attr['type']
    f.attr['value'] = f.children[0].attr['value'] + 1


def A73():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father
    f.attr['type'] = f.children[0].attr['type']
    f.attr['value'] = f.children[0].attr['value'] - 1

'''if'''
def A81():
    global index
    global CURRENT_CONDITION_NODE
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    CURRENT_CONDITION_NODE = f
    e = f.children[2]
    code_output('IF ' + str(e.attr['value']) + ' GOTO ' + str(CODE_SIZE + 2))
    code_output(None)
    # QUAT_DICT[index]=QuatWithAct('con', str(e.attr['value']), '_', '_')
    # index += 1
    # 省去T1算式
    QUAT_DICT[index]=QuatWithAct('if', str(e.attr['value']), '_', '_')
    index += 1
    # dest = CODE_SIZE + 2
    f.attr['back'] = CODE_SIZE - 1


def A82():
    global index
    prev = CURRENT_CONDITION_NODE.attr['back']
    CODE_RESULT[prev] = 'GOTO ' + str(CODE_SIZE)
    QUAT_DICT[CODE_SIZE - 1]=QuatWithAct('ie', '_', '_', '_')
    index = CODE_SIZE


'''While'''
def A91():
    global index
    global CURRENT_CONDITION_NODE
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father
    CURRENT_CONDITION_NODE = f
    e = f.children[2]
    code_output('IF ' + str(e.attr['value']) + ' GOTO ' + str(CODE_SIZE + 2))
    code_output(None)
    QUAT_DICT[index]=QuatWithAct('wh', '_', '_', '_')
    index += 1
    QUAT_DICT[index]=QuatWithAct('con', str(e.attr['value']), '_', '_')
    index += 1
    QUAT_DICT[index]=QuatWithAct('do', 'res', '_', '_')
    index += 1
    f.attr['back'] = CODE_SIZE - 1


def A92():
    global index
    prev = CURRENT_CONDITION_NODE.attr['back']
    CODE_RESULT[prev] = 'GOTO ' + str(CODE_SIZE + 1)
    code_output('GOTO ' + str(prev - 1))
    QUAT_DICT[CODE_SIZE - 2]=QuatWithAct('we', '_', '_', '_')
    index = CODE_SIZE - 1


def A101():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father.father
    f.attr['op'] = f.children[0].lexical_value
    f.attr['factor'] = f.children[1].attr['value']


def A102():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father.father
    f.attr['op'] = f.children[0].lexical_value
    f.attr['factor'] = f.children[1].attr['value']

def A103():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father.father
    f.attr['op'] = f.children[0].lexical_value
    f.attr['factor'] = f.children[1].attr['value']

def A104():
    f = symbol_for_str(LAST_STACK_TOP_SYMBOL).father.father.father.father
    f.attr['op'] = f.children[0].lexical_value
    f.attr['factor'] = f.children[1].attr['value']


def no_action():
    pass

SEMA_ACTION_TABLE['A11'] = A11
SEMA_ACTION_TABLE['A12'] = A12
SEMA_ACTION_TABLE['A13'] = A13
SEMA_ACTION_TABLE['A14'] = A14
SEMA_ACTION_TABLE['A15'] = A15
SEMA_ACTION_TABLE['A21'] = A21
SEMA_ACTION_TABLE['A22'] = A22
SEMA_ACTION_TABLE['A31'] = A31
SEMA_ACTION_TABLE['A41'] = A41
SEMA_ACTION_TABLE['A42'] = A42
SEMA_ACTION_TABLE['A43'] = A43
SEMA_ACTION_TABLE['A44'] = A44
SEMA_ACTION_TABLE['A51'] = A51
SEMA_ACTION_TABLE['A52'] = A52
SEMA_ACTION_TABLE['A61'] = A61
SEMA_ACTION_TABLE['A62'] = A62
SEMA_ACTION_TABLE['A71'] = A71
SEMA_ACTION_TABLE['A72'] = A72
SEMA_ACTION_TABLE['A73'] = A73
SEMA_ACTION_TABLE['A81'] = A81
SEMA_ACTION_TABLE['A82'] = A82
SEMA_ACTION_TABLE['A91'] = A91
SEMA_ACTION_TABLE['A92'] = A92
SEMA_ACTION_TABLE['A101'] = A101
SEMA_ACTION_TABLE['A102'] = A102
SEMA_ACTION_TABLE['A103'] = A103
SEMA_ACTION_TABLE['A104'] = A104
SEMA_ACTION_TABLE['null'] = no_action

def search_for_symbol(name):
    for e in SYMBOL_TABLE:
        if e.name == name:
            return e

def print_symbol_table():
    for t in SYMBOL_TABLE:
        print(t)

def next_token():
    r = Lexer.scanner()
    while r is None:
        r = Lexer.scanner()
    return r

def control():
    global LAST_STACK_TOP_SYMBOL
    SYMBOL_STACK.append('#')
    SYMBOL_STACK.append('<program>')  # 《program》
    token_tuple = next_token()
    # print('The first time to run', token_tuple)

    formulas = open('formulas.txt', 'w')
    stack = open('stack.txt', 'w')
    assem_code = open('result.asm', 'w')
    ASSEMBLY_CODE.append('\t.586')
    ASSEMBLY_CODE.append('\t.model flat, c')

    while len(SYMBOL_STACK) > 0:
        stack_top_symbol = SYMBOL_STACK[-1]
        while stack_top_symbol == 'null':
            '''
            空产生式，弹栈
            '''
            SYMBOL_STACK.pop()
            stack_top_symbol = SYMBOL_STACK[-1]

        if stack_top_symbol.startswith('A'):        # 语义动作
            '''
            如果是语义动作， 就执行语义动作
            '''
            do_sema_actions(stack_top_symbol)
            SYMBOL_STACK.pop()
            stack.write(str(SYMBOL_STACK) + '\n')
            continue

        current_token = token_tuple[0]
        # print('\t3', current_token)
        # print('2', token_tuple, '\t3', current_token)

        if current_token == 'OP' or current_token == 'SEP':
            current_token = token_tuple[1]
        # print('2', token_tuple, '\t4', current_token)

        if current_token == 'EOF':
            current_token = '#'
        # print('2', token_tuple, '\t5', current_token)

        if stack_top_symbol == 'null':
            LAST_STACK_TOP_SYMBOL = SYMBOL_STACK.pop()
            continue

        if stack_top_symbol == '#':
            break

        if not is_terminal(stack_top_symbol):
            '''
            非终结符
            '''
            try:
                p = Analysis_Table[stack_top_symbol][current_token]
                # print('In the try', p)
            except KeyError:
                # Stack top symbol unmatched, ignore it
                syntax_error('不匹配')
                token_tuple = next_token()
                continue
            # print('after ', p.right)
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
            SYMBOL_STACK.extend(reversed(p.right))  # 反序压栈
            symbol_for_str((LAST_STACK_TOP_SYMBOL)).children = []
            for symbol in p.right:
                if symbol.startswith('A'):
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
    global ERR_MSG
    if row is None:
        row = Lexer.current_row + 1
    if column is None:
        column = Lexer.current_column + 1
    # print('在%d行%d列出现了%s的语法错误' % (row, column, msg))
    ERR_MSG.append('语法错误：在%d行%d列出现了%s的语法错误' % (row, column, msg))

def show_err():
    global ERR_MSG
    for i in ERR_MSG:
        print(i)

def do_sema_actions(symbol):
    SEMA_ACTION_TABLE[symbol]()


def show_ass():
    for i in ASSEMBLY_CODE:
        print(i)


def show_Quat():
    i = 0
    for i in QUAT_DICT:
        print(QUAT_DICT[i])
if __name__ == '__main__':
    print(__package__)
    Pre_Deal()      # 读取文法， 可以考虑将扫描的文法分析表保存， 以欧化结构， 加快速度
    Lexer.read_source_file('1.c')   # 读取要分析的文件
    control()
    print('错误信息')
    print("------------")
    show_err()
    print("\n符号表")
    print("------------")
    print_symbol_table()
    print("\n中间代码")
    print("------------")
    print_code_result()
    print("\n中间代码(四元式)")
    print("------------")

    show_Quat()
    print("\nX86汇编")
    print("------------")

    show_ass()
