import multiprocessing
import os
from concurrent.futures.process import ProcessPoolExecutor
from datetime import datetime

import main_bugs
import weapon
from char.char_state import CharState
from config import names
from engine import Engine
from event.end import End
from event.user_action import UserAction
from rotation.rotation import Rotation
from statistic.statistics import Statistics
from utils import write_excel
from itertools import combinations
import pandas as pd

if not os.path.isdir('results/max_min'):
    os.makedirs('results/max_min')

def run(trinket_group, total_time):
    char_state = CharState(weapon.KL, 2360, 0.393)
    engine = Engine()
    statistics = Statistics()
    rotation = Rotation(char_state, engine, statistics, trinket_group)
    engine.append(UserAction(rotation, 0))
    engine.append(End(engine, total_time))
    engine.run()
    # write_excel(rotation.statistics.timeline)
    return statistics


def loop(trinket_group,total_time=180, loop_round=1000):
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
    key = '+'.join(['|'.join([names.get_name(i) for i in item]) for item in trinket_group])
    write_excel(max_statistics.timeline, 'results/max_min/%s_%s_%s.xlsx' % (key, total_time, 'max'))
    write_excel(min_statistics.timeline, 'results/max_min/%s_%s_%s.xlsx' % (key, total_time, 'min'))
    return key, total / (total_time * loop_round), max_dmg / total_time, min_dmg / total_time


def run_at_time(time, round=100):
    start = datetime.now()
    result = {'time': time}
    k, base, max_dmg_base, min_dmg_base = loop([], time, round)
    result[k] = base
    # available = ['black_hand','zug','earth','sand_bug','bugs', 'dawn','dragon_killer','spider','warrior']
    available = ['zug','bugs','dragon_killer','spider','warrior']
    # available = ['dragon_killer','spider']
    groups = []
    # for item in available:
    #     groups.append([[item]])
    available = combinations(available, 2)
    for item in available:
        groups.append([list(item)])
    # groups.append([['zug','warrior'],['dragon_killer','spider'], ['warrior','dawn']])
    # groups.append([['dragon_killer','spider'], ['warrior','dawn']])
    # groups.append([['warrior','spider'], ['warrior','dawn']])
    # groups.append([['warrior','dragon_killer'], ['warrior','dawn']])
    for trinket_group in groups:
        k, d, max_dmg, min_dmg = loop(trinket_group, time, round)
        result[k] = d - base
    print('loop %s cost:' % time, (datetime.now() - start).total_seconds())
    return result


def main(start=30, end=180, round=1000):
    pool = ProcessPoolExecutor(max_workers=max(int(multiprocessing.cpu_count() / 2 - 1), 1))
    # pool = ProcessPoolExecutor(max_workers=10)
    futures = []
    for i in range(start, end):
        f = pool.submit(run_at_time, i, round)
        futures.append(f)
    result_list = []
    now = datetime.now()
    for f in futures:
        it = f.result()
        best = 0
        best_k = None
        for k,v in it.items():
            if k != 'time' and k != '无' and k != '':
                if v > best:
                    best = v
                    best_k = k
        it['最优'] = best_k
        it['最优提升'] = best
        result_list.append(it)
        df = pd.DataFrame(result_list)
        name_map = {
            k : names.get_name(k) for k in df.columns
        }
        df.rename(columns=name_map, inplace=True)
        df.to_excel('results/result_%s.xlsx' % result_list[-1]['time'], encoding='utf_8_sig',
                    engine='xlsxwriter',
                    index=False)
    fs = os.listdir('results')
    for f in fs:
        if 'xlsx' in f and int(f.split('.')[0].split('_')[-1]) != end - 1:
            os.remove('results/' + f)
    df = pd.DataFrame(result_list)
    df.to_excel('results/result_%s.xlsx' % result_list[-1]['time'], encoding='utf_8_sig',
                engine='xlsxwriter',
                index=False)
    print("total time: ", (datetime.now() - now).total_seconds())


if __name__ == '__main__':
    main(170, 171, 5000)
    # main_bugs.main('bugs0', 30, 180, 5000)
    # main_bugs.main('bugs1', 30, 180, 5000)
    # main_bugs.main('bugs2', 30, 180, 5000)

