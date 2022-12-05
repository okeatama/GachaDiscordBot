import discord
from discord.ext import commands
from random import randint
import requests
from bs4 import BeautifulSoup
from dotenv import load_dotenv
from pathlib import Path
import os
import csv

import gachalist
import logging

csv_file_path = "./csv/"
detail_buffer = ""

# 2D list with format name, url, gameid
ssr_list = []
sr_list = []
r_list = []
uc_list = []
c_list = []

# initialize all the lists
with open(csv_file_path + "ssr.csv", "r") as file:
    csv_file = csv.reader(file)
    for line in csv_file:
        ssr_list.append(line)
    
with open(csv_file_path + "sr.csv", "r") as file:
    csv_file = csv.reader(file)
    for line in csv_file:
        sr_list.append(line)

with open(csv_file_path + "r.csv", "r") as file:
    csv_file = csv.reader(file)
    for line in csv_file:
        r_list.append(line)
        
with open(csv_file_path + "uc.csv", "r") as file:
    csv_file = csv.reader(file)
    for line in csv_file:
        uc_list.append(line)
        
with open(csv_file_path + "c.csv", "r") as file:
    csv_file = csv.reader(file)
    for line in csv_file:
        c_list.append(line)

master_list = ssr_list + sr_list + r_list + uc_list + c_list

env_path = Path("..//secret.env")
load_dotenv(dotenv_path=env_path)

logging.basicConfig(level=logging.INFO)

intents = discord.Intents.default()
intents.message_content = True

client = commands.Bot(command_prefix="!", intents = intents)
print("Booting up...")

def getdata(url): 
    r = requests.get(url) 
    return r.text

def scrape_img(line):
    with open("temp.txt", "w") as file:
        file.write(line[1])
    
    htmlData = getdata(line[1])
    soup = BeautifulSoup(htmlData, "html.parser")
    
    if line[2] == '0':
        # arknights
        imageTab = soup.find(id="image-tab-3")
        if imageTab is None:
            imageTab = soup.find(id="image-tab-1")
        
        anchor = imageTab.find("a")
        return anchor["href"]
    
    elif line[2] == '1':
        # fgo
        tab4 = soup.find(id="tab-4")
        anchor = tab4.find("a")
        return anchor["href"]
    
    elif line[2] == '2':
        # gfl
        tDollImage = soup.find(id='t-doll-image')
        anchor = tDollImage.find("a")
        return anchor["href"]
    
    elif line[2] == '3':
        # genshin
        anchor = soup.find(class_='image image-thumbnail')
        return anchor["href"]
    
def searchChar(name):
    for elem in master_list:
        if name.lower() == elem[0].lower():
            return elem
        
    return None
# =============================================================================
# def Hash(Number, Count):
#     Number = Number - 5 + Count
#     
#     try:
#         Bucket = gachalist.GachaList[Number]
#         # with open("prob.txt","a") as file:
#         #     file.write(str(Number))
# 
#     except IndexError:
#         if Count < 4:
#             Count = Count + 1
# 
#         Bucket = Hash(Number, Count)
#     
#     return Bucket
# =============================================================================

@client.event
async def on_ready():  # when the bot is ready
    await client.change_presence(activity=discord.Game('Suffering'))
    print(f'{client.user} has connected to Discord!')



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
    
# =============================================================================
#     BucketNumber = RarityRoll // 5
#     try:
#         Pool = gachalist.GachaList[BucketNumber]
#     
#     except IndexError:
#         Pool = Hash(BucketNumber, 1)
# =============================================================================
    Pool = []
    rarity = ""
    if RarityRoll < 5:
        Pool = ssr_list
        rarity = "SSR"
    elif RarityRoll < 15:
        Pool = sr_list
        rarity = "SR"
    elif RarityRoll < 30:
        Pool = r_list
        rarity = "R"
    elif RarityRoll < 55:
        Pool = uc_list
        rarity = "UC"
    else:
        Pool = c_list
        rarity = "C"
    
    CharaRoll = randint(0, len(Pool))
    
    line = Pool[CharaRoll]
    img_link = scrape_img(line)
    
    await ctx.send(img_link)
    await ctx.reply(f"{rarity} {line[0]}")

