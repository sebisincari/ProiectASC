from operator import index
from libraries.registers import registers

def creareRegFile(file_path='register_file.txt'):
    global register_file
    global reg_file_init

    with open(file_path, 'r') as file:
        for line in file:
            key, value = line.strip().split()
            register_file[key] = int(value)
            reg_file_init[key] = int(value)
    #print(reg_file_init)


def updateRegFile(output_file='register_file.txt'):
    with open(output_file, 'w') as file:
        for key, value in register_file.items():
            file.write(f"{key} {value}\n")


def decode():
    global index
    global cod_bin
    # print(len(cod_bin))
    # lenght = len(cod_bin)
    #print(index)
    #print(register_file['cml'])
    #print(len(cod_bin))
    while index <= register_file['cml'] - 1:
        
        instructiune = ""
        
        index += 8
        lun = 0
        for i in range (8):
            if cod_bin[index] == '1':
               lun += 2 ** i 
            print(lun)
            index -= 1
        index += 8
        
        #print(lun)
        while instructiune not in functii:
            index += 1
            instructiune += cod_bin[index]
            # print(index)
        print(instructiune)
        # print(index)
        functii[instructiune]()
        index += (8 - lun)
        # apel functie gasita


def readBin():
    global cod_bin
    with open('ram.bin', 'rb') as fisier:
        cod_bin = fisier.read()

    cod_bin = ''.join(format(byte, '08b') for byte in cod_bin)
    # print(cod_bin[len()])
    decode()


def decReg():
    global index
    global cod_bin
    gasit = 0
    binRegCurent = ""
    cheieRegCurent = ""
    
    index += 8
    lun = 0
    for i in range (8):
        if cod_bin[index] == '1':
            lun += 2 ** i 
        index -= 1
    index += 8
        
    while not gasit:
        index += 1
        binRegCurent += cod_bin[index]
        for numeReg, binReg in registers.items():
            if binReg == binRegCurent:
                cheieRegCurent = numeReg
                gasit = 1
                break
    index += (8 - lun)
    # aici are cheia reg
    return cheieRegCurent


def readRegVal(cheieReg):
    for cheie, val in register_file.items():
        if cheieReg == cheie:
            return val


def writeRegVal(cheieReg, valReg):
    register_file[cheieReg] = valReg


def decIntVal():
    global index
    global cod_bin
    num = 0
    aux = 1
    # print(index)
    index += 32
    for i in range(31):
        if index < register_file['cml'] - 1:
            if cod_bin[index] == '1':
                num += aux
        aux *= 2
        index -= 1
    # print(index)
    if cod_bin[index] == '1':
        num -= 2**32
    index -= 1
    index += 32
    # print("  " + str(num))
    return num


def decDoubleValMem(index, memory):
    num = 0
    aux = 1
    # print(index)
    index +=63
    for i in range(64):
        if memory[index] == '1':
            num += aux
        aux *= 2
        index -= 1
    # print(index)
    # print("  " + str(num))
    return num


def decIndexJmp():
    global index
    global cod_bin
    num = 0
    aux = 1
    # print(index)
    index += 16
    for i in range(16):
        if index < register_file['cml'] - 1:
            if cod_bin[index] == '1':
                num += aux
        aux *= 2
        index -= 1
    # print(index)
    index += 16
    # print("  " + str(num))
    return num
 

def readDouble(indexStart, memory):
    strbytes = ""
    # print(indexStart)
    # print(len(cod_bin))
    for i in range(64):
     
        if indexStart <= len(memory) - 1:
            strbytes += memory[indexStart]
            indexStart += 1
    return strbytes


def readByte(indexStart, memory):
    strbyte = ""
    # print(indexStart)
    # print(len(cod_bin))
    for i in range(8):
     
        if indexStart <= len(memory) - 1:
            strbyte += memory[indexStart]
            indexStart += 1
    return strbyte


def intToByte(val):
    byte = ""
    for i in range(8):
        byte = ''.join([str(val & 1),byte])
        val = (val >> 1)
    #print(byte)
    return byte


def intToDouble(val):
    bytes = ""
    for i in range(64):
        bytes = ''.join([str(val & 1),bytes])
        val = (val >> 1)
    #print(bytes)
    return bytes


