from tkinter import *
from tkinter.font import Font
import SparkApi
#以下密钥信息从控制台获取
appid = ""     #填写控制台中获取的 APPID 信息
api_secret = ""   #填写控制台中获取的 APISecret 信息
api_key =""    #填写控制台中获取的 APIKey 信息

#用于配置大模型版本，默认“general/generalv2”
domain = "general"   # v1.5版本
# domain = "generalv2"    # v2.0版本
#云端环境的服务地址
Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"  # v1.5环境的地址
# Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"  # v2.0环境的地址

modelType = '1.5'

win = Tk()
win.title("讯飞星火V1.0")
win.geometry("700x500")

scrollbar = Scrollbar(win)
scrollbar.pack(side=RIGHT, fill=Y)

font = Font(family="Microsoft YaHei", size=10)

text =[]

def getText(role,content):
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
    while (getlength(text) > 8000):
        del text[0]
    return text

def print_selection():
    global domain
    global Spark_url
    global modelType
    if var.get() == 1:
        domain = "general"
        Spark_url = "ws://spark-api.xf-yun.com/v1.1/chat"
        modelType = '1.5'
    else:
        domain = "generalv2"
        Spark_url = "ws://spark-api.xf-yun.com/v2.1/chat"
        modelType = '2.0'



# 运行函数
def runbuild():
    Input = str(inp1.get())
    inputText = ("我：" + Input + '\n')
    texts.insert(END, inputText)
    question = checklen(getText("user",Input))
    SparkApi.answer = ""
    SparkApi.main(appid,api_key,api_secret,Spark_url,domain,question)
    res = ('星火('+modelType+')回答：'+SparkApi.answer+'\n\n')
    texts.insert(END,str(res))


# 布局窗体
var = IntVar()
var.set(1)

r1 = Radiobutton(win, text="1.5模型", variable=var, value=1, command=print_selection)
r1.pack()
r1.place(x=10, y=5, width=100, height=20)

r2 = Radiobutton(win, text="2.0模型", variable=var, value=2, command=print_selection)
r2.pack()
r2.place(x=10, y=25, width=100, height=20)

inp1 = Entry(win, textvariable=StringVar(value='请输入问题'),font=font)
inp1.place(relx=0.15, rely=0.03, relwidth=0.7, relheight=0.05)

texts = Text(win, wrap=WORD,yscrollcommand=scrollbar.set,font=font,padx=10, pady=10)
texts.place(relx=0.03, rely=0.1, relwidth=0.94, relheight=0.85)
scrollbar.config(command=texts.yview)

btn = Button(win, text="生成结果",command=runbuild)
btn.place(relx=0.87, rely=0.03, relwidth=0.1, relheight=0.05)

# 载入窗体
win.mainloop()