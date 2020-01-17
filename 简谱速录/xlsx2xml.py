import argparse
from argparse import RawDescriptionHelpFormatter
import numpy as np
import pandas as pd
import os
import music21
from fractions import Fraction

'''
英文报错：
print('Multiple Pitch: ' + self.string + ' note (' + str(self.row + 1) + ',' + str(
    self.col + 1) + ')' + ', piece ' + str(self.piece_number + 1) +
      ' in ' + self.filepath.split('\\')[-1])

print('No Pitch or Multiple Same Pitch: ' + self.string + ' note (' + str(self.row + 1) + ',' + str(
    self.col + 1) + ')' + ', piece ' + str(self.piece_number + 1) + ' in ' +
      self.filepath.split('\\')[-1])      

print('Incomplete Measure: Measure ' + str(i + 1) + ', piece ' + str(len(piece_list) + 1) +
      ' in ' + filepath.split('\\')[-1])
'''


# TODO:泛音的问题还没有完全解决


class NumberedNote:
    def __init__(self, string, debug_info):
        self.element_count = {
            ' ': 0,  # 音符间隔
            '*': 0,  # 升半音
            '+': 0,  # 时值翻倍
            '-': 0,  # 时值减半
            '.': 0,  # 符点
            '/': 0,  # 降半音
            '0': 0,  # 空拍
            # 1-7:C-B
            '1': 0,
            '2': 0,
            '3': 0,
            '4': 0,
            '5': 0,
            '6': 0,
            '7': 0,
            '8': 0,  # 升一个八度
            '9': 0,  # 降一个八度
            't': 0,  # 三连音(triplet)
            'q': 0,  # 五连音(quintuplet)
            's': 0,  # 六连音(sextuplet)
            '`': 0,  # 泛音标记
        }

        self.note = None
        self.tuplet = 1
        self.string = string
        self.row = debug_info['row']
        self.col = debug_info['col']
        self.filepath = debug_info['filepath']
        self.piece_number = debug_info['piece_number']

    def assign(self, element):
        try:
            self.element_count[element] += 1
        except Exception:
            print(self.filepath)

    def _elements_count2note(self, elements_count):
        pitch_name = {'1': 'C',
                      '2': 'D',
                      '3': 'E',
                      '4': 'F',
                      '5': 'G',
                      '6': 'A',
                      '7': 'B'}
        if elements_count['0'] == 1:
            note = music21.note.Rest()
        else:
            note = music21.note.Note()
        have_pitch = False

        # 检查有无多个音高或相同音高
        if DEBUG:
            for i in range(1, 8):
                if elements_count[str(i)] == 1:
                    if have_pitch:
                        print('多个音高: ' + self.string + ' ，第' + str(self.row + 1) + ' 行，第' + str(
                            self.col + 1) + '个音符' + '，位于 ' + self.filepath.split('\\')[-1] +
                              '，第 ' + str(self.piece_number + 1) + '段')

                    have_pitch = True

            if have_pitch == False and elements_count['0'] == 0:
                print('无音高或多个相同音高: ' + self.string + ' ，第' + str(self.row + 1) + ' 行，第' + str(
                    self.col + 1) + '个音符' + '，位于 ' + self.filepath.split('\\')[-1] +
                      '，第 ' + str(self.piece_number + 1) + '段')

        # 转换音高
        for i in range(1, 8):
            if elements_count[str(i)] == 1:
                note.step = pitch_name[str(i)]
        # 在这里暂时使用跳音（即实心圆点）代表泛音
        # 实际上，应使用泛音记号（空心圆点）表示泛音，
        # 但是发现MuseScore对于MusicXML中泛音记号的显示有Bug。
        # 如果希望使用泛音记号（空心圆点），则将
        # articu = music21.articulations.Staccato()改为
        # articu = music21.articulations.StringHarmonic()
        if elements_count['`'] == 1:
            articu = music21.articulations.Staccato()  # StringHarmonic()
            articu.placement = 'above'
            note.articulations = [articu]
        if elements_count['8'] != 0:
            note.octave = note.octave + elements_count['8']
        if elements_count['9'] != 0:
            note.octave = note.octave - elements_count['9']
        if elements_count['-'] != 0:
            note.duration.quarterLength = note.duration.quarterLength / 2 ** elements_count['-']
        if elements_count['+'] != 0:
            note.duration.quarterLength = note.duration.quarterLength + elements_count['+']
        if elements_count['*'] == 1:
            note.pitch.accidental = music21.pitch.Accidental(1)
        if elements_count['/'] == 1:
            note.pitch.accidental = music21.pitch.Accidental(-1)
        if elements_count['.'] != 0:
            note.duration.dots = note.duration.dots + elements_count['.']

        if elements_count['t'] == 1:
            note.duration.quarterLength = note.duration.quarterLength * 2 / 3
        if elements_count['q'] == 1:
            note.duration.quarterLength = note.duration.quarterLength * 4 / 5
        if elements_count['s'] == 1:
            note.duration.quarterLength = note.duration.quarterLength * 4 / 6
        if self.tuplet != 1:
            if self.tuplet < 4:
                note.duration.quarterLength = note.duration.quarterLength * 2 / self.tuplet
            elif 4 < self.tuplet < 8:
                note.duration.quarterLength = note.duration.quarterLength * 4 / self.tuplet
            elif 8 < self.tuplet < 16:
                note.duration.quarterLength = note.duration.quarterLength * 8 / self.tuplet

        return note

    def get_note(self):
        self.note = self._elements_count2note(self.element_count)
        return self.note


