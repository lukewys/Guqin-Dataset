import numpy as np
import pandas as pd
import os


def add_overtone(filepath, save_filepath, measure_list):
    data = pd.read_excel(filepath, encoding='UTF-8-sig', header=None, sep='\t', dtype=str)
    for i in (measure_list):
        if isinstance(i, tuple):
            measure_num = range(i[0] - 1, i[1])
        else:
            measure_num = [i - 1]
        for measure in measure_num:
            for j in range(data.shape[1]):
                if not pd.isnull(data[j][measure]):
                    if data[j][measure].find(' ') > 0:
                        new_note = ''
                        for n in data[j][measure].split(' '):
                            new_note = new_note + '`' + n + ' '
                        new_note = new_note[:-1]
                        data[j][measure] = new_note
                    else:
                        data[j][measure] = '`' + data[j][measure]

    save_filepath = os.path.join(save_filepath, filepath.split('\\')[-2], filepath.split('\\')[-1])
    data.to_excel(save_filepath, encoding='UTF-8-sig', header=None, index=False)


if __name__ == '__main__':
    filepath = r''
    savepath = r''
    measure_list = [(2, 7), (46, 49), (143, 146)]

    add_overtone(filepath, savepath, measure_list)
