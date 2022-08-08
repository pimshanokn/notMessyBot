import os
import csv
import random
import discord
from discord.ext import commands
from dotenv import load_dotenv
bot = commands.Bot(command_prefix="!")

@bot.event
async def on_ready(): #if the bot is ready will proceed this
    print("Are you ready to observe?")

@bot.event
async def on_message(message): #ctx = context
    if message.author == bot.user:
        return

    if "saturn" in message.content.lower():
        #message.content.startswith("saturn")
        channel = message.channel
        await channel.send("✨🪐✨") #do one with moon
    await bot.process_commands(message)
    #command and event cannot work at the same time so we tell event to wait

@bot.command()
#random a number of messier objects
async def ranM(ctx, season):
    x = random.randint(1,110)
    with open ('messierCatalog.csv', 'r') as myFile:
        dictReader = csv.DictReader(myFile)
        dictRows = [dict(row) for row in dictReader]

    for obj in dictRows:
        if f"M{x}" == obj["M"]:
            ranMag = obj["MAG"]
            ranLevel = obj["VIEWING DIFFICULTY"]

    await ctx.channel.send(f"You should try to observe M{x} tonight " +
                                f"since it is {season.lower()}!")
    await ctx.channel.send(f"The viewing difficulty level is {ranLevel.lower()} " +
                            f"(magnitude: {ranMag}).")


@bot.command()
async def objInfo(ctx, mNum):
    #give info about a designated messier object
    with open ('messierCatalog.csv', 'r') as myFile:
        dictReader = csv.DictReader(myFile)
        dictRows = [dict(row) for row in dictReader]
    for obj in dictRows:
        if mNum == obj["M"]:
            mType = obj["TYPE"]
            mCon = obj["CONS"]
            mMag = obj["MAG"]
            mSeason = obj["VIEWING SEASON"]
            mLevel = obj["VIEWING DIFFICULTY"]

    cute = discord.Embed(title=mNum,
                        description="image by go-astronomy.com \n information by starlust.com",
                        color=0xFFF8E7)
    cute.add_field(name="Type", value=f"{mType}")
    cute.add_field(name="Constellation", value=f"{mCon}")
    cute.add_field(name="Magnitude", value=f"{mMag}")
    cute.add_field(name="Viewing Season", value=f"{mSeason}")
    cute.add_field(name="Viewing Difficulty", value=f"{mLevel}")

    thePic = f"https://www.go-astronomy.com/images/messier/big/messier-{mNum[1:]}.jpg"
    cute.set_thumbnail(url=thePic)
    await ctx.channel.send(embed=cute)

@bot.command()
#general messier objects based on season
async def seasonM(ctx, givenS):
    with open ('messierCatalog.csv', 'r') as myFile:
        dictReader = csv.DictReader(myFile)
        dictRows = [dict(row) for row in dictReader]

    totalNum = 0
    finalStr = ""
    for obj in dictRows:
        if obj['VIEWING SEASON'].lower() == givenS.lower():
            totalNum += 1
            finalStr += obj['M'] + ", "
    await ctx.channel.send(f"There are {totalNum} messier objects you can " +
                            f"observe in {givenS.lower()}!")
    await ctx.channel.send(f"They are: {finalStr[:-2]}")

@bot.command()
#show how many messier is up for observe in given season and level
async def ultimate(ctx, givenS, givenL):
    with open ('messierCatalog.csv', 'r') as myFile:
        dictReader = csv.DictReader(myFile)
        dictRows = [dict(row) for row in dictReader]

    totalNum = 0
    totalList = []
    for obj in dictRows:
        if obj['VIEWING SEASON'].lower() == givenS.lower():
            if obj['VIEWING DIFFICULTY'].lower() <= givenL.lower():
                totalList.append(obj['M'])
                totalNum += 1
#only come up with very when typing very hard
    await ctx.channel.send(f"There are {totalNum} messier objects you can " +
                            f"observe in {givenS.lower()} at {givenL.lower()} level.")
    await ctx.channel.send(f"They are {totalList}")
#come back and fix this

@bot.command()
async def commandsList(ctx):
    await ctx.channel.send("🌌Not Messy Bot's Commands🌌")
    await ctx.channel.send("- season: spring, summer, autumn, winter")
    await ctx.channel.send("- viewing difficulty: very easy, easy, moderate, hard, very hard")
    await ctx.channel.send("!ranM [season] - Randomize a messier object you should observe based on season!")
    await ctx.channel.send("!objInfo M[Messier number] - Get an information about a specific Messier object.")
    await ctx.channel.send("!seasonM [season] - See how many Messier objects can be observed this season.!")
    await ctx.channel.send("!ultimate [season] [level] - Randomize a messier objects you should observe basd on season and viewing difficulty.")
    await ctx.channel.send("ps. type saturn to receive a cute text. Happy observing!")
    #not efficient - try new way

bot.run(os.getenv("DISCORD_TOKEN"))
