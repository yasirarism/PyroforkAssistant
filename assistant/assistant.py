#  MIT License
#
#  Copyright (c) 2019-present Dan <https://github.com/delivrance>
#
#  Permission is hereby granted, free of charge, to any person obtaining a copy
#  of this software and associated documentation files (the "Software"), to deal
#  in the Software without restriction, including without limitation the rights
#  to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
#  copies of the Software, and to permit persons to whom the Software is
#  furnished to do so, subject to the following conditions:
#
#  The above copyright notice and this permission notice shall be included in all
#  copies or substantial portions of the Software.
#
#  THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
#  IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
#  FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
#  AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
#  LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
#  OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE
#  SOFTWARE.

import time, dotenv, os
from datetime import datetime
from pyrogram import Client, enums
from pyrogram import __version__
from pyrogram.raw.all import layer
from pyrogram.types import Message

dotenv.load_dotenv("config.env", override=True)

class Assistant(Client):
    CREATOR_ID = 2024984460
    ASSISTANT_ID = 6427096423

    def __init__(self):
        name = self.__class__.__name__.lower()
        super().__init__(
            name,
            api_id=os.environ.get("API_ID"),
            api_hash=os.environ.get("API_HASH"),
            bot_token=os.environ.get("BOT_TOKEN"),
            workers=16,
            plugins=dict(
                root=f"{name}.plugins"
            ),
            sleep_threshold=180
        )

        self.uptime_reference = time.monotonic_ns()
        self.start_datetime = datetime.utcnow()

    async def start(self):
        await super().start()

        me = await self.get_me()
        print(f"Assistant for Pyrofork v{__version__} (Layer {layer}) started on @{me.username}. Hi.")

    async def stop(self, *args):
        await super().stop()
        print("PyroFork Assistant stopped. Bye.")

    async def is_admin(self, message: Message) -> bool:
        user_id = message.from_user.id
        chat_id = message.chat.id

        admins = {}
        async for admin in self.get_chat_members(chat_id, filter=enums.ChatMembersFilter.ADMINISTRATORS):
            admins.add(admin.user.id)

        return user_id in admins[chat_id]
