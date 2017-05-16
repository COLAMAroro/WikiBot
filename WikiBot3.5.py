import discord
import wikipedia

token = "Mjg3NjU2MjM1MjU0NDE1MzYx.C-5xKQ.khJ9dPouM9783FMA0Ht-92XkS6A"

language = "en"

client = discord.Client()


@client.event
async def on_ready():
    print("Bot is ready")
    print(client.user.name)
    print(client.user.id)


@client.event
async def on_server_join(server):
    await client.send_message(server.default_channel, "Oi, i'm the WikiBot! https://en.wikipedia.org/wiki/Main_Page")


@client.event
async def on_message(message):
    if message.channel.is_private and message.author.id != client.user.id:
        await printout(message, message.content)

    else:
        ping = "<@" + client.user.id + ">"
        if message.content.startswith(ping):
        
            print("I'm called!")
            
            toretract = len(ping)
            query = message.content[toretract:]
            
            if query[0] == " ":
                query = query[1:]
            
            print("Query = " + query)
            
            await printout(message, query)


async def printout(message, query):
    wikipage = None
    lookup = True
    print("printout")

    try:
        wikipage = wikipedia.page(query)
        print("I found directly")            
                
    except wikipedia.exceptions.PageError:
        print("Can't access by default. Trying to search")
            
    except Exception:
        lookup = False
                
    if wikipage is None and lookup:
        wikipage = wikipedia.suggest(query)
            
    if wikipage is None and lookup:
        await client.send_message(message.channel, "Sorry, cannot find " + query + " :v")
    elif not lookup:
        await client.send_message(message.channel, "Something went wrong. Try to be more specific in search, or maybe I can't reach Wikipedia")
    else:
        imglist = wikipage.images
        if len(imglist) == 0:
            em = discord.Embed(title=wikipage.title, description=wikipedia.summary(query, sentences=2), colour=0x2DAAED, url=wikipage.url)
        else:
            em = discord.Embed(title=wikipage.title, description=wikipedia.summary(query, sentences=2), colour=0x2DAAED, url=wikipage.url, image=imglist[0])
            em.set_author(name=client.user.name, icon_url="https://wikibot.rondier.io")
            await client.send_message(message.channel, embed=em)
            await client.send_message(message.channel, "More at " + wikipage.url)

client.run(token)
