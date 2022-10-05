import io
import numbers
import os
import tempfile

from flask import Flask, render_template, request, send_file
from flask_socketio import SocketIO
from random import randint
from threading import Lock

import pyttsx3
engine_tts = pyttsx3.init()

# Background Thread
thread = None
thread_lock = Lock()

app = Flask(__name__, template_folder="./")
app.config['SECRET_KEY'] = 'jscblbcsdjhk!'
socketio = SocketIO(app, cors_allowed_origins='*')


def generate_sound_file(text: str, voice: int, rate: float, volume: float):
    temp_file = io.BytesIO()
    with tempfile.TemporaryDirectory() as temp_dir:
        voice = engine_tts.getProperty('voices')[voice]
        engine_tts.setProperty('voice', voice.id)
        engine_tts.setProperty('rate', rate)  # default is 200
        engine_tts.setProperty('volume', volume)
        file_name = 'sound.mp3'
        file_name = os.path.join(temp_dir, file_name)
        engine_tts.save_to_file(text, file_name)
        engine_tts.runAndWait()
        while not os.listdir(temp_dir):
            pass
        temp_file = io.BytesIO(open(file_name, 'rb').read())
    return temp_file


def background_thread():
    """ Trigger the audio player. """
    number = 0
    while True:
        file = generate_sound_file(text=str(number), voice=0, rate=200, volume=1).read()
        socketio.emit('audio', {'control': 'play', 'file': file})
        print("Say:", number)
        number += 1
        # A random delay
        socketio.sleep(randint(0, 3) + 5)


# @app.route('/a')
# def returnAudioFile():
#     """ Send audio. """
#     # path_to_audio_file = "/path/to/file"  # audio from project dir
#     # return send_file(
#     #    path_to_audio_file,
#     #    mimetype="audio/wav",
#     #    as_attachment=True,
#     #    attachment_filename="test.wav")
#     number_to_speak = number.get()
#     number.put(number_to_speak + 1)
#     print('hit', number_to_speak)
#     file = send_file(generate_sound_file(
#         text=str(number_to_speak), voice=0, rate=200, volume=1),
#         download_name='sound.mp3')

#     response = make_response(file)
#     response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
#     response.headers["Pragma"] = "no-cache"
#     response.headers["Expires"] = "0"
#     response.headers['Cache-Control'] = 'public, max-age=0'
#     return response

@app.route('/')
def index():
    """ Serve root index file ."""
    return render_template('index.htm')


@socketio.on('connect')
def connect():
    """ Decorator for connect. """
    global thread
    print('Websocket client connected')

    global thread
    with thread_lock:
        if thread is None:
            thread = socketio.start_background_task(background_thread)


@socketio.on('disconnect')
def disconnect():
    """ Decorator for disconnect. """
    print('Websocket client disconnected',  request.sid)


if __name__ == '__main__':
    socketio.run(app)
