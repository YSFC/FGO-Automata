import time
import random
from core import util, crds
from core.Dynamica import Dynamica
import uiautomator2 as u2
import os


class Automata():
    def __init__(self, ckp: str, spt: str, sft=(0, 0), apl: (int, str) = (0, ""), u2ConnectUrl = ""):
        """
        Parameters
        ----------
            ckp: str
        Path to the checkpoint image

            spt: str
        Path to the support image

            sft: (int, int), optional
        Coordinate shifts in (x, y). When there are blues straps at the edges. (Default: (0, 0))

            apl: (int, str), optional
        Number of the apples willl be used and the Path to the image of the apple. (Default: (0, ""))

        Examples
        --------
        Here are examples::

            shiki = Automata("assets/checkpoint.png", "assets/qp.png")
            bb = Automata("assets/checkpoint.png", "assets/qp.png", sft=(248, 0), apl=(1, "assets/silver.png"))
        """
        if u2ConnectUrl == "":
            urls = self.connect()
            if len(urls) == 0:
                raise Exception("模拟器没启动？")
            u2ConnectUrl = urls[0]
        self.device = u2.connect(u2ConnectUrl)
        self.shifts = sft
        self.checkpoint = ckp
        self.support = spt
        self.counts = apl[0]  # apple counts
        self.apple = apl[1]
        self.imgDict = {}

    def u2screenshot(self):
        screen_shot = self.device.screenshot(format="opencv")
        return screen_shot
    
    # battle related
    def select_cards(self, cards: [int]):
        """ Select Order Cards
        Parameters
        ----------
            cards: list
        A list of numbers of the card id (1~5 -> normal cards, 6,7,8 -> NP cards). 
        It should have maximum 3 number.   

        Examples
        --------
        Here are examples::

            select_cards([6]) # left the rest 2 randomly choosen
            select_cards([6,2]) # left the last 1 randomly choosen
            select_cards([1,2,3])
        """
        while not util.standby(self.u2screenshot(), crds.IMAGE["attack"], mode = 1, imgDict = self.imgDict):
            time.sleep(1)
        # tap ATTACK
        time.sleep(0.5)
        self.tap(crds.ATTACK, 10, 10)
        time.sleep(1.5)
        while len(cards) < 3:
            x = random.randrange(1, 6)
            if x in cards:
                continue
            cards.append(x)
        # tap CARDS
        for card in cards:
            self.tap(crds.CARDS[card-1], 40, 90)
            time.sleep(0.2)
        print("[INFO] Selected cards: ", cards)

    # new: self, skill, tar
    # combine select servant
    def select_servant_skill(self, skill: int, tar: int = 0, mode = 0):
        """ Select Servant Skill
        Parameters
        ----------
            skill: int
        The id of the skill. 1~9 counted from left.

            tar: int, optional
        The id of target servant. 1~3 counted from left.
        (If the skill has target servant)

        Examples
        --------
        Here are examples::

            select_servant_skill(1) # skill w/o target servants
            select_servant_skill(3, 2) # skill w/ target servants
        """        
        while not util.standby(self.u2screenshot(), crds.IMAGE["attack"], mode = 1, imgDict = self.imgDict):
            time.sleep(1)
        if mode == 1:
            print("最初技能等待")
            time.sleep(2)
        #time.sleep(0.2)
        self.tap(crds.SERVANT_SKILLS[skill-1], 10, 10)
        #self.tap(crds.SERVANT_SKILLS[skill-1], 10, 10)#来两次，老是莫名其妙没点上
        time.sleep(0.2)
        if tar != 0:
            self.select_servant(tar)

    def select_servant_skill2(self, servant: int, skill: int, target: int = 0):
        """ Select Servant Skill 2
        Parameters
        ----------
            servant: int
        The id of the servant. 1~3 counted from left.

            skill: int
        The id of the skill of the selected servant. 1~3 counted from left.

            target: int
        The id of target servant. 1~3 counted from left.
        (If the skill has target servant)
        """
        self.select_servant_skill((servant-1)*3+skill, target)

    def select_servant_skillM(self, skills: [(int, int)]):
        """ Select Multiple Servant Skill 
        Parameters
        ----------
            skills: list
        A list of a tuple of id of the skill and target servant.

        Examples
        --------
        Here are examples::

            select_servant_skillM([(1,0)]) # skill 1 w/o target servants
            select_servant_skill([(2,0), (4,1)]) # skill 2 w/o target and skill 4 w/ target servant 1
        """
        for skill in skills:
            self.select_servant_skill(skill[0], skill[1])

    def select_servant(self, servant: int):
        """ Select Servant
        Parameters
        ----------
            servant: int
        The id of the servant. 1~3 counted from left.
        """
        while not util.standby(self.u2screenshot(), crds.IMAGE["select"]):
            time.sleep(0.2)
        self.tap(crds.TARGETS[servant-1], 100, 100)

    def change_servant(self, org: int, tar: int):
        """ Change Servant
        Parameters
        ----------
            org: int
        Servant id on the left side(1~3) 

            tar: int
        Servant id on the right side(1~3)
        """
        while not util.standby(self.u2screenshot(), crds.IMAGE["order_change"]):
            time.sleep(0.2)
        self.tap(crds.SERVANTS[org-1], 90, 90)
        time.sleep(0.1)
        self.tap(crds.SERVANTS[tar+2], 90, 90)
        time.sleep(0.1)
        self.tap((950, 950), 100)  # confirm btn

    def toggle_master_skill(self):
        while not util.standby(self.u2screenshot(), crds.IMAGE["attack"]):
            time.sleep(0.2)
        self.tap(crds.MASTER)

    def select_master_skill(self, skill: int, org: int = 0, tar: int = 0):
        """ Servant Master Skill
        Parameters
        ----------
            skill: int
        Skill id 1~3, counted from left.

            org: int, optional
        Target servant id 1~3, counted from left.(When only 2 args)
        When implemented the 3rd arg, it is the id of the servants on the left side(1~3)

            tar: int, optional
        Servant id on the right side(1~3)

        Examples
        --------
        Here are examples::

            select_master_skill(1) # skill w/o target servants
            select_master_skill(2, 2) # skill w/ target servants
            select_master_skill(3, 1, 1) # Order Change

        """
        self.toggle_master_skill()
        self.tap(crds.MASTER_SKILLS[skill-1], 8, 8)
        if org != 0 and tar == 0:
            self.select_servant(org)
        elif org != 0:
            self.change_servant(org, tar)

    # pre-battle related
    def select_checkpoint(self, ckp: str = None):
        """ Select Checkpoint
        Parameters
        ----------
            ckp: str, optional
        Override the initially set checkpoint.

        Raises
        ------
            Exception("Out of AP!")
        When out of AP.
        """
        self.wait(self.checkpoint)
        if ckp is None:
            ckp = self.checkpoint
        coordinates = util.get_crd(self.u2screenshot(), ckp)
        self.tap(coordinates[0], 100)
        time.sleep(0.2)
        # check whether out of AP
        # Not tested
        # in progress
        time.sleep(1)
        if util.standby(self.u2screenshot(), crds.IMAGE["no_ap"], imgDict = self.imgDict):
            if self.counts > 0:
                self.eat_apple()
            else:
                raise Exception("Out of AP!")
        print("[INFO] Checkpoint selected.")

    def select_support(self, spt: str = None):
        """ Select Support
        Parameters
        ----------
            spt: str, optional
        Override the initially set support.
        """
        time.sleep(0.3)
        if spt is None:
            spt = self.support
        x = util.get_crd(self.u2screenshot(), spt)
        if len(x) == 0:
            self.tap((860, 430), 300, 100)
        else:
            self.tap(x[0])

    # advance support
    def advance_support(self, spt: str = None, tms: int = 3):
        """ Advance Support Selection
        Parameters
        ----------
            spt: str, optional
        Override the initially set support.

            tms: int, optional
        Max support list update times. (Default: 3)

        Raises
        ------
            Exception("Desired support not found!")
        Raises when reached maxium update times.
        """
        time.sleep(1.5)
        if spt is None:
            spt = self.support
        x = util.get_crd(self.u2screenshot(), spt, imgDict = self.imgDict)
        counter = False
        times = tms
        while len(x) == 0:
            if not counter:
                self.swipe((1000, 800), (1000, 300))
                counter = True
            else:
                update = self.update_support()
                if update:
                    counter = False
                    times -= 1
                    if times < 0:
                        raise Exception("Desired support not found!")
                else:
                    time.sleep(3)
            time.sleep(0.5)
            x = util.get_crd(self.u2screenshot(), spt)
        self.tap((x[0][0], x[0][1]))
        print("[INFO] Support selected.")

    def update_support(self) -> bool:
        """ Update Support List
        Returns
        -------
            bool
        `True` if successfully updated, otherwise is `False`.
        """
        btn = util.get_crd(self.u2screenshot(),
                           crds.IMAGE["update_support"])
        if len(btn) == 0:
            self.tap((1272,877), 1, 1)
        else:
            self.tap(btn[0], 1, 1)
        time.sleep(0.1)
        if util.standby(self.u2screenshot(), crds.IMAGE["confirm_update"]):
            self.tap((1240, 840), 10, 5)
            return True
        else:
            self.tap((950, 840))
            return False

    def get_current_battle(self) -> int:
        """ Get current Battle ID
        Returns
        -------
            int
        a number of current battle
        """
        return util.get_battle_id(self.u2screenshot())

    def reached_battle(self, btl: int) -> bool:
        """ Reached Battle
        Check whether reached a certain battle

        Parameters
        ----------
            btl: int
        The battle id.

        Returns
        -------
            bool
        `True` if reached the expected battle, otherwise `False`

        """
        cur = self.get_current_battle()
        return True if btl == cur else False

    # Dynamic battle related
    def dynamica_select(self):
        # tap Attack to show cards
        self.tap(crds.ATTACK, 100, 100)
        time.sleep(1)
        # init the class
        dym = Dynamica(sft=self.shifts)
        util.get_sh(self.shifts)
        util.split_cards("tmp.png")
        out = dym.dynamic_battle()  # get order
        for i in out:
            self.tap(crds.CARDS[i], 40, 90)
            time.sleep(0.2)

    def use_dynamica(self, target: int):
        """
        NOT TESTED!
        """
        while True:  # repeat until reached battle
            # wait for turn start
            while not util.standby(self.u2screenshot(), crds.IMAGE["attack"]):
                time.sleep(0.2)
                # end if finished battle
                if util.standby("tmp.png", crds.IMAGE["finish"], 0.8):
                    return

            if self.reached_battle(target):
                return
            # select cards
            self.dynamica_select()
            time.sleep(1)

    # after-battle related
    def finish_battle(self, lxcj = True):
        while not util.standby(self.u2screenshot(), crds.IMAGE["item"], mode = 2):
            #这个是跳出羁绊礼装或者别的卡进行关闭用，狗粮和qp不需要打开
            #就en浪费CPU
            #xs = util.get_crd(util.get_sh(self.shifts), crds.IMAGE["close"])
            #if len(xs) != 0:
                #self.tap(xs[0])
            self.tap((960, 540), 400, 200)
            time.sleep(0.2)
        time.sleep(0.2)
        x = util.get_crd(self.u2screenshot(), crds.IMAGE["item"])
        self.tap(x[0])
        if lxcj:
            while not util.standby(self.u2screenshot(), crds.IMAGE["lxcj"]):
                
                self.tap((960, 540), 400, 200)
                time.sleep(0.2)
            time.sleep(0.2)
            x = util.get_crd(self.u2screenshot(), crds.IMAGE["lxcj"])
            self.tap(x[0])
        time.sleep(2)
        if util.standby(self.u2screenshot(), crds.IMAGE["no_ap"], imgDict = self.imgDict):
            if self.counts > 0:
                self.eat_apple()
            else:
                raise Exception("Out of AP!")
        
        print("[INFO] Battle Finished.")

    # FLAWED
    def is_finished(self) -> bool:
        time.sleep(0.2)
        return util.standby(self.u2screenshot(), crds.IMAGE["finish"], 0.7)

    # AP related
    # Not tested
    def set_apples(self, cnt: int, apl: str):
        """ Set Apples
        Parameters
        ----------
            cnt: int
        Number of the apples willl be used.

            apl: str
        Path to the image of the apple.
        """
        self.counts = cnt
        self.apple = apl

    def eat_apple(self):
        x = util.get_crd(self.u2screenshot(), self.apple, imgDict = self.imgDict)
        #print(x)
        self.tap((x[0][0],x[0][1]))
        self.counts -= 1
        time.sleep(1)
        y = util.get_crd(self.u2screenshot(), crds.IMAGE["decide"], imgDict = self.imgDict)
        self.tap(y[0])

    # others
    def start_battle(self):
        while not util.standby(self.u2screenshot(), crds.IMAGE["start"], mode = 2, imgDict = self.imgDict):
            time.sleep(0.4)
        #x = util.get_crd(util.get_sh(self.shifts), crds.IMAGE["start"])
        #self.tap(x[0])
        self.tap((1775,1015), 1, 1)
        print("[INFO] Battle started.")

    def quick_start(self, advance=True, lxcj=True):
        """ Quick Start
        Select the default `checkpoint`, `support` and start the battle.

        Parameters
        ----------
            advance: bool, optional
        Set to `True` if you want to enable `advance support selection`, `False` to use the normal support selection.
        By default, it is `False`

        """
        if not lxcj:
            self.select_checkpoint()
            time.sleep(1)
        if advance:
            self.advance_support()
        else:
            self.select_support()
        if not lxcj:
            self.start_battle()

    def reset_shifts(self, sft: (int, int)):
        """ Reset Shifts
        Parameters
        ----------
            sft: (int, int)
        Coordinate shifts in (x, y). When there are blues straps at the edges.
        """
        self.shifts = sft

    def reset_checkpoint(self, ckp: str):
        """ Reset Checkpoint
        Parameters
        ----------
            ckp: (int, int)
        Path to the checkpoint image
        """
        self.checkpoint = ckp

    def reset_support(self, spt: str):
        """ Reset Support
        Parameters
        ----------
            spt: (int, int)
        Path to the support image
        """
        self.support = spt

    def tap(self, crd: (int, int), i: int = 10, j: int = 10):

        x = crd[0] + self.shifts[0]
        y = crd[1] + self.shifts[1]
        self.device.click(x,y)

    def swipe(self, org: (int, int), tar: (int, int)):
        original = (org[0] + self.shifts[0], org[1] + self.shifts[1])
        target = (tar[0] + self.shifts[0], tar[1] + self.shifts[1])
        self.device.swipe(original[0],original[1],target[0],target[1])

    def wait(self, pic: str):
        while not util.standby(self.u2screenshot(), pic):
            time.sleep(0.2)

    def aquire_screenshot(self) -> str:
        """ aquire screenshot
        Returns
        -------
            str
        Path of the screenshot image
        """
        return self.u2screenshot()

    def __str__(self):
        return ("Checkpoint: " + self.checkpoint + "\n" +
                "Support: " + self.support + "\n" +
                "Shift: " + str(self.shifts))

    def connect(self):  # 连接adb与uiautomator
        try:
            # os.system 函数正常情况下返回是进程退出码，0为正常退出码，其余为异常
            # 雷电模拟器
            if os.system('cd adb && adb connect 127.0.0.1:5554') != 0:
                print("连接模拟器失败")
                exit(1)
            if os.system('python -m uiautomator2 init') != 0:
                print("初始化 uiautomator2 失败")
                exit(1)
        except Exception as e:
            print('连接失败, 原因: {}'.format(e))
            exit(1)

        result = os.popen('cd adb && adb devices')  # 返回adb devices列表
        res = result.read()
        lines = res.splitlines()[0:]
        while lines[0] != 'List of devices attached ':
            del lines[0]
        del lines[0]  # 删除表头

        device_dic = {}  # 存储设备状态
        for i in range(0, len(lines) - 1):
            lines[i], device_dic[lines[i]] = lines[i].split('\t')[0:]
        lines = lines[0:-1]
        for i in range(len(lines)):
            if device_dic[lines[i]] != 'device':
                del lines[i]
        print(lines)
        return lines

