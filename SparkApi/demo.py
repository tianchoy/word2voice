import tkinter as tk
import pyaudio
import wave


def record(filename):
    print(filename)
    p = pyaudio.PyAudio()
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    RATE = 16000
    CHUNK = 1024

    stream = p.open(rate=RATE,
                    format=FORMAT,
                    channels=CHANNELS,
                    input=True,
                    frames_per_buffer=CHUNK)

    frames = []
    recording = False
    print('111111')
    while True:
        data = stream.read(CHUNK)
        if not data:  # 如果录音意外停止...  
            print('录音意外停止!')
            break
        frames.append(data)
        print('22222')

    print('33333')

    stream.stop_stream()
    stream.close()
    p.terminate()
    print('444444')

    wf = wave.open(filename, 'wb')

    print(wf)

    wf.setframerate(RATE)
    wf.setnchannels(CHANNELS)
    wf.setsampwidth(p.get_sample_size(FORMAT))

    wf.writeframes(b''.join(frames))
    wf.close()


def start_recording():
    global recording
    recording = True
    print("开始录音...")


def stop_recording():
    global recording
    recording = False
    print("录音结束。")
    record("output.wav")  # 调用record函数来保存录制的音频  


root = tk.Tk()  # 创建一个Tkinter窗口  
root.title("录音控制")  # 设置窗口标题  

start_button = tk.Button(root, text="开始录音", command=start_recording)  # 创建开始录音按钮并绑定点击事件处理函数  
start_button.pack()  # 添加到窗口中  

stop_button = tk.Button(root, text="结束录音", command=stop_recording)  # 创建结束录音按钮并绑定点击事件处理函数  
stop_button.pack()  # 添加到窗口中  

root.mainloop()  # 启动Tkinter事件循环，显示窗口并等待用户交互操作
