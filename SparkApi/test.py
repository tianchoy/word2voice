from tkinter import *
from tkinter.font import Font
import SparkApi
from config import appid,api_secret,api_key,domain,Spark_url,modelType
import threading
import pyperclip
from tkinter import messagebox
import pyttsx3
from ifly.record_voice import record
from ifly.ifly_a2t import audio_to_text
import keyboard


winTitle = '讯飞星火V1.5'
winSize = "800x600"
answerContent = ''
# 初始化窗体
win = Tk()
win.title(winTitle)
win.geometry(winSize)

# 录制用户语音
file = 'user_voice.wav'

# win.withdraw()

# 初始化语音插件
engine = pyttsx3.init()
engine.setProperty('rate',200)
engine.setProperty('volume',1)

voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)


# 滚动条设置
scrollbar = Scrollbar(win)
scrollbar.pack(side=RIGHT, fill=Y)

font = Font(family="Microsoft Yahei", size=10)  # 设置显示字体
text = []
def reads(content):
    engine.say(content)
    engine.runAndWait()
    engine.stop()

def getText(role, content):
    jsoncon = {}
    jsoncon["role"] = role
    jsoncon["content"] = content
    text.append(jsoncon)
    return text


def getlength(text):
    length = 0
    for content in text:
        temp = content["content"]
        leng = len(temp)
        length += leng
    return length


def checklen(text):
    while getlength(text) > 8000:
        del text[0]
    return text

def print_selection():
    print(var.get())
    global domain
    global Spark_url
    global modelType
    if var.get() == 1:
        domain = "general"
        Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"
        modelType = '1.5'
    elif var.get() == 2:
        domain = "generalv2"
        Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"
        modelType = '2.0'
    else :
        domain = "generalv3"
        Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat"
        modelType = '3.0'


def fetch_data():
    global answerContent
    Input = str(inp1.get())
    inputText = ("我：" + Input + '\n')
    texts.insert(END, inputText)
    question = checklen(getText("user", Input))
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    res = ('星火(' + modelType + ')回答：' + SparkApi.answer + '\n\n')
    answerContent = SparkApi.answer
    texts.insert(END, str(res))
    btn.config(text='生成', state='normal')

# 运行函数
def runbuild():
    thread = threading.Thread(target=fetch_data)
    thread.start()
    btn.config(text='生成中…', state='disabled')


# 清空输入
def clearbuild():
    inp1.delete(0, END)  # 清空输入
    texts.delete(1.0, END)



def copyContent():
    content = texts.get("1.0", "end-1c")
    if content != '':
        try:
            pyperclip.copy(content)
            messagebox.showinfo(winTitle, "复制成功")
        except:
            messagebox.showinfo(winTitle, "无法复制")
    else:
        messagebox.showinfo(winTitle, "内容为空？")

# 阅读线程
def readThread():
    if answerContent != '':
        reads(answerContent)
        btn3.config(text='朗读', state='normal')
    else:
        reads('有什么是我可以帮您的吗？')
        btn3.config(text='朗读', state='normal')

# 阅读内容
def readContent():
    thread = threading.Thread(target=readThread)
    thread.start()
    btn3.config(text='朗读中…', state='disabled')

def starts():
    result = messagebox.askyesno("提示：", "按下 A 键开始说话,\n按下 T 键停止说话。")
    # 判断用户选择结果
    if result:
        thread = threading.Thread(target=closed)
        thread.start()
        btn3.config(text='说话中…', state='disabled')
    else:
        messagebox.showinfo('提示','您也可以通过打字来提问')

def closed():
    global text_s
    global answerContent
    record(file)  # 录制音频
    txt_str = audio_to_text(file)  # 语音识别
    inputText = ("我：" + txt_str + '\n')
    texts.insert(END, inputText)
    question = checklen(getText("user", inputText))
    SparkApi.answer = ""
    SparkApi.main(appid, api_key, api_secret, Spark_url, domain, question)
    reads(SparkApi.answer)
    res = ('星火(' + modelType + ')回答：' + SparkApi.answer + '\n\n')
    answerContent = SparkApi.answer
    texts.insert(END, str(res))
    engine.say('即将为您打印出我的回答')
    engine.runAndWait()
    engine.stop()
    btn4.config(text='语音', state='normal')
    btn3.config(text='朗读', state='normal')

# 布局窗体
var = IntVar()
var.set(1) # 设置默认选择1.5模型

inp1 = Entry(win, textvariable=StringVar(value='请输入问题'), font=font)
inp1.place(relx=0.03, rely=0.03, relwidth=0.7, relheight=0.05)

r1 = Radiobutton(win, text="1.5模型", variable=var, value=1, command=print_selection)
r1.pack()
r1.place(relx=0.03, rely=0.1, relwidth=0.08, relheight=0.05)

r2 = Radiobutton(win, text="2.0模型", variable=var, value=2, command=print_selection)
r2.pack()
r2.place(relx=0.13, rely=0.1, relwidth=0.08, relheight=0.05)

r3 = Radiobutton(win, text="3.0模型(New)", variable=var, value=3, command=print_selection, state='disabled')
r3.pack()
r3.place(relx=0.22, rely=0.1, relwidth=0.15, relheight=0.05)

texts = Text(win, wrap=WORD, yscrollcommand=scrollbar.set, font=font, padx=10, pady=10)
texts.place(relx=0.03, rely=0.15, relwidth=0.94, relheight=0.82)
scrollbar.config(command=texts.yview)

btn = Button(win, text="提问", command=runbuild)
btn.place(relx=0.73, rely=0.03, relwidth=0.07, relheight=0.05)

btn1 = Button(win, text="清除", command=clearbuild)
btn1.place(relx=0.8, rely=0.03, relwidth=0.05, relheight=0.05)

btn2 = Button(win, text="复制", command=copyContent)
btn2.place(relx=0.85, rely=0.03, relwidth=0.05, relheight=0.05)

btn3 = Button(win, text="朗读", command=readContent)
btn3.place(relx=0.9, rely=0.03, relwidth=0.07, relheight=0.05)

btn4 = Button(win,text="语音", command=starts)
btn4.place(relx=0.66, rely=0.03, relwidth=0.07, relheight=0.05)

# 载入窗体
win.mainloop()
