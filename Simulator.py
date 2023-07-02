import sys

registers = {"000":0,"001":0,"010":0,"011":0,"100":0,"101":0,"110":0,"111":0}

var={}     


def add(inst_code ): 
    reg_str  = inst_code[7:10]          
    reg1_str  =inst_code[10:13]           
    reg2_str = inst_code[13:16]
    reg_sum = registers[reg1_str] + registers[reg2_str]

    registers[reg_str] =reg_sum

def sub(inst_code ): 
    reg_str  = inst_code[7:10]
    reg1_str  = inst_code[10:13]
    reg2_str = inst_code[13:16]

    reg_sub = registers[reg1_str] - registers[reg2_str]
    
    registers[reg_str] =reg_sub

def mul(inst_code ): 
    reg_str  = inst_code[7:10]
    reg1_str  = inst_code[10:13]
    reg2_str  = inst_code[13:16]
    
    reg_mul = registers[reg1_str] * registers[reg2_str]

    registers[reg_str] =reg_mul

def op_and(inst_code):
    reg_str  = inst_code[7:10]
    reg1_str  = inst_code[10:13]
    reg2_str  = inst_code[13:16]

    registers[reg_str] = int(registers[reg1_str] & registers[reg2_str])
    registers['111']=0

def get_16bit(num):
    num1=str(bin(num))[2:]
    str_len = 16-len(num1)
    if str_len >=0:
        str_final = "0"*str_len
        str_final = str_final + num1
        return str_final
    else:
        return None
    
def get_nbit(num1,n): 
    
    str_len = n - len(num1)
    if str_len >=0:
        str_final = "0"*str_len
        str_final = str_final + num1
        return str_final
    else:
        return None
    

def op_or(inst_code): 
    reg_str  = inst_code[7:10]
    reg1_str  = inst_code[10:13]
    reg2_str  = inst_code[13:16]

    registers[reg_str] = int(registers[reg1_str] | registers[reg2_str])
    registers['111']=0

def op_xor(inst_code): 
    reg_str  = inst_code[7:10]
    reg1_str  = inst_code[10:13]
    reg2_str  = inst_code[13:16]

    registers[reg_str] = int(registers[reg1_str] ^ registers[reg2_str])
    registers['111']=0

def op_invert(inst_code):

    reg1_str  = inst_code[10:13]   
    reg2_str   = inst_code[13:16]
    x=get_16bit(registers[reg2_str])
    res=''
    for i in x:
        if(i=='0'):
            res+='1'
        else:
            res+='0'
    registers[reg1_str] = int(res,2)
    registers['111']=0

def op_compare(inst_code):
    reg1_str_in  = inst_code[10:13]
    reg2_str_in   = inst_code[13:16]
    if registers[reg1_str_in] > registers[reg2_str_in]:
        registers["111"] = 2  
    elif registers[reg1_str_in] < registers[reg2_str_in]:
        registers["111"] = 4  
    else:
        registers["111"] = 1    
         
def move_imm(inst_code):
    reg=inst_code[6:9]
    imm_val=inst_code[9:16]
    registers[reg]=int(imm_val,2)
    registers['111']=0

def move_reg(inst_code): 
    reg=inst_code[10:13]
    reg2=inst_code[13:16]  
    registers[reg]=int(registers[reg2])
    registers['111']=0

def RShift(inst_code): 
    reg = inst_code[6:9]     
    val_imm = inst_code[9:16]      
    val_int = int(val_imm,2)
    registers[reg] = registers[reg] >> val_int
    registers['111']=0


def LShift(inst_code): 
    reg = inst_code[6:9]     
    val = inst_code[9:16]      
    val_int = int(val,2) 
    registers[reg] = registers[reg] << val_int
    registers['111']=0


def load(inst_code ):
    reg  = inst_code[6:9]
    mem_add = inst_code[9:16]
    mem_add = int(mem_add,2)
    if(var.get(mem_add)==None):
        var[mem_add]=0
    registers[reg] = int(var.get(mem_add))
    registers['111']=0

