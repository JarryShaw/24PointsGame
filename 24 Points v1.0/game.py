# -*- coding: utf-8 -*-

from random import randint
from itertools import permutations
from copy import copy

class Game:
    #初始化Game實例
    def __init__(self):
        self.problem = [0, 0, 0, 0]     #題目將被存儲在self.problem數組中
        self.hint = ''                  #提示將被存儲在self.hint字符串中
        self.make_problem()

    #根據調用__init__.Game實例的ptr參數返回相應信息
    def __getitem__(self, ptr):     
        if ptr == 0:
            return self.num
        else:
            return self.hint
    
    #打印題目
    def print_problem(self):
        for num in self.problem:
            print '\t',
            print num,
        print 
        #self.print_hint()

    #生成題目
    def make_problem(self):       
        for tmp in range(4):
            self.problem[tmp] += randint(1,13)

    #判斷輸入答案是否正確
    def check_answer(self, answer): 
        try:
            rst = eval(answer)
            if rst == 24:   return 1
            else        :   return 0
        except:
            return 0

    #打印提示
    def print_hint(self):           
        self.make_hint()

        if self.hint == '-1':
            print "本題無解。"
        else:
            print "一可能解為：", self.hint

    #將提示串預處理便於打印
    def probe_hint(self):
        #提示為空的情況
        if self.hint == '':         
            self.hint = '-1'
            return

        #將self.hint中存儲的十六進制數轉化爲十進制輸出
        hint_formula = ''           
        for char in self.hint:
            if      char == 'A':    hint_formula += str(10);   continue
            elif    char == 'B':    hint_formula += str(11);   continue
            elif    char == 'C':    hint_formula += str(12);   continue
            elif    char == 'D':    hint_formula += str(13);   continue
            else:   hint_formula += char
        self.hint = hint_formula

    #生成提示
    def make_hint(self):

        #possible_hint中存儲信息的通式
        #   A、B、C、D    分別表示四個數字（十六進制）
        #   %            表示+、-、*、/四個運算符之一
        #   _            表示括號或為空位

        # _ _ A % _ _ B _ % _  C  _  _  %  D  _  _
        # 0 1 2 3 4 5 6 7 8 9 10 11 12 13 14 15 16

        num_string = ''                         #存儲轉化為十六進制的self.num
        operators = '+-*/'*3
        possible_hint = ['0', '0', '0', '0',
                         '0', '0', '0', '0',
                         '0', '0', '0', '0',
                         '0', '0', '0', '0',
                         '0']
        parentheses = [                         #括號可能的組合及其坐標
                        [-1],
                        [1, 7],
                        [1, 11],
                        [5, 11],
                        [5, 15],
                        [9, 15],
                        [0, 12, 1, 7],
                        [1, 7, 9, 15],
                        [4, 16, 5, 11],
                        [5, 15, 9, 16],
                        [0, 11, 5, 12]
                    ]

        #將self.num中的數字轉化為十六進制存儲
        for num in self.problem:
            if num <= 9:    num_string += str(num); continue
            if num == 10:   num_string += 'A';      continue
            if num == 11:   num_string += 'B';      continue
            if num == 12:   num_string += 'C';      continue
            if num == 13:   num_string += 'D';      continue

        #對所有可能排列進行組合並驗算
        for item in list(map("".join, permutations(num_string))):               #全排列數字組合
            tmp1 = 2
            for digit in item:
                possible_hint[tmp1] = digit
                tmp1 += 4
            for operator in list(map("".join, permutations(operators, 3))):     #全排列運算符組合
                tmp2 = 3
                for opt in operator:
                    possible_hint[tmp2] = opt
                    tmp2 += 5
                for turple in parentheses:                                      #所有可能的括號組合
                    tmp_hint = copy(possible_hint)
                    hint_string = self.add_parenthesis(tmp_hint, turple)        

                    #將最終得到的hint_string去除未被取代的'0'字符
                    probed_hint = ''
                    for char in hint_string:
                        if char != '0':
                            probed_hint += char

                    #驗算結果並加入self.hint
                    if self.evaluate(probed_hint) == 24:
                        self.hint = map(''.join, probed_hint)
                        self.probe_hint()
                        return

        self.probe_hint()

    #插入括號
    def add_parenthesis(self, tmp_string, tmp_turple):
        if -1 in tmp_turple:
            return tmp_string
        tmp = 1
        for pointer in tmp_turple:
            if tmp % 2 == 1:
                tmp_string[pointer] = '('
                tmp += 1
            else:
                tmp_string[pointer] = ')'
                tmp += 1
        return tmp_string

    #計算答案
    def evaluate(self, tmp_formula):
        formula = ""
        for tmp3 in range(len(tmp_formula)):
            '''
            if tmp_formula[tmp3] == '/':
                
                counter = 1
                recorder = '/'
               
                while tmp_formula[tmp3 - counter].isalnum():
                    print tmp_formula[tmp3 - counter]
                    recorder += tmp_formula[tmp3 - counter]
                    counter += 1

                formula_list = list(formula)
                formula_list.append('')
                formula_list.append('')
                formula_list.append('')

                formula_list[tmp3 - counter] = '.'
                formula_list[tmp3 - counter + 1] = '0'
                formula = ''.join(formula_list)

                print recorder
                tmp4 = len(recorder)
                while tmp4 >= 0:
                    print formula
                    formula += recorder[tmp4-1]
                    tmp4 -= 1
            '''
            if tmp_formula[tmp3].isdigit():                 #將所有數字轉為浮點數據，以避免除法運算的取整問題
                formula += str(float(tmp_formula[tmp3]))
            elif tmp_formula[tmp3].isalpha():               #將十六進制數重新轉為十進制浮點數據
                if tmp_formula[tmp3] == 'A':    formula += str(10.0);   continue
                if tmp_formula[tmp3] == 'B':    formula += str(11.0);   continue
                if tmp_formula[tmp3] == 'C':    formula += str(12.0);   continue
                if tmp_formula[tmp3] == 'D':    formula += str(13.0);   continue
            else:                                           #運算符和括號直接保留
                formula += tmp_formula[tmp3]

        try:
            return eval(formula)
        except ZeroDivisionError:       #可能存在除數為零的情況
            return 0

def game():
    new_game = Game()
    new_game.print_problem()
    answer = raw_input("Your answer is ")

    if answer == 'hint':
        new_game.print_hint()
    elif new_game.check_answer(answer):
        print "You're right."
    else:
        print "You are wrong."

if __name__ == '__main__':
    game()
