import random
import numpy as np
from data_io import write_data, read_data

def split_data(data, train_ratio, valid_ratio):
  """Splits data into train, validation and test according to ratio."""
  train_data = []
  valid_data = []
  test_data = []

  # Split data by occupancy
  dic_occ = {"empty": 0, "low": 0, "medium": 0, "high": 0}
  for idx, item in enumerate(data):
    for i in dic_occ:
      if item["occupancy"] == i:
        dic_occ[i] += 1
  print("After balancing")
  print(dic_occ)

  train_num_dic = {}
  valid_num_dic = {}
  for i in dic_occ:
    train_num_dic[i] = int(train_ratio * dic_occ[i])
    valid_num_dic[i] = int(valid_ratio * dic_occ[i])

  random.seed(30)
  random.shuffle(data)
  for idx, item in enumerate(data):
    for i in dic_occ:
      if item["occupancy"] == i:
        if train_num_dic[i] > 0:
          train_data.append(item)
          train_num_dic[i] -= 1
        elif valid_num_dic[i] > 0:
          valid_data.append(item)
          valid_num_dic[i] -= 1
        else:
          test_data.append(item)

  print("train_length:" + str(len(train_data)))
  print("test_length:" + str(len(test_data)))
  print("valid_length:" + str(len(valid_data)))

  return train_data, valid_data, test_data

#add random data if there are very big differences between the occupancy class in dataset
def random_data(data, l, h):
  vect_e = np.array([x for x in data if x["occupancy"] == "empty"])
  vect_l = np.array([x for x in data if x["occupancy"] == "low"])
  vect_m = np.array([x for x in data if x["occupancy"] == "medium"])
  vect_h = np.array([x for x in data if x["occupancy"] == "high"])

  length = min(len(vect_e), len(vect_l), len(vect_m), len(vect_h))

  if (length == 0):
    return data
  indecs_e = []
  length_e = int(np.random.uniform(length * l, length * h))
  indecs_e.append(np.random.randint(low=0, high=len(vect_e), size=min(length_e, len(vect_e)), dtype=int))

  indecs_l = []
  length_l = int(np.random.uniform(length * l , length * h))
  indecs_l.append(np.random.randint(low=0, high=len(vect_l), size=min(length_l, len(vect_l)), dtype=int))

  indecs_m = []
  length_m = int(np.random.uniform(length * l, length * h))
  indecs_m.append(np.random.randint(low=0, high=len(vect_m), size=min(length_m, len(vect_m)), dtype=int))

  indecs_h = []
  length_h = int(np.random.uniform(length * l, length * h))
  indecs_h.append(np.random.randint(low=0, high=len(vect_h), size=min(length_h, len(vect_h)), dtype=int))

  vect_e = vect_e[indecs_e]
  vect_l = vect_l[indecs_l]
  vect_m = vect_m[indecs_m]
  vect_h = vect_h[indecs_h]

  rand_data = list(np.concatenate((vect_e, vect_l, vect_m, vect_h), axis = 0))
  return rand_data

def split(name, l, h, seed, dir):
    np.random.seed(seed)

    print("%%%%%%%%%%%% " + name + " %%%%%%%%%%%%")
    data = read_data("%s/complete_data" %(dir))

    #count the sequences that are many type of occupancy
    test_trans_data = []
    for idx, item in enumerate(data):
      if item["transition"] == 0:
        test_trans_data.append(item)
    print("test_transition_length:" + str(len(test_trans_data)))

    #print before balancing data
    dic_occ = {"empty": 0, "low": 0, "medium": 0, "high": 0}
    for idx, item in enumerate(data):
      for i in dic_occ:
        if item["occupancy"] == i:
          dic_occ[i] += 1
    print("Before balancing")
    print(dic_occ)
    rand_data = random_data(data, l, h)

    train_data, valid_data, test_data = split_data(rand_data, 0.6, 0.2)

    write_data(train_data, ("%s" %(dir)) + "/train")
    write_data(valid_data, ("%s" %(dir)) + "/valid")
    write_data(test_data, ("%s" %(dir)) + "/test")
    write_data(test_trans_data, ("%s" %(dir)) + "/test_transition")

if __name__ == "__main__":
  seed = 10
  l = 4.0
  h = 8.0
  step = 2
  seq_length = 60
  occ_length = 60
  name = "2019-12-09-14-RS14-H1_5sensors"
  in_dir = ("./data/%s_%ssec_s%d_o%d" % (name, step, seq_length, occ_length))


  split("home", l, h, seed, dir)