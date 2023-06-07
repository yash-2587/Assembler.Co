import sys

MAX_REG = 65535
MAX_FLOAT = 252


memAddress = dict()


class registers:

    def inside(own):
        own.regs = {"000": 0, "001": 0, "010": 0, "011": 0,
                     "100": 0, "101": 0, "110": 0, "111": "0"*16, "PC": 0}

    def clearFlag(own):
        own.regs["111"] = "0"*16

    def setOverflow(own):
        own.regs["111"] = "0"*12 + "1" + "000"

    def setLess(own):
        own.regs["111"] = "0"*13 + "1" + "00"

    def setGreater(own):
        own.regs["111"] = "0"*14 + "1" + "0"

    def setEqual(own):
        own.regs["111"] = "0"*15 + "1"

    def convBin8(own, num):
        binNum = bin(num)[2:]
        return "0"*(8-len(binNum)) + binNum

    def convBin16(own, num):
        binNum = bin(num)[2:]
        return "0"*(16-len(binNum)) + binNum

    def __repr__(own) -> str:
        return "{} {} {} {} {} {} {} {} {}".format(own.convBin8(own.regs["PC"]), own.convBin16(own.regs["000"]), 
        own.convBin16(own.regs["001"]), own.convBin16(own.regs["010"]),
        own.convBin16(own.regs["011"]), own.convBin16(own.regs["100"]), 
        own.convBin16(own.regs["101"]), own.convBin16(own.regs["110"]), own.regs["111"])


class operation:
    def inside(own, regs: registers) -> None:
        # operation of each opcode
        own.opcodes = {"10000": own.add, "10001": own.sub,  "10010": own.mov1,  "10011": own.mov2,  "10100": own.ld,  "10101": own.st,  "10110": own.mul,  "10111": own.div,  "11000": own.rs,  "11001": own.ls, "11010": own.xor,
                        "11011": own.orOps,  "11100": own.andOps,  "11101": own.notOps,  "11110": own.cmp,  "11111": own.jmp,  "01100": own.jlt,  "01101": own.jgt,  "01111": own.je,  "01010": own.hlt, "00000": own.addf, "00001": own.subf, "00010": own.movf}

        own.regsObj = regs
        own.regs = regs.regs

def floatInt(own, numeric):
    whole, dec = str(numeric).split(".")

    whole = int(whole)
    dec = float("0." + dec)

    binRepr = bin(whole)[2:] + "."

    for _ in range(7):
        whole, dec = str(dec * 2).split(".")
        binRepr += whole
        dec = float("0." + dec)

    binRepr = binRepr.rstrip("0")  # Remove trailing zeros

    pt = binRepr.find(".")

    exp = pt - 1

    binRepr = "".join(binRepr.split("."))
    mantissa = binRepr[1:6]

    num = "0" * (3 - len(bin(exp)[2:])) + bin(exp)[2:]
    num += mantissa + (5 - len(mantissa)) * "0"

    return int(num, 2)


    def binFloat(own, numeric):
        if len(numeric) < 8:
            num = "0" * (8 - len(numeric)) + numeric
        else:
            num = numeric[-8:]

        exp = int(num[:3], 2)
        whole = "1" + num[3:3+exp]
        whole = int(whole, 2)

        dec = 0
        for i in range(5 - exp):
            dec += 2**(-i-1) if num[3+i+exp] == "1" else 0

        return float(whole + dec)
