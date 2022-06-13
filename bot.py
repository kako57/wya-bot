#!/usr/bin/env python3

import os
import datetime
from typing import Dict
from discord.ext import commands
from dotenv import load_dotenv

from timetables import timetables

load_dotenv()
TOKEN = os.getenv('DISCORD_TOKEN')

bot = commands.Bot(command_prefix='!')

def cur_weekday():
  return datetime.datetime.today().weekday()

def cur_time():
  return datetime.datetime.now().strftime("%H:%M")

def unpack(d: Dict, *keys):
  return tuple(d[k] for k in keys)

def cap(s: str):
  if len(s) < 1:
    return ''
  if len(s) > 1:
    return s[0].upper() + s[1:]
  return s.upper()

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

  response += f"Looking for {person_name}'s timetable for {days[day] if day != cur_weekday() else f'today ({days[day]})'}:\n"
    
  normalized_name = person_name.lower()
  if normalized_name not in timetables:
    msg = f'{person_name} was not found in the timetable database\n'
    response += msg
  else:
    for section in timetables[normalized_name][day]:
      title, start_time, end_time, location = unpack(section, 'title', 'startTime', 'endTime', 'location')
      # section_row = f'{title.ljust(20)} from {start_time.ljust(5)} to {end_time.ljust(5)} @ {location.ljust(7)}\n'
      section_row = f'{title} from {start_time} to {end_time} @ {location}\n'
      # print(section_row)
      response += section_row

  await ctx.send(response)

bot.run(TOKEN)
