import json

# Write data to file
def write_data(data_to_write, path):
   with open(path, "w") as f:
    for idx, item in enumerate(data_to_write):
      dic = json.dumps(item, ensure_ascii=False)
      f.write(dic)
      f.write("\n")

# Read data
def read_data(path):
  data = []
  with open(path, "r") as f:
    lines = f.readlines()
    for idx, line in enumerate(lines):
      dic = json.loads(line)
      data.append(dic)
  print("data_length:" + str(len(data)))
  return data