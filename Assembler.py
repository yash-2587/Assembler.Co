import sys 
listu=[]
reg_dic = {"R0":'000',"R1":'001',"R2":'010',"R3":'011',"R4":'100',"R5":'101',"R6":'110'}
opcode_dic = {"add":'00000',"sub":'00001', "mov" : '00010', "movi":'00011', "ld":'00100', "st":'00101', "mul":'00110', "div":'00111', "rs":'01000', "ls":'01001', "xor":'01010', "or":'01011', "and":'01100', "not":'01101', "cmp":'01110', "jmp":'01111', "jlt": '11100', "jgt":'11101', "je":'11111', "hlt":'11010' }
global wrong
wrong=""
line=-1

#function for binary conversion
def convert_decimal_to_binary(num, num_bits):
    binary_str = bin(num)[2:].zfill(num_bits)
    return binary_str



def type_A(index, string):
    # Instruction type A: ADD, SUB, MOV, AND, OR, XOR
    # Set the first two bits to 00
    string += '00'
    # Convert register names to binary and add them to the string
    string = string + reg_dic[index[1]] + reg_dic[index[2]] + reg_dic[index[3]]
    return string

def type_B(index, string):
    # Instruction type B: immediate instructions
    if index[2][0] != '$':
        error = "Syntax Error: Invalid immediate value format, line with error is : " + str(line)
        return ""
    
    num = index[2][1:]  # Remove the dollar sign ('$') from the immediate value
    
    if not num.isdigit():
        error = "Syntax Error: Invalid immediate value format, line with error is : " + str(line)
        return ""
    
    immediate = int(num)
    
    if immediate < 0 or immediate > 127:
        error = "Syntax Error: Immediate value out of range, line with error is : " + str(line)
        return ""
    
    binary_str = format(immediate, '07b')  # Convert immediate value to a 7-bit binary string
    
    string += '0'  # Set the first bit to 0
    string = string + reg_dic[index[1]] + binary_str  # Convert the register name and immediate value to binary
    
    return string


def type_C(index, string):
    # Instruction type C: load and store instructions
    # Set bits 3-7 to 00000
    string = string + '00000'
    # Convert register names to binary and add them to the string
    string = string + reg_dic[index[1]] + reg_dic[index[2]]
    return string

def type_D(index, string):
    # Instruction type D: conditional jump instructions
    if(index[2] in dct1.keys()):
        e = ("Syntax Error: misuse of Label as Variable, line with error is : " + str(line))
        return ""
    elif(index[2] not in d.keys()):
        e = ("Syntax Error : Use of undefined variables, line with error is : " + str(line))
        return e
    else:
        # Set the first bit to 0 and convert register and memory addresses to binary
        string = string + '0' + reg_dic[index[1]] + d[index[2]]
        return string

def type_E(index, string):
    # Instruction type E: unconditional jump instructions
    if(index[1] in d.keys()):
        e = ("Syntax Error: misuse of Variable as Label, line with error is : " + str(line))
        return ""
    elif(index[1] not in dct1.keys()):
        e = ("Syntax Error : Use of undefine label, line with error is : " + str(line))
        return ""
    else:
        # Set bits 5-7 to 000 and convert memory addresses to binary
        string = string + '0000' + dct1[index[1]]
        return string

def type_F(index, string):
    # Instruction type F: HLT instruction
    # Set all bits to 0
    string += '00000000000'
    return string

x='0000000'
count=0
count1=0
d={}
dct1={}


def remove_empty(l):
    c = l.count('\n')
    for i in range(c):
        l.remove('\n')
    # helper function to remove empty lines from the input file
    return l

ans=''

def syntaxerrorcommon():
    global wrong     # define a function to handle general syntax errors
    e=("general syntax error, line with error is : " + str(line)) 

def typeerror():
    global wrong    
    wrong=("typoerror, line with error is : " + str(line))

for i in sys.stdin:
    listu.append(i)
nlines=len(listu)

line = 0  # Initialize line number counter
index = 0  # Initialize instruction index

