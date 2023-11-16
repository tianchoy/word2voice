from tkinter import *
from tkinter.font import Font
import SparkApi
import threading
import pyperclip
from tkinter import messagebox
import pyttsx3

# 以下密钥信息从控制台获取
appid = ""  # 填写控制台中获取的 APPID 信息
api_secret = ""  # 填写控制台中获取的 APISecret 信息
api_key = ""  # 填写控制台中获取的 APIKey 信息

# 用于配置大模型版本，默认“general/generalv2”
domain = "general"  # v1.5版本
# domain = "generalv2"    # v2.0版本
# domain = "generalv3"   #v3.0版本
# 云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v3.1/chat" #v3.0环境地址
modelType = '1.5'
winTitle = '讯飞星火V1.3'
winSize = "750x550"
answerContent = ''

# 初始化窗体
win = Tk()
win.title(winTitle)
win.geometry(winSize)


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
        messagebox.showinfo(winTitle, "空内容复制个啥？")

# 阅读线程
def readThread():
    if answerContent != '':
        reads(answerContent)
        btn3.config(text='朗读', state='normal')
    else:
        reads('你好歹先问个问题，你啥也不问，我说啥？')
        btn3.config(text='朗读', state='normal')

# 阅读内容
def readContent():
    thread = threading.Thread(target=readThread)
    thread.start()
    btn3.config(text='朗读中…', state='disabled')

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

btn = Button(win, text="生成", command=runbuild)
btn.place(relx=0.73, rely=0.03, relwidth=0.07, relheight=0.05)

btn1 = Button(win, text="清除", command=clearbuild)
btn1.place(relx=0.8, rely=0.03, relwidth=0.05, relheight=0.05)

btn2 = Button(win, text="复制", command=copyContent)
btn2.place(relx=0.85, rely=0.03, relwidth=0.05, relheight=0.05)

btn3 = Button(win, text="朗读", command=readContent)
btn3.place(relx=0.9, rely=0.03, relwidth=0.07, relheight=0.05)

# 载入窗体
win.mainloop()
