"""
This script uses the pyOCD library to interact with a microcontroller board.
Dependencies:
- pyOCD library
Usage:
- Ensure the pyOCD library is installed.
- Update the firmware file path ("I2S_Codec_PDMA_SCA_max.bin") if necessary.
- Run the script to perform the operations on the connected target board.
Note:
- The script is configured to connect to a target with the identifier "m467hjhae".
- Some sections of the code are commented out and can be uncommented for additional functionality 
- such as resetting and halting the target, stepping through instructions, and resuming execution.
"""
import logging
from pyocd.core.helpers import ConnectHelper
from pyocd.flash.file_programmer import FileProgrammer
from pyocd.core.memory_map import MemoryType
from pyocd.coresight.cortex_m import CortexM

logging.basicConfig(level=logging.INFO)

with ConnectHelper.session_with_chosen_probe(target_override="m467hjhae") as session:

    board = session.board
    target = board.target
    flash = target.memory_map.get_boot_memory()

    ###### Load firmware into device ######
    FileProgrammer(session).program("I2S_Codec_PDMA_SCA_max.bin")

    ###### Board info ######
    print("Board MSG:")
    print(f"Board's name: {board.name}")
    print(f"Board's description: {board.description}")
    print(f"Board's target_type: {board.target_type}")
    print(f"Board's unique_id: {board.unique_id}")
    print(f"Board's test_binary: {board.test_binary}")
    print(f"Unique ID: {board.unique_id}")

    ###### ram/rom info ######
    print(f"Part number:{target.part_number}")
    memory_map = target.get_memory_map()
    ram_region = memory_map.get_default_region_of_type(MemoryType.RAM)
    rom_region = memory_map.get_boot_memory()
    print("menory map:")
    print(memory_map)
    print("ram_region:")
    print(ram_region)
    print("rom_region(flash):")
    print(rom_region)

    ###### Irq info ######
    print("Irq:")
    print(board.target.irq_table)

    ###### Basic info ######
    print(f"pc reg: 0x{target.read_core_register('pc'):X}")
    print(f"CPUID:0x{target.read32(CortexM.CPUID):x}")
    print(f"device id:0x{target.read32(0x40015800):x}")
    print(f"flash size:{target.read32(0x1FFFF7CC):x} KB")


    ###### Reset and Run Example ######
    #target.reset_and_halt(reset_type = target.ResetType.SW)

    ## Read some registers.
    #print("pc: 0x%X" % target.read_core_register("pc"))

    #target.step()
    #print("pc: 0x%X" % target.read_core_register("pc"))

    #target.resume()
    #target.halt()
    #print("pc: 0x%X" % target.read_core_register("pc"))

    #target.reset_and_halt()

    #print("pc: 0x%X" % target.read_core_register("pc"))

    ###### write sram ######
    target.write32(0x20000030, 0xA2332227)
    print(f"write value:{target.read32(0x20000030):x}")

    ###### read block size ######
    SRAM_BEGAIN = 0x20000034
    x = target.read_memory_block32(SRAM_BEGAIN, 5)
    print(f"{hex(SRAM_BEGAIN)}, TxBuffVal:{target.read32(SRAM_BEGAIN):x}")
    print(f"{hex(SRAM_BEGAIN)}, TxBuffVal:{target.read32(SRAM_BEGAIN + 4):x}")
    print(f"{hex(SRAM_BEGAIN)}, TxBuffVal:{target.read32(SRAM_BEGAIN + 16):x}")
    print(x)
