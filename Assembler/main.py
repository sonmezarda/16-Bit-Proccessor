import json

labels={}
with open('instructions.json', 'r') as inf:
    ins = json.loads(inf.read())

def findLabels(file_name='assembly.txt'):
    with open(file_name, 'r') as af:
        for i, line in enumerate(af.readlines()):
            if line.split(' ')[0][-1] == ':':
                labels[line.split(' ')[0][:-1]] = i

def getInstDic(ins_name):
    ins_name = ins_name.upper()
    return ins[ins_name]    

defaults = getInstDic("defaults")

def getInstVal(ins_dic:dict, val_name):
    val = ins_dic.get(val_name)
    if(val == None):
        val = defaults[val_name]
    return val

def getInstCode(ins_dic):
    code = getInstVal(ins_dic,'mb') + getInstVal(ins_dic,'md') + getInstVal(ins_dic,'mi') + getInstVal(ins_dic,'sf')
    code += getInstVal(ins_dic, 'ma')
    code += getInstVal(ins_dic,'condition')
    code += getInstVal(ins_dic, "re")
    code += getInstVal(ins_dic,'empty')
    code += getInstVal(ins_dic,'opcode')
    code += getInstVal(ins_dic,'fa')
    code += getInstVal(ins_dic,'ds')
    code += getInstVal(ins_dic,'as')
    code += getInstVal(ins_dic,'bs')
    return code

# ADD r1, r2, r3
def setByFormat(code):
    inst = code.split(' ')[0]
    params = code.replace(inst, '').split(',')

    ins_dic = getInstDic(inst)
    if '#' in code:
        ins_dic['mb']='1'
    else:
        ins_dic['mb']='0'

    iformat = ins_dic.get('format')
    format_params = iformat.split(',')
    for i, param in enumerate(format_params):
        key = param.split(':')[0]
        format_val = param.split(':')[1]

        val = params[i].strip()
        if 'r' in format_val and val[0] == 'r':
            ins_dic[key] = getAsBin(val)
            
        elif '4#' in format_val and val[0] == '#':
            bi = getAsBin(val, bit_count=16)
            ins_dic['fa'] = bi[:4]
            ins_dic['ds'] = bi[4:8]
            ins_dic['as'] = bi[8:12]
            ins_dic['bs'] = bi[12:]
        
        elif '[r]' in format_val and val[0] == '[':
            reg = val.replace('[','').replace(']','')
            bi = getAsBin(reg, bit_count=16)
            ins_dic['fa'] = bi[:4]
            ins_dic['ds'] = bi[4:8]
            ins_dic['as'] = bi[8:12]
            ins_dic['bs'] = bi[12:]
        elif '#' in format_val and val[0] == '#':
            ins_dic['mb'] = '1'
            bi = getAsBin(val, bit_count=8)
            ins_dic['fa'] = bi[0:4]
            ins_dic[key] = bi[4:]
        elif '=' == 'X' : #=
            pass
        elif 'lbl' in format_val:
            bi = getAsBin(labels[val], bit_count=16)
            ins_dic['fa'] = bi[:4]
            ins_dic['ds'] = bi[4:8]
            ins_dic['as'] = bi[8:12]
            ins_dic['bs'] = bi[12:]
        else:
            getAsBin(val, bit_count=len(defaults[key]))

    return getInstCode(ins_dic)


def decimalToBinary(n):
    return bin(n).replace("0b", "")

def setBinaryLen(val, tlen, is_negative=False):
    dif = tlen-len(val)
    if is_negative:
        val = "1"*dif + val
    else:
        val = "0"*dif + val
    return val

def setHexLen(val, tlen, is_negative=False):
    dif = tlen-len(val)
    val = val[2:]
    if is_negative:
        val = "F"*dif + val
    else:
        val = "0"*dif + val
    return '0x'+val

def getAsBin(data, bit_count=4):
    data = str(data)
    data = data.lower()
    if data[0] == 'r':
        data = data[1:]
    if data[0] == '#':
        data = data[1:]

    if data[:2] == '0x':
        num = int(data, base=16)
    else:
        num = int(data)
    dec = decimalToBinary(num)
    bi = setBinaryLen(dec, bit_count)
    return bi 

def convertFile(file_name="assembly.txt", dest_file="lasthex"):
    hf = open(dest_file, 'w')
    hf.write('v2.0 raw\n')
    findLabels(file_name)
    with open(file_name, 'r') as af:
        for i, line in enumerate(af.readlines()):
            if line.split(' ')[0][-1] == ':':
                line = line.split(' ')[1:]
                line = " ".join(line)
            
            iCode = setByFormat(line)
            hCode = setHexLen(hex(int(iCode, 2)),10)
            hf.write(hCode[2:]+'\n')
                


if __name__ == "__main__":
    #_ = setByFormat('STR r0, #0xFFFC')
    #print(_)
    convertFile()
    
