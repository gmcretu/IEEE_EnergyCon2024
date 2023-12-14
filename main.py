from __future__ import absolute_import
from __future__ import division
from __future__ import print_function

import os
#os.environ["CUDA_VISIBLE_DEVICES"] = "-1"
import sys

from data_prepare import prepare_original_data
from data_split import split
import time
seed = 10


names = [ "2019-12-09-14-RS14-H1_5sensors", "2019-05-05-09-RS345-H4_5sensors", "2019-12-16-21-RS123-H1_5sensors", "2019-11-26-03-RS35-H1_5sensors", "2019-11-26-02-RS245-H1_5sensors", "2019-08-31-04-RS345-H3_5sensors"]

#number of seqeunces
seq_length = [60]
occ_factor = [1]     #for occ_length= factor *seq_length
l = 2.0         #for balance the set
h = 3.0         #for balance the set
step = [2]       #seconds , for HPD mobile = 2 (=20 de seconds)
nr_sensors = 5

for name in names:
    for i in step:
        for seq in seq_length:
            for factor in occ_factor:
                occ_length = factor * seq   #compute occupancy length

                in_dir = ("./data/%s_%ssec_s%d_o%d" % (name, i, seq, occ_length))
                if not os.path.exists("%s" % (in_dir)):
                    os.makedirs("%s" % (in_dir))

                #write console in txt file
                stdoutOrigin = sys.stdout
                sys.stdout = open(in_dir + "/" + "console.txt", "w")

                #prepare data
                data = prepare_original_data(name, "./dataset/%s.csv" % (name), in_dir, seq, occ_length, i, nr_sensors)
                print("\n")

                #split data
                split(name, l, h, seed, in_dir)

