class Statistics:

    def __init__(self):
        self.timeline = {}

    def add_dmg(self, name, dmg, is_crit, priority):
        self.add_end(name, priority)
        self.timeline[name][-1]['dmg'] = dmg
        self.timeline[name][-1]['crit'] = is_crit

    def add_start(self, name, priority):
        l = self.timeline.setdefault(name, [])
        if len(l) == 0:
            l.append({
                'start': priority
            })
        else:
            if 'end' not in l[-1]:
                return
            l.append({
                'start': priority
            })

    def add_end(self, name, priority):
        l = self.timeline.setdefault(name, [])
        if len(l) > 0:
            l[-1]['end'] = priority
        else:
            raise Exception('add an end before start.')

    def calculate(self):
        pass

    def total_dmg(self):
        total = 0
        for spell, dmg in self.timeline.items():
            for d in dmg:
                if 'dmg' in d and isinstance(d['dmg'], float):
                    total += d['dmg']
        return total

    def dps(self, seconds):

        return self.total_dmg() / seconds
