import math
import os

import xlsxwriter

from config.names import get_name


def write_excel(timelines, excel_name='timeline.xlsx'):
    max_col = 0
    workbook = xlsxwriter.Workbook(excel_name)
    worksheet = workbook.add_worksheet()
    wrapped = {}

    for k, cells in timelines.items():
        if 'end' not in cells[-1]:
            # print('remove end: ', k, cells[-1])
            cells.remove(cells[-1])
        for c in cells:
            c['start'] *= 10
            c['end'] *= 10
        if len(cells) > 0:
            row_max_col = int(math.ceil(cells[-1]['end']))
            if row_max_col > max_col:
                max_col = row_max_col
    for k, cells in timelines.items():
        queue = list(cells)
        wrapped[k] = []
        if len(cells) == 0:
            print('k:', k, 'no value')
            continue

        for i in range(max_col):
            found = False
            for q in queue:
                start = q['start']
                end = q['end']
                if i <= start < i + 1:
                    wrapped[k].append(start - i - 1)
                    found = True
                    break
                elif i < end <= i + 1:
                    wrapped[k].append(end - i)
                    found = True
                    break
                elif start < i < i + 1 < end:
                    wrapped[k].append(1)
                    found = True
                    break
            if not found:
                wrapped[k].append(0)
    final = {}
    for k, t in timelines.items():
        w = wrapped[k]
        index = 0
        in_range = False
        final[k] = {
            'cells': w,
            'desc': []
        }
        for i,value in enumerate(w):
            if in_range:
                if value != 1:
                    in_range = False
                    index += 1
                    final[k]['desc'][-1]['range'].append(i)
            else:
                if value != 0:
                    in_range = True
                    desc_items = final[k]['desc']
                    desc_items.append({
                        'desc': '',
                        'range': [i]
                    })
                    if 'dmg' in t[index]:
                        # desc_items[-1]['desc'] = 'dmg: %s, crit: %s' % (t[index]['dmg'], t[index]['crit'])
                        desc_items[-1]['desc'] = t[index]['dmg']
        if in_range:
            final[k]['desc'][-1]['range'].append(len(w) - 1)


    for i in range(max_col):
        if i % 10 == 0:
            worksheet.write(0, i + 1, i / 10)

    current_row = 1
    for k, v in final.items():
        worksheet.write(current_row, 0, get_name(k))
        desc = v['desc']
        for item in desc:
            r = item['range']
            if len(r) != 2:
                print("failed to find range...", k, item)
                continue
            if r[0] != r[1]:
                # worksheet.merge_range(current_row, 1 + r[0], current_row, 1 + r[1], '%s  duration: %s' % (item['desc'], (r[1] - r[0]) / 10))
                worksheet.merge_range(current_row, 1 + r[0], current_row, 1 + r[1], item['desc'])
        current_row +=1
        cells = v['cells']
        for i, value in enumerate(cells):
            if value < 0:
                value = -value
                worksheet.conditional_format(current_row, i + 1, current_row, i + 1,
                                             {'type': 'data_bar',
                                              'bar_solid': True,
                                              'bar_direction': 'right',
                                              'max_type': 'num',
                                              'min_type': 'num',
                                              'bar_only': True,
                                              'min_value': 0,
                                              'max_value': 1})
            worksheet.write(current_row, i + 1, value)
        worksheet.conditional_format(current_row, 1, current_row, len(cells), {
            'type': 'data_bar',
            'bar_solid': True,
            'bar_direction': 'left',
            'max_type': 'num',
            'min_type': 'num',
            'min_value': 0,
            'bar_only': True,
            'max_value': 1
        })
        current_row += 1
    worksheet.set_column(1,max_col,1)
    workbook.close()
