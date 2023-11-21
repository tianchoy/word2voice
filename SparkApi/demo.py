import pyaudio
import wave
import tkinter as tk

class AudioRecorder:
    def __init__(self):
        self.filename = "output.wav"
        self.p = pyaudio.PyAudio()
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        self.RATE = 16000
        self.CHUNK = 1024
        self.frames = []
        self.recording = False
        self.input_device_index = None  # Set to the desired input device index

        self.root = tk.Tk()
        self.root.title("Audio Recorder")

        self.start_button = tk.Button(self.root, text="开始录音", command=self.start_recording)
        self.start_button.pack()

        self.stop_button = tk.Button(self.root, text="停止录音", command=self.stop_recording, state=tk.DISABLED)
        self.stop_button.pack()

        # Find and print available input devices along with their indices
        self.list_input_devices()

    def list_input_devices(self):
        print("Available Input Devices:")
        for i in range(self.p.get_device_count()):
            info = self.p.get_device_info_by_index(i)
            if info['maxInputChannels'] > 0:
                print(f"Index: {info['index']}, Name: {info['name']}, Channels: {info['maxInputChannels']}")

    def start_recording(self):
        if not self.recording:
            self.recording = True
            self.start_button.config(state=tk.DISABLED)
            self.stop_button.config(state=tk.NORMAL)
            print("开始录音...")
            if self.input_device_index is not None:
                self.stream = self.p.open(
                    rate=self.RATE,
                    format=self.FORMAT,
                    channels=self.CHANNELS,
                    input=True,
                    frames_per_buffer=self.CHUNK,
                    input_device_index=self.input_device_index
                )
                self.record_audio()
            else:
                print("请设置输入设备索引！")

    def record_audio(self):
        while self.recording:
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            self.root.update()

    def stop_recording(self):
        if self.recording:
            self.recording = False
            self.start_button.config(state=tk.NORMAL)
            self.stop_button.config(state=tk.DISABLED)
            print("录音结束.")

            if hasattr(self, 'stream') and self.stream.is_active():
                self.stream.stop_stream()
                self.stream.close()
                self.p.terminate()

                wf = wave.open(self.filename, 'wb')
                wf.setnchannels(self.CHANNELS)
                wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
                wf.setframerate(self.RATE)
                wf.writeframes(b''.join(self.frames))
                wf.close()

                self.frames = []  # 清空录音帧数据

    def run(self):
        self.root.mainloop()

# Create an instance of AudioRecorder
audio_recorder = AudioRecorder()
audio_recorder.run()
