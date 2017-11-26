# -*- coding: utf-8 -*-

import os
import sys

if sys.version_info[0] > 2:
    print("This game runs on python 2 only")

#選擇顯示模式
if len(sys.argv) > 1:
    if sys.argv[1] in ('--console', '-c'):
        from chesslib.gui_console import display
        display(game)
        exit(0)
    elif sys.argv[1] in ('--help', '-h'):
        print '''Usage: game.py [OPTION]\n\n\tPlay a game of 24 points\n\n\tOptions:\n\t -c, --console\tplay in console mode\n\n'''
        exit(0)

try:
    from gamelib.gui_tkinter import Tkinter_Game
    start_game = Tkinter_Game()
except ImportError:
    from gamelib.gui_console import Console_Game
    start_game = Console_Game()
    