# -*- coding: utf-8 -*-

from game import Game

class Console_Game:
    def __init__(self):
        self.state = 1      #紀錄遊戲狀態（1表示進行，0表示終止）
        self.round = 1    #紀錄遊戲輪數

        #輸出介紹信息
        print "\n\
歡迎您進入24點遊戲。\n\
遊戲過程中，請直接根據提示信息輸入答案；\n\
如需瞭解遊戲規則，請輸入 -a\n\
如需獲取答案提示，請輸入 -h\n\
退出遊戲，請輸入 -q\n\
        "

        #進入遊戲
        while self.state:
            self.game_module()
        print "已退出遊戲。"

    #遊戲模塊
    def game_module(self):
        print "第%s輪遊戲：" %str(self.round)
        new_game = Game()
        new_game.print_problem()

        self.round += 1

        input_string = raw_input("請輸入您的答案：\n")
        while 1:
            #請求瞭解遊戲規則
            if input_string == '-a':
                print "\n\
根據給出的四個數字，通過加、減、乘、除四則運算，使得最終結果是24。\n\
例如，給出 6, 12, 7, 12 四個數字，則注意到 12-(6-7)*12=24 ，\n\
從而得出結果，並輸入 12-(6-7)*12 。\n\
特別地，如答案為無解，請輸入 -1 。\
                "
                input_string = raw_input("請輸入您的答案：\n")
            #請求輸出遊戲提示
            elif input_string == '-h':
                new_game.print_hint()
                break
            #請求退出當前遊戲
            elif input_string == '-q':
                self.state = 0
                break
            #判斷輸入是否有效，如有效則判斷結果是否正確
            elif new_game.check_answer(input_string):
                print "回答正確。\n是否進入下一輪？"
                tmp_input = raw_input("是，請輸入 -y\n否，請輸入 -n\n")
                while 1:
                    #繼續下一輪遊戲
                    if tmp_input == '-y':
                        self.game_module()
                        break
                    #退出遊戲
                    elif tmp_input == '-n':
                        self.state = 0
                        break
                    #其他情況
                    else:
                        tmp_input = raw_input("錯誤指令，請重新輸入：\n")
                break
            #其他情況
            else:
                input_string = raw_input("錯誤指令，請重新輸入您的答案：\n")

def console_game():
    new_game = Console_Game()

if __name__ == '__main__':
    console_game()
