reg_dic = {"R0":'000',"R1":'001',"R2":'010',"R3":'011',"R4":'100',"R5":'101',"R6":'110'}
opcode_dic = {"add":'00000',"sub":'00001', "mov" : '00010', "movi":'00011', "ld":'00100', "st":'00101', "mul":'00110', "div":'00111', "rs":'01000', "ls":'01001', "xor":'01010', "or":'01011', "and":'01100', "not":'01101', "cmp":'01110', "jmp":'01111', "jlt": '11100', "jgt":'11101', "je":'11111', "hlt":'11010' }
global error
error=""
line=-1

def run(done):
    # Extract the numerical part from the string
    num = done[1:]
    
    # Convert the numerical part into a binary string
    binary_str = ""
    if int(num) == 0:
        binary_str = '0000000'
    else:
        while int(num) > 0:
            # Calculate the remainder when num is divided by 2
            p = int(num) % 2
            
            # Add the remainder to the left of the current binary string
            binary_str = str(p) + binary_str
            
            # Divide num by 2 to get the next bit of the binary string
            num = int(num) // 2
        
        # Add leading zeros if necessary to make the binary string 7 bits long
        x = len(binary_str)
        if x <= 7:
            binary_str = '0'*(7-x) + binary_str
        
    # Return the binary string
    return binary_str

def type_A(j, string):
    # Instruction type A: ADD, SUB, MOV, AND, OR, XOR
    # Set the first two bits to 00
    string += '00'
    # Convert register names to binary and add them to the string
    string = string + reg_dic[j[1]] + reg_dic[j[2]] + reg_dic[j[3]]
    return string

def type_B(j, string):
    # Instruction type B: immediate instructions
    if(int(j[2][1:])<0 or int(j[2][1:])>127):
        e = ("Syntax Error : Immediate value out of range, line with error is : " + str(line))
        # exit()
    # Set the first bit to 0
    string += '0'
    # Convert the immediate value to binary and add it to the string
    a = run(j[2])
    string = string + reg_dic[j[1]] + a
    return string

def type_C(j, string):
    # Instruction type C: load and store instructions
    # Set bits 3-7 to 00000
    string = string + '00000'
    # Convert register names to binary and add them to the string
    string = string + reg_dic[j[1]] + reg_dic[j[2]]
    return string

def type_D(j, string):
    # Instruction type D: conditional jump instructions
    if(j[2] in dict_1.keys()):
        e = ("Syntax Error: misuse of Label as Variable, line with error is : " + str(line))
        return ""
    elif(j[2] not in d.keys()):
        e = ("Syntax Error : Use of undefined variables, line with error is : " + str(line))
        return e
    else:
        # Set the first bit to 0 and convert register and memory addresses to binary
        string = string + '0' + reg_dic[j[1]] + d[j[2]]
        return string

def type_E(j, string):
    # Instruction type E: unconditional jump instructions
    if(j[1] in d.keys()):
        e = ("Syntax Error: misuse of Variable as Label, line with error is : " + str(line))
        return ""
    elif(j[1] not in dict_1.keys()):
        e = ("Syntax Error : Use of undefine label, line with error is : " + str(line))
        return ""
    else:
        # Set bits 5-7 to 000 and convert memory addresses to binary
        string = string + '0000' + dict_1[j[1]]
        return string

def type_F(j, string):
    # Instruction type F: HLT instruction
    # Set all bits to 0
    string += '00000000000'
    return string

x='0000000'
count=0
counti=0
d={}
dict_1={}


def remove_empty(l):
    c = l.count('\n')
    for i in range(c):
        l.remove('\n')
    # helper function to remove empty lines from the input file
    return l

sol=''

def generalsyntaxerror():
    global error     # define a function to handle general syntax errors
    e=("general syntax error, line with error is : " + str(line)) 

def typoerror():
    global error    
    error=("typoerror, line with error is : " + str(line))

