# RISC-V Assembler and Simulator

This project consists of two main components: an assembler and a simulator for a subset of the RISC-V instruction set architecture (ISA). The assembler converts RISC-V assembly code into machine code, while the simulator emulates the execution of the generated machine code on a RISC-V processor model.

## Features

### Supported Instructions
- **R-type**: `add`, `sub`, `sll`, `slt`, `sltu`, `xor`, `srl`, `or`, `and`
- **I-type**: `lw`, `addi`, `sltiu`, `jalr`
- **S-type**: `sw`
- **B-type**: `beq`, `bne`, `blt`, `bge`, `bltu`, `bgeu`
- **U-type**: `lui`, `auipc`
- **J-type**: `jal`

### Assembler
- Translates assembly code to 32-bit machine code.
- Supports labels and immediate value conversion.
- Checks for the virtual halt instruction (`beq zero,zero,0`) to terminate simulation.

### Simulator
- Models 32 RISC-V registers and memory.
- Executes machine code instructions step-by-step.
- Outputs register states and memory contents after each instruction.
- Handles data hazards and control flow instructions.

## Installation

1. **Prerequisites**: Python 3.x
2. **Clone the repository** or download the files `Assembler.py` and `Simulator.py`.

## Usage

### Assembler
1. Prepare your RISC-V assembly code in `input.txt`.
2. Run the assembler:
   ```bash
   python Assembler.py
   ```
3. Generated machine code is saved in `output.txt`.

**Note**: Ensure the last instruction is `beq zero,zero,0` (virtual halt) to terminate simulation.

### Simulator
1. Run the simulator after generating machine code:
   ```bash
   python Simulator.py
   ```
2. Simulation results are saved in `output_sim.txt`, showing register and memory states after each cycle.

## Example

### Assembly Code (`input.txt`)
```assembly
addi t0, zero, 5
addi t1, zero, 3
add t2, t0, t1
beq zero,zero,0
```

### Generated Machine Code (`output.txt`)
```
00000000000000000000000000010111
...
```

### Simulator Output (`output_sim.txt`)
```
0b00000000000000000000000000000100 0b00000000000000000000000000000101 ...
0x00010000:0b00000000000000000000000000001000
...
```

## Output Format

- **Registers**: Each line starts with the program counter (PC) in binary, followed by 32 registers (32-bit binary values).
- **Memory**: Hexadecimal addresses with 32-bit binary values.

