'''
生成8086汇编代码
'''

from Parser import *



if __name__ == '__main__':
    AssemblyCode = []
    Pre_Deal()      # 读取文法， 可以考虑将扫描的文法分析表保存， 以欧化结构， 加快速度
    Lexer.read_source_file('1.c')   # 读取要分析的文件
    control()
    for i in CODE_RESULT:
        print('before: ', [i])
