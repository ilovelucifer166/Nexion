from discord.ext import commands
from commands.chat_command import generate_response  # Changed import path
from collections import deque

class ChatCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.conversation_histories = {}

    @commands.command()
    async def chat(self, ctx, *, prompt: str):
        if not prompt:
            await ctx.reply("Please provide a message after !chat")
            return
            
        async with ctx.channel.typing():
            try:
                # Get or create conversation history
                history = self.conversation_histories.setdefault(ctx.author.id, deque(maxlen=6))
                response = generate_response(ctx.author.id, prompt, self.bot.config, history)
                history.extend([
                    {"role": "user", "content": prompt},
                    {"role": "assistant", "content": response}
                ])
                await ctx.reply(response)
            except Exception as e:
                await ctx.reply(f"An error occurred: {str(e)}")