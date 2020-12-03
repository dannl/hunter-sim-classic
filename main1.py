import multiprocessing
from concurrent.futures.process import ProcessPoolExecutor
from datetime import datetime

import weapon
from char.char_state import CharState
from config import names
from engine import Engine
from event.end import End
from event.user_action import UserAction
from rotation.rotation import Rotation
from statistic.statistics import Statistics
from utils import write_excel
import pandas as pd

zgblackhand = ['zug', 'black_hand']
earthblackhand = ['earth', 'black_hand']
sandblackhand = ['sand_bug', 'black_hand']
apblackhand = ['ap', 'black_hand']
bugblackhand = ['bugs', 'black_hand']
sandbugs = ['sand_bug', 'bugs']
earthbugs = ['earth', 'bugs']

def run(trinket_group, total_time):
    char_state = CharState(weapon.CJ, 2460, 0.383)
    engine = Engine()
    statistics = Statistics()
    rotation = Rotation(char_state, engine, statistics, trinket_group)
    engine.append(UserAction(rotation, 0))
    engine.append(End(engine, total_time))
    engine.run()
    # write_excel(rotation.statistics.timeline)
    return statistics


def loop(trinket_group, total_time=180, loop_round=1000):
    total = 0
    max_dmg = 0
    min_dmg = 100000000
    max_statistics = None
    min_statistics = None
    for i in range(loop_round):
        statistics = run(list(trinket_group), total_time)
        dmg = statistics.total_dmg()
        total += dmg
        if dmg > max_dmg:
            max_dmg = dmg
            max_statistics = statistics
        if dmg < min_dmg:
            min_dmg = dmg
            min_statistics = statistics
    key = '+'.join(['|'.join(item) for item in trinket_group])
    # write_excel(max_statistics.timeline, 'results/%s_%s_%s.xlsx' % (key, total_time, 'max'))
    write_excel(min_statistics.timeline, 'results/%s_%s_%s.xlsx' % (key, total_time, 'min'))
    return key, total / (total_time * loop_round), max_dmg / total_time, min_dmg / total_time


def run_at_time(time, round=10000):
    start = datetime.now()
    item = {'time': time}
    k, base, max_dmg_base, min_dmg_base = loop([], time, round)
    item[k] = base
    # item[k + 'max'] = max_dmg_base
    # item[k + 'min'] = min_dmg_base
    for trinket_group in [[['black_hand']], [['zug']], [['earth']], [['sand_bug']], [['ap']],
                          [['bugs']], [['dawn']], [['dragon_killer']], [['dragon_teeth']], [['spider']], [['warrior']]]:
        k, d, max_dmg, min_dmg = loop(trinket_group, time, round)
        item[k] = d - base
        # item[k + 'delta'] = d - base
        # item[k + 'max'] = max_dmg
        # item[k + 'min'] = min_dmg
    print('loop %s cost:' % time, (datetime.now() - start).total_seconds())
    return item

def main(start=30, end=180):
    pool = ProcessPoolExecutor(max_workers=max(int(multiprocessing.cpu_count() / 2 - 1), 1))
    futures = []
    for i in range(start, end):
        f = pool.submit(run_at_time, i)
        futures.append(f)
    result_list = []
    now = datetime.now()
    for f in futures:
        it = f.result()
        result_list.append(it)
        df = pd.DataFrame(result_list)
        name_map = {
            k : names.get_name(k) for k in df.columns
        }
        df.rename(columns=name_map, inplace=True)
        df.to_excel('results/result_%s.xlsx' % result_list[-1]['time'], encoding='utf_8_sig',
                    engine='xlsxwriter',
                    index=False)
    print("total time: ", (datetime.now() - now).total_seconds())


if __name__ == '__main__':
    # write_excel(run([sandblackhand], 180).timeline)
    main()
    # write_excel(run([['dawn']], 180).timeline, 'dawn.xlsx')
    # write_excel(run([['dragon_killer']], 180).timeline, 'killer.xlsx')
    # write_excel(run([['dragon_teeth']], 180).timeline, 'teeth.xlsx')
    # write_excel(run([['spider']], 180).timeline,'spider.xlsx')
    # write_excel(run([['warrior']], 180).timeline, 'warrior.xlsx')

    # for trinket_group in [[['black_hand']], [['earth']], [['sand_bug']], [['ap']],
    #                       [['bugs']], [['dawn']], [['dragon_killer']], [['dragon_teeth']], [['spider']], [['warrior']]]:
    #     k, d, max_dmg, min_dmg = loop(trinket_group, 30, 1)

