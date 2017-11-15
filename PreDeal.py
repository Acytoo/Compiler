'''
导入文法， 预计以后不再修改文法后，可以将结果保存， 以便以后分析程序更快
为新数据结构做出修改
因为不支持头文件引入， 所以没有加入include的判断， 如果要求可以判断# include开头就跳过这一行
11.13.2017
@acytoo
'''


import Lexer
from GrammarScanExtLib import Formula, Symbol

TERMINAL_SET = set()

NON_TERMINAL_SET = set()

SYMBOL_DICT = {}

FORMULA_LIST = []

Analysis_Table = {}

SYMBOL_TABLE = []

def symbol_for_str(string):
    return SYMBOL_DICT[string]


def is_terminal(string):
    return string in TERMINAL_SET


def Scan_Grammar():

    f = open('grammer.txt', 'r', encoding='utf8')
    lines = f.readlines()
    terminal = False
    formula = False
    for line in lines:

        if line.strip()[0] == '$':
            continue
        '''
        if line.strip() == '':
            continue
        注意：不能有空行， 会增加一层判断， 意义不大并且影响程序效率
        '''
        if line.strip() == '*terminals':
            terminal = True
            formula = False
            continue
        if line.strip() == '*productions':
            terminal = False
            formula = True
            continue
        if line.strip() == '*end':
            break
        if terminal:
            TERMINAL_SET.update([line.strip()])
        if formula:
            left = line.split('::=')[0].strip()
            NON_TERMINAL_SET.update([left])

            try:
                right = line.split('::=')[1].strip()
                if right == '':
                    raise IndexError
                p = Formula(left, right.split(' '))
            except IndexError:
                p = Formula(left, ['null'])

            FORMULA_LIST.append(p)

    for s in TERMINAL_SET:
        sym = Symbol(s, sym_type='T')
        SYMBOL_DICT[s] = sym

    for s in NON_TERMINAL_SET:
        sym = Symbol(s, sym_type='N')
        SYMBOL_DICT[s] = sym


def Deduce_Empty():
    '''
    判断是否能产生空产生式
    '''
    changes = True
    while changes:
        changes = False
        for p in FORMULA_LIST:
            if not symbol_for_str(p.left).is_nullable:
                if p.right[0] == 'null':
                    symbol_for_str(p.left).is_nullable = True
                    changes = True
                    continue
                else:
                    right_is_nullable = symbol_for_str(p.right[0]).is_nullable
                    # For X -> Y1 ... YN, Nullable(X) = Nullable(Y1) &
                    # Nullable(Y2) ... & Nullable(YN)
                    for r in p.right[1:]:
                        if r.startswith('P'):
                            continue
                        right_is_nullable = right_is_nullable & symbol_for_str(
                            r).is_nullable

                    if right_is_nullable:
                        changes = True
                        symbol_for_str(p.left).is_nullable = True


def Gen_First():
    '''
    计算first集合, 转所求元素first集合为所有元素first集合
    @acytoo
    '''
    for s in TERMINAL_SET:
        # For each terminal, initialize First with itself.
        sym = SYMBOL_DICT[s]
        sym.first_set = set([s])

    for s in NON_TERMINAL_SET:
        sym = SYMBOL_DICT[s]
        if sym.is_nullable:
            sym.first_set = set(['null'])
        else:
            sym.first_set = set()

    while True:
        first_set_is_stable = True
        for p in FORMULA_LIST:
            sym_left = symbol_for_str(p.left)
            if p.right[0] == 'null':
                sym_left.first_set.update(set(['null']))
                continue
            previous_first_set = set(sym_left.first_set)

            for s in p.right:
                # For X -> Y..., First(X) = First(X) U First(Y)
                sym_right = symbol_for_str(s)
                sym_left.first_set.update(sym_right.first_set)
                # For X -> Y1 Y2 ... Yi-1 , if Y1...Yi-1 is all nullable
                # Then First(X) = First(X) U First(Y1) U First(Y2) ...
                if sym_right.is_nullable:
                    continue
                else:
                    break

            if previous_first_set != sym_left.first_set:
                first_set_is_stable = False

        if first_set_is_stable:
            break


