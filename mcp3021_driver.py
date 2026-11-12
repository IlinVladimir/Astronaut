import smbus
import time

class MCP3021:
    def __init__(self, dynamic_range, verbose=False):
        self.bus = smbus.SMBus(1)
        self.dynamic_range = dynamic_range
        self.address = 0x4D
        self.verbose = verbose

    def deinit(self):
        self.bus.close()

    def get_number(self):
        # Читаем 2 байта (16-битное слово) из устройства по шине I2C
        data = self.bus.read_word_data(self.address, 0)
        
        # В SMBus старший и младший байты при чтении слова меняются местами (little-endian):
        lower_data_byte = data >> 8
        upper_data_byte = data & 0xFF
        
        # Собираем 10-битное число по спецификации MCP3021
        number = (upper_data_byte << 6) | (lower_data_byte >> 2)
        
        if self.verbose:
            print(f"Принятые данные: {data}, Старший байт: {upper_data_byte:x}, Младший байт: {lower_data_byte:x}, Число: {number}")
        return number

    def get_voltage(self):
        number = self.get_number()
        # Разрядность MCP3021 составляет 10 бит (1024 уровня, максимальный код 1023)
        return (number / 1023) * self.dynamic_range


if __name__ == "__main__":
    try:
        # Динамический диапазон измеряется мультиметром на контакте PWR блока AUX (при перемычке 5V)
        adc = MCP3021(dynamic_range=5.18)
        
        while True:
            voltage = adc.get_voltage()
            print(f"Напряжение (MCP3021): {voltage:.2f} В")
            time.sleep(1)
            
    finally:
        adc.deinit()