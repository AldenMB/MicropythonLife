from machine import Pin, I2C
from ssd1306 import SSD1306_I2C
from life import Life
from time import sleep

i2c = I2C(0, sda=Pin(0), scl=Pin(1), freq=400_000)
oled = SSD1306_I2C(128, 64, i2c)

oled.text("Welcome to the", 0, 0)
oled.text("Game", 20, 20)
oled.text("of", 55, 30)
oled.text("Life", 80, 40)
oled.show()

life = Life((128, 64), oled.buffer)
parity = bytearray(128 * 64 // 8)
while True:
    life.randomize()
    oled.show()
    # apply brent's cycle detection algorithm
    power = lam = 1
    while life.buffer != parity:
        if power == lam:
            parity[:] = life.buffer
            # This should identify loops a bit quicker,
            # since they are generally small:
            power += 1  # *= 2
            lam = 0
        life.step()
        lam += 1
        oled.show()

    oled.fill_rect(0, 0, 57, 10, 0)
    oled.text("Looped!", 0, 0)
    oled.show()
    sleep(30)
