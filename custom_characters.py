import time
import RPi.GPIO as GPIO
from RPLCD import CharLCD, cleared, cursor
lcd = CharLCD(cols=16, rows=2, pin_rs=8, pin_e=10, pins_data=[12, 16, 18, 22])


up = (
    0b00000,
	0b00100,
	0b00100,
	0b01110,
	0b01110,
	0b11111,
	0b11111,
	0b00000,
)

up1 = (
    0b00000,
	0b00100,
	0b00100,
	0b01110,
	0b01010,
	0b10001,
	0b11111,
	0b00000,
)

down = (
    0b00000,
	0b11111,
	0b11111,
	0b01110,
	0b01110,
	0b00100,
	0b00100,
	0b00000,
)

same = (
    0b00000,
	0b11111,
	0b11111,
	0b00000,
	0b00000,
	0b11111,
	0b11111,
	0b00000,
)

lcd.create_char(0, up1)
lcd.create_char(1, down)
lcd.create_char(2, same)

def main():
	# Main program block
	GPIO.setwarnings(False)
	lcd.write_string(unichr(0))
	lcd.write_string(unichr(1))
	lcd.write_string(unichr(2))
	time.sleep(25)

if __name__  ==  '__main__':

	try:
		main()
	except KeyboardInterrupt:
		pass
	finally:
		lcd.clear()
		GPIO.cleanup()
