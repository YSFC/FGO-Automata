from core.Automata import Automata
import logging
import time
import uiautomator2 as u2
import os

#logging.basicConfig(filename='automata.log',filemode='w',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',datefmt='%y/%m/%d %I:%M:%S %p') 


bb = Automata("assets/Ember4.png", "assets/wucan.png", (0, 0))
bb.set_apples(10, "assets/gold.png")

count = 0
while count < 27:
    bb.quick_start()
    time.sleep(10)
    # BATTLE 1
    bb.select_servant_skill(2, mode = 1)
    bb.select_servant_skill(4)
    bb.select_servant_skill(5)
    bb.select_servant_skill(9)
    bb.select_cards([8])
    time.sleep(15)

    # BATTLE 2
    bb.select_servant_skill(3)
    bb.select_cards([6])
    time.sleep(18)

    # BATTLE 3
    bb.select_cards([7])
    time.sleep(10)
    # FINISH
    bb.finish_battle()
    time.sleep(5)