with open ("input.txt") as f:
    instruction =remove_empty(f.readlines())    # read the input file and remove empty lines

    if ('hlt' not in instruction[-1]):
        e=("Syntax Error : Missing hlt instruction")  # check if the last instruction is 'hlt'
        # exit() 
    elif ('hlt' not in instruction[-1]):
        error=("Syntax Error : hlt not being used as the last instruction")   # check if 'hlt' is the last instruction
        # exit()

for i in instruction:
    line += 1  # Increase line number counter
    string = ''  # Initialize empty string for binary representation of instruction
    j = i.split()  # Split instruction into its components

    # Check if instruction begins with 'var'
    if j[0] != 'var':
        # If instruction has a label, remove it
        if ':' in j[0]:
            j.remove(j[0])

        # Handle special case of 'mov' instruction
        if j[0] == 'mov':
            if j[2][0] == 'R':
                j[0] = 'movi'
            else:
                j[0] = 'mov'

        # Check if 'FLAGS' register is being used illegally
        if 'FLAGS' in j:
            if j[0] != 'mov':
                e = ("line with error is : " + str(line))
                # exit()

        # Handle arithmetic and logical instructions
        if j[0] == 'add' or j[0] == 'sub' or j[0] == 'mul' or j[0] == 'xor' or j[0] == 'or' or j[0] == 'and':
            string += opcode_dic[j[0]]  # Add opcode to binary string
            if len(j) != 4:  # Check if there are three operands
                generalsyntaxerror()
            for k in range(1, 4):
                if j[k] not in reg_dic.keys():  # Check if operands are registers
                    typoerror()

            # Generate binary representation of instruction
            sol += (type_A(j, string)) + '\n'

        # Handle 'mov', 'rs', and 'ls' instructions
        elif j[0] == 'mov' or j[0] == 'rs' or j[0] == 'ls':
            string += opcode_dic[j[0]]  # Add opcode to binary string
            if len(j) != 3:  # Check if there are two operands
                generalsyntaxerror()
            if j[1] not in reg_dic.keys():  # Check if first operand is a register
                typoerror()
            # Generate binary representation of instruction
            sol += (type_B(j, string)) + '\n'

        # Handle 'movi', 'div', 'cmp', and 'not' instructions
        elif j[0] == 'movi' or j[0] == 'div' or j[0] == 'cmp' or j[0] == 'not':
            string += opcode_dic[j[0]]  # Add opcode to binary string
            if len(j) != 3:  # Check if there are two operands
                generalsyntaxerror()
            if j[1] not in reg_dic.keys():  # Check if first operand is a register
                typoerror()
            if j[2] not in reg_dic.keys():  # Check if second operand is a register
                typoerror()
            # Generate binary representation of instruction
            sol += (type_C(j, string)) + '\n'

        # Check if instruction is a jump instruction
        elif j[0] == 'jmp' or j[0] == 'jlt' or j[0] == 'je' or j[0] == 'jgt':
            # Add opcode to machine code string
            string += opcode_dic[j[0]]
            # Check that there are exactly 2 arguments
            if len(j) != 2:
                # Call error function if syntax is incorrect
                generalsyntaxerror()
            # Call instruction_type_E to generate machine code and add to string
            sol += (type_E(j, string)) + '\n'

        # Check if instruction is a halt instruction
        elif j[0] == 'hlt':
            # Add opcode to machine code string
            string += opcode_dic[j[0]]
            # Check that there is only 1 argument
            if len(j) != 1:
                # Call error function if syntax is incorrect
                generalsyntaxerror()
            # Call instruction_type_F to generate machine code and add to string
            sol += (type_F(j, string)) + '\n'

        # If instruction is not recognized, call error function
        else:
            typoerror()


               
# Create a new file named "output.txt" 
file2 = open('output.txt', 'w')

# Print the value of the variable 
print(error)

if error != '':
    file2.write(error)

else:
    file2.write(sol)

file2.close()
