#/usr/bin/python3
import discord
from discord.ext import commands
import json
import asyncio
import random


with open("config.json","r") as f1:
    config = json.load(f1)

bot = commands.Bot(command_prefix=config["prefix"])

general = discord.Object(id=config["general"])
dicechannel = discord.Object(id=config["dicechannel"])
initiativechannel = discord.Object(id=config["initiativechannel"])

cards = [ 'Ace', 'King', 'Queen', 'Jack', 'Ten', 'Nine', 'Eight', 'Seven', 'Six',
                        'Five', 'Four', 'Three', 'Two']
suits = [ 'Hearts', 'Diamonds', 'Clubs', 'Spades']

deckOfCards = []
for card in cards:
    for suit in suits:
        newcard = card + " of " + suit
        deckOfCards.append(newcard)

initiativeround = dict()

onJoinMessage = [
                    "Hacker Voice: I'm in.",
                    "... everyone roll a save vs Death by DMBot",
                    "No. No, you can't do that. I don't care what it says in the Player's Handbook.",
                    "!roll 1d1000000000000",
                    " ** I am here! ** Now let's get this show on the road."
                 ]
   

@bot.event
async def on_ready():
    print('Logged in as')
    print(bot.user.name)
    print(str(initiativeround))
    await bot.send_message(dicechannel, random.choice(onJoinMessage))


@bot.event
async def on_message(message):

    if message.content.lower().startswith("!cards"):
        size = len(deckOfCards)
        decksize = "There are " + str(size) + " cards left in the deck."
        await bot.send_message(message.channel, decksize)
    
    if message.content.lower().startswith("!initreset"):
        deckOfCards.clear()
        for card in cards:
            for suit in suits:
                newcard = card + " of " + suit
                deckOfCards.append(newcard)
        await bot.send_message(initiativechannel, "Initiative has been reset")


    if message.content.lower().startswith("!initiative"):
        userID = message.author.id
        print(userID)
        usercard = random.choice(deckOfCards)
        initiativeround.update({userID : usercard})
        print(initiativeround)
        deckOfCards.remove(usercard)
        initiativemessage = str("You drew a " + usercard)
        await bot.send_message(message.author, initiativemessage) 
        

    if message.content.lower().startswith("!reveal"):
        userID = message.author.id
        usercard = initiativeround.get(userID)
        print(usercard)
        initiativeround.pop(userID)       
        initiativemessage = message.author.name + " drew a " + usercard
        await bot.send_message(initiativechannel, initiativemessage)

    if message.content.lower().startswith("!commands"):
        await bot.send_message(message.channel,"These are the list of commands for DM-Bot:\n")
        await bot.send_message(message.channel,"!initiative  <Partial functionality>\n") 
        await bot.send_message(message.channel,
           "     This command will draw a random card from a deck and message you with the result.\n")
        await bot.send_message(message.channel,"!reveal  <Disabled>\n")
        await bot.send_message(message.channel,
           "     This command will reveal what your initiative card is to the general channel")
        await bot.send_message(message.channel,"!roll\n")
        await bot.send_message(message.channel,
           "     This command should be written in the format of NdK +M or NdK +MdQ. DM-Bot will roll\n")
        await bot.send_message(message.channel,
           "     K or Q sided dice N or M number of times. \n\n")


    if message.content.lower().startswith("!roll"):
        userID = message.author.name
        args = message.content.split(" ")
        argsize = len(args)
        total = int(0)
        result = []
        for i in range(1,argsize):
            if '+' in args[i]:
                if not 'd' in args[i]:
                    dicemod = args[i]
                    dicemod = dicemod[1:]
                    total = total + int(dicemod)
                elif 'd' in args[i]:
                    rolls, limit = map(int, args[i].split('d'))
                    if limit > 9000:
                        await bot.send_message(message.channel, ("Fuckoff " + userID + "! That's over 9000!"))
                        return
                    elif limit < 0:
                        await bot.send_message(message.channel, "Fuck this shit, I'm out.")
                        return
                    elif rolls == 0:
                        await bot.send_message(message.channel,(userID + " rolled a joint ... obviously."))  
                        return  
                    elif rolls > 99:
                        await bot.send_message(message.channel, (userID + ", I'm gonna tie you up and make you eat all those dice"))
                        return                                
                    for r in range(rolls):
                        theroll = random.randint(1,limit)
                        result.append(theroll)
                        total = total + theroll
                else:
                    await bot.send_message(message.channel, "Hold up, there was an error, code x116")
            elif '-' in args[i]:
                if not 'd' in args[i]:
                    dicemod = args[i]
                    dicemod = dicemod[1:]
                    total = total - int(dicemod)
                elif 'd' in args[i]:
                    rolls, limit = map(int, args[i].split('d'))
                    if limit > 9000:
                        await bot.send_message(message.channel, ("Fuckoff " + userID + "! That's over 9000!"))
                        return
                    elif limit < 0:
                        await bot.send_message(message.channel, "Fuck this shit, I'm out.")
                        return
                    elif rolls > 99:
                        await bot.send_message(message.channel, (userID + ", I'm gonna tie you up and make you eat all those dice"))
                        return
                    elif rolls == 0:
                        await bot.send_message(message.channel, (userID + " rolled a joint ... obviously."))  
                        return              
                    for r in range(abs(rolls)):
                        theroll = random.randint(1,limit)
                        result.append(theroll)
                        total = total - theroll
                else:
                    await bot.send_message(message.channel, "Hold up, there was an error, code x134")
            else:
                if not 'd' in args[i]:
                    await bot.send_message(message.channel, "invalid format, try again.")
                    return
                elif 'd' in args[i]:
                    rolls, limit = map(int, args[i].split('d'))
                    if limit > 9000:
                        await bot.send_message(message.channel, ("Fuckoff " + userID + "! That's over 9000!!"))
                        return
                    elif limit < 0:
                        await bot.send_message(message.channel, "Fuck this shit, I'm out.")
                        return
                    elif rolls == 0:
                        await bot.send_message(message.channel, (userID + " rolled a joint ... obviously."))
                        return  
                    elif rolls > 99:
                        await bot.send_message(message.channel, (userID + ", I'm gonna tie you up and make you eat all those dice"))
                        return                                                      
                    for r in range(rolls):
                        theroll = random.randint(1,limit)
                        result.append(theroll)
                        total = total + theroll
                else:
                    await bot.send_message(message.channel, "Hold up, there was an error, code x151")

        dieresults = ""
        for die in result:
            dieresults += " [ " + str(die) + " ] "
        finalmessage = (userID + " rolled: " + dieresults + "\n")
        finalmessage += ("for a total of: " + str(total))
        await bot.send_message(message.channel, finalmessage)

bot.run(config["token"])