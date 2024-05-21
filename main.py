from pyrogram.errors import BotBlocked, UserDeactivated
from pyrogram.filters import private
from pyrogram.client import Client
import asyncio

from db import init_db
from query import (
    getUserByID,
    createUserByID,
    getAliveUsers,
    updateUserStatusByID
)
from config import CONF

app: Client = Client(
    name=CONF['APP_NAME'],
    api_id=CONF['API_ID'],
    api_hash=CONF['API_HASH'],
    bot_token=CONF['BOT_TOKEN'])


def check(message: str) -> bool:
    words = set(word.lower() for word in message.split(' '))
    if words & CONF['WORDS']:
        return True
    return False


async def check_messages():
    while True:
        # Get active users
        users = await getAliveUsers()
        for user in users:
            # Send our text to users
            try:
                response = await app.send_message(user.id, "Текст")
                if check(message=response.text):
                    # Update user status to finished if message sent
                    await updateUserStatusByID(user_id=user.id, status="finished")
            except (BotBlocked, UserDeactivated):
                # Update user status to dead if message did not send
                await updateUserStatusByID(user_id=user.id, status="dead")


@app.on_message(private)
async def handle_message(client, message):
    # There We will handle users
    sender_user_id: int = int(message.from_user.id)
    user = await getUserByID(id=sender_user_id)

    # If user is not in DB we will create it
    if not user:
        await createUserByID(id=sender_user_id)


async def main():
    # Initialize all tasks

    # Create DBs before start App and Checker
    await init_db()

    # Start Main App
    await app.start()

    # Start Checker
    await check_messages()

if __name__ == "__main__":
    asyncio.run(main())
