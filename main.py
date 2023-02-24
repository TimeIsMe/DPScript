#                   Data Processing Script.
# ------------------------------------------------------------
# File Name: main.py
# Author: Mingliang Wang
# Version: 1.0
# Brief:
# Date: 2023/02/24
# ------------------------------------------------------------

import sys
import os
import re
import numpy as np
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d

pattern = r'^([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)(.{2})([-+]?(\d+(\.\d*)?|\.\d+)([eE][-+]?\d+)?)$'

RESULT_FILE = r'result.txt'

labelList = ['best', 'upper right', 'upper left', 'lower left', 'lower right', 'right', 'center left',
             'center right', 'lower center', 'upper center', 'center']

class dataset:
    def __init__(self, in_file_name=None, out_file_name=None) -> None:
        self._fp = None
        self.in_file_name = in_file_name
        self.out_file_name = out_file_name
        self._header = []
        self._rawdata = []
        self._procdata = np.zeros((2,), dtype=np.float32)
        self.out_list = None
        self._vol_cur_0 = 0.0
        self._max_cur = 0.0
        self._pce = 0.0
        self._ff = 0.0
        self._vol = None
        self._cur = None
        self._pces = None
        try:
            self._fp = open(self.in_file_name, 'r')
        except IOError:
            print("can't open the file:{0}".format(self.in_file_name))

    def _pre_proc(self):
        for line in self._fp.readlines():
            mt = re.match(pattern, line)
            if mt is None:
                self._header.append(line)
            else:
                mt = mt.string
                num1, num2 = mt.split(', ')
                self._rawdata.append([num1, num2])

        # vol=-vol, cur=cur*1000/0.09.
        data_tmp = np.asarray(self._rawdata, dtype=np.float32)
        ary = np.asarray((-1, 1000.0), dtype=np.float32)
        data_tmp = np.multiply(data_tmp, ary)
        ary = np.asarray((1, 0.09), dtype=np.float32)
        data_tmp = np.divide(data_tmp, ary)

        # Intercept the voltage value between 0.2 and 1.4.
        data_list = []
        _v, _ = data_tmp[0]
        for [v, c] in data_tmp:
            if v > _v:
                break
            if -0.20-0.00001 < v < 1.2+0.00001:
                data_list.append([v, c, v*c])
            _v = v
        self._procdata = np.asarray(data_list, dtype=np.float32)

        self._vol = self._procdata[..., 0]
        self._cur = self._procdata[..., 1]
        self._pces = self._procdata[..., 2]

    def _get_vol_cur_0(self):
        f = interp1d(self._cur, self._vol)
        self._vol_cur_0 = f(0.0)
        pass
        # cur_abs = np.absolute(self._cur)
        # index = np.argmin(cur_abs)
        # self._vol_cur_0 = self._vol[index]

    def _get_cur_vol_0(self):
        vol_abs = np.absolute(self._vol)
        index = np.argmin(vol_abs)
        self._cur_vol_0 = self._cur[index]

    def _get_max_cur(self):
        _, self._max_cur, _= np.amax(self._procdata, 0)
        print("max current: {0}".format(self._max_cur))

    def _get_ff(self):
        self._get_cur_vol_0()
        self._get_vol_cur_0()
        tmp = self._vol_cur_0 * self._cur_vol_0
        m = np.amin(self._pces)
        m = m/tmp
        self._ff = abs(m)*100.0

    def _get_pce(self):
        self._pce = abs(np.amin(self._pces))


    def run(self):
        self._pre_proc()
        self._get_ff()
        self._get_pce()
        self.out_list = np.round(self._procdata, 3)

    def get_result(self):
        vol = self._vol_cur_0
        cur = abs(self._cur_vol_0)
        pce = self._pce
        ff = self._ff
        return vol, cur, pce, ff

    def get_output(self):
        out_data = ''
        for line in self._header:
            out_data += line
        out_array = self.out_list
        for [v, c, p] in out_array:
            line = str(format(v, '.3f')) + ', ' + str(format(c, '.3f')) + ', ' + str(format(p, '.3f')) + '\n'
            out_data += line
        with open(self.out_file_name, 'w') as ofp:
            ofp.write(out_data)
            ofp.flush()
            ofp.close()

    def __del__(self):
        self._fp.close()


DATA_EXT = ['.txt', ]


def main():
    if (len(sys.argv) != 3):
        print("The App arg is invalid")
        print("Example: python3 main.py ./InDataDir ./OutDataDir")
        exit(1)

    in_data_dir = sys.argv[1]
    out_data_dir = sys.argv[2]
    if not os.path.isdir(in_data_dir):
        print("Invalid input data dir.")
        exit(2)

    i = 0
    if out_data_dir[-1] == '/':
        out_data_dir = out_data_dir[:-1]
    name_len = len(out_data_dir)
    while os.path.isdir(out_data_dir):
        out_data_dir = out_data_dir[:name_len]
        out_data_dir = out_data_dir + str(i)
        i = i+1
    if out_data_dir[-1] != '/':
        out_data_dir = out_data_dir + '/'
    os.mkdir(out_data_dir)

    # get data file path.
    data_path_list = [os.path.join(in_data_dir, d_file)
                 for d_file in os.listdir(in_data_dir)
                 if os.path.splitext(d_file)[1] in DATA_EXT]

    # open result file.
    res_file = out_data_dir + RESULT_FILE
    try:
        r_fp = open(res_file, 'x')
        r_fp.write('-' * 60 + '\r\n')
        tmp = "%-12s\t%-12s\t%-12s\t%-12s\t%-12s\n"%("FileName", "JSC(mA/cm2)", "VOC(V)", "FF(%)", "PCE(%)\r\n")
        r_fp.write(tmp)
        r_fp.write('-' * 60 + '\r\n')
    except IOError:
        print("can't open the result file:{0}".format(res_file))
        exit(3)

    group_index = 0
    old_group_index = -1

    # start interactive mode
    plt.ion()
    for data_file_name in data_path_list:
        r = re.findall(r'[/\\]\d+\.\d+\.txt', data_file_name)
        if not r:
            continue
        # this file should be drawn.
        r = r[0]
        name = r[1:]
        print("{0}".format(r))
        out_data_file_name = out_data_dir + r[1:]
        print("{0}".format(out_data_file_name))
        ds = dataset(data_file_name, out_data_file_name)
        ds.run()
        ds.get_output()
        vol, cur, pce, ff = ds.get_result()

        # record the result into result.txt
        result_line = "%-12s\t%-12s\t%-12s\t%-12s\t%-12s\n"%(name, str(format(cur, '.2f')), str(format(vol, '.3f')),
                                                       str(format(ff, '.1f')), str(format(pce, '.2f')))
        r_fp.write(result_line)

        # draw
        tmp = name.split('.')
        group_index = int(tmp[0])
        result_list = ds.out_list
        vol_list = result_list[..., 0]
        cur_list = result_list[..., 1]
        plt.figure(group_index)
        plt.plot(vol_list, cur_list, linewidth=1, label=name)
        plt.legend(loc='best', fontsize=12)
        if group_index != old_group_index:
            old_group_index = group_index
            plt.axhline(0, color='black', linewidth=1)
            plt.axvline(0, color='black', linewidth=1)
            plt.xlabel("Voltage(V)")
            plt.ylabel("Current Density(mA*cm-2)")

        del ds
    r_fp.close()


if __name__ == '__main__':
    main()
    input("input Enter to exit...")
    exit(0)