def Gen_Follow():
    """
    同first，适应新符号集修改，如遇bug, 回退11.11版本
    @acytoo
    """
    for s in NON_TERMINAL_SET:
        sym = symbol_for_str(s)
        sym.follow_set = set()

    symbol_for_str('<s>').follow_set.update(set(['#']))

    while True:
        follow_set_is_stable = True
        for p in FORMULA_LIST:
            sym_left = symbol_for_str(p.left)
            if sym_left.is_terminal():
                continue
            for s in p.right:
                if s == 'null':
                    continue
                if s.startswith('P'):
                    continue
                if symbol_for_str(s).is_terminal():
                    continue
                current_symbol = symbol_for_str(s)
                previous_follow_set = set(current_symbol.follow_set)
                next_is_nullable = True
                for s2 in p.right[p.right.index(s) + 1:]:
                    if s2.startswith('P'):
                        continue
                    # For X -> sYt, Follow(Y) = Follow(Y) U First(t)
                    next_symbol = symbol_for_str(s2)
                    current_symbol.follow_set.update(next_symbol.first_set)
                    if next_symbol.is_nullable:
                        continue
                    else:
                        next_is_nullable = False
                        break
                if next_is_nullable:
                    # For X -> sYt, if t is nullable, Follow(Y) = Follow(Y) U
                    # Follow(X)
                    current_symbol.follow_set.update(sym_left.follow_set)

                if current_symbol.follow_set != previous_follow_set:
                    follow_set_is_stable = False

        if follow_set_is_stable:
            break


def Gen_Select():
    """
    最终得到select集
    """
    while True:
        select_set_is_stable = True
        for p in FORMULA_LIST:
            sym_left = symbol_for_str(p.left)
            previous_select = set(p.select)
            if p.right[0] == 'null':
                # For A -> a, if a is null, Select(i) = Follow(A)
                p.select.update(sym_left.follow_set)
                continue
            sym_right = symbol_for_str(p.right[0])
            # Otherwise, Select(i) = First(a)
            p.select.update(sym_right.first_set)
            # If a is nullable, Select(i) = First(a) U Follow(A)
            if sym_right.is_nullable:
                p.select.update(sym_right.first_set.union(sym_left.follow_set))
            if previous_select != p.select:
                select_set_is_stable = False
        if select_set_is_stable:
            break


def Gen_Ana_Table():
    """
    产生分析表
    """
    global Analysis_Table
    for non_terminal in NON_TERMINAL_SET:
        if non_terminal.startswith('P'):
            continue
        Analysis_Table[non_terminal] = {}
        for p in FORMULA_LIST:
            if non_terminal == p.left:
                for symbol in p.select:
                    Analysis_Table[non_terminal][symbol] = p
        # Calculate SYNC


        for symbol in symbol_for_str(non_terminal).follow_set:
            if is_terminal(symbol):
                try:
                    p = Analysis_Table[non_terminal][symbol]
                except KeyError:
                    Analysis_Table[non_terminal][symbol] = 'SYNC'

        for symbol in symbol_for_str(non_terminal).first_set:
            if is_terminal(symbol):
                try:
                    p = Analysis_Table[non_terminal][symbol]
                except KeyError:
                    Analysis_Table[non_terminal][symbol] = 'SYNC'


def print_symbol_table():
    for t in SYMBOL_TABLE:
        print(t)

def Pre_Deal():
    '''
    总调用，扫描文法，生成first, follow, select, 集合， 生成表格：注意：修改了follow集合的
    求法， 以及对应的表示方法， 在调用时应注意， 11.11.2017
    @acytoo
    '''
    Scan_Grammar()
    Deduce_Empty()
    Gen_First()
    Gen_Follow()
    Gen_Select()
    Gen_Ana_Table()

def show_ana_tab():
    for i in Analysis_Table:
        print(i)
def prettyprint_parsing_table():
    for non_terminal in Analysis_Table.keys():
        symbol_to_production_list = []
        for symbol in Analysis_Table[non_terminal]:
            p = Analysis_Table[non_terminal][symbol]
            symbol_to_production = str(symbol) + ':' + str(p)
            symbol_to_production_list.append(symbol_to_production)

        print(non_terminal)
        print(symbol_to_production_list)

if __name__ == '__main__':
    Pre_Deal()
    # Lexer.read_source_file('1.c')
    # show_ana_tab()
    # prettyprint_parsing_table()
