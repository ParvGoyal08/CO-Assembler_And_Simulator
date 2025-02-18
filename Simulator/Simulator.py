import sys
registers={
    '00000': 0,
    '00001': 0,
    '00010': 256,
    '00011': 0,
    '00100': 0,
    '00101': 0,
    '00110': 0,
    '00111': 0,
    '01000': 0,
    '01001': 0,
    '01010': 0,
    '01011': 0,
    '01100': 0,
    '01101': 0,
    '01110': 0,
    '01111': 0,
    '10000': 0,
    '10001': 0,
    '10010': 0,
    '10011': 0,
    '10100': 0,
    '10101': 0,
    '10110': 0,
    '10111': 0,
    '11000': 0,
    '11001': 0,
    '11010': 0,
    '11011': 0,
    '11100': 0,
    '11101': 0,
    '11110': 0,
    '11111': 0
}

memory = {(i): 0 for i in range(1,33)}

def decimal_to_hexadecimal(decimal_num):
    base_address = 0x00010000
    address_increment = (decimal_num - 1) * 4
    hex_address = base_address + address_increment
    return f'0x{hex_address:08x}'

def binary_to_decimal(binary):
    binary = str(binary)
    length = len(binary)
    if binary[0] == '1':
        binary = ''.join('1' if bit == '0' else '0' for bit in binary)
        decimal = -1 * ((int(binary, 2) + 1) % (1 << length))  
    else:
        decimal = int(binary, 2)  
    return decimal
def unsigned(binary):
    decimal = 0
    for digit in binary:
        decimal = decimal*2 + int(digit)
    return decimal

def decimal_to_binary(decimal_num,l):
   
    if decimal_num< 0:
        binary_repr = bin(decimal_num & 0xFFF)[3:]
        while len(binary_repr) < l:
            binary_repr = '1' + binary_repr
    
        return binary_repr
    else:
        binary_repr = bin(decimal_num)[2:]

        while len(binary_repr) < l:
            binary_repr = '0' + binary_repr
    
    return binary_repr


def decimal_to_binary_2s_complement(decimal_num):
    binary_num = bin(abs(decimal_num))[2:]
    binary_num = binary_num.zfill(32)
    if decimal_num < 0:
        binary_num = ''.join('1' if bit == '0' else '0' for bit in binary_num)
        binary_num = bin(int(binary_num, 2) + 1)[2:]

    return str(binary_num)



input_file = "s_test4.txt"
with open(input_file,'r') as s:
    input = s.readlines()

pc=0
output_file = "output_sim.txt"
with open(output_file,'w') as s:
    

    while ((pc//4)<len(input)):
        instruction=input[pc//4]
        opcode = instruction[25:32]       
        if opcode == '0110011':  # R-type instruction
            funct3 = instruction[17:20]
            rs1 = instruction[12:17]
            rs2 = instruction[7:12]
            rd = instruction[20:25]


            pc+=4
            
        elif opcode == '0000011' or opcode=='0010011' or opcode=='1100111':  # I-type instruction
            rd = instruction[20:25:1]
            rs1 = instruction[12:17:1]
            imm_i = instruction[0:12:1]
            num = binary_to_decimal(imm_i)
            pc+=4
            if funct3 == '010' and opcode=='0000011':  # lw
                registers[rd]=memory[decimal_to_hexadecimal(registers[rs1]+num)]
            elif funct3 == '000' and opcode=='0010011':  # addi
                # print(num)
                registers[rd] = registers[rs1] + num
            elif funct3 == '011' and opcode=='0010011':  # sltiu
                registers[rd] = int(registers[rs1] < num)
            elif funct3 == '000' and opcode=='1100111':  # jalr
                if rd == '00000':
                    registers[rd]=0

                else:
                    registers[rd] = pc
                    pc = registers[rs1]+ binary_to_decimal(imm_i)
                    pc = decimal_to_binary(pc,32)
                    pc = pc[0:31] + '0'
                    pc = binary_to_decimal(pc)

                



        elif opcode == '0100011':  # S-type instruction
            rs1 = instruction[7:12:1]
            imm_s = instruction[0:7:1]+ instruction[-8:-13:1]
            address = decimal_to_hexadecimal(registers[rs1] + binary_to_decimal(imm_s))
            if funct3 == '010':  # sw
                memory[address] = registers[instruction[12:17:1]]

            pc+=4
        
        elif opcode == '1100011':  # B-type instruction
            imm_b = binary_to_decimal(instruction[0]+instruction[-8]+instruction[1:7]+instruction[-12:-9:]+'0')
            rs1 = instruction[12:17:1]
            rs2 = instruction[7:12:1]
            pc+=4
            if funct3 == '000':  # beq
                if registers[rs1] == registers[rs2]:
                    pc += imm_b   # PC will be incremented after this instruction, so decrement by 1
            elif funct3 == '001':  # bne
                if registers[rs1] != registers[rs2]:
                    pc += imm_b  # PC will be incremented after this instruction, so decrement by 1
            elif funct3 == '100':  # blt
                if registers[rs1] < registers[rs2]:
                    pc += imm_b # PC will be incremented after this instruction, so decrement by 1
            elif funct3 == '101':  # bge
                if registers[rs1] >= registers[rs2]:
                    pc += imm_b  # PC will be incremented after this instruction, so decrement by 1
    # 
    # 
            elif funct3 == '110':  # bltu
                if registers[rs1] < registers[rs2]:
                    pc += imm_b   # PC will be incremented after this instruction, so decrement by 1
            elif funct3 == '111':  # bgeu
                if registers[rs1] >= registers[rs2]:
                    pc += imm_b   # PC will be incremented after this instruction, so decrement by 1
    # 
    # 


        elif opcode == '1101111':  # J-type instruction
            pc+=4
            rd = instruction[-12:-7:1]
            imm_j = instruction[0]+instruction[12:20:1]+instruction[11]+instruction[1:11]+'0'
            imm_j = binary_to_decimal(imm_j)
            registers[rd] = pc + 4  # Store address of next instruction in rd jal
            pc += imm_j



        elif opcode == '0110111':  # U-type instruction (LUI)
            imm_u = binary_to_decimal(instruction[0:20:1]+"000000000000")
            registers[rd] = imm_u
            pc+=4

        elif opcode == '0010111':  # U-type instruction (AUIPC)
            imm_u = binary_to_decimal(instruction[0:20:1]+"000000000000")
            registers[rd] = pc + imm_u
            pc+=4

        elif opcode == '0000011':  # Load instruction (e.g., lw)
            address = instruction[-12:-7:1]
            imm_u = binary_to_decimal(instruction[0:20:1]+"000000000000")
            address = decimal_to_hexadecimal(registers[rs1] + imm_u)
            registers[rd] = memory[address]
            pc+=4

        elif opcode == '0100011':  # Store instruction (e.g., sw)
            address = registers[rs1] + imm_i
            imm_u = binary_to_decimal(instruction[0:20:1]+"000000000000")
            address = decimal_to_hexadecimal(registers[rs1] + imm_s)
            memory[address] = registers[rs2]
            pc+=4


            # Add more conditional branch instructions here

        
        line=""
        line='0b'+decimal_to_binary(pc,32)+" "+line.strip()
        for i in registers:
                line = line+'0b'+decimal_to_binary(registers[i],32,)+ " "
                

        s.write(line)
        s.write('\n')
    for i in (memory):
                lin2 = ""
                lin2 = lin2+(decimal_to_hexadecimal(i)) + ':' +'0b'+decimal_to_binary(memory[i],32)
                s.write(lin2+'\n')


