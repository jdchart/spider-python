import json

def writeJson(data, path):
    with open(path, 'w', encoding='utf-8') as f:
        json.dump(data, f, ensure_ascii=False, indent=4)

def readJson(path):
    with open(path, 'r') as f:
        return json.load(f)
    
def rescale(val, oldMin, oldMax, a, b):
    return a + (((val - oldMin) * (b - a)) / (oldMax - oldMin))