import csv
import os
from datetime import datetime
import numpy as np
from data_io import write_data

LABEL_OCC = "occupancy"
LABEL_SENS = "sensors"
LABEL_TRANSITION = "transition"     #is 1 if there is only one occupation in the occupancy sequence (occ_length)
LABEL_LASTDATE = "last_date"
LABEL_LASTOCC = "last_occ"

Occupancy = {"E": 0, "L": 1, "M": 2, "H": 3, "1": 2, "0": 0}
dict_occ = {0: "empty", 1: "low", 2: "medium", 3: "high"}

# name
# the path of dataset
# sequence length (0:50, 1:51, 2:52...) from dataset
# occupancy length - the size of the sequence where we are looking for the occupation to be the same (for TRANSITION)
# step
def prepare_original_data(name, file_to_read, out_dir, max_sequence, occ_length, step, nr_sensors):
    data = []
    min_sequence = int(max_sequence * 3 / 4)
    treshold = 1        #one hour

    #check the number of elements per line based on the number of sensors
    line_len = 5
    if nr_sensors == 4:
        line_len = 6
    elif nr_sensors == 5:
        line_len = 7

    #read the data from a file
    with open(file_to_read, "r") as f:
        lines = csv.reader(f)
        raw_data=[]      #brut date
        row_count = 0
        line_seq = []
        for idx, line in enumerate(lines):
            line_seq.append(line)
            if idx%step == 0 and len(line) == line_len:
                line_med = []
                row_count = row_count + 1
                try:
                    line[0] = datetime.strptime(line[0], '%m/%d/%Y %H:%M')
                except:
                    line[0] = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')  #for HPDmobile

                # weighted average
                if idx != 0:
                    #x = np.random.uniform(0, math.pi, step)             #sinus
                    #x = np.random.uniform(-math.pi/2, math.pi/2, step)  #cos
                    x = np.random.uniform(0, 10, step)                   #linear
                    x1 = np.sort(x)

                    #w = [math.sin(i) for i in x1]     #sinus
                    #w = [math.cos(i) for i in x]      #cos
                    w = x1                             #linear

                    line_med.append(line[0])
                    line1 = sum([float(line_seq[i][1]) * w[i] for i in range(step)]) / sum(w)
                    line_med.append(str(float("{:.2f}".format(line1))))
                    line2 = sum([float(line_seq[i][2]) * w[i] for i in range(step)]) / sum(w)
                    line_med.append(str(float("{:.2f}".format(line2))))
                    if nr_sensors in [3, 4, 5]:
                        line3 = sum([float(line_seq[i][3]) * w[i] for i in range(step)]) / sum(w)
                        line_med.append(str(float("{:.2f}".format(line3))))
                    if nr_sensors in [4, 5]:
                       line4 = sum([float(line_seq[i][4]) * w[i] for i in range(step)]) / sum(w)
                       line_med.append(str(float("{:.2f}".format(line4))))
                    if nr_sensors == 5:
                        line5 = sum([float(line_seq[i][5]) * w[i] for i in range(step)]) / sum(w)
                        line_med.append(str(float("{:.2f}".format(line5))))
                    line_med.append(line[line_len - 1])
                else:
                    line_med.append(line[0])
                    line_med.append(line[1])
                    line_med.append(line[2])
                    if nr_sensors in [3, 4, 5]:
                        line_med.append(line[3])
                    if nr_sensors in [4, 5]:
                        line_med.append(line[4])
                    if nr_sensors == 5:
                        line_med.append(line[5])
                    line_med.append(line[line_len - 1])

                line_seq = []
                raw_data.append([i for i in line_med[0:line_len]])

        #prepare data, split on sequences
        idx = 0
        while idx < (row_count - max_sequence - 1):
            data_seq = {}
            data_seq[LABEL_OCC] = []
            data_seq[LABEL_SENS] = []

            #compute time differences
            for i in range(idx, idx + max_sequence - 1):
                diff = abs(raw_data[i][0] - raw_data[i + 1][0])

                if (diff.total_seconds() / 3600) > treshold:
                    break
            vector = raw_data[idx:i+2]
            if i < (idx + max_sequence - 2):
                idx = i + 1
            else:
                idx += 1
            if len(vector) < min_sequence:  #check for min sequence
                continue

            #append in data_new the values from sensors
            count_occ = [0, 0, 0, 0]

            for j, line in enumerate(vector):
                data_seq[LABEL_SENS].append([float(k) for k in line[1:(nr_sensors + 1)]])
                if j >= len(vector) - occ_length:       # looking at Occ class in a part of sequnce
                    count_occ[Occupancy[line[nr_sensors + 1]]] += 1

            #check occupancy
            type_occ = np.argmax(count_occ)
            data_seq[LABEL_OCC] = dict_occ[type_occ]

            if max(count_occ) == occ_length:
                data_seq[LABEL_TRANSITION] = 1
            else:
                data_seq[LABEL_TRANSITION] = 0

            data_seq[LABEL_LASTDATE] = str(line[0])
            data_seq[LABEL_LASTOCC] = Occupancy[line[nr_sensors+1]]
            data_seq["name"] = name
            data.append(data_seq)

    print("data_length " + name + ": "+ str(len(data)))
    write_data(data, "%s/complete_data" % (out_dir))
    return data

if __name__ == "__main__":
    name = "2019-12-09-14-RS14-H1_5sensors"
    seq_length = 60
    occ_length = 60
    nr_sensors = 5
    step = 2 #seconds
    out_dir = ("./data/%s_%ssec_s%d_o%d" % (name, step, seq_length, occ_length))

    if not os.path.exists("%s" %(out_dir)):
        os.makedirs("%s" % (out_dir))

    data = prepare_original_data(name, "./dataset/%s.csv" % (name), out_dir, seq_length, occ_length, step, nr_sensors)
