import discord
from discord.ext import commands
import config
import json
import introduction_message
import datetime


intents = discord.Intents.all()
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.event
async def on_ready():
    await bot.tree.sync()
    print("Bot is ready")

#slash command that takes entry
@bot.tree.command()
async def entry(interaction : discord.Interaction, para : int, quarter : int):
    """Enter your progress reading the Quran."""

    if interaction.channel_id != 1218213695939805194:
        await interaction.response.send_message("Kindly use the entry channel to make an entry.", ephemeral=True)
        return

    member = interaction.user

    with open('data.json', 'r+') as file:
        dic = json.load(file)
        member_string = str(member.id)
        dic[member_string] = [para, quarter]
        file.seek(0)
        json.dump(dic, file, indent= 4)

    if quarter != 0:
        response = f'{member.name} has read {para} para and is {quarter} quarter through it.'
    else:
        response = f'{member.name} has read {para} para.'
    
    await interaction.response.send_message(response)


@bot.tree.command()
async def leaderboard(interaction : discord.Interaction):
    """Show the leaderboard of the Quran Quest."""

    if interaction.channel_id != 1218214154695868496:
        await interaction.response.send_message("Kindly use the leaderboard channel to check the leaderboard.", ephemeral=True)
        return

    #deletes the previous message
    await interaction.channel.purge(limit = 1)


    with open('data.json', 'r') as file:
        dic = json.load(file)
    
    sorted_dic = sorted(dic.items(), key=lambda x: (x[1][0], x[1][1]), reverse=True)
    
    embed = discord.Embed(title="Leaderboard", description="Progress of reading the Quran", color=0xF3E5AB)
    rank = 1
    for i in sorted_dic:
        member = await bot.fetch_user(int(i[0]))
        embed.add_field(name= f"{rank}. {member.name}" , value=f'Para: {i[1][0]}, Quarter: {i[1][1]}', inline=False)
        rank += 1
    
    # Get the current UTC time
    current_utc_time = datetime.datetime.now(datetime.timezone.utc)
    
    # Add the UTC offset for GMT+6 (6 hours ahead)
    current_gmt6_time = current_utc_time + datetime.timedelta(hours=6)
    
    # Format the current time and add it to the footer of the embed
    current_time_str = current_gmt6_time.strftime('%I:%M %p %d-%m-%Y GMT+6')
    embed.set_footer(text=f"Last updated: {current_time_str}")
    

    await interaction.response.send_message(embed=embed)

@bot.command()
async def introduction(ctx):
    await ctx.channel.purge(limit = 1)
    await ctx.send(introduction_message.message)

bot.run(config.discord_token)