while index < len(listu):
    line += 1  # Increase line number counter
    string = ''  # Initialize empty string for binary representation of instruction
    index_j = listu[index].split()  # Split instruction into its components

    # Check if instruction begins with 'var'
    if index_j[0] != 'var':
        # If instruction has a label, remove it
        if ':' in index_j[0]:
            index_j.remove(index_j[0])

        # Handle special case of 'mov' instruction
        if index_j[0] == 'mov':
            if index_j[2][0] == 'R':
                index_j[0] = 'movi'
            else:
                index_j[0] = 'mov'
        # Handle special case of 'mov' instruction



        # Check if 'FLAGS' register is being used illegally
        if 'FLAGS' in index_j:
            if index_j[0] != 'mov':
                e = ("line with error is : " + str(line))
                # exit()

        # Handle arithmetic and logical instructions
        if index_j[0] == 'add' or index_j[0] == 'sub' or index_j[0] == 'mul' or index_j[0] == 'xor' or index_j[0] == 'or' or index_j[0] == 'and':
            string += opcode_dic[index_j[0]]  # Add opcode to binary string
            if len(index_j) != 4:  # Check if there are three operands
                syntaxerrorcommon()
            for k in range(1, 4):
                if index_j[k] not in reg_dic.keys():  # Check if operands are registers
                    typeerror()

            # Generate binary representation of instruction
            ans += (type_A(index_j, string)) + '\n'

        # Handle 'mov', 'rs', and 'ls' instructions
        elif index_j[0] == 'mov' or index_j[0] == 'rs' or index_j[0] == 'ls':
            string += opcode_dic[index_j[0]]  # Add opcode to binary string
            if len(index_j) != 3:  # Check if there are two operands
                syntaxerrorcommon()
            if index_j[1] not in reg_dic.keys():  # Check if first operand is a register
                typeerror()
            # Generate binary representation of instruction
            ans += (type_B(index_j, string)) + '\n'

        # Handle 'movi', 'div', 'cmp', and 'not' instructions
        elif index_j[0] == 'movi' or index_j[0] == 'div' or index_j[0] == 'cmp' or index_j[0] == 'not':
            string += opcode_dic[index_j[0]]  # Add opcode to binary string
            if len(index_j) != 3:  # Check if there are two operands
                syntaxerrorcommon()
            if index_j[1] not in reg_dic.keys():  # Check if first operand is a register
                typeerror()
            if index_j[2] not in reg_dic.keys():  # Check if second operand is a register
                typeerror()
            # Generate binary representation of instruction
            ans += (type_C(index_j, string)) + '\n'
        elif index_j[0] == 'ld' or index_j[0] == 'st':
            string += opcode_dic[index_j[0]]  # Add opcode to binary string
            if len(index_j) != 3:  # Check if there are two operands
                syntaxerrorcommon()
            if index_j[1] not in reg_dic.keys():  # Check if first operand is a register
                typeerror()
            # Generate binary representation of instruction
            ans += (type_D(index_j, string)) + '\n'    

        # Check if instruction is a jump instruction
        elif index_j[0] == 'jmp' or index_j[0] == 'jlt' or index_j[0] == 'je' or index_j[0] == 'jgt':
            # Add opcode to machine code string
            string += opcode_dic[index_j[0]]
            # Check that there are exactly 2 arguments
            if len(index_j) != 2:
                # Call error function if syntax is incorrect
                syntaxerrorcommon()
            # Call instruction_type_E to generate machine code and add to string
            ans += (type_E(index_j, string)) + '\n'

        # Check if instruction is a halt instruction
        elif index_j[0] == 'hlt':
            # Add opcode to machine code string
            string += opcode_dic[index_j[0]]
            # Check that there is only 1 argument
            if len(index_j) != 1:
                # Call error function if syntax is incorrect
                syntaxerrorcommon()
            # Call instruction_type_F to generate machine code and add to string
            ans += (type_F(index_j, string)) + '\n'

        # If instruction is not recognized, call error function
        else:
            typeerror()
    
    index += 1

print(ans)
