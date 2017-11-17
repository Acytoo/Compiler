'''
新的词法分析器， 适配新的语义分析步骤
11.12.2017
@acytoo
'''
import sys

KEYWORD_LIST = ['if', 'else', 'while', 'break', 'continue', 'for', 'double', 'int', 'float', 'long', 'short',
                'switch', 'case', 'return', 'void']

SEPARATOR_LIST = ['{', '}', '[', ']', '(', ')', '~', ',', ';', '.', '?', ':']

OPERATOR_LIST = ['+', '++', '-', '--', '+=', '-=', '*', '*=', '%', '%=', '->', '|', '||', '|=',
                 '/', '/=', '>', '<', '>=', '<=', '=', '==', '!=', '!']

CATEGORY_DICT = {
    "double": 265,
    "int": 266,
    "break": 268,
    "else": 269,
    "switch": 271,
    "case": 272,
    "char": 276,
    "return": 278,
    "float": 281,
    "continue": 284,
    "for": 285,
    "void": 287,
    "do": 292,
    "if": 293,
    "while": 294,
    "static": 295,
    "{": 299,
    "}": 300,
    "[": 301,
    "]": 302,
    "(": 303,
    ")": 304,
    "~": 305,
    ",": 306,
    ";": 307,
    "?": 310,
    ":": 311,
    "<": 314,
    "<=": 315,
    ">": 316,
    ">=": 317,
    "=": 318,
    "==": 319,
    "|": 320,
    "||": 321,
    "|=": 322,
    "^": 323,
    "^=": 324,
    "&": 325,
    "&&": 326,
    "&=": 327,
    "%": 328,
    "%=": 329,
    "+": 330,
    "++": 331,
    "+=": 332,
    "-": 333,
    "--": 334,
    "-=": 335,
    "->": 336,
    "/": 337,
    "/=": 338,
    "*": 339,
    "*=": 340,
    "!": 341,
    "!=": 342,
    "ID": 256,
    'INT10': 346,
    'FLOAT': 347,
    'STRING': 351,
}

current_column = -1
current_row = 0
Sfile_content = []  # 源文件内容， 二维list, 行读取
ERR_MSG = []

def is_keyword(s):
    return s in KEYWORD_LIST


def is_separator(s):
    return s in SEPARATOR_LIST


def is_operator(s):
    return s in OPERATOR_LIST


def get_cate_id(s):
    return CATEGORY_DICT[s]


def ungetc():
    global current_column
    global current_row
    current_column = current_column - 1
    if current_column < 0:
        current_row = current_row - 1
        current_column = len(Sfile_content[current_column]) - 1
    return Sfile_content[current_row][current_column]


def read_source_file(file):
    '''
    打开方式加入utf8编码， 改全部读为按照行读取
    '''
    global Sfile_content
    f = open(file, 'r', encoding='utf8')
    Sfile_content = f.readlines()
    f.close()


def lexical_error(msg, row=None, column=None):
    global current_row
    global current_column
    global ERR_MSG
    if row is None:
        row = current_row + 1
    if column is None:
        column = current_column + 1
    # print('在%d行%d列出现了%s的错误' % (row, column, msg))
    ERR_MSG.append('词法错误：在%d行%d列出现了%s的词法错误' % (row, column, msg))

def getchar():
    global current_column
    global current_row
    current_column += 1
    if current_column == len(Sfile_content[current_row]):
        current_row += 1
        current_column = 0
    if current_row == len(Sfile_content):
        return 'EOF'
    return Sfile_content[current_row][current_column]


def scanner():
    global current_row
    global current_column
    '''
    扫描器第三版， 连续判断， 效率高， 去除状态跳转
    方便修改
    '''
    current_char = getchar()
    # print('\t\t\tcurrent char', [current_char])
    if current_char == '#':
        '''
        不支持引用头文件， 宏定义等。可以说明一下， 比如显示“饮用了某个头文件，
        宏定义了什么等”，但对生成汇编代码没有帮助， 所以这里就先跳过了
        '''
        current_row += 1
        current_column = 0
        return None
    if current_char == 'EOF':
        return ('EOF', '', '')
    if current_char.strip() == '':
        # 遇到空格， 跳过
        return None
    if current_char.isdigit():
        int_value = 0
        while current_char.isdigit():
            int_value = int_value * 10 + int(current_char)
            current_char = getchar()

        if current_char != '.':
            ungetc()
            return ('INT', int_value, get_cate_id('INT10'))

        float_value = str(int_value) + '.'
        current_char = getchar()
        while current_char.isdigit():
            float_value += current_char
            current_char = getchar()
        ungetc()
        return ('FLOAT', float_value, get_cate_id('FLOAT'))
    if current_char.isalpha() or current_char == '_':
        string = ''
        while current_char.isalpha() or current_char.isdigit() or current_char == '_':
            string += current_char
            current_char = getchar()
            if current_char == 'EOF':
                break

        ungetc()
        if is_keyword(string):
            return (string, '', get_cate_id(string))
        else:
            return ('ID', string, get_cate_id('ID'))

    if current_char == '\"':
        str_literal = ''
        row = current_row + 1
        column = current_column + 1

        current_char = getchar()
        while current_char != '\"':
            str_literal += current_char
            current_char = getchar()
            if current_char == 'EOF':
                lexical_error('缺少 \"', row, column)

                current_row = row
                current_column = column
                return ('EOF', '', '')
        return('STRING_LITERAL', str_literal, get_cate_id('STRING'))

    if current_char == '/':
        '''
        所有形式的注释直接跳过
        '''
        next_char = getchar()
        row = int(current_row) + 1
        column = int(current_column) + 1
        if next_char == '*':
            comment = ''
            next_char = getchar()
            while True:
                if next_char == 'EOF':
                    lexical_error('/*形式的注释未正常结束', row, column)
                    return ('EOF', '', '')
                if next_char == '*':
                    end_char = getchar()
                    if end_char == '/':
                        # /**/, 暂时忽略这个
                        return None
                    if end_char == 'EOF':
                        lexical_error('/*形式的注释未正常结束', row, column)
                        return ('EOF', '', '')
                comment += next_char
                next_char = getchar()
        elif next_char == '/':
            current_row += 1
            current_column = 0
            return None
        else:
            ungetc()
            op = current_char
            current_char = getchar()
            if is_operator(current_char):
                op += current_char
            else:
                ungetc()
            return ('OP', op, get_cate_id(op))

    if is_separator(current_char):
        return ('SEP', current_char, get_cate_id(current_char))

    if is_operator(current_char):
        op = current_char
        current_char = getchar()
        if is_operator(current_char):
            op += current_char
        else:
            ungetc()
        return ('OP', op, get_cate_id(op))
    else:
        '''
        其他情况属于位置字符串
        '''
        lexical_error('未识别的字符: ' + current_char)


if __name__ == '__main__':
    #file_name = sys.argv[1]
    file_name = '1.c'
    read_source_file(file_name)
    while True:
        r = scanner()
        if r[0] == 'EOF':
            break
        if r is not None:
            print(r)
