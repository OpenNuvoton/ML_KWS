from pyocd.core.helpers import ConnectHelper
from pyocd.flash.file_programmer import FileProgrammer
from pyocd.core.memory_map import MemoryType
from pyocd.coresight.cortex_m import CortexM

import logging
logging.basicConfig(level=logging.INFO)

import numpy as np

with ConnectHelper.session_with_chosen_probe(target_override="m467hjhae") as session:

    board = session.board
    target = board.target
    flash = target.memory_map.get_boot_memory()

    ###### Load firmware into device ######
    FileProgrammer(session).program("m460.bin")
    
    ###### Board info ######
    #print("Board MSG:")
    #print("Board's name:%s" % board.name)
    #print("Board's description:%s" % board.description)
    #print("Board's target_type:%s" % board.target_type)
    #print("Board's unique_id:%s" % board.unique_id)
    #print("Board's test_binary:%s" % board.test_binary)
    #print("Unique ID: %s" % board.unique_id)
    
    ###### ram/rom info ######
    print("Part number:%s" % target.part_number)
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
    #print("Irq:")
    #print(board.target.irq_table)
    
    ###### Basic info ######
    print("pc reg: 0x%X" % target.read_core_register('pc'))
    print("CPUID:0x%x" % target.read32(CortexM.CPUID))
    #print("device id:0x%x" % target.read32(0x40015800))
    #print("flash size:%x KB" % target.read32(0x1FFFF7CC))


    ###### Reset and Run ######
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
    print("write value:%x" % target.read32(0x20000030))
    
    ###### read block size ######
    sram_begain = 0x20000034
    x = target.read_memory_block32(sram_begain, 5)
    print("{}, TxBuffVal:{:x}".format( hex(sram_begain), target.read32((sram_begain))))
    print("{}, TxBuffVal:{:x}".format( hex(sram_begain), target.read32((sram_begain + 4))))
    print("{}, TxBuffVal:{:x}".format( hex(sram_begain), target.read32((sram_begain + 16))))
    print(x)
    