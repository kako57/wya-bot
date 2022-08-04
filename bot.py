#!/usr/bin/env python3

import os
import datetime
from discord.ext import commands
from dotenv import load_dotenv

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from models import User

load_dotenv()

db_path = os.getenv('DB_PATH')
if db_path is None or db_path == '':
  db_path = 'sqlite:///:memory:'
else:
  db_path = f'sqlite:///{db_path}'

engine = create_engine(db_path, echo=True)

# Session class for database access
Session = sessionmaker(bind=engine)

TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

def cur_weekday():
  return datetime.datetime.today().weekday()

def cur_time():
  return datetime.datetime.now().strftime("%H:%M")

def capitalize(s: str):
  if len(s) < 1:
    return ''
  if len(s) > 1:
    return s[0].upper() + s[1:]
  return s.upper()

@bot.command(name='register', help="Register yourself.\nYou can pass a `preferred_name`", pass_context=True)
async def register(ctx, preferred_name=None):
  session = Session()
  response = ""
  if preferred_name is None:
    preferred_name = ctx.message.author.display_name
  print(f'registering user id {ctx.message.author.id} with name {preferred_name}')
  try:
    session.add(User(name=preferred_name, discord_id=ctx.message.author.id))
    session.commit()
    response += f"<@{ctx.message.author.id}> has been registered as {preferred_name}\n"
  except:
    response += f"There was a problem registering you. Are you already registered?\n"

  session.close()

  await ctx.send(response)


@bot.command(name='rename', help="Change your preferred name to new_name")
async def rename(ctx, new_name):
  response = ""
  if new_name is None or not isinstance(new_name, str):
    response += "new_name not provided"
    await ctx.send(response)
    return
  session = Session()
  print(f'registering user id {ctx.message.author.id} with name {new_name}')
  session.add(User(name=new_name, discord_id=ctx.message.author.id))
  session.close()
  await ctx.send(response)

@bot.command(name='wya', help="Slaps `person_name`'s timetable in chat")
async def wya(ctx, person_name, day=None):
  response = ''
  days = [
    'monday',
    'tuesday',
    'wednesday',
    'thursday',
    'friday',
    'saturday',
    'sunday'
  ]

  if day is None:
    day = cur_weekday()
  elif isinstance(day, str):
    day = day.strip().lower()
    if day in days:
      day = days.index(day)
    else:
      response += 'WARNING: Cannot parse day. Bot will use the day today instead.\n'
      day = cur_weekday()

  response += f"Looking for {person_name}'s timetable for {capitalize(days[day]) if day != cur_weekday() else f'today ({capitalize(days[day])})'}:\n"

  await ctx.send(response)

bot.run(TOKEN)
