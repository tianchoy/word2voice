import pyttsx3
from tkinter import *

engine = pyttsx3.init()

def onStart(name):
    print('开始说话:')

def onEnd(name, completed):
    print('说话结束:',  completed)

engine.connect('started-utterance', onStart)
engine.connect('finished-utterance', onEnd)

engine.setProperty('rate',150)
engine.setProperty('volume',1)

voices = engine.getProperty('voices')
engine.setProperty('voice',voices[0].id)

def run1():
     a = input(inp1.get())
     b = input(inp2.get())
     print(a)
     print(b)
    #  engine.say('你好，你叫'+a+'你的年龄是：'+b+'岁,对吗？')
    #  engine.runAndWait()
    #  engine.stop
    #  s =  (a, b, a + b)
    #  txt.insert(END, s)   # 追加显示运算结果
def run2():
     inp1.delete(0, END)  # 清空输入
     inp2.delete(0, END)  # 清空输入

root = Tk()
root.geometry('460x240')
root.title('文字转语音')

lb1 = Label(root, text='请输入两个数，按下面按钮进行加法计算')
lb1.place(relx=0.1, rely=0.1, relwidth=0.8, relheight=0.1)
inp1 = Entry(root)
inp1.place(relx=0.1, rely=0.2, relwidth=0.3, relheight=0.1)
inp2 = Entry(root)
inp2.place(relx=0.6, rely=0.2, relwidth=0.3, relheight=0.1)

# 方法-直接调用 run1()
btn1 = Button(root, text='加法', command=run1)
btn1.place(relx=0.1, rely=0.4, relwidth=0.3, relheight=0.1)

# 方法二利用 lambda 传参数调用run2()
btn2 = Button(root, text='清空', command=lambda: run2())
btn2.place(relx=0.6, rely=0.4, relwidth=0.3, relheight=0.1)

# 在窗体垂直自上而下位置60%处起，布局相对窗体高度40%高的文本框
txt = Text(root)
txt.place(rely=0.6, relheight=0.4)

root.mainloop()




# 