# =============================================================================
#     if Pool[CharaRoll].split()[0] == "genshin":
#         URL = "https://genshin-impact.fandom.com/wiki/" + Pool[CharaRoll].split()[1]
#         htmlData = getdata(URL)
#         soup = BeautifulSoup(htmlData, "html.parser")
#         item = soup.find("img", class_ = "pi-image-thumbnail")
#         ImgURL = item["src"]
#         
#         with open("temp.txt", "w") as file:
#             file.write(URL)
#         
#         await ctx.send(Pool[-1])
#         await ctx.send(ImgURL)
#         
#         
#     elif Pool[CharaRoll].split()[0] == "alchemy":
#         URL = "https://alchemystars.fandom.com/wiki/" + Pool[CharaRoll].split()[1]
#         htmlData = getdata(URL)
#         soup = BeautifulSoup(htmlData, "html.parser")
#         item = soup.find("img", class_ = "pi-image-thumbnail")
#         ImgURL = item["src"]
#         
#         with open("temp.txt", "w") as file:
#             file.write(URL)
#         
#         await ctx.send(Pool[-1])
#         await ctx.send(ImgURL)
#     
#     else:
#         URL = "https://gamepress.gg/" + Pool[CharaRoll].split()[0] + "/" + Pool[CharaRoll].split()[1] + "/" + Pool[CharaRoll].split()[2]
#         htmlData = getdata(URL)
#         soup = BeautifulSoup(htmlData, "html.parser")
#         item = soup.find("img", class_ = "image-style-_00h")
#         if item is None:
#             item = soup.find("img", class_ = "image-style-servant-image")
#             if item is None:
#                 item = soup.find("img", typeof = "foaf:Image")
#                 if item is None:
#                     await ctx.send("404 ERROR NOT FOUND " + Pool[CharaRoll].split()[2])
#         ImgURL = "https://gamepress.gg" + item["src"]
#         
#         with open("temp.txt", "w") as file:
#             file.write(URL)
#         
#         await ctx.send(Pool[-1])
#         await ctx.send(ImgURL)
# =============================================================================
        
@client.command(
    help = "Gives website for more detail",
    brief = ""
    )
async def detail(ctx):
    with open("temp.txt", "r") as file:
        URL = file.read()
        
    await ctx.send(URL)
    
@client.command(
    help = "Searches for character of any rarity (non case sensitive)",
    brief=""
    )
async def search(ctx, *, name):
    line = searchChar(name)
    if not line:
        await ctx.send("No search result for the name {}".format(name))
    else:
        img_url = scrape_img(line)
        await ctx.send(img_url)
            
    
@client.command(
    help = "Give number for a skin of the given operator",
    brief=''
    )
async def skin(ctx, num, *, name):
    line = searchChar(name)
    
    if not line:
        await ctx.send("No search result for the name {}".format(name))
    else:
        with open("temp.txt", "w") as file:
            file.write(line[1])

        htmlData = getdata(line[1])
        soup = BeautifulSoup(htmlData, "html.parser")
        
        if line[2] == '0':
            # arknights
            # apply offset id image-tab-6
            
            divId = "image-tab-" + str(5 + int(num))
            imageTab = soup.find(id=divId)
            if imageTab is None:
                imageTab = soup.find(id="image-tab-3")
                
                if imageTab is None:
                    imageTab = soup.find(id="image-tab-1")
                
                anchor = imageTab.find("a")
                await ctx.send(anchor["href"])
                return
            
            img = imageTab.find("img")
            await ctx.send("https://gamepress.gg" + img["src"])
        
        elif line[2] == '1':
            # fgo
            # id tab c2 to c3
            
            divId = "tab-c" + str(1 + int(num))
            tab = soup.find(id=divId)
            if tab is None:
                tab = soup.find(id="tab-4")
        
            anchor = tab.find("a")
            await ctx.send(anchor["href"])
        
        elif line[2] == '2':
            # gfl
            # need to scrape another different section
            # div class=views-row
            viewRows = soup.find_all(class_='views-row')
            
            try:
                tDollImage = viewRows[int(num)-1].find_all(class_='costume-row-item')[0]
            except IndexError:
                tDollImage = soup.find(id='t-doll-image')
            
            anchor = tDollImage.find("a")
            await ctx.send(anchor["href"])
        
        elif line[2] == '3':
            # genshin
            # not available in wiki
            anchor = soup.find(class_='image image-thumbnail')
            await ctx.send(anchor["href"])
        
