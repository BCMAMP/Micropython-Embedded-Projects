import time
import ustruct

class ILI9341:
    def __init__(self, spi, cs, dc, rst, w=240, h=320, r=0):
        self.spi = spi
        self.cs = cs
        self.dc = dc
        self.rst = rst
        self.width = w
        self.height = h
        self.init()

    def write_cmd(self, cmd):
        self.dc.low()
        self.cs.low()
        self.spi.write(bytearray([cmd]))
        self.cs.high()

    def write_data(self, data):
        self.dc.high()
        self.cs.low()
        self.spi.write(data)
        self.cs.high()

    def init(self):
        self.rst.low()
        time.sleep_ms(50)
        self.rst.high()
        time.sleep_ms(50)
        
        
        for cmd, data in [
            (0xEF, b'\x03\x80\x02'),
            (0xCF, b'\x00\xC1\x30'),
            (0xED, b'\x64\x03\x12\x81'),
            (0xE8, b'\x85\x00\x78'),
            (0xCB, b'\x39\x2C\x00\x34\x02'),
            (0xF7, b'\x20'),
            (0xEA, b'\x00\x00'),
            (0xC0, b'\x23'),       
            (0xC1, b'\x10'),       
            (0xC5, b'\x3E\x28'),   
            (0xC7, b'\x86'),       
            (0x36, b'\x48'),       
            (0x3A, b'\x55'),       
            (0xB1, b'\x00\x18'),   
            (0xB6, b'\x08\x82\x27'), 
            (0xF2, b'\x00'),       
            (0x26, b'\x01'),       
        ]:
            self.write_cmd(cmd)
            if data: self.write_data(data)
            
        self.write_cmd(0x11) 
        time.sleep_ms(120)
        self.write_cmd(0x29) 

    def set_window(self, x0, y0, x1, y1):
        self.write_cmd(0x2A) 
        self.write_data(ustruct.pack(">HH", x0, x1))
        self.write_cmd(0x2B) 
        self.write_data(ustruct.pack(">HH", y0, y1))
        self.write_cmd(0x2C) 

    def fill(self, color):
        self.set_window(0, 0, self.width - 1, self.height - 1)
        hi, lo = (color >> 8) & 0xff, color & 0xff
        buf = bytearray([hi, lo] * self.width)
        self.dc.high()
        self.cs.low()
        for _ in range(self.height):
            self.spi.write(buf)
        self.cs.high()

    def text(self, string, x, y, color=0xffff, bg=0x0000, size=2):
        
        font = {
            '0': [0x3E,0x51,0x49,0x45,0x3E], '1': [0x00,0x42,0x7F,0x40,0x00],
            '2': [0x42,0x61,0x51,0x49,0x46], '3': [0x21,0x41,0x45,0x4B,0x31],
            '4': [0x18,0x14,0x12,0x7F,0x10], '5': [0x27,0x45,0x45,0x45,0x39],
            '6': [0x3C,0x4A,0x49,0x49,0x30], '7': [0x01,0x71,0x09,0x05,0x03],
            '8': [0x36,0x49,0x49,0x49,0x36], '9': [0x06,0x49,0x49,0x29,0x1E],
            'A': [0x7E,0x11,0x11,0x11,0x7E], 'B': [0x7F,0x49,0x49,0x49,0x36],
            'C': [0x3E,0x41,0x41,0x41,0x22], 'D': [0x7F,0x41,0x41,0x22,0x1C],
            '*': [0x14,0x08,0x3E,0x08,0x14], '#': [0x24,0x7F,0x24,0x7F,0x24],
            ':': [0x00,0x36,0x36,0x00,0x00], ' ': [0x00,0x00,0x00,0x00,0x00],
            'M': [0x7F,0x02,0x0C,0x02,0x7F], 'm': [0x7C,0x04,0x18,0x04,0x7C],
            'a': [0x20,0x54,0x54,0x54,0x78], 's': [0x48,0x54,0x54,0x54,0x20], 
            'u': [0x3C,0x40,0x40,0x20,0x7C], 'k': [0x7F,0x08,0x14,0x22,0x41], 
            'n': [0x7C,0x04,0x04,0x04,0x78], 'p': [0x7C,0x14,0x14,0x14,0x08], 
            'w': [0x3C,0x40,0x38,0x40,0x3C], 'o': [0x38,0x44,0x44,0x44,0x38], 
            'r': [0x7C,0x08,0x04,0x04,0x08], 'd': [0x08,0x14,0x14,0x18,0x7F]
        }
        
        hi_c, lo_c = (color >> 8) & 0xff, color & 0xff
        hi_b, lo_b = (bg >> 8) & 0xff, bg & 0xff
        
       
        for char in str(string):
            bitmap = font.get(char, [0x00, 0x00, 0x00, 0x00, 0x00])
            self.set_window(x, y, x + (6 * size) - 1, y + (8 * size) - 1)
            
            buf = bytearray()
            for page in range(8 * size):
                y_pixel = page // size
                for col in range(6 * size):
                    x_pixel = col // size
                    if x_pixel < 5 and (bitmap[x_pixel] & (1 << y_pixel)):
                        buf.append(hi_c); buf.append(lo_c)
                    else:
                        buf.append(hi_b); buf.append(lo_b)
                        
            self.dc.high()
            self.cs.low()
            self.spi.write(buf)
            self.cs.high()
            x += 6 * size

def color565(r, g, b):
    return (r & 0xf8) << 8 | (g & 0xfc) << 3 | b >> 3