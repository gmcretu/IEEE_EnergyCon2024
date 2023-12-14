import csv

dict_occ = {'0': "E", '1': "L", '2': "M", '3': "H", '4': "H", '5': "H"}

def get_csv(nr_sensors, list_nameH, outDir):
    total_length = 0
    open(outDir, 'w').close()
    last_line = 0
    for nameH in list_nameH:
        nameH_split = nameH.split("_")
        fileEnv = "dataset_HPDmobile/" + nameH_split[-1] + "_ENVIRONMENTAL/" + nameH_split[-1] + "_" +  nameH_split[-2] + "_ENV/" + \
                    nameH + "_env.csv"

        fileOcc = "dataset_HPDmobile/" + nameH_split[-1] + "_GROUNDTRUTH/" + nameH_split[0] + "_" + nameH_split[2] + "_groundtruth.csv"

        index_init = 0
        with open(fileEnv, "r") as f:
            lines = csv.reader(f)
            raw_data=[]      #brut date
            for idx, line in enumerate(lines):
                if idx != 0:
                    #line[0] = datetime.strptime(line[0], '%Y-%m-%d %H:%M:%S')
                    if '' in line:
                        if last_line != 0:
                            line = last_line
                        else:
                            index_init = idx
                            continue
                    if nr_sensors == 3:
                        raw_data.append([line[0], line[2], line[4], line[6]])
                    elif nr_sensors == 4:
                        raw_data.append([line[0], line[2], line[3], line[4], line[6]])
                    elif nr_sensors == 5:
                        raw_data.append([line[0], line[2], line[3], line[4], line[6], line[7]])
                    last_line = line

        index_end = idx
        with open(fileOcc, "r") as f:
            lines = csv.reader(f)
            for idx, line in enumerate(lines):
                if idx < index_end and idx > index_init:
                    if idx != 0:
                        line[2] = dict_occ[line[2]]
                        raw_data[idx-index_init-1].append(line[2])

        print("data_length " + nameH + ": "+ str(len(raw_data)))
        total_length = total_length + len(raw_data)
        fileOut = open(outDir, 'a', newline='')
        with fileOut:
            write = csv.writer(fileOut)
            write.writerows(raw_data)
        fileOut.close()

    print("data_length " + ": " + str(total_length))

if __name__ == "__main__":

    nr_sensors = 5

    get_csv(nr_sensors,
            ["2019-12-01_RS1_H1", "2019-12-02_RS1_H1", "2019-12-03_RS1_H1", "2019-12-04_RS1_H1", "2019-12-05_RS1_H1",
             "2019-12-01_RS2_H1", "2019-12-02_RS2_H1", "2019-12-03_RS2_H1", "2019-12-04_RS2_H1", "2019-12-05_RS2_H1",
             "2019-12-01_RS3_H1", "2019-12-02_RS3_H1", "2019-12-03_RS3_H1", "2019-12-04_RS3_H1", "2019-12-05_RS3_H1",],
             "dataset/2019-12-16-21-RS123-H1_5sensors.csv")