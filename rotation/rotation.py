from buff.buff.eagle import Eagle
from buff.buff.fake_death import FakeDeathTrigger
from buff.buff.rapid import Rapid
from buff.buff.weakness import Weakness
from buff.trigger import Trigger
from buff.trinket.ap import Ap
from buff.trinket.black_hand import BlackHand
from buff.trinket.dawn import Dawn
from buff.trinket.dragon_killer import DragonKiller
from buff.trinket.dragon_teeth import DragonTeeth
from buff.trinket.earth import Earth
from buff.trinket.spider import Spider
from buff.trinket.warrior import Warrior
from event.cast_done import CastDone
from event.gcd_done import GCDDone
from event.user_action import UserAction
from rotation.buff_executors.bugs_executor import BugsExecutor
from rotation.buff_executors.earth_executor import EarthExecutor
from rotation.buff_executors.lasting_buff_executor import LastingBuffExecutor
from rotation.buff_executors.spider_executor import SpiderExecutor
from rotation.buff_executors.sand_bug_executor import SandBugExecutor
from rotation.buff_executors.zug_executor import ZugExecutor
from rotation.executors.aim_executor import AimExecutor
from rotation.executors.auto_executor import AutoExecutor
from rotation.executors.multi_executor import MultiExecutor
from spell.aim import Aim
from spell.auto import Auto
from spell.multi import Multi


class Rotation:

    def __init__(self, char_state, engine, statistics, trinket_groups):
        self.executors = []
        self.char_state = char_state
        self.engine = engine
        self.statistics = statistics
        self.casting = False
        self.in_gcd = False
        self.auto = Auto()
        self.aim = Aim()
        self.multi = Multi()
        self.rapid = Rapid()
        self.available_trinket = self.setup_available_trinket()
        self.current_trinket = None
        self.trinket_groups = trinket_groups
        self.switch_next_trinket_group()
        self.executors.append(AutoExecutor(self.auto))
        self.executors.append(AimExecutor(self.aim))
        self.executors.append(MultiExecutor(self.multi))
        self.before_dmg_triggers = {}
        self.before_dmg_triggers.setdefault(self.auto.name, []).append(Trigger(self.rapid, 1))
        self.after_dmg_triggers = {}
        self.after_dmg_triggers.setdefault(self.auto.name, []).append(Trigger(Eagle(), 0.05))
        if char_state.t2:
            self.after_dmg_triggers[self.auto.name].append(Trigger(Weakness(), 0.03))
        if len(trinket_groups) > 0:
            self.after_dmg_triggers[self.auto.name].append(FakeDeathTrigger())

    def get_trinket(self, name):
        executor = self.available_trinket.get(name)
        if executor:
            return executor.spell

    def setup_available_trinket(self):
        available = {}

        def add_item(cls, spell=None):
            if spell:
                excutor = cls(spell)
            else:
                excutor = cls()
            excutor.enabled = False
            self.executors.append(excutor)
            available[excutor.spell.name] = excutor
        add_item(LastingBuffExecutor, Ap())
        add_item(LastingBuffExecutor, BlackHand())
        add_item(LastingBuffExecutor, DragonTeeth())
        add_item(LastingBuffExecutor, Dawn())
        add_item(LastingBuffExecutor, Warrior())
        add_item(EarthExecutor, DragonKiller())
        add_item(EarthExecutor, Earth())
        add_item(SpiderExecutor, Spider())
        add_item(BugsExecutor)
        add_item(SandBugExecutor)
        add_item(ZugExecutor)
        return available

    def switch_next_trinket_group(self):
        if self.current_trinket:
            for trinket in self.current_trinket:
                executor = self.available_trinket.get(trinket)
                if executor:
                    executor.spell.dequip(self.engine, self.char_state)
                    executor.enabled = False
        if len(self.trinket_groups) > 0:
            self.current_trinket = self.trinket_groups.pop(0)
            for trinket in self.current_trinket:
                # trinket.equip(self.engine, self.char_state)
                executor = self.available_trinket.get(trinket)
                if executor:
                    executor.spell.equip(self.engine, self.char_state)
                    executor.enabled = True
        else:
            self.current_trinket = []

    def perform(self):
        spell = None
        buff = None
        for executor in self.executors:
            spell, buff = executor.attempt_cast(self, self.engine, self.char_state)
            if spell or buff:
                break
        current = self.engine.current_priority()
        if spell:
            self.start_casting_trigger(spell.name)
            self.set_casting(True)
            self.statistics.add_start(spell.name, current)
            if spell.trigger_gcd:
                self.in_gcd = True
                self.engine.append(GCDDone(self, current + 1.5))
            end_time = spell.calculate_finish_time(self.char_state, current)
            self.engine.append(
                CastDone(self, self.engine, self.char_state, spell, self.statistics, end_time))
        if buff:
            self.statistics.add_start(buff.name, current)
            buff.perform(self, self.engine, self.char_state)
            self.engine.append(UserAction(self, self.engine.current_priority()))

    def is_casting(self):
        return self.casting

    def is_in_gcd(self):
        return self.in_gcd

    def set_casting(self, val):
        self.casting = val

    def start_casting_trigger(self, name):
        triggers = self.before_dmg_triggers.get(name)
        if triggers:
            for t in triggers:
                t.trigger(self, self.engine, self.char_state)
                    # self.statistics.add_start(t.buff.name, self.engine.current_priority())

    def trigger(self, name):
        triggers = self.after_dmg_triggers.get(name)
        if triggers:
            for trigger in triggers:
                if trigger.trigger(self, self.engine, self.char_state):
                    self.statistics.add_start(trigger.buff.name, self.engine.current_priority())
        triggers = self.after_dmg_triggers.get('all')
        if triggers:
            for trigger in triggers:
                if trigger.trigger(self, self.engine, self.char_state):
                    self.statistics.add_start(trigger.buff.name, self.engine.current_priority())

    def add_trigger(self, name, trigger):
        self.after_dmg_triggers.setdefault(name, []).append(trigger)

    def remove_trigger(self, name, s_name):
        triggers = self.after_dmg_triggers.get(name)
        if triggers:
            items_to_remove = []
            for t in triggers:
                if t.buff.name == s_name:
                    items_to_remove.append(t)
            for item in items_to_remove:
                triggers.remove(item)

    def update_trinket_next_available(self):
        pass