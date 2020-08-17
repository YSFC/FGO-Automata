from core.Automata import Automata
import logging
import time
logging.basicConfig(filename='automata.log',filemode='w',level=logging.INFO,format='%(asctime)s %(levelname)s %(message)s',datefmt='%y/%m/%d %I:%M:%S %p') 
bb = Automata("assets/Ember4.png", "assets/wucan.png", (0, 0))
bb.set_apples(9, "assets/silver.png")

count = 0
while count < 27:
    bb.quick_start()
    time.sleep(20)
    # BATTLE 1
    bb.select_servant_skill(2, mode = 1)
    time.sleep(1.7)
    bb.select_servant_skill(4)
    time.sleep(1.7)
    bb.select_servant_skill(5)
    time.sleep(1.7)
    bb.select_servant_skill(7)
    time.sleep(1.7)
    bb.select_servant_skill(9)
    time.sleep(1.7)
    #bb.select_servant_skill(8)
    bb.select_master_skill(2, 3)
    bb.select_cards([8])
    time.sleep(21)
    # BATTLE 2
    bb.select_servant_skill(3)
    time.sleep(1.7)
    bb.select_cards([6])
    time.sleep(21)
    # BATTLE 3
    bb.select_cards([7])
    time.sleep(19)
    
    # FINISH
    bb.finish_battle()
    time.sleep(5)

