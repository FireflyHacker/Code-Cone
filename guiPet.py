from random import randint
from nicegui import ui
import time
import serial
import petcontroller
from threading import Thread

pictures = {
    "alone": ["./faces/icecream_alone.png"],
    "bored": ["./faces/icecream_bored.png"],
    "excited": ["./faces/icecream_excited.png"],
    "awake": ["./faces/icecream.png"],
    "confused": ["./faces/icecream.png"],
    "dread": ["./faces/icecream.png"],
    "frustrated": ["./faces/icecream.png"],
    "full": ["./faces/icecream.png"],
    "joke": ["./faces/icecream_joke.png"],
    "happy": ["./faces/icecream_happylook.png"],
    "laughing": ["./faces/icecream_excited.png"],
    "looking": ["./faces/icecream_looking1.png", "./faces/icecream_looking2.png"],
    "sad": ["./faces/icecream_sad.png"],
    "shocked": ["./faces/icecream.png"],
    "sleep": ["./faces/icecream_sleeping.png"],
    "smart": ["./faces/icecream_excited.png"],
    "thanks": ["./faces/icecream_thanks.png"],
    "tired": ["./faces/icecream_sleeping.png"]
}


class BytePet:
    @ui.refreshable
    def stats(self, hunger: str, mood: str, social: str, chatlog: [str]):
        with ui.column().classes("h-full col-4"):
            with ui.column().classes("h-1/6 p-5"):
                ui.label(f'Hunger: {hunger}').classes("text-left text-3xl")
                ui.label(f'Mood: {mood}').classes("text-left text-3xl")
                ui.label(f'Social: {social}').classes("text-left text-3xl")
            with ui.scroll_area().classes("h-5/6 w-full p-5"):
                ui.chat_message(chatlog)

    def __init__(self):
        self.ser = SerialPortManager()
        self.chatlog = ['zzzzzzzzz']
        ui.image("./faces/codecone.png").classes("h-20 w-48 z-10 absolute top-0 left-0 m-2")

        with ui.grid(columns=2).classes("w-full gap-0"):
            self.image_label = ui.image(pictures['sleep'][0]).classes("col-8")
            self.stats('8','8','8',self.chatlog)

        ui.timer(1.0, self.pet_loop)
        ui.timer(0.25, self.ser_loop)
        ui.run()

    def pet_loop(self):
        petcontroller.idle_faces()
        petcontroller.fix_numbers()
        if petcontroller.face != petcontroller.save['lastface']:
            petcontroller.save['lastface'] = petcontroller.face
            i = 0
            if len(pictures[petcontroller.face]) != 1:
                i = randint(0, len(pictures[petcontroller.face]) - 1)
            self.image_label.set_source(pictures[petcontroller.face][i])

        if petcontroller.text != petcontroller.save['lasttext']:
            petcontroller.save['lasttext'] = str(petcontroller.text)
            self.chatlog.insert(0, str(petcontroller.text))

        self.stats.refresh(str(round(petcontroller.save['hunger'])), str(round(petcontroller.save['mood'])),
                           str(round(petcontroller.save['social'])), self.chatlog)

    def ser_loop(self):
        if not self.ser.isRunning:
            self.ser.openPort()
            self.ser.start()
        buf = self.ser.read_buffer()
        if bytearray(buf) != bytearray():
            petcontroller.new_barcode(str(buf))
            print(str(buf))


class SerialPortManager:
    # A class for management of serial port data in a separate thread
    def __init__(self):
        try:
            self.openPort()
            self.serialPort = None
            self.isRunning = False
            self.serialPortBuffer = bytearray()
        except Exception as e:
            print("Barcode Reader ERROR:", str(e))
            exit(0)

    def openPort(self):
        try:
            self.serialPort = serial.Serial('COM4', 9600)
            print("connected")
            self.isRunning = False
        except:
            print("ERROR")

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


BytePet()
