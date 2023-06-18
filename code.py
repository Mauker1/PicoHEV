import board
import busio
import audiomp3
import audiobusio
import time
from digitalio import DigitalInOut, Direction, Pull
import pwmio
from adafruit_motor import servo
import displayio
from adafruit_st7735r import ST7735R
import terminalio
from adafruit_display_text import label
import adafruit_imageload
from adafruit_display_shapes.rect import Rect
from adafruit_display_shapes.circle import Circle
from adafruit_display_shapes.roundrect import RoundRect
from adafruit_display_shapes.triangle import Triangle
import adafruit_ina219

def blink(times):
    for _ in range(times):
        led.value = False
        time.sleep(0.1)
        led.value = True
        time.sleep(0.1)

def close_keyboard(servo):
    print("Closing keyboard...")
    servo.angle = 20
    time.sleep(0.5)
    print("Done.")

def open_keyboard(servo):
    print("Opening keyboard...")
    servo.angle = 180
    time.sleep(0.5)
    print("Done.")

# Servo test
def servo_direct_test():
    print("servo test: 0")
    servo1.angle = 0
    time.sleep(2)
    print("servo test: 180")
    servo1.angle = 180  # Open
    time.sleep(2)
    servo1.angle = 0  # Closed

# Servo smooth test
def servo_smooth_test():
    print("servo smooth test: 180 - 0, -1º steps")
    for angle in range(180, 0, -9):  # 180 - 0 degrees, -1º at a time.
        servo1.angle = angle
        time.sleep(0.01)
    time.sleep(1)
    print("servo smooth test: 0 - 180, 1º steps")
    for angle in range(0, 180, 9):  # 0 - 180 degrees, 1º at a time.
        servo1.angle = angle
        time.sleep(0.01)
    time.sleep(1)

def setup():
    close_keyboard(servo1)
    for i in range(50):
        up_can1(i)

    for i in range(50):
        up_can2(i)

    for i in range(50):
        up_can3(i)

    led.value = True
    show_splash()
    reset_front_leds()
    play_splash_sound()
    show_green_leds()
    open_keyboard(servo1)
    hide_splash_screen()
    show_charger_ready()

def up_can1(i):
    can1.duty_cycle = int(i * 2 * 65535 / 100)  # Up
    time.sleep(0.02)

def up_can2(i):
    can2.duty_cycle = int(i * 2 * 65535 / 100)  # Up
    time.sleep(0.02)

def up_can3(i):
    can3.duty_cycle = int(i * 2 * 65535 / 100)  # Up
    time.sleep(0.02)

def down_can1(i):
    can1.duty_cycle = 65535 - int(i * 2 * 65535 / 100)  # Down
    time.sleep(0.02)

def down_can2(i):
    can2.duty_cycle = 65535 - int(i * 2 * 65535 / 100)  # Down
    time.sleep(0.02)

def down_can3(i):
    can3.duty_cycle = 65535 - int(i * 2 * 65535 / 100)  # Down
    time.sleep(0.02)

def show_splash():
    try:
        mainGroup.append(splash)

        splash.append(bg_sprite)

        logo_group.append(circ1)
        logo_group.append(circ2)
        logo_group.append(circ3)
        logo_group.append(circ4)
        logo_group.append(rect1)
        logo_group.append(tria1)
        logo_group.append(tria2)

        splash.append(logo_group)
        splash.append(text_title)
        splash.append(text_subtitle)
        splash.append(text_h3)
        splash.append(text_h4)
    except ValueError:
        pass

def hide_splash_screen():
    try:
        mainGroup.remove(splash)
        splash.remove(bg_sprite)
        logo_group.remove(circ1)
        logo_group.remove(circ2)
        logo_group.remove(circ3)
        logo_group.remove(circ4)
        logo_group.remove(rect1)
        logo_group.remove(tria1)
        logo_group.remove(tria2)
        splash.remove(logo_group)
        splash.remove(text_title)
        splash.remove(text_subtitle)
        splash.remove(text_h3)
        splash.remove(text_h4)
    except ValueError:
        pass

def soft_reset():
    mp3.deinit()
    hide_charger_empty()
    reset_front_leds()
    time.sleep(0.5)
    show_charger_ready()
    show_green_leds()
    open_keyboard(servo1)

def reset_front_leds():
    ledGreen.value = True
    ledYellow.value = True
    ledRed.value = True

def show_green_leds():
    ledGreen.value = True
    ledYellow.value = False
    ledRed.value = False

