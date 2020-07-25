import json
import itertools
import random
import sys
import json

def read_settings(filename):
    with open(filename) as json_file:
        data = json.load(json_file)
        return data

def generate_dic(name, choice):
    dic = {}
    dic["name"] = name
    dic["choice"] = choice
    return dic

def generate_sample(settings):
    res = [generate_dic(setting["name"], random.choice(setting["choices"])) for setting in settings]
    return {
        "average": sum(value["choice"]["weight"] for value in res)/len(settings) if len(settings)>0 else -1,
        "res": res
    }

def generate(settings, interval=None):
    settings = list(filter(lambda x: x["choices"], settings))
    result = [generate_sample(settings) for _ in range(1000)]

    if (not interval):
        return random.choice(result)

    right = list(filter(lambda a: a["average"] >= interval[0] and a["average"] <= interval[1], result))
    wrong = list(filter(lambda a: a["average"] < interval[0] or a["average"] > interval[1], result))

    if (not right):
        raise Exception("This list don't permit to choose a sample that verify the rule")

    if (random.randint(0, 99) == 0):
        return random.choice(wrong)
    else:
        return random.choice(right)

# settings = read_settings()

# print(generate(settings))



if (len(sys.argv) < 2):
    f2 = open("error_log.txt", "w")
    sys.stdout = f2
    print("Error file not specified")
    f2.close()
else:
    if len(sys.argv) > 2:
        middle = int(sys.argv[2])
        interval = [middle - 1 if middle > 1 else 0, middle + 1 if middle < 10 else 0]
    else:
        interval = [4, 6]
    try: 
        res = json.dumps(generate(read_settings(sys.argv[1]), interval)["res"], indent=1)
    except:
        res = json.dumps(generate(read_settings(sys.argv[1]))["res"], indent=1)
    print(res)





