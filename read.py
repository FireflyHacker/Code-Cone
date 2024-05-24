from urllib import request, parse
import time
import serial
import petcontroller
import guiPet
from threading import Thread

ser = serial.Serial('COM4', 9600)
data = ""
ready = False


def scanner():
    global data
    output = ''
    while output == '':
        output = ser.readline()

    if output:
        try:
            data = output.decode(encoding="latin-1")
        except Exception as e:
            print("ERROR: " + str(e))


def pet_loop():
    while not ready:
        petcontroller.idle_faces()
        petcontroller.fix_numbers()
        petcontroller.print_new_face()
        time.sleep(1)


if __name__ == "__main__":
    gui_thread = Thread(target=guiPet.start_gui())
    gui_thread.start()

    while True:
        # Start threads
        pet_thread = Thread(target=pet_loop)
        scanner_thread = Thread(target=scanner)
        scanner_thread.start()
        pet_thread.start()
        # Wait for scanner returns with data we need
        scanner_thread.join()
        # Tell the pet loop thread we are ready for it
        ready = True
        # Wait for the petcontroller to finish its current update
        pet_thread.join()
        # Update the barcode data
        petcontroller.new_barcode(data)
        petcontroller.print_new_face()
        data = ""
        # Not ready for pet loop yet
        ready = False