def decFct():
    global index
    global cod_bin
    global functions
    index+=1
    binFct=str(cod_bin[index])
    index+=1
    binFct=binFct+str(cod_bin[index])
    return binFct



def addi():
    global cod_bin
    regD = decReg()
    reg1 = decReg()
    val = decIntVal()
    vReg1 = readRegVal(reg1)
    vRegD = vReg1 + val
    writeRegVal(regD, vRegD)


def j():
    global cod_bin
    global index
    # print(decIndexJmp(cod_bin))
    index = decIndexJmp() - 1


def li():
    global cod_bin
    regD = decReg()
    newVal = decIntVal()
    writeRegVal(regD, newVal)


def ret():
    global index
    global cod_bin
    index = register_file['cml'] + 1


def add():
    global cod_bin
    regD = decReg()
    reg1 = decReg()
    reg2 = decReg()
    vReg1 = readRegVal(reg1)
    vReg2 = readRegVal(reg2)
    vRegD = vReg1 + vReg2
    writeRegVal(regD, vRegD)


def bge():
    global cod_bin
    global index
    reg1 = decReg()
    reg2 = decReg()
    vReg1 = readRegVal(reg1)
    vReg2 = readRegVal(reg2)
    label = decIndexJmp() 
    if vReg1 >= vReg2:
        index=label-1
    


def beqz():
    global cod_bin
    global index
    regInterogat = decReg()
    indexSalt = decIndexJmp()
    regVal = readRegVal(regInterogat)
    # print(indexSalt)
    # print(regVal)
    if regVal == 0:
        index = indexSalt - 1


def mv():
    global cod_bin
    regDest = decReg()
    regSursa = decReg()
    val = readRegVal(regSursa)
    # print(regDest)
    # print(val)
    writeRegVal(regDest, val)


def sd():
    global cod_bin
    
    regSursa = decReg()
    offset = decIntVal()
    regDest = decReg()
    valSursa = readRegVal(regSursa)
    valDest = readRegVal(regDest)
    strByte = str(intToDouble(valSursa))
    # print (valSursa)
    indexByte = (offset + valDest) * 8
    memory = str(cod_bin[register_file['cml']:])
    memory_start = str(memory[:indexByte])
    memory_end = str(memory[indexByte + 64:])
    #print(indexByte)
    #print(strByte)
    #print(memory_start + strByte)

    memory=memory_start+strByte+memory_end

    cod_bin=cod_bin[:register_file['cml']]+memory
 
    #print (memory_start + memory_end)
    

    with open('ram.bin', 'wb') as file:
        file.write(bytes(int(cod_bin[i:i+8], 2) for i in range(0, len(cod_bin), 8)))
    #print("sbb")


def fmvs():
    return 0


def lb():
    global cod_bin
    # global strByte
    
    regDest = decReg()
    offset = decIntVal()
    regSursa = decReg()
    vRegSursa = readRegVal(regSursa)
    memory = cod_bin[register_file['cml']:]
    # a0-t1*8
    # strByte = ""
    indexByte = (offset + vRegSursa) * 8
    #print(indexByte)
    # print(int(vRegSursa))
    # if indexByte < len(cod_bin):
    strByte = readByte(indexByte, memory)
    pow2 = 1
    num = 0
    # print(strByte)
    # strByte = strByte[::-1]
    #print(strByte)
    for i in range(7, -1, -1):
        num += pow2 * int(strByte[i])
        pow2 *= 2
    # print(num)
    writeRegVal(regDest, num)


def sb():
    #print("sb")
    # global strByte
    global cod_bin
    
    regSursa = decReg()
    offset = decIntVal()
    regDest = decReg()
    valSursa = readRegVal(regSursa)
    valDest = readRegVal(regDest)
    strByte = str(intToByte(valSursa))
    # print (valSursa)
    indexByte = (offset + valDest) * 8
    memory = str(cod_bin[register_file['cml']:])
    memory_start = str(memory[:indexByte])
    memory_end = str(memory[indexByte + 8:])
    #print(indexByte)
    #print(strByte)
    #print(memory_start + strByte)

    memory=memory_start+strByte+memory_end

    cod_bin=cod_bin[:register_file['cml']]+memory
 
    #print (memory_start + memory_end)
    
    with open('ram.bin', 'wb') as file:
        file.write(bytes(int(cod_bin[i:i+8], 2) for i in range(0, len(cod_bin), 8)))
    #print("sbb")