def string2measure(string, measure, debug_info):
    tmp_note_list = []
    note = NumberedNote(string, debug_info)
    tmp_note_list.append(note)
    is_chord = False
    ind = 0
    while ind < (len(string)):
        c = string[ind]
        if c != ' ':
            if c == '[':  # 如果是多连音的情况，则读取方括号中的数字并将判断下标跳过方括号
                ind_end = string.index(']')
                tuplet = string[ind + 1:ind_end]
                note.tuplet = int(tuplet)
                ind = ind_end + 1
            else:
                note.assign(c)
                ind += 1

        elif ind != len(string) - 1:  # 空格在中间位置而不在最后
            is_chord = True  # 标记为和弦
            tmp_note_list.append(NumberedNote(string, debug_info))  # 先在tmp_note_list中加入一个带有debug信息的空音符
            note = tmp_note_list[-1]  # 将当前音符置为刚刚加入的音符，等待后续添加信息
            ind += 1

        else:  # 空格在最后的情况
            ind += 1

    if is_chord == False:  # 如果不是和弦，则直接讲该简谱音符转换为音符并加入小节中
        measure.append(note.get_note())
    else:  # 如果是和弦，则以tmp_note_list中的音符生成和弦类变量并加入小节中
        chord = music21.chord.Chord()
        chord_duration = tmp_note_list[-1].get_note().duration
        for chord_note in tmp_note_list:
            chord.add(chord_note.get_note().pitch)
        chord.duration = chord_duration
        measure.append(chord)
    return measure


