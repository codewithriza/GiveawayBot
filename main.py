import discord
from discord.ext import commands
from discord.ui import View, Button
import asyncio
import random
import datetime
import os
from dotenv import load_dotenv

load_dotenv()

bot = commands.Bot(command_prefix='g!',intents=discord.Intents.all())

class GiveawayView(View):
    def __init__(self, channel):
        super().__init__()
        self.channel = channel

    @discord.ui.button(label='Enter Giveaway', style=discord.ButtonStyle.green)
    async def enter_giveaway(self, button: discord.ui.Button, interaction: discord.Interaction):
        await interaction.followup.send("You have entered the giveaway!", ephemeral=True)




@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Game(name=f'g!help for a list of commands! 🥳 🎉 Currently in {len(bot.guilds)} servers! 🎉'))
    print('Ready to giveaway!')

@bot.command()
async def ghelp(ctx):

    ghelp = discord.Embed(color=0x7289da)
    ghelp.set_author(name='Commands/Help', icon_url='')
    ghelp.add_field(name='help', value='Shows this message.', inline=False)
    ghelp.add_field(name='giveaway', value='Starts a giveaway for the server! This command will ask you a few questions to set up the giveaway.', inline=False)
    ghelp.add_field(name='reroll `#channel_name` `message id`', value='Rerolls the winner of a giveaway. Requires the "Giveaway Host" role.', inline=False)
    ghelp.set_footer(text='Use the prefix "g!" before all commands!')
    await ctx.send(embed=ghelp)

@bot.command()
@commands.has_permissions(administrator=True)
async def giveaway(ctx):
    try:
        giveaway_questions = ['Which channel would you like to host the giveaway in?', 'What is the prize for this giveaway?', 'How long should the giveaway run for (in seconds)?']
        giveaway_answers = []

        def check(m):
            return m.author == ctx.author and m.channel == ctx.channel

        for question in giveaway_questions:
            await ctx.send(question)
            try:
                message = await bot.wait_for('message', timeout=30.0, check=check)
            except asyncio.TimeoutError:
                await ctx.send('You didn\'t answer in time. Please try again and be sure to send your answer within 30 seconds of the question.')
                return
            else:
                giveaway_answers.append(message.content)

        try:
            c_id = int(giveaway_answers[0][2:-1])
        except:
            await ctx.send(f'You failed to mention the channel correctly. Please do it like this: {ctx.channel.mention}')
            return

        channel = bot.get_channel(c_id)
        prize = str(giveaway_answers[1])
        time = int(giveaway_answers[2])

        await ctx.send(f'The giveaway for {prize} will begin shortly.\nPlease direct your attention to {channel.mention}, this giveaway will end in {time} seconds.')

        give = discord.Embed(color=0x2ecc71)
        give.set_author(name='GIVEAWAY TIME!', icon_url='https://i.imgur.com/VaX0pfM.png')
        give.add_field(name=f'{ctx.author.name} is giving away: {prize}!', value=f'React with 🎉 to enter!\n Ends in {round(time / 60, 2)} minutes!', inline=False)
        end = datetime.datetime.utcnow() + datetime.timedelta(seconds=time)
        give.set_footer(text=f'Giveaway ends at {end.strftime("%m/%d/%Y, %H:%M")} UTC!')
        my_message = await channel.send(embed=give, view=GiveawayView(channel))

        await asyncio.sleep(time)

        users = await my_message.fetch_message().users().flatten()
        users.pop(users.index(bot.user))
        winner = random.choice(users)

        winning_announcement = discord.Embed(color=0xff2424)
        winning_announcement.set_author(name='THE GIVEAWAY HAS ENDED!', icon_url='https://i.imgur.com/DDric14.png')
        winning_announcement.add_field(name=f'🎉 Prize: {prize}', value=f'🥳 **Winner**: {winner.mention}\n 🎫 **Number of Entrants**: {len(users)}', inline=False)
        winning_announcement.set_footer(text='Thanks for entering!')
        await channel.send(embed=winning_announcement)

    except Exception as e:
        error_embed = discord.Embed(title='Error Encountered', description='It looks like there is an issue with the giveaway command.', color=discord.Color.red())
        error_embed.add_field(name='Error Message', value=str(e), inline=False)
        error_embed.add_field(name='How to Fix', value='Please create an issue on [GitHub](https://github.com/codewithriza/js-exercism/issues) and we will support you soon.', inline=False)
        error_embed.set_footer(text='Please report this issue for further assistance.')
        await ctx.send(embed=error_embed)


@bot.command()
@commands.has_role(os.getenv('ADMIN_ROLE_ID'))
async def reroll(ctx, channel: discord.TextChannel, id_: int):
    try:
        new_message = await channel.fetch_message(id_)
    except:
        await ctx.send("Incorrect id.")
        return

    users = await new_message.reactions[0].users().flatten()
    users.pop(users.index(bot.user))
    winner = random.choice(users)

    reroll_announcement = discord.Embed(color=0xff2424)
    reroll_announcement.set_author(name='The giveaway was re-rolled by the host!', icon_url='https://i.imgur.com/DDric14.png')
    reroll_announcement.add_field(name='🥳 New Winner:', value=f'{winner.mention}', inline=False)
    await channel.send(embed=reroll_announcement)

bot.run(os.getenv('TOKEN'))
