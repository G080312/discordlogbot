import os
import discord
from dotenv import load_dotenv
from FileName import image
import cv2
import tempfile

def image(content):
  try:
    img = None
    file = tempfile.NamedTemporaryFile(dir='../', delete=False)
    file.write(requests.get(content).content)
    file.close()
    img = cv2.imread(file.name)
    cv2.imwrite('files/log.png',img)
    os.remove(file.name)
    return img
  except:
    img = None
    os.remove(file.name)
    return img

ban_user = (
  1,
  1
)
bot_authors = (
  1,
  1
)

intents = discord.Intents.default()
intents.voice_states = True
intents.message_content = True
intents.members = True
bot = discord.Client(intents=intents)
load_dotenv(".env")

channelsID = 1

@bot.event
async def on_message(message):
  send_channel = bot.get_channel(channelsID)
  if message.author.bot:
    return
  elif message.guild and not message.author.id in bot_authors and not message.author.bot:
    file = open('files/index.html', 'a', encoding='UTF-8')
    for attachment in message.attachments:
      if attachment.url.endswith(("png", "jpg", "jpeg")):
        file.writelines(f"<nav><div><img src={message.author.display_avatar}></div><h1>{message.author.name}<span>{message.created_at}<samp> | {message.author} | {message.author.id} | {message.guild.name} | {message.guild.id} | {message.channel.name} | {message.channel.id}</samp></span></h1><p>{message.content}</p><strong><img src={attachment.url}></strong></nav>\n")
        file.close()
        embed = discord.Embed(color=0x4169e1)
        try:
          image(attachment.url)
          name="upload.png"
          Imagefile = discord.File(fp="files/log.png",filename=name,spoiler=False)
          embed.set_image(url=f"attachment://{name}")
          embed.add_field(name="",value=f"message: {message.content}\nchannel: {message.channel.name}({message.channel.id})")
          embed.set_author(name=message.author,icon_url=message.author.display_avatar)
          await send_channel.send(file=Imagefile,embed=embed)
        except:
          pass
    if not message.attachments:
      file = open('files/index.html', 'a', encoding='UTF-8')
      file.writelines(f"<nav><div><img src={message.author.display_avatar}></div><h1>{message.author.name}<span>{message.created_at}<samp> | {message.author} | {message.author.id} | {message.guild.name} | {message.guild.id} | {message.channel.name} | {message.channel.id}</samp></span></h1><p>{message.content}</p></nav>\n")
      file.close()
      embed = discord.Embed(color=0x4169e1)
      embed.set_author(name=message.author,icon_url=message.author.display_avatar)
      embed.add_field(name="",value=f"message: {message.content}\nchannel: {message.channel.name}({message.channel.id})")
      await send_channel.send(embed=embed)
  print(f"[GUILD] {message.author.name} > {message.content}     |[{message.guild.name}{message.guild.id}]|[{message.channel.name}{message.channel.id}]|")

@bot.event
async def on_message_delete(message):
  send_channel = bot.get_channel(channelsID)
  if message.author.bot:
    return
  elif message.guild and not message.author.id in bot_authors and not message.author.bot:
    for attachment in message.attachments:
      embed = discord.Embed(color=0xff4242)
      if attachment.url.endswith(("png", "jpg", "jpeg")):
        try:
          image(attachment.url)
          embed = discord.Embed(color=0xff4242)
          name="upload.png"
          file = discord.File(fp="files/log.png",filename=name,spoiler=False)
          embed.set_image(url=f"attachment://{name}")
          embed.add_field(name="",value=f"message: {message.content}\nchannel: {message.channel.name}({message.channel.id})")
          embed.set_author(name=message.author,icon_url=message.author.display_avatar)
          await send_channel.send(file=file,embed=embed)
        except:
          return
    if not message.attachments:
      embed = discord.Embed(color=0xff4242)
      embed.set_author(name=message.author,icon_url=message.author.display_avatar)
      embed.add_field(name="",value=f"message: {message.content}\nchannel: {message.channel.name}({message.channel.id})")
      await send_channel.send(embed=embed)

@bot.event
async def on_voice_state_update(member, before, after):
  if before.channel != after.channel:
    sendchannel = bot.get_channel(channelsID)
    channelsID = []
    if before.channel is not None and before.channel.id in channelsID:
      voice_leave = discord.Embed(color=0xff4242)
      voice_leave.set_author(name=f"leave {member.name}",icon_url=member.display_avatar)
      await sendchannel.send(embed=voice_leave)
    if after.channel is not None and after.channel.id in channelsID:
      voice_connect = discord.Embed(color=0x426eff)
      voice_connect.set_author(name=f"Join {member.name}",icon_url=member.display_avatar)
      await sendchannel.send(embed=voice_connect)

bot.run(os.getenv("TOKEN"))
