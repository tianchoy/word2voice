from ifly.record_voice import record
from ifly.ifly_a2t import audio_to_text
file = 'user_voice.wav'           # 语音录制，识别文件
record(file)                # 录制音频 
txt_str = audio_to_text(file)               # 语音识别
print(txt_str)                              # 打印识别结果