def strlen():
    global cod_bin
    memory = str(cod_bin[register_file['cml']:])
    vfStiva = reg_file_init['sp']
    vfStiva *= 8
    bazaStiva = register_file['sp']
    bazaStiva *= 8
    startstr = readDouble(vfStiva-64,memory) 
    startstr = decDoubleValMem(0,startstr)
    ibyte = startstr
    byte = readByte(ibyte,memory)
    knt = 1
    while byte != "00000000":
        ibyte += 8
        byte = readByte(ibyte,memory)
        knt +=1
    writeRegVal("a0",knt) 


def call():
    binFct=decFct()
    if binFct == "00":
        strlen()



def ld():
    global cod_bin
    # global strByte
    
    regDest = decReg()
    offset = decIntVal()
    regSursa = decReg()
    vRegSursa = readRegVal(regSursa)
    memory = cod_bin[register_file['cml']:]
    # a0-t1*8
    # strByte = ""
    indexByte = (offset + vRegSursa) * 8
    #print(indexByte)
    # print(int(vRegSursa))
    # if indexByte < len(cod_bin):
    strByte = readByte(indexByte, memory)
    print(strByte)
    pow2 = 1
    num = 0
    # print(strByte)
    # strByte = strByte[::-1]
    #print(strByte)
    for i in range(63, -1, -1):
        num += pow2 * int(strByte[i])
        pow2 *= 2
    # print(num)
    writeRegVal(regDest, num)


def lw():
    return 0


def fld():
    return 0


def slli():
    return 0


def fsw():
    return 0


def la():
    return 0


def srai():
    regDest=decReg()
    regSursa=decReg()
    vShift=decIntVal()
    vRegSursa=int(readRegVal(regSursa))
    vRegDest=vRegSursa>>vShift
    writeRegVal(regDest, vRegDest)



def ble():
    global cod_bin
    global index
    reg1 = decReg()
    reg2 = decReg()
    vReg1 = readRegVal(reg1)
    vReg2 = readRegVal(reg2)
    label = decIndexJmp() 
    if vReg1 <= vReg2:
        index=label-1


def fsubd():
    return 0


def fmuld():
    return 0


def fgts():
    return 0


def flts():
    return 0


def flw():
    return 0


def sub():
    global cod_bin
    regD = decReg()
    reg1 = decReg()
    reg2 = decReg()
    vReg1 = readRegVal(reg1)
    vReg2 = readRegVal(reg2)
    vRegD = vReg1 - vReg2
    writeRegVal(regD, vRegD)


def bnez():
    global cod_bin
    global index
    regInterogat = decReg()
    indexSalt = decIndexJmp()
    regVal = readRegVal(regInterogat)
    # print(indexSalt)
    # print(regVal)
    if regVal != 0:
        index = indexSalt - 1


def faddd():
    return 0


def fsqrtd():
    return 0


def bgt():
    global cod_bin
    global index
    reg1 = decReg()
    reg2 = decReg()
    vReg1 = readRegVal(reg1)
    vReg2 = readRegVal(reg2)
    label = decIndexJmp() 
    if vReg1 > vReg2:
        index=label-1


def fmvsx():
    return 0


def fmuls():
    return 0


def fadds():
    return 0


functii = {'111': addi, '1101': j, '1100': li, '1011': ret, '1000': add, '0100': bge, '0000': beqz, '10011': mv,
           '10010': sd, '10101': fmvs, '01011': lb, '01010': sb, '01101': call, '01100': ld, '01111': lw, '00011': fld,
           '101001': slli, '101000': fsw, '011101': la, '011100': srai, '001101': ble, '001100': fsubd, '001111': fmuld,
           '001110': fgts, '001001': flts, '001000': flw, '0001001': sub, '0001000': bnez, '0001011': faddd,
           '0001010': fsqrtd, '0010101': bgt, '0010100': fmvsx, '0010111': fmuls, '0010110': fadds}
functions = {
    "strlen": "00",
    "printf": "01",
    "scanf": "10",
    "cfunc": "11"
}
register_file = {}
reg_file_init = {}
index = -1
cod_bin = ""
# strByte = ""
creareRegFile()
readBin()
#register_file['a0'] = 1
updateRegFile()

#print(register_file['a0'])
