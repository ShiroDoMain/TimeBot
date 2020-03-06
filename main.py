# -*- coding: utf-8 -*-
# @Time : 2020/3/4 1:26 下午
# @Author : shiro
# @Software: PyCharm
import asyncio
import time
from mirai import Session, Plain, Image

authKey = "your authKey"
qq = yourbotqqnum


async def main():
    for i in range(1, 13):
        Time = int(time.strftime("%I%M%S", time.localtime(time.time())))
        if Time == (i*10000):
            async with Session(f"mirai://localhost:8080/?authKey={authKey}&qq={qq}") as session:
		# 向个人报时
                await session.sendFriendMessage(
                    qqID,# 接受qq
                    [
                        Image.fromFileSystem("./timeimg/{}.jpg".format(int(i))),
                        Plain(text="Now time")
                    ]
                )
		# 在群里报时
		await session.sendGroupMessage(
                    qqID,# 群组qq
                    [
                        Image.fromFileSystem("./timeimg/{}.jpg".format(int(i))),
                        Plain(text="Now time")
                    ]
                )
                print('{}点已放送'.format(i))
                break

while True:
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        exit()
