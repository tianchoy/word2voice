# 引入插件
import pyttsx3
from tkinter import *

#执行阅读的函数，必须放在调用之前
def runBuild():
    word = text.get('1.0', 'end')
    engine.say(word)
    engine.runAndWait()
    engine.stop

#初始化文字转语音插件
engine = pyttsx3.init()
engine.setProperty("rate",150)
engine.setProperty("volume",1)
voice = engine.getProperty("voices")
engine.setProperty('voice',voice[0].id)

#初始化界面插件
root = Tk()
root.geometry('550x270')
root.title("文字转语音V0.1")

label1 = Label(root,text="把文字填进去")
label1.place(relx=0,rely=0.1,relwidth=0.2,relheight=0.1)

text = Text(root)
text.place(relx=0.03,rely=0.2,relwidth=0.94,relheight=0.5)

btn = Button(root,text="阅读",command=runBuild)
btn.place(relx=0.03, rely=0.8, relwidth=0.1, relheight=0.1)

root.mainloop()