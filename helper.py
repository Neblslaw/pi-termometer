def generate_crc(data):
    """Calculates 8-Bit Sensirion CRC with polynomial 0x31 (x^8 + x^5 + x^4 + 1)"""
    crc = 0xFF
    for byte in data:
        crc ^= byte
        for _ in range(8):
            if crc & 0x80:
                crc = (crc << 1) ^ 0x31
            else:
                crc = crc << 1
    return crc & 0xFF

def is_crc_valid(data):
    return generate_crc(data[:2]) == data[2]
