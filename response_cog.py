import openai 
import discord
from discord.ext import commands
import concurrent.futures

class ResponseCog(commands.Cog):
    def __init__(self, bot):
        self.bot = bot
        self.GPT_model = "gpt-3.5-turbo"

    def gpt_answer(self,msg):
        query = str(msg)
        response = openai.ChatCompletion.create(
        messages=[
                    {'role': 'system', 'content': 'You only answer in numbers, you do not answer with words'},
                    {'role': 'user', 'content': query},
                ],
            model=self.GPT_model,
            temperature=0.3,
            max_tokens = 150,
            )
        return response['choices'][0]['message']['content']


    @commands.Cog.listener()
    async def on_message(self, message):
        username = str(message.author)
        user_message = str(message.content)
        channel = str(message.channel)

        if message.author == self.bot.user:
            print(f"{username} answered: '{user_message}' ({channel})")
            return

        print(f"{username} said: '{user_message}' ({channel})")
        
        if "tester" in user_message.lower():
            with concurrent.futures.ThreadPoolExecutor() as pool:
                response = await self.bot.loop.run_in_executor(pool, self.gpt_answer, user_message)
                await message.reply(response)
    
    @commands.command()
    async def help(self,ctx):
        command1 = 'kFetchmyStats "Username" "region"'
        embed = discord.Embed(
        title = "Here are my commands:",
        description = f"- {command1}",
        color = discord.Color.blue()
        )
        await ctx.send(embed=embed)

async def setup(bot: commands.Bot) -> None:
    await bot.add_cog(ResponseCog(bot))