def show_yellow_leds():
    ledGreen.value = False
    ledYellow.value = True
    ledRed.value = False

def show_red_leds():
    ledGreen.value = False
    ledYellow.value = False
    ledRed.value = True

def play_splash_sound():
    mp3 = audiomp3.MP3Decoder(open("001_hev_startup.mp3", "rb"))
    audio.play(mp3)

    i=0
    c=0
    lim=140
    loadRect = Rect(10, 110, i, 10, fill=0xFFFFFF)
    splash.append(loadRect)
    while audio.playing:
        if i <= lim:
            i += 1
            c += 1
            if c == 5:
                show_green_leds()
            elif c == 10:
                show_yellow_leds()
            elif c == 15:
                show_red_leds()
                c = 0
            splash.append(Rect(10, 110, i, 10, fill=0xFFFFFF))
            time.sleep(0.12)
        pass

    mp3.deinit()
    print("Done playing!")

def play_charging_sound():
    mp3 = audiomp3.MP3Decoder(open("002_Charging.mp3", "rb"))
    audio.play(mp3)
    return mp3

def play_charging_finished_sound():
    mp3 = audiomp3.MP3Decoder(open("003_ChargeEnd.mp3", "rb"))
    audio.play(mp3)
    return mp3

def play_charger_empty_sound():
    mp3 = audiomp3.MP3Decoder(open("004_HEVEmpty.mp3", "rb"))
    audio.play(mp3)
    return mp3

def show_charger_ready():
    try:
        chargerOnGroup.append(hev_tile)
        chargerOnGroup.append(txt_charger)
        chargerOnGroup.append(txt_ready)
        mainGroup.append(chargerOnGroup)
    except ValueError:
        pass

def hide_charger_ready_group():
    try:
        mainGroup.remove(chargerOnGroup)
    except ValueError:
        pass

def hide_hev_tile_green():
    try:
        chargerOnGroup.remove(hev_tile)
    except ValueError:
        pass

def hide_txt_charger():
    try:
        chargerOnGroup.remove(txt_charger)
    except ValueError:
        pass

def hide_ready_text():
    try:
        chargerOnGroup.remove(txt_ready)
    except ValueError:
        pass

def show_charger_online():
    try:
        chargerOnGroup.append(txt_online)
    except ValueError:
        pass

def hide_charger_online():
    try:
        chargerOnGroup.remove(txt_online)
    except ValueError:
        pass

def show_charger_empty():
    try:
        chargerOffGroup.append(hev_depleted_tile)
        chargerOffGroup.append(txt_charger2)
        chargerOffGroup.append(txt_empty)
        mainGroup.append(chargerOffGroup)
    except ValueError:
        pass

def hide_charger_empty():
    try:
        mainGroup.remove(chargerOffGroup)
        chargerOffGroup.remove(hev_depleted_tile)
        chargerOffGroup.remove(txt_charger2)
        chargerOffGroup.remove(txt_empty)
    except ValueError:
        pass

def show_current():
    try:
        chargerCurrentInfoGroup.append(label_current)
        mainGroup.append(chargerCurrentInfoGroup)
    except ValueError:
        pass

def show_power():
    try:
        chargerPowerInfoGroup.append(label_power)
        mainGroup.append(chargerPowerInfoGroup)
    except ValueError:
        pass

def update_current(current):
    label_current.text = "{} mA".format(current)

def update_power(power):
    label_power.text = "{} W".format(power)

def hide_current_and_power():
    try:
        chargerCurrentInfoGroup.remove(label_current)
        chargerPowerInfoGroup.remove(label_power)
        mainGroup.remove(chargerCurrentInfoGroup)
        mainGroup.remove(chargerPowerInfoGroup)
    except ValueError:
        pass

def release_displays():
    print("releasing displays...")
    # Release any resources currently in use for the displays
    displayio.release_displays()

# Constants
SCREEN_TOP_SHIFT = 24
# Initial screen constants
init_title = "H.E.V. Charger"
init_subtitle = "Mauker V. 1.0"
init_h3 = "Disconnected"
init_h4 = "Initializing..."
font = terminalio.FONT
color = 0xFFFFFF
# Display bitmap and colors
color_bitmap = displayio.Bitmap(128, 160, 1)
color_palette = displayio.Palette(4)
color_palette[0] = 0x000000 # Black
color_palette[1] = 0xFFFFFF # White
color_palette[2] = 0x00FF00 # Green
color_palette[3] = 0x0000FF # Red

