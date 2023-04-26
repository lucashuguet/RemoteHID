import json


def printFunc(keymap):
    with open("../keys/" + keymap + ".json", "r") as f:
        data = json.load(f)

        return data["functions"]
    return None


def getbytes(char_key, keymap):
    output = []
    
    with open("../keys/" + keymap + ".json", "r") as f:
        data = json.load(f)

        chars = data["chars"]

        for char in chars:
            if char == char_key:
                return chars[char]

        return None


def getfuncbytes(func_key, keymap):
    output = []
    
    with open("../keys/" + keymap + ".json", "r") as f:
        data = json.load(f)

        functions = data["functions"]

        for func in functions:
            if func == func_key:
               return functions[func]

    return None
 

def getcompbytes(char, keymap):
    output = []
    
    with open("../keys/" + keymap + ".json", "r") as f:
        data = json.load(f)

        composition = data["composition"]

        for comp in composition:
            if comp == char:
                for press in composition[comp]:
                    tmp = []
                    if len(press) == 1:
                        tmp.append("None")
                    else:
                        tmp.append(press[0])

                    key = press[-1]
                    if len(key) == 1:
                        bytecode = getbytes(key, keymap)
                    else:
                        bytecode = getfuncbytes(key, keymap)

                    if bytecode:
                        ashex = bytecode[2:]
                        tmp.append(bytearray.fromhex(ashex))
                        output.append(tmp)
                    else:
                        return None

    if output:
        return output
    else:
        return None
