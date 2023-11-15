from openai import OpenAI, APIError, APITimeoutError
from tkinter import *

# //初始化
client = OpenAI()
win = Tk()

win.title("GPT生成器V0.1")
win.geometry("600x400")

# 运行函数
def runbuild():
    word =inp1.get('1.0', 'end')
    text.delete(1.0, END)
    try:
        completion = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "system", 'content': word}
            ]
        )
        print(completion['choices'][0]['message']['content'])
        result = completion['choices'][0]['message']['content']

    except APITimeoutError as err:
        print(f"openAI API Timeout Error: {err}")
        result = err
    except APIError as err:
        print(f"openAI API Error: {err}")
        result = err
    except Exception as err:
        print(f"An unexpected error occurred: {err}")
        result = err

    text.insert(END,result)


# 布局窗体
lab1 = Label(win, text="输入问题:")
lab1.place(relx=-0.07, rely=0.01, relwidth=0.3, relheight=0.1)

inp1 = Text(win)
inp1.place(relx=0.15, rely=0.03, relwidth=0.7, relheight=0.05)

text = Text(win)
text.place(relx=0.03, rely=0.1, relwidth=0.94, relheight=0.85)

btn = Button(win, text="生成结果", command=runbuild)
btn.place(relx=0.87, rely=0.03, relwidth=0.1, relheight=0.05)

# 载入窗体
win.mainloop()