# =============================================================================
# @client.command(
#     help = "Gets a specific SSR character",
#     brief = ""
#     )
# async def ssr(ctx, name):
#     for character in gachalist.SSR:
#         if character.split()[-1].lower() == name.lower():
#             
#             if character.split()[0] == "genshin":
#                 URL = "https://genshin-impact.fandom.com/wiki/" + character.split()[1]
#                 htmlData = getdata(URL)
#                 soup = BeautifulSoup(htmlData, "html.parser")
#                 item = soup.find("img", class_ = "pi-image-thumbnail")
#                 ImgURL = item["src"]
#                 
#                 with open("temp.txt", "w") as file:
#                     file.write(URL)
#                 
#                 await ctx.send(ImgURL)
#                 
#             elif character.split()[0] == "alchemy":
#                 URL = "https://alchemystars.fandom.com/wiki/" + character.split()[1]
#                 htmlData = getdata(URL)
#                 soup = BeautifulSoup(htmlData, "html.parser")
#                 item = soup.find("img", class_ = "pi-image-thumbnail")
#                 ImgURL = item["src"]
#                 
#                 await ctx.send(ImgURL)
#                 
#             else:
#                 URL = "https://gamepress.gg/" + character.split()[0] + "/" + character.split()[1] + "/" + character.split()[2]
#                 htmlData = getdata(URL)
#                 soup = BeautifulSoup(htmlData, "html.parser")
#                 item = soup.find("img", class_ = "image-style-_00h")
#                 if item is None:
#                     item = soup.find("img", class_ = "image-style-servant-image")
#                     if item is None:
#                         item = soup.find("img", typeof = "foaf:Image")
#                         if item is None:
#                             await ctx.send("404 ERROR NOT FOUND " + character.split()[2])
#                 ImgURL = "https://gamepress.gg" + item["src"]
#                 
#                 with open("temp.txt", "w") as file:
#                     file.write(URL)
#                 
#                 await ctx.send(ImgURL)
# 
# @client.command(
#     help = "Gets a specific SR character",
#     brief = ""
#     )
# async def sr(ctx, name):
#     for character in gachalist.SR:
#         if character.split()[-1].lower() == name.lower():
#             
#             if character.split()[0] == "genshin":
#                 URL = "https://genshin-impact.fandom.com/wiki/" + character.split()[1]
#                 htmlData = getdata(URL)
#                 soup = BeautifulSoup(htmlData, "html.parser")
#                 item = soup.find("img", class_ = "pi-image-thumbnail")
#                 ImgURL = item["src"]
#                 
#                 with open("temp.txt", "w") as file:
#                     file.write(URL)
#                 
#                 await ctx.send(ImgURL)
#                 
#             elif character.split()[0] == "alchemy":
#                 URL = "https://alchemystars.fandom.com/wiki/" + character.split()[1]
#                 htmlData = getdata(URL)
#                 soup = BeautifulSoup(htmlData, "html.parser")
#                 item = soup.find("img", class_ = "pi-image-thumbnail")
#                 ImgURL = item["src"]
#                 
#                 await ctx.send(ImgURL)
#                 
#             else:
#                 URL = "https://gamepress.gg/" + character.split()[0] + "/" + character.split()[1] + "/" + character.split()[2]
#                 htmlData = getdata(URL)
#                 soup = BeautifulSoup(htmlData, "html.parser")
#                 item = soup.find("img", class_ = "image-style-_00h")
#                 if item is None:
#                     item = soup.find("img", class_ = "image-style-servant-image")
#                     if item is None:
#                         item = soup.find("img", typeof = "foaf:Image")
#                         if item is None:
#                             await ctx.send("404 ERROR NOT FOUND " + character.split()[2])
#                 ImgURL = "https://gamepress.gg" + item["src"]
#                 
#                 with open("temp.txt", "w") as file:
#                     file.write(URL)
#                 
#                 await ctx.send(ImgURL)
#                 
# @client.command(
#     help = "Gets a specific Rare character",
#     brief = ""
#     )
# async def r(ctx, name):
#     for character in gachalist.R:
#         if character.split()[-1].lower() == name.lower():
#             
#             if character.split()[0] == "alchemy":
#                 URL = "https://alchemystars.fandom.com/wiki/" + character.split()[1]
#                 htmlData = getdata(URL)
#                 soup = BeautifulSoup(htmlData, "html.parser")
#                 item = soup.find("img", class_ = "pi-image-thumbnail")
#                 ImgURL = item["src"]
#                 
#                 await ctx.send(ImgURL)
#             
#             else:
#                 URL = "https://gamepress.gg/" + character.split()[0] + "/" + character.split()[1] + "/" + character.split()[2]
#                 htmlData = getdata(URL)
#                 soup = BeautifulSoup(htmlData, "html.parser")
#                 item = soup.find("img", class_ = "image-style-_00h")
#                 if item is None:
#                     item = soup.find("img", class_ = "image-style-servant-image")
#                     if item is None:
#                         item = soup.find("img", typeof = "foaf:Image")
#                         if item is None:
#                             await ctx.send("404 ERROR NOT FOUND " + character.split()[2])
#                 ImgURL = "https://gamepress.gg" + item["src"]
#                 
#                 with open("temp.txt", "w") as file:
#                     file.write(URL)
#                 
#                 await ctx.send(ImgURL)
#         
#         
#                 
# @client.command(
#     help = "Gets a specific uncommon character",
#     brief = ""
#     )
# async def uc(ctx, name):
#     for character in gachalist.UC:
#         if character.split()[-1].lower() == name.lower():
#             
#             if character.split()[0] == "alchemy":
#                 URL = "https://alchemystars.fandom.com/wiki/" + character.split()[1]
#                 htmlData = getdata(URL)
#                 soup = BeautifulSoup(htmlData, "html.parser")
#                 item = soup.find("img", class_ = "pi-image-thumbnail")
#                 ImgURL = item["src"]
#                 
#                 await ctx.send(ImgURL)
#             
#             else:
#                 URL = "https://gamepress.gg/" + character.split()[0] + "/" + character.split()[1] + "/" + character.split()[2]
#                 htmlData = getdata(URL)
#                 soup = BeautifulSoup(htmlData, "html.parser")
#                 item = soup.find("img", class_ = "image-style-_00h")
#                 if item is None:
#                     item = soup.find("img", class_ = "image-style-servant-image")
#                     if item is None:
#                         item = soup.find("img", typeof = "foaf:Image")
#                         if item is None:
#                             await ctx.send("404 ERROR NOT FOUND " + character.split()[2])
#                 ImgURL = "https://gamepress.gg" + item["src"]
#                 
#                 with open("temp.txt", "w") as file:
#                     file.write(URL)
#                 
#                 await ctx.send(ImgURL)
#         
#         
#             
# @client.command(
#     help = "Gets a specific common character",
#     brief = ""
#     )
# async def c(ctx, name):
#     for character in gachalist.C:
#         if character.split()[-1].lower() == name.lower():
#        
#             URL = "https://gamepress.gg/" + character.split()[0] + "/" + character.split()[1] + "/" + character.split()[2]
#             htmlData = getdata(URL)
#             soup = BeautifulSoup(htmlData, "html.parser")
#             item = soup.find("img", class_ = "image-style-_00h")
#             if item is None:
#                 item = soup.find("img", class_ = "image-style-servant-image")
#                 if item is None:
#                     item = soup.find("img", typeof = "foaf:Image")
#                     if item is None:
#                         await ctx.send("404 ERROR NOT FOUND " + character.split()[2])
#             ImgURL = "https://gamepress.gg" + item["src"]
#             
#             with open("temp.txt", "w") as file:
#                 file.write(URL)
#             
#             await ctx.send(ImgURL)
# =============================================================================
    

client.run(os.environ.get("DISCORD_BOT_TOKEN"))