# Other screen constants
# Show charge ready or online
textCharger = "CHARGER"
textReady = "READY"
textOnline = "ONLINE"
# Charger info
txt_current = "{} mA".format(0)
txt_power = "{} W".format(0)
# Show charge empty
textEmpty = "EMPTY"

# Global vars
# Make the display contexts
mainGroup = displayio.Group()
splash = displayio.Group()
logo_group = displayio.Group()
texts = displayio.Group()
# Charger screen
chargerOnGroup = displayio.Group()
chargerOffGroup = displayio.Group()
chargerCurrentInfoGroup = displayio.Group()
chargerPowerInfoGroup = displayio.Group()

# Energo cans LEDs setup
can1 = pwmio.PWMOut(board.GP18, frequency=5000, duty_cycle=0)
can2 = pwmio.PWMOut(board.GP17, frequency=5000, duty_cycle=0)
can3 = pwmio.PWMOut(board.GP16, frequency=5000, duty_cycle=0)

# INA219 setup
# SCL, SDA
i2c = busio.I2C(board.GP15, board.GP14)
ina219 = adafruit_ina219.INA219(i2c)

# Pico LED setup
led = DigitalInOut(board.LED)
led.direction = Direction.OUTPUT
led.value = False

# Front LEDs setup
ledGreen = DigitalInOut(board.GP19)
ledYellow = DigitalInOut(board.GP20)
ledRed = DigitalInOut(board.GP21)

ledGreen.direction = Direction.OUTPUT
ledYellow.direction = Direction.OUTPUT
ledRed.direction = Direction.OUTPUT

ledGreen.value = False
ledYellow.value = False
ledRed.value = False

release_displays()

# Servo setup
pwm_servo = pwmio.PWMOut(board.GP26, duty_cycle=2 ** 15, frequency=50)
servo1 = servo.Servo(
    pwm_servo, min_pulse=500, max_pulse=2200
)  # tune pulse for specific servo

open_keyboard(servo1)

# Display setup
# spi = busio.SPI(board.SCK1, board.MOSI1, board.MISO1)
# MOSI = Tx = SDA
spi = busio.SPI(board.GP2, board.GP3)
tft_cs = board.GP13
tft_dc_rs = board.GP4

display_bus = displayio.FourWire(
    spi, command=tft_dc_rs, chip_select=tft_cs, reset=board.GP6
)

print("Instantiating display...")
display = ST7735R(display_bus, width=128, height=160)
display.rotation = 270

audio = audiobusio.I2SOut(board.GP10, board.GP11, board.GP9)
mp3 = audiomp3.MP3Decoder(open("001_hev_startup.mp3", "rb"))
mp3.deinit()

# Create the texts
# Splash texts
text_title = label.Label(font, text=init_title, color=color)
text_subtitle = label.Label(font, text=init_subtitle, color=color)
text_h3 = label.Label(font, text=init_h3, color=color)
text_h4 = label.Label(font, text=init_h4, color=color)
# Charger ready/online texts
txt_charger = label.Label(font, text=textCharger, color=color_palette[2])
txt_ready = label.Label(font, text=textReady, color=color_palette[2])
txt_online = label.Label(font, text=textOnline, color=color_palette[2])
# Charger info texts
label_current = label.Label(font, text=txt_current, color=color_palette[2])
label_power = label.Label(font, text=txt_power, color=color_palette[2])
# Empty
txt_charger2 = label.Label(font, text=textCharger, color=color_palette[3])
txt_empty = label.Label(font, text=textEmpty, color=color_palette[3])

# Setup text positions
# Splash text positions
text_title.x = 70
text_title.y = 38

text_subtitle.x = 70
text_subtitle.y = 51

text_h3.x = 70
text_h3.y = 67

text_h4.x = 70
text_h4.y = 91
# Ready/Online texts positions
txt_charger.x = 32
txt_charger.y = SCREEN_TOP_SHIFT + 28
txt_charger.scale = 3

txt_ready.x = 42
txt_ready.y = SCREEN_TOP_SHIFT + 68
txt_ready.scale = 3

txt_online.x = 42
txt_online.y = SCREEN_TOP_SHIFT + 68
txt_online.scale = 3

label_current.x = 10
label_current.y = 120

label_power.x = 80
label_power.y = 120

# Empty texts positions
txt_charger2.x = 32
txt_charger2.y = SCREEN_TOP_SHIFT + 28
txt_charger2.scale = 3

txt_empty.x = 42
txt_empty.y = SCREEN_TOP_SHIFT + 68
txt_empty.scale = 3

