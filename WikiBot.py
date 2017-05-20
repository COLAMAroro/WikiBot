import discord    
import asyncio
import wikipedia
from tkn import *

language = "en"

client = discord.Client()


@client.event
@asyncio.coroutine
def on_ready():
    print("Bot is ready")
    print(client.user.name)
    print(client.user.id)

@client.event
@asyncio.coroutine
def on_server_join(server):
    yield from client.send_message(server.default_channel, "Oi, i'm the WikiBot! https://en.wikipedia.org/wiki/Main_Page")

@client.event
@asyncio.coroutine
def on_message(message):
    if message.channel.is_private and message.author.id != client.user.id:
        yield from printout(message, message.content)

    else:
        ping = "<@" + client.user.id + ">"
        if message.content.startswith(ping):
        
            print("I'm called!")
            
            toretract = len(ping)
            query = message.content[toretract:]

            while len(query) != 0 and query[0] == " ":
                query = query[1:]

            (lang, query) = yield from setlang(query)

            print("Query = " + query)
            yield from printout(message, query, lang)


@asyncio.coroutine
def printout(message, query, lang):
    wikipage = None
    lookup = True
    disambiguation = False
    print("printout")

    wikipedia.set_lang(lang)

    try:
        wikipage = wikipedia.page(query)
        print("I found directly")            
                
    except wikipedia.PageError:
        print("Can't access by default. Trying to search")
        
    except wikipedia.DisambiguationError:
        yield from client.send_message(message.channel, "This query leads to a disambiguation page. Please be more specific.")
        disambiguation = True
            
    except Exception:
        lookup = False
                
    if wikipage is None and lookup and not disambiguation:
        wikipage = wikipedia.suggest(query)
            
    if wikipage is None and lookup and not disambiguation:
        yield from client.send_message(message.channel, "Sorry, cannot find " + query + " :v")
    elif not lookup:
        yield from client.send_message(message.channel, "Something went wrong. Check the language, or maybe I can't reach Wikipedia")
    else:
        imglist = wikipage.images
        if len(imglist) == 0:
            em = discord.Embed(title=wikipage.title, description=wikipedia.summary(query, sentences=2), colour=0x2DAAED, url=wikipage.url)
        else:
            em = discord.Embed(title=wikipage.title, description=wikipedia.summary(query, sentences=2), colour=0x2DAAED, url=wikipage.url, image=imglist[0])
            em.set_author(name=client.user.name, icon_url="https://wikibot.rondier.io")
            yield from client.send_message(message.channel, embed=em)
            yield from client.send_message(message.channel, "More at <" + wikipage.url + ">")


    wikipedia.set_lang("en")

@asyncio.coroutine
def setlang(query):
    if len(query) <= 4 or query[0] != '!' or query[3] != " ":
        return ("en", query)
    else:
        lang = query[1] + query[2]
        nquery = query[4:]
        return (lang, nquery)

client.run(token)

