import json

def decode_JSON(JSON):

    JSON_dict = json.loads(JSON)
    return JSON_dict

def code_JSON(JSON):
    JSON = json.dumps(JSON)
    return JSON