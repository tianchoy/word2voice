import pyttsx3

engine = pyttsx3.init()

name = input('请输入你的名字:')
age = input('请输入你的年龄:')


def onStart():
    print('开始说话:')


def onEnd(completed):
    print('说话结束:', completed)


engine.connect('started-utterance', onStart)
engine.connect('finished-utterance', onEnd)

engine.setProperty('rate', 150)
engine.setProperty('volume', 1)
voices = engine.getProperty('voices')
engine.setProperty('voice', voices[0].id)
engine.say('你好，你叫' + name + '你的年龄是：' + age + '岁,对吗？')
engine.runAndWait()
engine.stop()