#function

    def addf(own, instruction):
        # removing filler bits
        instruction = instruction[2:]

        # Clearing the flag
        own.regsObj.clearFlag()

        reg3 = instruction[6:]
        own.regs[reg3] = own.floatInt(own.binFloat(bin(own.regs[instruction[:3]])[
                                        2:]) + own.binFloat(bin(own.regs[instruction[3:6]])[2:]))

        # checking for overflow
        if own.regs[reg3] > MAX_FLOAT:
            own.regsObj.setOverflow()

            own.regs[reg3] %= (MAX_FLOAT+1)

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def subf(own, instruction):
        # removing filler bits
        instruction = instruction[2:]

        # Clearing the flag
        own.regsObj.clearFlag()

        reg3 = instruction[6:]

        # checking for overflow
        if own.binFloat(bin(own.regs[instruction[:3]])[2:]) - own.binFloat(bin(own.regs[instruction[3:6]])[2:]) < 1:
            own.regs[reg3] = 0
            own.regsObj.setOverflow()
        else:
            own.regs[reg3] = own.floatInt(own.binFloat(bin(own.regs[instruction[:3]])[
                2:]) - own.binFloat(bin(own.regs[instruction[3:6]])[2:]))

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def movf(own, instruction):
        # Clearing the flag
        own.regsObj.clearFlag()

        own.regs[instruction[:3]] = own.floatInt(own.binFloat(instruction[3:]))

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def add(own, instruction):
        # removing filler bits
        instruction = instruction[2:]

        # Clearing the flag
        own.regsObj.clearFlag()

        # Doing the operation
        reg3 = instruction[6:]
        own.regs[reg3] = own.regs[instruction[:3]] + \
            own.regs[instruction[3:6]]

        # checking for overflow
        if own.regs[reg3] > MAX_REG:
            own.regsObj.setOverflow()

            own.regs[reg3] %= (MAX_REG+1)

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def sub(own, instruction):
        # removing filler bits
        instruction = instruction[2:]

        # Clearing the flag
        own.regsObj.clearFlag()

        # Doing the operation
        reg3 = instruction[6:]
        own.regs[reg3] = own.regs[instruction[:3]] - \
            own.regs[instruction[3:6]]

        # checking for overflow
        if own.regs[reg3] < 0:
            own.regs[reg3] = 0
            own.regsObj.setOverflow()

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def mov1(own, instruction):
        # Clearing the flag
        own.regsObj.clearFlag()

        own.regs[instruction[:3]] = int(instruction[3:], 2)

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def mov2(own, instruction):
        # removing filler bits
        instruction = instruction[5:]

        if instruction[:3] != "111":
            own.regs[instruction[3:]] = own.regs[instruction[:3]]
        else:
            own.regs[instruction[3:]] = int(own.regs[instruction[:3]], 2)

        # Clearing the flag
        own.regsObj.clearFlag()

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def ld(own, instruction):
        # Clearing the flag
        own.regsObj.clearFlag()

        if int(instruction[3:], 2) in memAddress:
            own.regs[instruction[:3]] = memAddress[int(instruction[3:], 2)]
        else:
            own.regs[instruction[:3]] = 0
            memAddress[int(instruction[3:], 2)] = 0

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def st(own, instruction):
        # Clearing the flag
        own.regsObj.clearFlag()

        memAddress[int(instruction[3:], 2)] = own.regs[instruction[:3]]

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def mul(own, instruction):
        # removing filler bits
        instruction = instruction[2:]

        # Clearing the flag
        own.regsObj.clearFlag()

        # Doing the operation
        reg3 = instruction[6:]
        own.regs[reg3] = own.regs[instruction[:3]] * \
            own.regs[instruction[3:6]]

        # checking for overflow
        if own.regs[reg3] > MAX_REG:
            own.regsObj.setOverflow()

            own.regs[reg3] %= (MAX_REG+1)

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def div(own, instruction):
        # removing filler bits
        instruction = instruction[5:]

        # Clearing the flag
        own.regsObj.clearFlag()

        # quotient
        own.regs["000"] = own.regs[instruction[:3]] // own.regs[instruction[3:]]
        # remainder
        own.regs["001"] = own.regs[instruction[:3]] % own.regs[instruction[3:]]

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def rs(own, instruction):
        # Clearing the flag
        own.regsObj.clearFlag()

        own.regs[instruction[:3]] = own.regs[instruction[:3]] >> int(instruction[3:], 2)

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def ls(own, instruction):
        # Clearing the flag
        own.regsObj.clearFlag()

        own.regs[instruction[:3]] = own.regs[instruction[:3]] << int(instruction[3:], 2)

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def xor(own, instruction):
        # removing filler bits
        instruction = instruction[2:]

        # Clearing the flag
        own.regsObj.clearFlag()

        # Doing the operation
        reg3 = instruction[6:]
        own.regs[reg3] = own.regs[instruction[:3]] ^ \
            own.regs[instruction[3:6]]

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def orOps(own, instruction):
        # removing filler bits
        instruction = instruction[2:]

        # Clearing the flag
        own.regsObj.clearFlag()

        # Doing the operation
        reg3 = instruction[6:]
        own.regs[reg3] = own.regs[instruction[:3]] | \
            own.regs[instruction[3:6]]

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def andOps(own, instruction):
        # removing filler bits
        instruction = instruction[2:]

        # Clearing the flag
        own.regsObj.clearFlag()

        # Doing the operation
        reg3 = instruction[6:]
        own.regs[reg3] = own.regs[instruction[:3]] & \
            own.regs[instruction[3:6]]

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def notOps(own, instruction):
        # removing filler bits
        instruction = instruction[5:]

        # Clearing the flag
        own.regsObj.clearFlag()

        # Doing the operation
        num = own.regsObj.convBin16(own.regs[instruction[:3]])

        invert = ["1" if i == "0" else "0" for i in num]
        own.regs[instruction[3:]] = int("".join(invert), 2)

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def cmp(own, instruction):
        # removing filler bits
        instruction = instruction[5:]

        # Setting FLAGS
        if own.regs[instruction[:3]] == own.regs[instruction[3:]]:
            own.regsObj.setEqual()
        elif own.regs[instruction[:3]] > own.regs[instruction[3:]]:
            own.regsObj.setGreater()
        elif own.regs[instruction[:3]] < own.regs[instruction[3:]]:
            own.regsObj.setLess()

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] += 1

    def jmp(own, instruction):
        # removing filler bits
        instruction = instruction[3:]

        # Clearing the flag
        own.regsObj.clearFlag()

        # printing the object
        print(own.regsObj)

        # Setting the program counter
        own.regs["PC"] = int(instruction, 2)

    def jlt(own, instruction):
        # removing filler bits
        instruction = instruction[3:]

        FLAGS = own.regs["111"]

        # Clearing the flag
        own.regsObj.clearFlag()

        # printing the object
        print(own.regsObj)

        # Checking flag
        # Setting the program counter
        if FLAGS[-3] == "1":
            own.regs["PC"] = int(instruction, 2)
        else:
            own.regs["PC"] += 1

    def jgt(own, instruction):
        # removing filler bits
        instruction = instruction[3:]

        FLAGS = own.regs["111"]

        # Clearing the flag
        own.regsObj.clearFlag()

        # printing the object
        print(own.regsObj)

        # Checking flag
        # Setting the program counter
        if FLAGS[-2] == "1":
            own.regs["PC"] = int(instruction, 2)
        else:
            own.regs["PC"] += 1

    def je(own, instruction):
        # removing filler bits
        instruction = instruction[3:]

        FLAGS = own.regs["111"]

        # Clearing the flag
        own.regsObj.clearFlag()

        # printing the object
        print(own.regsObj)

        # Checking flag
        # Setting the program counter
        if FLAGS[-1] == "1":
            own.regs["PC"] = int(instruction, 2)
        else:
            own.regs["PC"] += 1

    def hlt(own, instruction):
        global lines
