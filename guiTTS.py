#!/usr/bin/env python
import PySimpleGUI as sg
from pygame import mixer
import time
import os
import _TTS


layout = [[sg.Text('What would you like me to say?')],
          [sg.MLine(size=(60, 10), enter_submits=True)],
          [sg.Button('Speak', bind_return_key=True), sg.Exit()]]

window = sg.Window('Text to Speech', layout)

i = 0
#mixer.init()

if __name__ == "__main__":
    while True:
        event, values = window.read()
        if event in (sg.WIN_CLOSED, 'Exit'):
            break
        # Get the text and convert to mp3 file
        tts = _TTS._TTS()
        tts.save(values[0], 'speech{}.wav'.format(i))
        del tts
        # playback the speech
        mixer.init()
        mixer.music.load('speech{}.wav'.format(i))
        mixer.music.play()
        # wait for playback to end
        while mixer.music.get_busy():
            time.sleep(.1)
        mixer.stop()
        i += 1

    window.close()

    # try to remove the temp files. You'll likely be left with 1 to clean up
    try:
        for j in range(i):
            os.remove('speech{}.wav'.format(j))
    except:
        pass
