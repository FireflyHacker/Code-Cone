from random import randint
from tkinter import *
from tkinter import ttk
from PIL import ImageTk, Image
import time
import serial
import petcontroller
from threading import Thread
import _TTS

pictures = {
    "alone":["./faces/alone1.png","./faces/alone2.png","./faces/alone3.png"],
    "bored":["./faces/bored1.png","./faces/bored2.png","./faces/bored3.png","./faces/bored4.png","./faces/bored5.png"],
    "excited":["./faces/excited1.png","./faces/excited2.png","./faces/excited3.png","./faces/excited4.png","./faces/excited5.png"],
    "awake":["./faces/awake.png"],
    "confused":["./faces/confused.png"],
    "dread":["./faces/dread.png"],
    "frustrated":["./faces/frustrated1.png","./faces/frustrated2.png"],
    "full":["./faces/full1.png","./faces/full2.png"],
    "joke":["./faces/hacker1.png","./faces/hacker2.png","./faces/hacker3.png","./faces/hacker4.png","./faces/hacker5.png"],
    "happy":["./faces/happy1.png","./faces/happy2.png","./faces/happy3.png","./faces/happy4.png","./faces/happy5.png","./faces/happy6.png","./faces/happy7.png"],
    "laughing":["./faces/laughing.png"],
    "looking":["./faces/looking1.png","./faces/looking2.png","./faces/looking3.png","./faces/looking4.png","./faces/looking5.png","./faces/looking6.png","./faces/looking7.png","./faces/looking8.png"],
    "sad":["./faces/sad1.png","./faces/sad2.png","./faces/sad3.png"],
    "shocked":["./faces/shocked1.png","./faces/shocked2.png"],
    "sleep":["./faces/sleep1.png","./faces/sleep2.png","./faces/sleep3.png"],
    "smart":["./faces/smart1.png","./faces/smart2.png"],
    "thanks":["./faces/thanks.png"],
    "tired":["./faces/tired.png"]
}

class BytePet:
    def __init__(self, root):
        root.title("Byte Pet")
        root.geometry('1920x1080')

        self.ser = SerialPortManager()
        self.ser.start()

        mainframe = ttk.Frame(root)
        mainframe.pack(fill="both", expand=True)

        self.image_label = ttk.Label(mainframe, relief="ridge", borderwidth=5)
        self.image_label.image = ImageTk.PhotoImage(Image.open("./faces/alone1.png").resize((1080, 1080)))
        self.image_label['image'] = self.image_label.image

        stats_frame = ttk.Frame(mainframe, relief="ridge", borderwidth=5)
        self.stats_label = ttk.Label(stats_frame, text="Stats")
        self.text_label = ttk.Label(stats_frame, text="THIS IS THE TALKING PET")
        self.stats_display_lable = ttk.Label(stats_frame, text="THIS IS THE HEALTH AND SHIT")

        self.stats_label.grid(column=0, row=0, sticky="N W")
        self.text_label.grid(column=0, row=1, sticky="N W")
        self.stats_display_lable.grid(column=0, row=2, sticky="N W")
        self.image_label.pack(side="left", fill="both", expand=False)
        stats_frame.pack(side="right", fill="both", expand=True)

        self.pet_loop()
        self.ser_loop()

    def pet_loop(self):
        petcontroller.idle_faces()
        petcontroller.fix_numbers()
        if petcontroller.face != petcontroller.save['lastface']:
            petcontroller.save['lastface'] = petcontroller.face
            i = 0
            if len(pictures[petcontroller.face]) != 1:
                i = randint(0, len(pictures[petcontroller.face])-1)
            print(i)
            self.image_label.image = ImageTk.PhotoImage(Image.open(pictures[petcontroller.face][i]).resize((1080, 1080)))
            self.image_label['image'] = self.image_label.image

        petcontroller.print_new_face()
        if petcontroller.text != petcontroller.save['lasttext']:
            petcontroller.save['lasttext'] = str(petcontroller.text)
            self.text_label['text'] = petcontroller.text
            tts = _TTS._TTS()
            tts.start(petcontroller.text)
            del(tts)
        self.stats_display_lable['text'] = "Hunger: " + str(round(petcontroller.save['hunger'])) + "\nMood: " + str(round(petcontroller.save['mood'])) + "\nSocial: " + str(round(petcontroller.save['social']))
        root.after(1000, self.pet_loop)

    def ser_loop(self):
        buf = self.ser.read_buffer()
        if bytearray(buf) != bytearray():
            petcontroller.new_barcode(str(buf))
            print(str(buf))
        root.after(250, self.ser_loop)


class SerialPortManager:
    # A class for management of serial port data in a separate thread
    def __init__(self):
        self.isRunning = False
        self.serialPort = serial.Serial('COM8', 9600)
        # Create a byte array to store incoming data
        self.serialPortBuffer = bytearray()

    def start(self):
        self.isRunning = True
        self.serialPortThread = Thread(target=self.thread_handler)
        self.serialPortThread.start()

    def stop(self):
        self.isRunning = False

    def thread_handler(self):
        while self.isRunning:
            # Wait until there is data waiting in the serial buffer
            while self.serialPort.in_waiting > 0:
                # Read only one byte from serial port
                serialPortByte = self.serialPort.read(1)
                self.serialPortBuffer.append(int.from_bytes(serialPortByte, byteorder='big'))
                # Process incoming bytes
                self.main_process(serialPortByte)

        if self.serialPort.is_open:
            self.serialPort.close()

    def read_buffer(self):
        # Return a copy of serial port buffer
        buffer = self.serialPortBuffer
        # Clear serial port buffer
        self.serialPortBuffer = bytearray()
        return buffer

    def __del__(self):
        if self.serialPort.is_open:
            self.serialPort.close()

    def main_process(self, inputByte):
        # Print the received byte in Python terminal
        try:
            character = inputByte.decode("ascii")
        except UnicodeDecodeError:
            pass
        else:
            print(character, end="")


if __name__ == "__main__":
    root = Tk()
    ttk.Style().theme_use('classic')
    BytePet(root)
    root.mainloop()
