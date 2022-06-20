import discord
from discord.ext import commands
from random import randint
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
from os import getenv

import gachalist
import logging

env_path = Path("..//secret.env")
load_dotenv(dotenv_path=env_path)

logging.basicConfig(level=logging.INFO)

client = commands.Bot(command_prefix="!")

def getdata(url): 
    r = requests.get(url) 
    return r.text

def Hash(Number, Count):
    Number = Number - 5 + Count
    
    try:
        Bucket = gachalist.GachaList[Number]
        # with open("prob.txt","a") as file:
        #     file.write(str(Number))
    
    
    except IndexError:
        if Count < 4:
            Count = Count + 1
        
        Bucket = Hash(Number, Count)
    
    return Bucket    
        


@client.command(
    help = "Gacha roll",
    brief = "5% for SSR, 10% for SR, 15% for R, 25% for UC and 45% for C"
    )
async def roll(ctx):
    RarityRoll = randint(0,99)
    # 5% for SSR
    # 10% for SR
    # 15% for R
    # 25% for UC
    # 45% for C
    
    BucketNumber = RarityRoll // 5
    try:
        Pool = gachalist.GachaList[BucketNumber]
    
    except IndexError:
        Pool = Hash(BucketNumber, 1)
    
    CharaRoll = randint(0, len(Pool)-2)

    if Pool[CharaRoll].split()[0] == "genshin":
        URL = "https://genshin-impact.fandom.com/wiki/" + Pool[CharaRoll].split()[1]
        htmlData = getdata(URL)
        soup = BeautifulSoup(htmlData, "html.parser")
        item = soup.find("img", class_ = "pi-image-thumbnail")
        ImgURL = item["src"]
        
        with open("temp.txt", "w") as file:
            file.write(URL)
        
        await ctx.send(Pool[-1])
        await ctx.send(ImgURL)
        
        
    elif Pool[CharaRoll].split()[0] == "alchemy":
        URL = "https://alchemystars.fandom.com/wiki/" + Pool[CharaRoll].split()[1]
        htmlData = getdata(URL)
        soup = BeautifulSoup(htmlData, "html.parser")
        item = soup.find("img", class_ = "pi-image-thumbnail")
        ImgURL = item["src"]
        
        with open("temp.txt", "w") as file:
            file.write(URL)
        
        await ctx.send(Pool[-1])
        await ctx.send(ImgURL)
    
    else:
        URL = "https://gamepress.gg/" + Pool[CharaRoll].split()[0] + "/" + Pool[CharaRoll].split()[1] + "/" + Pool[CharaRoll].split()[2]
        htmlData = getdata(URL)
        soup = BeautifulSoup(htmlData, "html.parser")
        item = soup.find("img", class_ = "image-style-_00h")
        if item is None:
            item = soup.find("img", class_ = "image-style-servant-image")
            if item is None:
                item = soup.find("img", typeof = "foaf:Image")
                if item is None:
                    await ctx.send("404 ERROR NOT FOUND " + Pool[CharaRoll].split()[2])
        ImgURL = "https://gamepress.gg" + item["src"]
        
        with open("temp.txt", "w") as file:
            file.write(URL)
        
        await ctx.send(Pool[-1])
        await ctx.send(ImgURL)
        
@client.command(
    help = "Gives website for more detail",
    brief = ""
    )
async def detail(ctx):
    with open("temp.txt", "r") as file:
        URL = file.read()
        
    await ctx.send(URL)

@client.command(
    help = "Gets a specific SSR character",
    brief = ""
    )
async def ssr(ctx, name):
    for character in gachalist.SSR:
        if character.split()[-1].lower() == name.lower():
            
            if character.split()[0] == "genshin":
                URL = "https://genshin-impact.fandom.com/wiki/" + character.split()[1]
                htmlData = getdata(URL)
                soup = BeautifulSoup(htmlData, "html.parser")
                item = soup.find("img", class_ = "pi-image-thumbnail")
                ImgURL = item["src"]
                
                with open("temp.txt", "w") as file:
                    file.write(URL)
                
                await ctx.send(ImgURL)
                
            elif character.split()[0] == "alchemy":
                URL = "https://alchemystars.fandom.com/wiki/" + character.split()[1]
                htmlData = getdata(URL)
                soup = BeautifulSoup(htmlData, "html.parser")
                item = soup.find("img", class_ = "pi-image-thumbnail")
                ImgURL = item["src"]
                
                await ctx.send(ImgURL)
                
            else:
                URL = "https://gamepress.gg/" + character.split()[0] + "/" + character.split()[1] + "/" + character.split()[2]
                htmlData = getdata(URL)
                soup = BeautifulSoup(htmlData, "html.parser")
                item = soup.find("img", class_ = "image-style-_00h")
                if item is None:
                    item = soup.find("img", class_ = "image-style-servant-image")
                    if item is None:
                        item = soup.find("img", typeof = "foaf:Image")
                        if item is None:
                            await ctx.send("404 ERROR NOT FOUND " + character.split()[2])
                ImgURL = "https://gamepress.gg" + item["src"]
                
                with open("temp.txt", "w") as file:
                    file.write(URL)
                
                await ctx.send(ImgURL)

@client.command(
    help = "Gets a specific SR character",
    brief = ""
    )