# Bitmaps
hevLogo, hevPalette = adafruit_imageload.load("/hev.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
hev_tile = displayio.TileGrid(hevLogo, x = 2, y = 26, pixel_shader=hevPalette)
hevDepletedLogo, hevDepletedPalette = adafruit_imageload.load("/hevDepleted.bmp", bitmap=displayio.Bitmap, palette=displayio.Palette)
hevDepletedPalette[1] = 0x0000FF
hev_depleted_tile = displayio.TileGrid(hevDepletedLogo, x = 2, y = 26, pixel_shader=hevDepletedPalette)

# Splash tile and bitmap
bg_sprite = displayio.TileGrid(color_bitmap, pixel_shader=color_palette, x=0, y=0)
logo_bitmap = displayio.Bitmap(60, 60, 2)
logo_grip = displayio.TileGrid(logo_bitmap, x=2, y=28, pixel_shader=color_palette)

# Splash icon
circ1 = Circle(32, 58, 30, fill=0xFFFFFF, outline=0xFFFFFF)
circ2 = Circle(32, 58, 29, fill=0xFFFFFF, outline=0xFFFFFF)
circ3 = Circle(32, 58, 28, fill=0xFFFFFF, outline=0xFFFFFF)
circ4 = Circle(32, 58, 27, fill=0x000000, outline=0xFFFFFF)
rect1 = Rect(23, 55, 25, 30, fill=0xFFFFFF)
tria1 = Triangle(8,74, 24,74, 24,88, fill=0xFFFFFF)
tria2 = Triangle(48,82, 58,70, 48,55, fill=0xFFFFFF)

# Attach main group to display
display.show(mainGroup)

setup()

isCharging = False
isEmpty = False
lastInfoTime = -1
lastEmptyTime = -1
charger_info_update_time = 10**9
charger_empty_time = 5 * (10**9)
current_threshold = 80
cans_charged = 3
charge_counter = 0

# Main loop
while True:
    # Store the current time
    now = time.monotonic_ns()
    # bus_voltage -> Current on load (V- side)
    # current -> Current in mA
    # power -> Power in watts
#    print("Bus Voltage:                 {} V".format(ina219.bus_voltage))
#    print("Shunt Voltage:               {} mV".format(ina219.shunt_voltage / 1000))
#    print("Current:                     {} mA".format(ina219.current))
#    print("Power:                       {} W".format(ina219.power))
#    print("Power (calculated):          {} W".format((ina219.current/1000) * 12))
#    time.sleep(1)
    current = ina219.current
    power = (current / 1000) * 12 * 0.93

    #print("Current:                     {} mA".format(ina219.current))
    #time.sleep(0.5)
    if current > current_threshold and isCharging == False and isEmpty == False:
        isCharging = True
        isEmpty = False
        mp3 = play_charging_sound()
        hide_ready_text()
        show_charger_online()
        show_current()
        show_power()
        show_yellow_leds()

    if isCharging:
        if charge_counter >= 51:
            charge_counter = 0
            cans_charged -= 1

        if cans_charged == 3:
            down_can3(charge_counter)
        elif cans_charged == 2:
            down_can2(charge_counter)
        elif cans_charged == 1:
            down_can1(charge_counter)
        elif cans_charged == 0:
            up_can1(charge_counter)
            up_can2(charge_counter)
            up_can3(charge_counter)
        else:
            cans_charged = 3
            charge_counter = -1

        charge_counter += 1

        if now > lastInfoTime + charger_info_update_time:
            lastInfoTime = now
            update_current(current)
            update_power(power)

    if current < current_threshold and isCharging:
        isCharging = False
        isEmpty = True
        audio.stop()
        mp3.deinit()
        mp3 = play_charging_finished_sound()
        show_red_leds()
        time.sleep(1)
        mp3.deinit()
        hide_charger_online()
        hide_hev_tile_green()
        hide_txt_charger()
        hide_charger_ready_group()
        hide_current_and_power()
        show_charger_empty()
        mp3 = play_charger_empty_sound()
        close_keyboard(servo1)
        lastEmptyTime = now

    if isEmpty and isCharging == False and (now >= (lastEmptyTime + charger_empty_time)):
        isEmpty = False
        lastEmptyTime = -1
        soft_reset()

    # This seems to be needed, otherwise I'm getting:
    # Traceback (most recent call last):
    #   File "code.py", line 402, in <module>
    #   File "code.py", line 189, in hide_ready_text
    #   ValueError: object not in sequence
    time.sleep(0.1)