def store(inst_code ):
    reg  = inst_code[6:9]
    mem_add = inst_code[9:16]
    mem_add = int(mem_add,2)
    var[mem_add]   = registers[reg]
    registers['111']=0
    
def op_div(inst_code ):
    reg1 = inst_code[10:13]
    reg2 = inst_code[13:16]
    registers["000"] = int(registers[reg1]/registers[reg2])
    registers["001"]  = registers[reg1]%registers[reg2]
    registers['111']=0


def jlt(inst_code,prog_count):
    if(registers["111"]==4):
        registers['111']=0
        return int(inst_code[9:16],2)
    else:
        registers['111']=0
        return prog_count

def jgt(inst_code,prog_count):
    if(registers["111"]==2):
        registers['111']=0
        return int(inst_code[9:16],2)
    else:
        registers['111']=0
        return prog_count

def je(inst_code,prog_count):
    if(registers["111"]==1):
        registers['111']=0
        return int(inst_code[9:16],2)
    else:
        registers['111']=0
        return prog_count

def jmp(inst_code):
    registers['111']=0
    return int(inst_code[9:16],2)


def form(prog_in,var):
    for i in list(sorted(var)):
        prog_in.append(get_nbit(str(bin(var[i]))[2:],16))

   
    prog_in = [string.rstrip('\n') for string in prog_in]
    
    for inst in prog_in:
      
        print(inst)
 
    total_lines=len(prog_in)
    while(total_lines<128):
        print("0000000000000000")
       
        total_lines+=1
        
def call(inst_code,prog_count): 
    
    opcode=inst_code[:5]
    print(get_nbit(str(bin(prog_count))[2:],7), end="        ")


    prog_count = prog_count + 1

    if(opcode=="00000"):
        add(inst_code)  

    elif(opcode=="00001"):
        sub(inst_code, )

    elif(opcode=="00010"):
        move_imm(inst_code)

    elif(opcode=="00011"):
        move_reg(inst_code)

    elif(opcode=="00100"):
        load(inst_code)

    elif(opcode=="00101"):
        store(inst_code)  

    elif(opcode=="00110"):
        mul(inst_code)

    elif(opcode=="00111"):
        op_div(inst_code)

    elif(opcode=="01000"):
        RShift(inst_code) 

    elif(opcode=="01001"): 
        LShift(inst_code)

    elif(opcode=="01010"):
        op_xor(inst_code) 

    elif(opcode=="01011"):
        op_or(inst_code)

    elif(opcode=="01100"):
        op_and(inst_code) 

    elif(opcode=="01101"):
        op_invert(inst_code) 

    elif(opcode=="01110"):
        op_compare(inst_code) 

    elif(opcode=="01111"):
        prog_count = jmp(inst_code) 

    elif(opcode=="11100"):
        prog_count = jlt(inst_code,prog_count) 

    elif(opcode=="11101"):
        prog_count = jgt(inst_code,prog_count) 

    elif(opcode=="11111"):
        prog_count = je(inst_code,prog_count)

    elif(opcode=="10011"):
        registers['111']=0
        
    else:
        pass
    for i in list(registers.keys())[0:7]:
        output = get_nbit(str(bin(registers[i]))[2:],16)
        print(output,end =' ')
     

    output = (get_nbit(str(bin(registers["111"]))[2:],16))
    print(output)
   
    return prog_count


      
def main():
   
    prog_in = []

    prog_count = 0
    
    prog_in= sys.stdin.readlines()
    
   
    inst_code = prog_in[prog_count]
    while(prog_count < len(prog_in)):
        hlt = inst_code[:5]
        inst_code = prog_in[prog_count]
        temp_prog_counter = call(inst_code,prog_count)
        if(hlt=="10011"):
            break
        prog_count=temp_prog_counter
    form(prog_in,var)
    

if __name__ =="__main__":
    main()