def xlsx2xml(filepath, save_filepath, split):
    data = pd.read_excel(filepath, encoding='UTF-8-sig', dtype='str', header=None, sep='\t')
    data = np.array(data)
    # 如果琴谱大部分小节都是八分音符为一拍，则在录入时可以在xlsx文件后加'_8fenyinfu'来避免DEBUG检查不完整小节。
    if DEBUG:
        if filepath.find('8fenyinfu') != -1:
            half_quarter = True
        else:
            half_quarter = False

    measure_list = music21.stream.Stream()
    measure_length = 0  # 记录前一小节的时值用来在拍号改变时生成新的拍号
    piece_list = []
    for row in range(data.shape[0]):
        # if np.isnan(data[row, 0])
        if data[row, 0] == 'nan' or type(data[row, 0]) != str:
            if split:
                piece_list.append(measure_list)
                measure_list = music21.stream.Stream()
                measure_length = 0
            else:
                pass
        else:
            measure = music21.stream.Measure(number=row + 1)

            for col in range(data.shape[1]):
                # if not np.isnan(data[i, 0]) and type(data[i, j]) == str:
                if data[row, col] != 'nan' and type(data[row, col]) == str:
                    debug_info = {
                        'row': row,
                        'col': col,
                        'filepath': filepath,
                        'piece_number': len(piece_list)
                    }

                    measure = string2measure(data[row, col], measure, debug_info)

            if measure.duration.quarterLength != measure_length:
                # 如果这一小节的时值与上一小节不同，则重新生成拍号
                if int(measure.duration.quarterLength) != 0:  # 如果是弱起则不插入拍号
                    ts = music21.meter.TimeSignature()
                    if measure.duration.quarterLength % 1 != 0:  # 如果不是以四分音符为一拍，则需要计算分子分母
                        if isinstance(measure.duration.quarterLength, Fraction):
                            measure.duration.quarterLength = float(measure.duration.quarterLength)
                            if DEBUG:
                                # 有的时候复杂的多连音会使music21生成Fraction类型的时值，只要这个时值正常就没问题。
                                print('Fraction: ', measure.duration.quarterLength, '，位于第' + str(row) + '行',
                                      '位于 ' + filepath.split('\\')[-1] + ' 第 ' + str(len(piece_list) + 1) + ' 段')
                        num, den = float.as_integer_ratio(measure.duration.quarterLength)
                        ts.denominator = 4 * den
                        ts.numerator = int(measure.duration.quarterLength * den)
                    else:  # 如果以四分音符为一拍，则可以直接指定拍号
                        ts.denominator = 4
                        ts.numerator = int(measure.duration.quarterLength)
                    measure.insert(0, ts)
                    measure_length = measure.duration.quarterLength

            if DEBUG:
                if half_quarter == False:
                    if (measure.duration.quarterLength % 1) != 0:
                        print('不完整小节：第 ' + str(row + 1) + ' 行，位于 ' + filepath.split('\\')[-1]
                              + ' 第 ' + str(len(piece_list) + 1) + ' 段')

                    # 如果是小于1拍或者弱起，就不插入拍号，也不赋值分子
                    if int(measure.duration.quarterLength) != 0:
                        ts.numerator = int(measure.duration.quarterLength)
                else:
                    if ((measure.duration.quarterLength * 2) % 1) != 0:
                        print('不完整小节：第 ' + str(row + 1) + ' 行，位于 ' + filepath.split('\\')[-1]
                              + ' 第 ' + str(len(piece_list) + 1) + ' 段')
                    ts.numerator = int(measure.duration.quarterLength * 2)

            measure_list.append(measure)

    piece_list.append(measure_list)

    save_score(piece_list, filepath, save_filepath)


def save_score(piece_list, filepath, save_filepath):
    file_dir, file_name = os.path.split(filepath)
    _, file_folder = os.path.split(file_dir)

    # 输出谱子的保存路径会带有输入谱子的上一级文件夹
    # 即，谱子/古琴谱/a.xlsx，输出为：输出路径/古琴谱/a.xlsx
    save_folder = os.path.join(save_filepath, file_folder)

    # 如果保存路径文件夹不存在则生成文件夹
    if not os.path.exists(save_folder):
        os.makedirs(save_folder)
    # 如果有多段，则每一段分开保存，保存时乐谱声部名为‘Guqin’，音色为钢琴，标题为文件名
    if len(piece_list) != 1:
        piece = 1
        for i in range(len(piece_list)):
            score = music21.stream.Score()
            part = music21.stream.Part()
            part.partName = 'Guqin'
            part.insert(0, music21.instrument.Guitar)  # Newly added
            part.append(piece_list[i])
            score.insert(0, part)
            score.insert(0, music21.metadata.Metadata())
            score.metadata.title = file_name.split('.')[0] + '_' + str(piece)
            score.metadata.composer = ''
            score.write('xml',
                        fp=os.path.join(save_folder,
                                        file_name.split('.')[0] + '_' + str(piece) + '.xml'))
            if DEBUG == False:
                print('已转换：', file_name.split('.')[0] + '_' + str(piece) + '.xml')
            piece += 1
    # 如果只有一段，则直接保存，保存时乐谱声部名为‘Guqin’，音色为钢琴，标题为文件名
    else:
        score = music21.stream.Score()
        part = music21.stream.Part()
        part.partName = 'Guqin'
        part.insert(0, music21.instrument.Guitar())
        part.append(piece_list[0])
        score.insert(0, part)
        score.insert(0, music21.metadata.Metadata())
        score.metadata.title = file_name.split('.')[0]
        score.metadata.composer = ''
        score.write('xml',
                    fp=os.path.join(save_folder,
                                    file_name.split('.')[0] + '.xml'))
        if DEBUG == False:
            print('已转换：', file_name.split('.')[0] + '.xml')


