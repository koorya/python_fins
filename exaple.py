import fins
import udp
import time

# функция для чтения слова из памяти ПЛК
def read_int(int_addr):
    mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, int_addr, 1)
    return int.from_bytes(mem_area[-2:], 'big')

# подключение к ПЛК с помощью библиотеки по FINS
fins_instance = udp.UDPFinsConnection()
fins_instance.connect('172.16.201.201')
fins_instance.dest_node_add=1
fins_instance.srce_node_add=25

# адрес переменной состояния в области памяти ПЛК
state = b'\x00\x01\x00' 
# адрес переменной фокуса дальше (к биту привязана кнопка прибора)
ff_bit = b'\x00\x64\x04'
# адрес переменной фокус ближе (привязана кнопка)
fn_bit = b'\x00\x64\x05'

# если находится в состоянии 10, то нужно дать команду 11. (следующая четверть оборота)
# Если находится в состоянии 15, то нужно дать команду 16 (возврат в нулевое положение и отключение прибора)
if 1 == int(input("reset. 1 - yes, 0 - no\n")): # нужно ли сбрасывать прибор, то есть ввести его в состояние 18, в котором он выключит прибор, если он был включен
    # задаем состояние, которое запишем в область памяти ПЛК через FINS
    pc = 18 
    # записываем состояние через FINS
    fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, state, pc.to_bytes(2, 'big'), 1) 

# заводим переменную для ввода с клавиатуры
pc = 1 
# пока прибор не окажется в состоянии 18 продолжаем работать
while pc != 0 and pc != 18 : 
    # читаем текущее состояние прибора 
    cur_state = read_int(state)

    # выводим текущее состояние прибора
    print("cur_state = {0}".format(cur_state))

    # если текущее состояние 10, то есть три варианта - покрутить фокус взад-вперед, либо перейти к слудующему шагу (пращать на четверть оборота), 
    # либо выйти из программы
    if cur_state == 10 :
        # предлагаем ввести команду
        print("Level")
        pc = int(input("enter command. 1 - next, 4 - focus far, 5 - focus near, 0 - exit\n"))
        if pc == 1 :
            # задаем состояние прибору для дальнейшего выполнения работы.
            pc = 11
            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, state, pc.to_bytes(2, 'big'), 1)
        if pc == 4 :
            # включаем кнопку "фокус дальше", ожидаем 3 секунды и выключаем обратно
            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_BIT,ff_bit,b'\x01',1)
            time.sleep(3)
            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_BIT,ff_bit,b'\x00',1)
        if pc == 5 :
            # включаем кнопку "фокус ближе", ожидаем 3 секунды и выключаем обратно
            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_BIT,fn_bit,b'\x01',1)
            time.sleep(3)
            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().CIO_BIT,fn_bit,b'\x00',1)
    # в случае, если прибор в состоянии 15, можем дать ему команды 16 (вернуться в исходное состояние) либо просто выйти из программы.
    if cur_state == 15 :
        print("Level")
        pc = int(input("enter command. 1 - next, 0 - exit\n"))
        if pc == 1 :
            # задаем состояние прибору для дальнейшего выполнения работы.
            pc = 16
            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, state, pc.to_bytes(2, 'big'), 1)

    # если состояние 20 - значит прибор отработал полностью, 
    # если 0, то еще не начинал работать
    if cur_state == 20 or cur_state == 0:
        print("Wait for")
        pc = int(input("enter command. 1 - next, 0 - exit\n"))
        if pc == 1 :
            # запускаем прибор для выполнения алгоритма
            pc = 1
            fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, state, pc.to_bytes(2, 'big'), 1)
    # ожидаем полсекунды для следующего опроса прибора о его состоянии
    time.sleep(0.5)

# при выходе из программы можно задать какое-нибудь состояние прибору при желании.
#pc = 18
fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, state, pc.to_bytes(2, 'big'), 1)

# в качестве примера использования библиотеки для записи и чтения слова
#fins_instance.memory_area_write(fins.FinsPLCMemoryAreas().WORK_WORD, mem_addr, b'\x00\x01',1)
#mem_area = fins_instance.memory_area_read(fins.FinsPLCMemoryAreas().WORK_WORD, mem_addr, 1)
