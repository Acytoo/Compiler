
if __name__ == '__main__':
    PreDeal.Pre_Deal()      # 读取文法， 可以考虑将扫描的文法分析表保存， 以欧化结构， 加快速度
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
