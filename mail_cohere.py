import discord
import os
import cohere
from dotenv import load_dotenv

load_dotenv()

DISCORD_TOKEN = os.getenv("DISCORD_TOKEN")
COHERE_API_KEY = os.getenv("COHERE_API_KEY")

intents = discord.Intents.default()
intents.message_content = True

cohere_client = cohere.Client(COHERE_API_KEY)

class MyClient(discord.Client):
    async def on_ready(self):
        print(f'Logged in as {self.user}')

    async def on_message(self, message):
        print(f"Received message: {message.content}")

        if message.author == self.user:
            return

        msg_content = message.content.strip().lower()

        # Basic replies
        if msg_content == 'ping':
            await message.channel.send('pong')
            return

        elif msg_content in ['hi', 'hello', 'hey']:
            await message.channel.send('Hello there!')
            return

        elif "your name" in msg_content or "who are you" in msg_content:
            await message.channel.send("My name is Arushi. I'm here to help you!")
            return

        # Chat with Cohere for everything else
        try:
            response = cohere_client.chat(
                message=message.content,
                model="command-r",
                temperature=0.7,
                max_tokens=300
            )

            print("Cohere raw response:", response)

            reply = getattr(response, "text", None)
            if not reply and hasattr(response, "generations"):
                reply = response.generations[0].text

            if reply:
                await message.channel.send(reply)
            else:
                await message.channel.send("Sorry, I couldn't generate a response.")

        except Exception as e:
            print(f"Cohere error: {e}")
            await message.channel.send("Sorry, there was an error with the AI response.")

client = MyClient(intents=intents)
client.run(DISCORD_TOKEN)
