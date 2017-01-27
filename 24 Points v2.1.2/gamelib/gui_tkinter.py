# -*- coding: utf-8 -*-

from Tkinter import *
from game import Game
from random import randint
from tkMessageBox import askokcancel, showinfo
#from PIL import Image, ImageTk

class Tkinter_Game():
    def __init__(self):
        self.round = 0                          #遊戲輪次數
        self.problem = [0, 0, 0, 0]             #遊戲題目（十進制整型數組）
        self.problem_string = ''                #遊戲題目（十六進制字符串）

        self.number_order = {1:'', 2:'', 3:'', 4:''}   #十六進制數字的按鍵順序紀錄
        self.number_counter = 0                        #十六進制數字按鍵的紀錄數字

        self.bracket_counter = 0                #括號對的紀錄數字（左+1，右-1）

        self.label_width = 300                  #歡迎界面Label構件的寬度
        self.label_height = 100                 #歡迎界面Label構件的高度

        self.welcome_button_width = 100         #歡迎界面Button構件的寬度
        self.welcome_button_height = 50         #歡迎界面Button構件的高度

        self.poker_width = 700                  #遊戲界面撲克牌顯示模塊的寬度
        self.poker_height = 300                 #遊戲界面撲克牌顯示模塊的高度

        self.state_width = 700                  #遊戲界面狀態欄顯示模塊的寬度
        self.state_height = 50                  #遊戲界面狀態欄顯示模塊的高度

        self.board_width = 700                  #遊戲界面按鍵區顯示模塊的寬度
        self.board_height = 250                 #遊戲界面按鍵區顯示模塊的高度

        self.poker_canvas_width = int((self.poker_width - 1) / 9)   #撲克牌模塊Canvas構件的寬度
        self.poker_canvas_height = int(self.poker_height * 2 / 3)   #樸克牌模塊Canvas構件的高度

        self.state = ''                         #狀態欄模塊的顯示內容（十進制，用於直接顯示）
        self.state_string = ''                  #狀態欄模塊的顯示內容（十六進制，用於刪除操作）
        #self.state_state = StringVar()

        #self.file_name = ['', '' ,'' ,'']      #需要顯示的樸克牌文件名稱
        #self.file_icon = {}                    #需要顯示的樸克牌文件內容

        self.operator_button_width = int((self.board_width - 1) / 12)       #按鍵區模塊的按鍵寬度
        self.operator_button_height = int((self.board_height - 1) / 12)     #按鍵區模塊的按鍵高度

        self.root_window = Tk()                 #定義根窗口
        self.welcome_page(self.root_window)     #顯示歡迎界面

        self.root_window.mainloop()

    #進入遊戲後的歡迎界面
    def welcome_page(self, root):
        root.title("24點 - 24 Games")                        #設置窗口標題
        root.geometry('700x600')                            #設置窗口大小
        #root.bind("<Configure>", self.global_refresh)      #窗口格局修改時調用global_refresh刷新界面
        root.resizable(width=False,height=False)            #禁止改變窗口格局

        #歡迎界面的顯示標籤
        self.welcome_label = Label(root, width=self.label_width, height=self.label_height, text='24點')
        self.welcome_label.place(x=self.label_width / 3 * 2, y=self.label_height*2)

        #歡迎界面的顯示標籤框架（用welcome_label取代其中的label構件）
        self.welcome_frame = LabelFrame(root, width=self.label_width, height=self.label_height, borderwidth=0, relief='flat', labelwidget=self.welcome_label)
        self.welcome_frame.place(x=self.label_width / 3 * 2, y=self.label_height*2)

        #開始遊戲按鈕，響應為start()
        self.start_button = Button(root, text='開始遊戲', command=self.start)
        self.start_button.place(x=self.welcome_button_width*3, y=self.welcome_button_height*8)

        #退出遊戲按鈕，響應為quit()
        self.quit_button = Button(root, text='退出遊戲', command=self.quit)
        self.quit_button.place(x=self.welcome_button_width*3, y=self.welcome_button_height*10)

    #點擊“開始遊戲”／“繼續遊戲”，進入新遊戲
    def start(self):
        self.round += 1             #遊戲輪次數更新
        self.problem_string = ''    #初始化遊戲題目字符串
        self.new_game = Game()      #生成新遊戲
        self.problem = self.new_game.problem

        self.transfer_problem()             #轉化遊戲題目，獲取遊戲題目整型數組
        self.front_play(self.root_window)   #切入遊戲界面

    #點擊“退出遊戲”，退出遊戲
    def quit(self):
        self.root_window.destroy()

    #進入遊戲界面後的顯示邏輯
    def front_play(self, root):
        self.poker_allocation(root)     #樸克牌顯示模塊
        self.state_allocation(root)     #狀態欄顯示模塊
        self.board_allocation(root)     #按鍵區顯示模塊

    #遊戲界面撲克牌顯示模塊（上部）的佈局
    def poker_allocation(self, root):
        #樸克牌顯示模塊的框架
        self.poker_frame = Frame(root, width=self.poker_width, height=self.poker_height, borderwidth=0, background='Green', relief='flat')
        self.poker_frame.grid(row=0, column=0)

        #第一張撲克牌的顯示畫布
        self.poker_canvas_1st = Canvas(self.poker_frame, width=self.poker_canvas_width, height=self.poker_canvas_height, borderwidth=0, relief='raised')
        self.poker_canvas_1st.place(x=self.poker_canvas_width, y=int(self.poker_canvas_height / 6))

        #第二張撲克牌的顯示畫布
        self.poker_canvas_2nd = Canvas(self.poker_frame, width=self.poker_canvas_width, height=self.poker_canvas_height, borderwidth=0, relief='raised')
        self.poker_canvas_2nd.place(x=self.poker_canvas_width*3, y=int(self.poker_canvas_height / 6))

        #第三張撲克牌的顯示畫布
        self.poker_canvas_3rd = Canvas(self.poker_frame, width=self.poker_canvas_width, height=self.poker_canvas_height, borderwidth=0, relief='raised')
        self.poker_canvas_3rd.place(x=self.poker_canvas_width*5, y=int(self.poker_canvas_height / 6))

        #第四張撲克牌的顯示畫布
        self.poker_canvas_4th = Canvas(self.poker_frame, width=self.poker_canvas_width, height=self.poker_canvas_height, borderwidth=0, relief='raised')
        self.poker_canvas_4th.place(x=self.poker_canvas_width*7, y=int(self.poker_canvas_height / 6))
        
        #放置撲克牌與上述畫布中
        self.place_pokers()

        '''
        if not self.round > 1: #由歡迎界面進入遊戲界面時除外
            self.place_pokers()
        '''

    #放置樸克牌於四個Canvas構件中
    def place_pokers(self):
        #print self.problem_string
        self.make_poker(self.poker_canvas_1st, self.problem_string[0], self.poker_canvas_width, int(self.poker_canvas_height / 6))
        self.make_poker(self.poker_canvas_2nd, self.problem_string[1], self.poker_canvas_width*3, int(self.poker_canvas_height / 6))
        self.make_poker(self.poker_canvas_3rd, self.problem_string[2], self.poker_canvas_width*5, int(self.poker_canvas_height / 6))
        self.make_poker(self.poker_canvas_4th, self.problem_string[3], self.poker_canvas_width*7, int(self.poker_canvas_height / 6))

        '''
        self.make_poker()
        self.poker_canvas_1st.create_image(self.poker_canvas_width, int(self.poker_canvas_height / 6), image=self.file_icon[0], tags=self.file_name[0], anchor='c')
        self.poker_canvas_2nd.create_image(self.poker_canvas_width*3, int(self.poker_canvas_height / 6), image=self.file_icon[1], tags=self.file_name[1], anchor='c')
        self.poker_canvas_3rd.create_image(self.poker_canvas_width*5, int(self.poker_canvas_height / 6), image=self.file_icon[2], tags=self.file_name[2], anchor='c')
        self.poker_canvas_4th.create_image(self.poker_canvas_width*7, int(self.poker_canvas_height / 6), image=self.file_icon[3], tags=self.file_name[3], anchor='c')
        '''

    #生成樸克牌及其花色
    def make_poker(self, root_canvas, poker_number, xpoz, ypoz):
        colour = randint(1,4)
        if colour == 1: #Spade
            poker_suit = '♠️'
        elif colour == 2: #Heart
            poker_suit = '♥️'
        elif colour == 3: #Diamond
            poker_suit = '♦️'
        else: #colour == 4 #Club
            poker_suit = '♣️'

        #print colour, poker_suit, ' ', poker_number

        self.draw_poker(root_canvas, poker_suit, poker_number, xpoz, ypoz)

    #繪製樸克牌
    def draw_poker(self, root, suit, number, xpoz, ypoz):
        xpoz = self.poker_canvas_width
        ypoz = self.poker_canvas_height

        #撲克牌對角處的數字
        root.create_text(int(xpoz*0.1), int(ypoz*0.1), text=self.transfer_string(number))
        root.create_text(int(xpoz*0.9), int(ypoz*0.9), text=self.transfer_string(number))

        #根據撲克牌的花色和數字繪製各牌面
        if number == '1':
            xp = [int(xpoz*0.55)]
            yp = [int(ypoz*0.5)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        elif number == '2':
            xp = [int(xpoz*0.55), int(xpoz*0.55)]
            yp = [int(ypoz*0.2), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        elif number == '3':
            xp = [int(xpoz*0.55), int(xpoz*0.55), int(xpoz*0.55)]
            yp = [int(ypoz*0.2), int(ypoz*0.5), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        elif number == '4':
            xp = [int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.8), int(xpoz*0.8)]
            yp = [int(ypoz*0.2), int(ypoz*0.8), int(ypoz*0.2), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        elif number == '5':
            xp = [int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.55), int(xpoz*0.8), int(xpoz*0.8)]
            yp = [int(ypoz*0.2), int(ypoz*0.8), int(ypoz*0.5), int(ypoz*0.2), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        elif number == '6':
            xp = [int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8)]
            yp = [int(ypoz*0.2), int(ypoz*0.5), int(ypoz*0.8), int(ypoz*0.2), int(ypoz*0.5), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        elif number == '7':
            xp = [int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.55), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8)]
            yp = [int(ypoz*0.2), int(ypoz*0.5), int(ypoz*0.8), int(ypoz*0.35), int(ypoz*0.2), int(ypoz*0.5), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        elif number == '8':
            xp = [int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8)]
            yp = [int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8), int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        elif number == '9':
            xp = [int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.55), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8)]
            yp = [int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8), int(ypoz*0.5), int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        elif number == 'A':     #10
            xp = [int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.55), int(xpoz*0.55), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8)]
            yp = [int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8), int(ypoz*0.3), int(ypoz*0.7), int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        elif number == 'B':     #11
            xp = [int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.55), int(xpoz*0.55), int(xpoz*0.55), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8)]
            yp = [int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8), int(ypoz*0.3), int(ypoz*0.5), int(ypoz*0.7), int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        elif number == 'C':     #12
            xp = [int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.45), int(xpoz*0.45), int(xpoz*0.65), int(xpoz*0.65), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8)]
            yp = [int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8), int(ypoz*0.3), int(ypoz*0.7), int(ypoz*0.3), int(ypoz*0.7), int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)
        else: #number == 'D'    #13
            xp = [int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.3), int(xpoz*0.45), int(xpoz*0.45), int(xpoz*0.55), int(xpoz*0.65), int(xpoz*0.65), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8), int(xpoz*0.8)]
            yp = [int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8), int(ypoz*0.3), int(ypoz*0.7), int(ypoz*0.5), int(ypoz*0.3), int(ypoz*0.7), int(ypoz*0.2), int(ypoz*0.4), int(ypoz*0.6), int(ypoz*0.8)]
            for tmp in range(len(xp)):
                root.create_text(xp[tmp], yp[tmp], text=suit)

        '''
        for tmp in range(4):
            colour = randint(1,4)
            if colour == 1:
                poker_suit = 'Spade'
            elif colour == 2:
                poker_suit = 'Heart'
            elif colour == 3:
                poker_suit = 'Diamond'
            else: #colour == 4
                poker_suit = 'Club'

            poker_number = str(self.problem[tmp])
            self.file_name[tmp] = 'cards/image_%s_%s.png' % (poker_suit, poker_number)
            self.file_icon[tmp] = ImageTk.PhotoImage(file=self.file_name[tmp], width=self.poker_canvas_width, height=self.poker_canvas_height)
        '''

    #遊戲界面狀態欄顯示模塊（中部）的佈局
    def state_allocation(self, root):
        #狀態欄的顯示標籤
        self.state_label = Label(root, width=self.state_width, height=self.state_height, background='Grey', relief='sunken', anchor='center', text=self.state)
        self.state_label.place(x=0, y=self.poker_height)

        #狀態欄的框架（用state_label取代其中的Label構件）
        self.state_frame = LabelFrame(root, width=self.state_width, height=self.state_height, borderwidth=0, relief='flat', labelwidget=self.state_label)
        self.state_frame.grid(row=1, column=0)

        #print 'state_allocation() called'

    #遊戲界面按鍵區顯示模塊（下部）的佈局
    def board_allocation(self, root):
        #按鍵區的框架
        self.board_frame = Frame(root, width=self.board_width, height=self.board_height, background='White')
        self.board_frame.grid(row=2, column=0)

        #board_canvas = Canvas(root, width=self.board_canvas_width, height=self.board_canvas_height, borderwidth=0, background='Blue', relief='flat')
        #board_canvas.place(x=int((self.board_canvas_width-1)/2), y=(self.state_height + self.poker_height))

        #加號（➕）
        self.board_button_adder = Button(root, text='+', command=self.operator_adder)
        self.board_button_adder.place(x=self.operator_button_width*1, y=(self.poker_height + self.state_height + self.operator_button_height*1))

        #減號（➖）
        self.board_button_subtracter = Button(root, text='-', command=self.operator_subtracter)
        self.board_button_subtracter.place(x=self.operator_button_width*1, y=(self.poker_height + self.state_height + self.operator_button_height*3))

        #乘號（✖️）
        self.board_button_multiplier = Button(root, text='*', command=self.operator_multiplier)
        self.board_button_multiplier.place(x=self.operator_button_width*1, y=(self.poker_height + self.state_height + self.operator_button_height*5))
        
        #除號（➗）
        self.board_button_devider = Button(root, text='/', command=self.operator_devider)
        self.board_button_devider.place(x=self.operator_button_width*1, y=(self.poker_height + self.state_height + self.operator_button_height*7))
        
        #左括號（(）
        self.board_button_bracketLeft = Button(root, text='(', command=self.operator_bracketLeft)
        self.board_button_bracketLeft.place(x=self.operator_button_width*1, y=(self.poker_height + self.state_height + self.operator_button_height*9))
        
        #右括號（)）
        self.board_button_bracketRight = Button(root, text=')', command=self.operator_bracketRight)
        self.board_button_bracketRight.place(x=self.operator_button_width*1, y=(self.poker_height + self.state_height + self.operator_button_height*11))

        #數字按鍵
        self.button_pokers(root)

        #刪除
        self.board_button_delete = Button(root, text='刪除', command=self.delete)
        self.board_button_delete.place(x=self.operator_button_width*10, y=(self.poker_height +self.state_height + self.operator_button_height*1))

        #清空
        self.board_button_clear = Button(root, text='清空', command=self.clear)
        self.board_button_clear.place(x=self.operator_button_width*10, y=(self.poker_height + self.state_height + self.operator_button_height*4))

        #無解
        self.board_button_unsolvable = Button(root, text='無解', command=self.unsolvable)
        self.board_button_unsolvable.place(x=self.operator_button_width*10, y=(self.poker_height + self.state_height + self.operator_button_height*7))

        #確定（或提交）
        self.board_button_submit = Button(root, text='確定', command=self.submit)
        self.board_button_submit.place(x=self.operator_button_width*10, y=(self.poker_height + self.state_height + self.operator_button_height*10))

        #初始時禁用運算符和右括號
        if self.number_counter == 0:
            self.operator_button_disable()
            self.bracketRight_button_disable()

    #遊戲界面按鍵區顯示模塊中樸克牌（數字）的佈局
    def button_pokers(self, root):
        #第一個數字
        self.board_button_poker1st = Button(root, text=str(self.problem[0]), command=self.poker_1st)
        self.board_button_poker1st.place(x=self.operator_button_width*4, y=(self.poker_height + self.state_height + self.operator_button_height*3))

        #第二個數字
        self.board_button_poker2nd = Button(root, text=str(self.problem[1]), command=self.poker_2nd)
        self.board_button_poker2nd.place(x=self.operator_button_width*4, y=(self.poker_height + self.state_height + self.operator_button_height*9))

        #第三個數字
        self.board_button_poker3rd = Button(root, text=str(self.problem[2]), command=self.poker_3rd)
        self.board_button_poker3rd.place(x=self.operator_button_width*7, y=(self.poker_height + self.state_height + self.operator_button_height*3))

        #第四個數字
        self.board_button_poker4th = Button(root, text=str(self.problem[3]), command=self.poker_4th)
        self.board_button_poker4th.place(x=self.operator_button_width*7, y=(self.poker_height + self.state_height + self.operator_button_height*9))

    #加號（➕）按鍵
    def operator_adder(self):
        self.state += '+'
        self.state_string += '+'
        #print self.state
        self.state_refresh(self.root_window)

        '''
        self.operator_button_disable()
        self.bracketLeft_button_active()
        self.bracketRight_button_disable()
        self.poker_button_active()
        '''

    #減號（➖）按鍵
    def operator_subtracter(self):
        self.state += '-'
        self.state_string += '-'
        #print self.state
        self.state_refresh(self.root_window)

        '''
        self.operator_button_disable()
        self.bracketLeft_button_active()
        self.bracketRight_button_disable()
        self.poker_button_active()
        '''

    #乘號（✖️）按鍵
    def operator_multiplier(self):
        self.state += '*'
        self.state_string += '*'
        #print self.state
        self.state_refresh(self.root_window)

        '''
        self.operator_button_disable()
        self.bracketLeft_button_active()
        self.bracketRight_button_disable()
        self.poker_button_active()
        '''

    #除號（➗）按鍵
    def operator_devider(self):
        self.state += '/'
        self.state_string += '/'
        #print self.state
        self.state_refresh(self.root_window)

        '''
        self.operator_button_disable()
        self.bracketLeft_button_active()
        self.bracketRight_button_disable()
        self.poker_button_active()
        '''

    #左括號按鍵（(）按鍵
    def operator_bracketLeft(self):
        self.state += '('
        self.state_string += '('
        #print self.state
        self.bracket_counter += 1 
        self.state_refresh(self.root_window)

        '''
        self.operator_button_disable()
        #self.bracketLeft_button_active()
        self.bracketRight_button_disable()
        self.poker_button_active()
        '''  

    #右括號按鍵（)）按鍵
    def operator_bracketRight(self):
        self.state += ')'
        self.state_string += ')'
        #print self.state
        self.bracket_counter -= 1
        self.state_refresh(self.root_window)

        '''
        self.operator_button_active()
        self.bracketLeft_button_disable()
        self.bracketRight_button_disable()
        self.poker_button_disable()
        '''

    #第一張樸克牌的數字按鍵
    def poker_1st(self):
        self.state += str(self.problem[0])
        self.state_string += self.problem_string[0]
        #print self.state
        self.number_counter += 1                        #數字按鍵記錄自增
        self.number_order[self.number_counter] = '1'    #數字按鍵紀錄第number_counter位為第一個數字
        self.state_refresh(self.root_window)
        #self.board_button_poker1st.config(state='disabled')

        '''
        self.operator_button_active()
        self.bracketLeft_button_disable()
        self.bracketRight_button_active()
        self.poker_button_disable()
        '''

    #第二張樸克牌的數字按鍵
    def poker_2nd(self):
        self.state += str(self.problem[1])
        self.state_string += self.problem_string[1]
        #print self.state
        self.number_counter += 1                        #數字按鍵記錄自增
        self.number_order[self.number_counter] = '2'    #數字按鍵紀錄第number_counter位為第二個數字
        self.state_refresh(self.root_window)
        #self.board_button_poker1st.config(state='disabled')

        '''
        self.operator_button_active()
        self.bracketLeft_button_disable()
        self.bracketRight_button_active()
        self.poker_button_disable()
        '''

    #第三張樸克牌的數字按鍵
    def poker_3rd(self):
        self.state += str(self.problem[2])
        self.state_string += self.problem_string[2]
        #print self.state
        self.number_counter += 1                        #數字按鍵記錄自增
        self.number_order[self.number_counter] = '3'    #數字按鍵紀錄第number_counter位為第三個數字
        self.state_refresh(self.root_window)
        #self.board_button_poker1st.config(state='disabled')

        '''
        self.operator_button_active()
        self.bracketLeft_button_disable()
        self.bracketRight_button_active()
        self.poker_button_disable()
        '''

    #第四張樸克牌的數字按鍵
    def poker_4th(self):
        self.state += str(self.problem[3])
        self.state_string += self.problem_string[3]
        #print self.state
        self.number_counter += 1                        #數字按鍵記錄自增
        self.number_order[self.number_counter] = '4'    #數字按鍵紀錄第number_counter位為第四個數字
        self.state_refresh(self.root_window)
        #self.board_button_poker1st.config(state='disabled')

        '''
        self.operator_button_active()
        self.bracketLeft_button_disable()
        self.bracketRight_button_active()
        self.poker_button_disable()
        '''

    #刪除（退格）按鍵
    def delete(self):
        self.delete_button_counter()    #恢復紀錄數值，state_string退格一位
        #print self.state
        #print self.state_string
        self.state_refresh(self.root_window)
        #print self.state
        #print 'delete() done'

    #刪除操作時所有按鍵的紀錄恢復，state_string退格一位
    def delete_button_counter(self):
        if self.state_string == '':
            #self.clear()
            return

        if self.state_string[-1].isalnum():     #退位為數字，數字按鍵記錄退位一格
            self.number_order[self.number_counter] = ''
            self.number_counter -= 1
        elif self.state_string[-1] == '(':      #退位為左括號，括號記錄自減
            self.bracket_counter -= 1
        elif self.state_string[-1] == ')':      #退位為右括號，括號記錄自增
            self.bracket_counter += 1
        else:                                   #退位為運算符，無操作
            pass

        self.state_string = self.state_string[:-1]  #state_string退格一位
        self.transfer_state()                       #將state_string轉化為state

    #清空按鍵
    def clear(self):
        self.state = ''         #清空state的值
        self.state_string = ''  #清空state_string的值

        self.number_counter = 0     #恢復數字按鍵記錄
        self.bracket_counter = 0    #恢復括號按鍵記錄

        #逐一清空數字按鍵記錄
        for tmp in range(4):
            self.number_order[self.number_counter] = ''

        #print self.state
        self.state_refresh(self.root_window)
        self.clear_button_state()

    #清空操作時按鍵的狀態恢復
    def clear_button_state(self):
        self.operator_button_disable()      #恢復初始狀態後，禁用運算符
        self.bracketLeft_button_active()    #恢復初始狀態後，啟用左括號
        self.bracketRight_button_disable()  #恢復初始狀態後，禁用右括號

        #恢復初始狀態後，啟用所有數字按鍵
        self.board_button_poker1st.config(state='normal')
        self.board_button_poker2nd.config(state='normal')
        self.board_button_poker3rd.config(state='normal')
        self.board_button_poker4th.config(state='normal')

    #無解按鍵
    def unsolvable(self):
        #'-1'表示無解，檢查答案是否正確
        if self.new_game.check_answer('-1'):
            if askokcancel('回答正確！', '是否繼續遊戲？'):
                self.start()    #進入新一輪遊戲
            else:
                self.quit()     #退出遊戲
        else:
            #self.new_game.make_hint()
            hint = self.new_game.hint
            hint_message = '一可能解為 %s=24' % hint
            showinfo(title='回答錯誤！', message=hint_message)   #回答錯誤時，顯示一正確解
            if askokcancel('回答錯誤！', '是否繼續遊戲？'):
                #self.clear()
                self.start()    #進入新一輪遊戲
            else:
                self.quit()     #退出遊戲

    #確認（提交）按鍵
    def submit(self):
        #未使用所有數字按鍵時，禁止提交
        if self.number_counter != 4:
            showinfo(title='尚未完成！', message='您尚未完成當前題目，請繼續作答。')
            return

        #完成作答後，檢查答案是否正確
        if self.new_game.check_answer(self.state):
            if askokcancel('回答正確！', '是否繼續遊戲？'):
                #self.clear()
                self.start()    #進入新一輪遊戲
            else:
                self.quit()     #退出遊戲
        else:
            self.new_game.make_hint()
            hint = self.new_game.hint
            if hint == '-1':    #無解
                hint_message = '本題無解。'
            else:               #有解，顯示一可能解
                hint_message = '一可能解為 %s=24' % hint
            showinfo(title='回答錯誤！', message=hint_message)
            if askokcancel('回答錯誤！', '是否繼續遊戲？'):
                #self.clear()
                self.start()    #進入新一輪遊戲
            else:
                self.quit()     #退出遊戲

    #將十六進制的字符串顯示轉化為十進制數字顯示
    def transfer_string(self, number):
        if number == 'A':
            return 10
        elif number == 'B':
            return 11
        elif number == 'C':
            return 12
        elif number == 'D':
            return 13
        else: #number < 10
            return number

    #將十進制整形數組題目串轉化為十六進制字符串存儲
    def transfer_problem(self):
        for num in self.problem:
            if num < 10:
                self.problem_string += str(num)
            elif num == 10:
                self.problem_string += 'A'
            elif num == 11:
                self.problem_string += 'B'
            elif num == 12:
                self.problem_string += 'C'
            else: #num == 13
                self.problem_string += 'D'

    #將十六進制字符串狀態串轉化為十進制字符串顯示
    def transfer_state(self):
        self.state = ''
        for char in self.state_string:
            if char == 'A':
                self.state += '10'
            elif char == 'B':
                self.state += '11'                
            elif char == 'C':
                self.state += '12'
            elif char == 'D':
                self.state += '13'                
            else:   #int(char) < 10 and not char.isalnum()
                self.state += char

    #在界面格局被修改時刷新歡迎界面
    def welcome_refresh(self, event={}, xsize=700, ysize=600):
        if event:
            xsize = int((event.width-1) / 7)
            ysize = int((event.height-1) / 12)

        self.label_width = xsize * 3
        self.label_height = ysize * 2

        self.welcome_button_width = xsize * 1
        self.welcome_button_height = ysize * 1

        self.welcome_page()

    #在界面格局被修改時刷新遊戲界面
    def global_refresh(self, event={}, xsize=700, ysize=600):
        if event:
            xsize = int((event.width-1) / 7)
            ysize = int((event.height-1) / 12)

        self.poker_width = xsize * 7
        self.poker_height = ysize * 6

        self.state_width = xsize * 7
        self.state_height = ysize * 1

        self.board_width = xsize * 7
        self.board_height = ysize * 5

        self.poker_canvas_width = int((self.poker_width - 1) / 9)
        self.poker_canvas_height = int(self.poker_height * 2 / 3)

        #self.state_text = StringVar()

        self.operator_button_width = int((self.board_width - 1) / 12)
        self.operator_button_height = int((self.board_height - 1) / 12)

        if not self.round > 1: #由歡迎界面進入遊戲界面時除外
            self.poker_frame.destroy()
            self.state_frame.destroy()
            self.board_frame.destroy()

        self.front_play(self.root_window)

    #在狀態欄顯示內容被修改時刷新狀態欄
    def state_refresh(self, root):
        if self.number_counter == 4:    #所有數字鍵均已使用後強制提繳
            self.compulsive_submit()
            #print 'compulsive_submit() called'
        elif self.state_string != '':   #刷新狀態時，更新按鍵狀態
            self.update_button_state()
            #print 'button_state updated'
        else:
            pass

        self.state_label.config(text=self.state)
        #print self.state

    #當所有數字鍵均已使用後，自動補全右括號並強制提交（或刪除和清空）
    def compulsive_submit(self):
        self.operator_button_disable()      #強制提繳時，禁用運算符
        self.bracketLeft_button_disable()   #強制提繳時，僅用左括號
        self.bracketRight_button_disable()  #強制提繳時，禁用右括號
        self.poker_button_disable()         #強制提繳時，禁用數字鍵

        while self.bracket_counter != 0:    #自動在串末補全右括號
            self.state += ')'
            self.state_string += ')'
            self.bracket_counter -= 1

    #按鍵操作後所有按鍵的狀態調整
    def update_button_state(self):
        if self.state_string[-1].isalnum():     #按下數字鍵時
            self.operator_button_active()           #啟用運算符
            self.bracketLeft_button_disable()       #禁用左括號
            self.bracketRight_button_active()       #啟用右括號
            self.poker_button_disable()             #禁用數字鍵
        elif self.state_string[-1] == '(':      #按下左括號時
            self.operator_button_disable()          #禁用運算符
            #self.bracketLeft_button_active()       #啟用左括號
            self.bracketRight_button_disable()      #禁用右括號
            self.poker_button_active()              #啟用數字鍵
        elif self.state_string[-1] == ')':      #按下右括號時
            self.operator_button_active()           #啟用運算符
            self.bracketLeft_button_disable()       #禁用左括號
            self.bracketRight_button_disable()      #禁用右括號
            self.poker_button_disable()             #禁用數字鍵
        else:                                   #按下運算符時
            self.operator_button_disable()          #禁用運算符
            self.bracketLeft_button_active()        #啟用左括號
            self.bracketRight_button_disable()      #禁用右括號
            self.poker_button_active()              #啟用數字鍵

    #按下數字鍵或右括號後，禁用左括號
    def bracketLeft_button_disable(self):
        self.board_button_bracketLeft.config(state='disabled')

    #按下運算符鍵後，恢復左括號（第三個運算符處除外）
    def bracketLeft_button_active(self):
        if self.number_counter < 3:     #第三個運算符之後（即第四個數字之前）不再啟用
            self.board_button_bracketLeft.config(state='normal')

    #按下運算符後，禁用右括號
    def bracketRight_button_disable(self):
        self.board_button_bracketRight.config(state='disabled')

    #按下數字鍵及左括號後，恢復右括號（第一個數字處除外）
    def bracketRight_button_active(self):       #無左括號使用，或第二個數字之後，或前兩位非左括號的情況下啟用
        if self.bracket_counter > 0 and self.number_counter > 1 and self.state_string[-2] != '(':
            self.board_button_bracketRight.config(state='normal')

    #按下運算符後，禁用所有運算符
    def operator_button_disable(self):
        self.board_button_adder.config(state='disabled')
        self.board_button_subtracter.config(state='disabled')
        self.board_button_multiplier.config(state='disabled')
        self.board_button_devider.config(state='disabled')
        #print 'operator_button disabled'

    #按下數字鍵（或退格刪除運算符）後，恢復所有運算符
    def operator_button_active(self):
        self.board_button_adder.config(state='normal')
        self.board_button_subtracter.config(state='normal')
        self.board_button_multiplier.config(state='normal')
        self.board_button_devider.config(state='normal')

    #按下樸克牌數字鍵後，禁用所有數字鍵
    def poker_button_disable(self):
        self.board_button_poker1st.config(state='disabled')
        self.board_button_poker2nd.config(state='disabled')
        self.board_button_poker3rd.config(state='disabled')
        self.board_button_poker4th.config(state='disabled')

    #按下運算符（或退格刪除數字）後，恢復未使用的數字鍵
    def poker_button_active(self):
        self.board_button_poker1st.config(state='normal')
        self.board_button_poker2nd.config(state='normal')
        self.board_button_poker3rd.config(state='normal')
        self.board_button_poker4th.config(state='normal')

        #禁用使用過的數字鍵
        for ctr in range(1, self.number_counter+1):
            if self.number_order[ctr] == '1':
                self.board_button_poker1st.config(state='disabled')
            elif self.number_order[ctr] == '2':
                self.board_button_poker2nd.config(state='disabled')
            elif self.number_order[ctr] == '3':
                self.board_button_poker3rd.config(state='disabled')
            elif self.number_order[ctr] == '4':
                self.board_button_poker4th.config(state='disabled')
            else: #self.number_order[tmp] == ''
                continue

def tkinter_game():
    new_game = Tkinter_Game()

if __name__ == '__main__':
    tkinter_game()
