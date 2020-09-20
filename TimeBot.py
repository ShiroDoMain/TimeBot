import asyncio
import time

from PIL import Image as IMG, ImageFont, ImageDraw
from graia.application.entry import (GraiaMiraiApplication, Session, MessageChain, Group, Member, MemberPerm, Plain,
                                     Image)
from graia.broadcast import Broadcast

GP = []

loop = asyncio.get_event_loop()

bcc = Broadcast(loop=loop)
app = GraiaMiraiApplication(
    broadcast=bcc,
    connect_info=Session(
        host="http://localhost:2333", #  host and port
        authKey="aaaaaaaaaaaa", #  your miraihttp-api authkey
        account=114514, #  your qqbot num
        websocket=True
    )
)

# 如果有必要可以自己更换图片
def time_draw(time_now,msg):
    with IMG.open('img/time.jpg') as image:
        img_draw = ImageDraw.Draw(image)
        img_draw.text((0,263), time_now, font=ImageFont.truetype('Font/PUTHIAfont.ttf', 23), fill=(0,0,0))
        i = 0
        for word in msg:
            i += 25
            img_draw.text((87,i),word,font=ImageFont.truetype('Font/HYXinHaiXingKaiW.ttf',25),fill=(0,0,0))
        image.save("img/time_cache.jpg")


# 你可以在这里配置需要发送在图片上的文字，建议不要超过六个字
def ask(time):
    if time in range(0, 6):
        return '我睡着了w'
    elif time in range(6, 7):
        return '快点起床!'
    elif time in range(7, 8):
        return '快恰早饭!'
    elif time in range(8, 11):
        return '滚去学习!'
    elif time in range(11, 12):
        return '去恰午饭!'
    elif time in range(12, 13):
        return '去睡午觉!'
    elif time in range(13, 16):
        return '快去学习!'
    elif time in range(16, 18):
        return '去吃晚饭!'
    elif time in range(18, 22):
        return '快点上号!'
    elif time in range(22, 25):
        return '滚去睡觉！'



async def tell_time(bot=app,message:MessageChain=MessageChain):
    lt = int(time.strftime("%H%M%S", time.localtime(time.time())))
    ht = int(time.strftime("%H", time.localtime(time.time())))
    time_num = int(lt / 10000)
    time_draw(time.strftime("%H:%M", time.localtime(time.time())),ask(ht))
    for ID in GP:
        if time_num == 7:
            v = await bot.uploadVoice(open('www.amr','rb')) #  语音也是可以自己换的哦
            await bot.sendGroupMessage(ID,message.create([v]))
        await bot.sendGroupMessage(ID, message.create([Image.fromLocalFile(f'img/time_cache.jpg')]))


async def Run():
    last_time = time.localtime()
    print(last_time)
    while True:
        curr_time = time.localtime()
        if curr_time.tm_sec < 50 and curr_time.tm_min < 59 and curr_time.tm_min != 0:
            wait_time = 50 - curr_time.tm_sec
            await asyncio.sleep(wait_time)
        elif curr_time.tm_min == 0 and \
                curr_time.tm_hour != last_time.tm_hour:
            asyncio.ensure_future(tell_time())
            last_time = curr_time
            print(time.strftime("Time: %H:%M:%S"))
            await asyncio.sleep(20)



@bcc.receiver('GroupMessage')
async def Time(bot: GraiaMiraiApplication, group: Group, message: MessageChain, member: Member):

    if message.asDisplay() == '开启整点报时': #  and member.id == 1808107177:
        if (member.permission != MemberPerm.Owner) and (member.permission != MemberPerm.Administrator):
            await bot.sendGroupMessage(group.id, message.create([Plain(text='Permission denied->权限不足，只有管理员or群主可以开启或者关闭')]))
        elif group.id in GP:
            await bot.sendGroupMessage(group.id, message.create([Plain(text=f'{group.name}->已开启整点报时,请勿重复提交')]))
        else:
            GP.append(group.id)
            await bot.sendGroupMessage(group.id, message.create([Plain(text=f'{group.name}->开启整点报时')]))
    if message.asDisplay() == '关闭整点报时': # and member.id == 1808107177:
        if (member.permission != MemberPerm.Owner) and (member.permission != MemberPerm.Administrator):
            await bot.sendGroupMessage(group.id, message.create([Plain(text='Permission denied->权限不足，只有管理员or群主可以开启或者关闭')]))
        elif group.id not in GP:
            await bot.sendGroupMessage(group.id, message.create([Plain(text=f'{group.name}->未关闭整点报时')]))
        else:
            GP.remove(group.id)
            await bot.sendGroupMessage(group.id, message.create([Plain(text=f'{group.name}->关闭整点报时')]))

async def main():
    asyncio.create_task(Run())

if __name__ == '__main__':
    # coro = asyncio.create_task(Run(GraiaMiraiApplication, MessageChain))
    asyncio.run_coroutine_threadsafe(main(),loop)
    app.launch_blocking()
