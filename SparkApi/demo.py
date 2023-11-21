import tkinter as tk
import pyaudio
import wave

recording = False
frames = []

# 录制用户语音
file = 'user_voice.wav'


def record(filename):
    global recording, frames
    p = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    stream = p.open(rate=RATE, format=FORMAT, channels=CHANNELS, input=True, frames_per_buffer=CHUNK)

    frames = []
    recording = True
    while recording:
        data = stream.read(CHUNK)
        frames.append(data)
        root.update()

    stream.stop_stream()
    stream.close()
    p.terminate()

    wf = wave.open(filename, 'wb')
    wf.setframerate(RATE)
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))
    wf.writeframes(b''.join(frames))
    wf.close()


def start_recording():
    global recording
    recording = True
    print("开始录音...")
    record(file)


def stop_recording():
    global recording
    recording = False
    print("录音结束。")


root = tk.Tk()
root.title("录音控制")

start_button = tk.Button(root, text="开始录音", command=start_recording)
start_button.pack()
stop_button = tk.Button(root, text="结束录音", command=stop_recording)
stop_button.pack()

root.mainloop()
