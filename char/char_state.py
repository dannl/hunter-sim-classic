class CharState:

    def __init__(self, weapon, ap, crit, haste=1.15, t1=False, t2=True, t25=False, r12=False):
        self.weapon = weapon
        self.ap = ap
        self.crit = crit - 0.038
        self.__haste = haste
        self.t1 = t1
        self.t2 = t2
        self.t25 = t25
        self.r12 = r12
        self.target_armor = 3750 - 2250 - 505 - 640
        self.haste_buff = {}

    def haste(self):
        return self.__haste

    def apply_haste(self, apply, since, end):
        if str(apply) not in self.haste_buff:
            self.__haste *= apply
        self.haste_buff[str(apply)] = {
            'start': since,
            'end': end
        }

    def remove_haste(self, apply):
        if str(apply) in self.haste_buff:
            self.__haste /= apply
            del self.haste_buff[str(apply)]

    def haste_at(self, priority):
        if not self.haste_buff:
            return self.__haste
        result = self.__haste
        for k, v in self.haste_buff.items():
            if not (v['start'] <= priority < v['end']):
                result /= float(k)
        return result