import time

import uiautomation as ui
import pyperclip
import openai
wx=ui.WindowControl(Name="微信") #绑定名为微信的主窗口控件
wx.SwitchToThisWindow() # 切换窗口
hw=wx.ListControl(Name="会话") # 寻找会话控件绑定
history_dic={"user":[],"assistant":[]}
msg = ""
while True:  #循环等待消息
    time.sleep(1)
    try:
        we=hw.TextControl(serchDepth=4) #查找未读信息
        if we.Name:
                    we.Click(simulateMove=False) #点击未读信息
                    lastMsg=wx.ListControl(Name="消息").GetChildren()[-1].Name
                    print(lastMsg)
                    #自己发的消息就不读取
                    if lastMsg == msg:
                        continue
                    #填写自己的key,每个账号都有自己的key
                    openai.api_key = "sk-xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                    #openai.organization="org-xxxxxxxxxxxxxxxxxxxxxxxxxxxx"
                    # 发送内容给chatgpt
                    messages=[
                        {"role": "system", "content": "你是一个AI助手"},
                    ]
                    # 存储前十次的聊天记录实现上下文对话
                    if len(history_dic['user'])>10:
                        for i in range(10):
                            messages.append({"role":"user","content":history_dic['user'][-(10-i)]})
                            messages.append({"role":"assistant","content":history_dic['assistant'][-(10-i)]})
                    else:
                        for i in range(len(history_dic['user'])):
                            messages.append({"role": "user", "content": history_dic['user'][-(len(history_dic['user']) - i)]})
                            messages.append({"role": "assistant", "content": history_dic['assistant'][-(len(history_dic['user'])  - i)]})
                    messages.append({"role":"user","content":lastMsg})
                    response = openai.ChatCompletion.create(
                        model="gpt-3.5-turbo",
                        messages=messages
                    )
                    msg=""
                    # 把chatgpt响应的内容提取出来
                    for choice in response.choices:
                        msg += choice.message.content
                    print(msg)
                    history_dic["user"].append(lastMsg)
                    history_dic["assistant"].append(msg)
                    # 发送内容
                    pyperclip.copy(msg.replace('{br}', '\n'))
                    wx.SendKeys("{Ctrl}v", waitTime=0)
                    wx.SendKeys("{Enter}", waitTime=0)
                    # 不显示聊天，等待下一条信息
                    wx.TextControl(SubName=msg[:5]).RightClick()
                    ment = ui.MenuControl(ClassName="CMenuWnd")
                    #ment.TextControl(Name="不显示聊天").Click()
    except Exception as e:

        print(e)