def get_file_list(filepath, file_extension='.xlsx', recursive=True):
    '''
    @:param filepath: a string of directory
    @:param file_extension: a string of list of strings of the file extension wanted, format in, for example, '.xml', with the ".".
    @:return A list of all directories of files in given extension in given filepath.
    If recursive is True，search the directory recursively.
    '''
    pathlist = []
    if recursive:
        for root, dirs, files in os.walk(filepath):
            for file in files:
                if type(file_extension) is list:
                    for exten in file_extension:
                        if file.endswith(exten):
                            pathlist.append(os.path.join(root, file))
                elif type(file_extension) is str:
                    if file.endswith(file_extension):
                        pathlist.append(os.path.join(root, file))
    else:
        files = os.listdir(filepath)
        for file in files:
            if type(file_extension) is list:
                for exten in file_extension:
                    if file.endswith(exten):
                        pathlist.append(os.path.join(filepath, file))
            elif type(file_extension) is str:
                if file.endswith(file_extension):
                    pathlist.append(os.path.join(filepath, file))
    if len(pathlist) == 0:
        print('Wrong or empty directory')
        raise FileNotFoundError
    return pathlist


if __name__ == '__main__':
    parser = argparse.ArgumentParser(
        description="Converts special text score notation in xlsx files to MusicXML files.\n"
                    "Format: xlsx2xml.py <input_dir> <output_dir> [no-split] [debug]\n"
                    "input_dir: directory containing .xlsx files, output_dir: directory to store .musicxml files\n"
                    "Example usage: \n"
                    "xlsx2xml.py Dataset/input Dataset/output\n"
                    "Argument \"--no-split\" could be added to avoid splitting the score"
                    "according to phrase notation.\n"
                    "Argument \"--no-split\" could be added to check syntax error and potential incomplete bar.\n"
                    "将以xlsx格式储存的文字转录谱转换为MusicXML文件。"
                    "命令行格式：xlsx2xml.py <input_dir> <output_dir> [no-split] [debug]\n"
                    "input_dir: .xlsx 文件储存路径, output_dir: .musicxml 文件输出路径。\n"
                    "命令行示例：xlsx2xml.py Dataset/input Dataset/output\n"
                    "如果不需要在转换时按段切割谱子，则在最后加上--no-split参数\n"
                    "加入--debug参数可以有限度地自动检查录入错误与不完整小节。\n"
        , formatter_class=RawDescriptionHelpFormatter)
    parser.add_argument('input_dir', type=str, help="Directory of .xlsx files")
    parser.add_argument('output_dir', type=str,
                        help="Output directory, all subdirectory in [input_dir] would be created")
    parser.add_argument('--no-split', dest='split', action='store_false',
                        help="Do not split Guqin score, default as spiting Guqin score according to paragraph notation.")
    parser.add_argument('--debug', dest='debug', action='store_false',
                        help="Activate debug mode, will print some error check result.")

    parser.set_defaults(split=True)

    args = parser.parse_args()

    DEBUG = args.debug

    file_list = get_file_list(args.input_dir)
    for file_path in file_list:
        xlsx2xml(file_path, args.output_dir, args.split)