async def sr(ctx, name):
    for character in gachalist.SR:
        if character.split()[-1].lower() == name.lower():
            
            if character.split()[0] == "genshin":
                URL = "https://genshin-impact.fandom.com/wiki/" + character.split()[1]
                htmlData = getdata(URL)
                soup = BeautifulSoup(htmlData, "html.parser")
                item = soup.find("img", class_ = "pi-image-thumbnail")
                ImgURL = item["src"]
                
                with open("temp.txt", "w") as file:
                    file.write(URL)
                
                await ctx.send(ImgURL)
                
            elif character.split()[0] == "alchemy":
                URL = "https://alchemystars.fandom.com/wiki/" + character.split()[1]
                htmlData = getdata(URL)
                soup = BeautifulSoup(htmlData, "html.parser")
                item = soup.find("img", class_ = "pi-image-thumbnail")
                ImgURL = item["src"]
                
                await ctx.send(ImgURL)
                
            else:
                URL = "https://gamepress.gg/" + character.split()[0] + "/" + character.split()[1] + "/" + character.split()[2]
                htmlData = getdata(URL)
                soup = BeautifulSoup(htmlData, "html.parser")
                item = soup.find("img", class_ = "image-style-_00h")
                if item is None:
                    item = soup.find("img", class_ = "image-style-servant-image")
                    if item is None:
                        item = soup.find("img", typeof = "foaf:Image")
                        if item is None:
                            await ctx.send("404 ERROR NOT FOUND " + character.split()[2])
                ImgURL = "https://gamepress.gg" + item["src"]
                
                with open("temp.txt", "w") as file:
                    file.write(URL)
                
                await ctx.send(ImgURL)
                
@client.command(
    help = "Gets a specific Rare character",
    brief = ""
    )
async def r(ctx, name):
    for character in gachalist.R:
        if character.split()[-1].lower() == name.lower():
            
            if character.split()[0] == "alchemy":
                URL = "https://alchemystars.fandom.com/wiki/" + character.split()[1]
                htmlData = getdata(URL)
                soup = BeautifulSoup(htmlData, "html.parser")
                item = soup.find("img", class_ = "pi-image-thumbnail")
                ImgURL = item["src"]
                
                await ctx.send(ImgURL)
            
            else:
                URL = "https://gamepress.gg/" + character.split()[0] + "/" + character.split()[1] + "/" + character.split()[2]
                htmlData = getdata(URL)
                soup = BeautifulSoup(htmlData, "html.parser")
                item = soup.find("img", class_ = "image-style-_00h")
                if item is None:
                    item = soup.find("img", class_ = "image-style-servant-image")
                    if item is None:
                        item = soup.find("img", typeof = "foaf:Image")
                        if item is None:
                            await ctx.send("404 ERROR NOT FOUND " + character.split()[2])
                ImgURL = "https://gamepress.gg" + item["src"]
                
                with open("temp.txt", "w") as file:
                    file.write(URL)
                
                await ctx.send(ImgURL)
        
        
                
@client.command(
    help = "Gets a specific uncommon character",
    brief = ""
    )
async def uc(ctx, name):
    for character in gachalist.UC:
        if character.split()[-1].lower() == name.lower():
            
            if character.split()[0] == "alchemy":
                URL = "https://alchemystars.fandom.com/wiki/" + character.split()[1]
                htmlData = getdata(URL)
                soup = BeautifulSoup(htmlData, "html.parser")
                item = soup.find("img", class_ = "pi-image-thumbnail")
                ImgURL = item["src"]
                
                await ctx.send(ImgURL)
            
            else:
                URL = "https://gamepress.gg/" + character.split()[0] + "/" + character.split()[1] + "/" + character.split()[2]
                htmlData = getdata(URL)
                soup = BeautifulSoup(htmlData, "html.parser")
                item = soup.find("img", class_ = "image-style-_00h")
                if item is None:
                    item = soup.find("img", class_ = "image-style-servant-image")
                    if item is None:
                        item = soup.find("img", typeof = "foaf:Image")
                        if item is None:
                            await ctx.send("404 ERROR NOT FOUND " + character.split()[2])
                ImgURL = "https://gamepress.gg" + item["src"]
                
                with open("temp.txt", "w") as file:
                    file.write(URL)
                
                await ctx.send(ImgURL)
        
        
            
@client.command(
    help = "Gets a specific common character",
    brief = ""
    )
async def c(ctx, name):
    for character in gachalist.C:
        if character.split()[-1].lower() == name.lower():
       
            URL = "https://gamepress.gg/" + character.split()[0] + "/" + character.split()[1] + "/" + character.split()[2]
            htmlData = getdata(URL)
            soup = BeautifulSoup(htmlData, "html.parser")
            item = soup.find("img", class_ = "image-style-_00h")
            if item is None:
                item = soup.find("img", class_ = "image-style-servant-image")
                if item is None:
                    item = soup.find("img", typeof = "foaf:Image")
                    if item is None:
                        await ctx.send("404 ERROR NOT FOUND " + character.split()[2])
            ImgURL = "https://gamepress.gg" + item["src"]
            
            with open("temp.txt", "w") as file:
                file.write(URL)
            
            await ctx.send(ImgURL)
    

client.run(getenv("DISCORD_BOT_TOKEN"))