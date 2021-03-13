# assembler for HACK assembly language
import sys
import re
# tables to map C-instruction symbols to appropriate
# binary equivalent
COMP_TABLE = {
    "0": "0101010",
    "1": "0111111",
    "-1": "0111010",
    "D": "0001100",
    "A": "0110000",
    "M": "1110000",
    "!D": "0001101",
    "!A": "0110001",
    "!M": "1110001",
    "-D": "0001111",
    "-A": "0110011",
    "-M": "1110011",
    "D+1": "0011111",
    "A+1": "0110111",
    "M+1": "1110111",
    "D-1": "0001110",
    "A-1": "0110010",
    "M-1": "1110010",
    "D+A": "0000010",
    "D+M": "1000010",
    "D-A": "0010011",
    "D-M": "1010011",
    "A-D": "0000111",
    "M-D": "1000111",
    "D&A": "0000000",
    "D&M": "1000000",
    "D|A": "0010101",
    "D|M": "1010101",
}

DEST_TABLE = {
    "null": "000",
    "M": "001",
    "D": "010",
    "MD": "011",
    "A": "100",
    "AM": "101",
    "AD": "110",
    "AMD": "111"
}

JUMP_TABLE = {
    "null": "000",
    "JGT": "001",
    "JEQ": "010",
    "JGE": "011",
    "JLT": "100",
    "JNE": "101",
    "JLE": "110",
    "JMP": "111"
}

SYMBOL_TABLE = {
    "SP": 0,
    "LCL": 1,
    "ARG": 2,
    "THIS": 3,
    "THAT": 4,
    "R0": 0,
    "R1": 1,
    "R2": 2,
    "R3": 3,
    "R4": 4,
    "R5": 5,
    "R6": 6,
    "R7": 7,
    "R8": 8,
    "R9": 9,
    "R10": 10,
    "R11": 11,
    "R12": 12,
    "R13": 13,
    "R14": 14,
    "R15": 15,
    "SCREEN": 16384,
    "KBD": 24576
}

VARIABLE_COUNTER = 16

# reads in *.asm file contents
# and removes comments and whitespace
# returns an array where each element
# is a string representation of the assembly instruction
def readAsmIn(asmFileName):
    fileContents = open(asmFileName, "r")
    contents = [line.strip() for line in fileContents]
    contents = filter(lambda x: x[0:2] != "//", contents) # filter comments
    contents = filter(lambda x: x != "", contents) # filter empty lines
    contents = [line.split("//")[0] for line in contents] # remove inline comments
    contents = [line.strip() for line in contents]
    return contents

def decodeAInstruction(aInstruction):
    instruction = ""
    global VARIABLE_COUNTER
    if aInstruction[1:].isnumeric():
        instruction = format(int(aInstruction[1:]), "016b")
    elif aInstruction[1:] not in SYMBOL_TABLE.keys():
        SYMBOL_TABLE[aInstruction[1:]] = VARIABLE_COUNTER
        VARIABLE_COUNTER+=1
        instruction = format(SYMBOL_TABLE[aInstruction[1:]], "016b")
    else:
        instruction = format(SYMBOL_TABLE[aInstruction[1:]], "016b")
    return instruction

def decodeCInstruction(cInstruction):
    parsed = re.split(r'=|;', cInstruction) # split instr with regex
    if "=" in cInstruction and ";" in cInstruction:
        (dest, comp, jump) = (parsed[0], parsed[1], parsed[2])
    elif "=" in cInstruction:
        (dest, comp, jump) = (parsed[0], parsed[1], "null")
    elif ";" in cInstruction:
        (dest, comp, jump) = ("null", parsed[0], parsed[1])
    else:
        (dest, comp, jump) = ("null", parsed[0], "null")
        
    instruction = "111" + COMP_TABLE[comp] + DEST_TABLE[dest] + JUMP_TABLE[jump]
    return instruction

def decodeAsmInstructions(asmInstructions):
    decodedInstructions = []
    PC = 0 
    # 1st pass
    for instruction in asmInstructions:
        if instruction[0] == "(" and instruction[-1] == ")":
            SYMBOL_TABLE[instruction[1:-1]] = PC
            continue
        PC+=1
    # 2nd pass
    for instruction in asmInstructions:
        if instruction[0] == "(" and instruction[-1] == ")": # skip if label
            continue 
        if "@" in instruction:
            decoded = decodeAInstruction(instruction)
            decodedInstructions.append(decoded)
        else:
            decoded = decodeCInstruction(instruction)
            decodedInstructions.append(decoded)
    return decodedInstructions

# contents is an array with each element being
# a string representing the translated 16-bit HACK instruction
def writeHackOut(outFileName, contents):
    file = open(outFileName, "w")
    file.write("\n".join(contents))

if __name__ == "__main__":
    if len(sys.argv) == 2:
        asmFile = sys.argv[1]
        outFile = asmFile.split(".")[0] + ".hack"
    else:
        print("Error: No *.asm file given\nUsage: assembler.py filename")
        exit(1)
        # asmFile = "06/max/Max.asm"
        # outFile = asmFile.split(".")[0] + ".hack"

    asmInstructions = readAsmIn(asmFile)
    decodedInstructions = decodeAsmInstructions(asmInstructions)
    writeHackOut(outFile, decodedInstructions)
