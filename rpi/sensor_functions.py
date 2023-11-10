import time
#import board
import busio
from digitalio import DigitalInOut, Direction
import adafruit_fingerprint

#led = DigitalInOut(board.D13)
#led.direction = Direction.OUTPUT

# uart = busio.UART(board.TX, board.RX, baudrate=57600)

# If using with a computer such as Linux/RaspberryPi, Mac, Windows with USB/serial converter:
import serial
#uart = serial.Serial("/dev/ttyUSB0", baudrate=57600, timeout=1)

#finger = adafruit_fingerprint.Adafruit_Fingerprint(uart)

#Fingerprint sensor API found at: https://docs.circuitpython.org/projects/fingerprint/en/latest/api.html
##################################################

def get_num():
    """Use input() to get a valid number from 1 to 127. Retry till success!"""
    i = 0
    while (i > 127) or (i < 1):
        try:
            i = int(input("Enter ID # from 1-127: "))
        except ValueError:
            pass
    return i

def get_fingerprint():
#    """Get a finger print image, template it, and see if it matches!"""
#    print("Waiting for image...")
#    while finger.get_image() != adafruit_fingerprint.OK:
#        pass
#    print("Templating...")
#    if finger.image_2_tz(1) != adafruit_fingerprint.OK:
#        return False
#    print("Searching...")
#    if finger.finger_search() != adafruit_fingerprint.OK:
#        return False
#    return True


# pylint: disable=too-many-branches
def get_fingerprint_detail():
    """Get a finger print image, template it, and see if it matches!
    This time, print out each error instead of just returning on failure"""
    print("Getting image...", end="")
    i = finger.get_image()
    if i == adafruit_fingerprint.OK:
        print("Image taken")
    else:
        if i == adafruit_fingerprint.NOFINGER:
            print("No finger detected")
        elif i == adafruit_fingerprint.IMAGEFAIL:
            print("Imaging error")
        else:
            print("Other error")
        return False

    print("Templating...", end="")
    i = finger.image_2_tz(1)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False

    print("Searching...", end="")
    i = finger.finger_fast_search()
    # pylint: disable=no-else-return
    # This block needs to be refactored when it can be tested.
    if i == adafruit_fingerprint.OK:
        print("Found fingerprint!")
        return True
    else:
        if i == adafruit_fingerprint.NOTFOUND:
            print("No match found")
        else:
            print("Other error")
        return False


# pylint: disable=too-many-statements
def enroll_finger():
    location = get_num()
    """Take a 2 finger images and template it, then store in 'location'"""
    for fingerimg in range(1, 3):
        if fingerimg == 1:
            print("Place finger on sensor...", end="")
        else:
            print("Place same finger again...", end="")

        while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

        print("Templating...", end="")
        i = finger.image_2_tz(fingerimg)
        if i == adafruit_fingerprint.OK:
            print("Templated")
        else:
            if i == adafruit_fingerprint.IMAGEMESS:
                print("Image too messy")
            elif i == adafruit_fingerprint.FEATUREFAIL:
                print("Could not identify features")
            elif i == adafruit_fingerprint.INVALIDIMAGE:
                print("Image invalid")
            else:
                print("Other error")
            return False

        if fingerimg == 1:
            print("Remove finger")
            time.sleep(1)
            while i != adafruit_fingerprint.NOFINGER:
                i = finger.get_image()

    print("Creating model...", end="")
    i = finger.create_model()
    if i == adafruit_fingerprint.OK:
        print("Created")
    else:
        if i == adafruit_fingerprint.ENROLLMISMATCH:
            print("Prints did not match")
        else:
            print("Other error")
        return False

    print("Storing model #%d..." % location, end="")
    i = finger.store_model(location)
    if i == adafruit_fingerprint.OK:
        print("Stored")
    else:
        if i == adafruit_fingerprint.BADLOCATION:
            print("Bad storage location")
        elif i == adafruit_fingerprint.FLASHERR:
            print("Flash storage error")
        else:
            print("Other error")
        return False

    return True

##################################################
# CUSTOM FUNCTIONS:

# Check sensor status: returns boolean true/false
'''
Check function can be used in the application to make sure that the sensor is connected properly before attempting to use it
If the check is unsuccesful an info display can show the user to connect the sensor to the device for example.
'''
def check():
    return finger.check_module()

# Soft reset for the sensor
'''
The soft reset sends the _SOFTRESET = const(0x3D) packet that the sensor must acknowledge receiving, otherwise a runtime error is raised.
This functionality can be useful to resolve possible error states in the application going forward.
'''
def reset():
    finger.soft_reset()

# Targeted search function
'''
Targeted search takes a location as a parameter and loads a model stored to that location. It then proceeds taking an image with the sensor, and templating it to another slot.
The compare templates sensor function operates on slots 1 & 2, so they are used on this function. The stored location template is loaded on slot 1 and the taken image template on slot 2.
'''
def search_location(location):
    # Load a template model to slot '1'
    finger.load_model(location,1)
    print("Place finger to the sensor")
    # Take image from the sensor
    while True:
            i = finger.get_image()
            if i == adafruit_fingerprint.OK:
                print("Image taken")
                break
            if i == adafruit_fingerprint.NOFINGER:
                print(".", end="")
            elif i == adafruit_fingerprint.IMAGEFAIL:
                print("Imaging error")
                return False
            else:
                print("Other error")
                return False

    # Template the image to validate with existing image
    print("Templating...", end="")
    i = finger.image_2_tz(2)
    if i == adafruit_fingerprint.OK:
        print("Templated")
    else:
        if i == adafruit_fingerprint.IMAGEMESS:
            print("Image too messy")
        elif i == adafruit_fingerprint.FEATUREFAIL:
            print("Could not identify features")
        elif i == adafruit_fingerprint.INVALIDIMAGE:
            print("Image invalid")
        else:
            print("Other error")
        return False
    
    if (finger.compare_templates() == adafruit_fingerprint.OK):
        print("Fingerprint matched! Welcome.")
        return True
    return False
