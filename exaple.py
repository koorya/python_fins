import fins
import udp
import time

def read_int(int_addr):
    mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, int_addr, 1)
    return int.from_bytes(mem_area[-2:], 'big')

fins_instance = udp.UDPFinsConnection()
fins_instance.connect('172.16.201.201')
fins_instance.dest_node_add=1
fins_instance.srce_node_add=25
"""
for i in range(2):
    fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_BIT,b'\x00\x64\x03',b'\x01',1)
    mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00')
    print(mem_area)
    time.sleep(1)
    fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_BIT,b'\x00\x64\x03',b'\x00',1)
    mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().CIO_WORD,b'\x00\x64\x00')
    print(mem_area)
    time.sleep(1)
"""
state = b'\x00\x01\x00'

# если 10, то 11. Если 15, то 16
if 1 == int(input("reset. 1 - yes, 0 - no\n")):
    pc = 18
    fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, state, pc.to_bytes(2, 'big'), 1)

pc = 1
while pc != 0 and pc != 18 :
    cur_state = read_int(state)


    print("cur_state = {0}".format(cur_state))

    if cur_state == 10 :
        print("Level")
        pc = int(input("enter command. 1 - next, 0 - exit\n"))
        if pc == 1 :
            pc = 11
            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, state, pc.to_bytes(2, 'big'), 1)

    if cur_state == 15 :
        print("Level")
        pc = int(input("enter command. 1 - next, 0 - exit\n"))
        if pc == 1 :
            pc = 16
            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, state, pc.to_bytes(2, 'big'), 1)

    if cur_state == 20 or cur_state == 0:
        print("Wait for")
        pc = int(input("enter command. 1 - next, 0 - exit\n"))
        if pc == 1 :
            pc = 1
            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, state, pc.to_bytes(2, 'big'), 1)

    time.sleep(0.5)

#pc = 18
fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, state, pc.to_bytes(2, 'big'), 1)

#fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, mem_addr, b'\x00\x01',1)
#mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, mem_addr, 1)
