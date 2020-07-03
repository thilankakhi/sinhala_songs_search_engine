import json
from googletrans import Translator
import re
import os

separator = ','
translator=Translator()
final_songs_list= []
id = 1

with open('sinhala_songs.json' , encoding='utf-8') as songs:
  songs_list = json.load(songs)

def traslate_value(multiple):
  translated = []
  for one in multiple:
    translated.append(translator.translate(one,dest="si").text)
  if(len(translated)!=1):
   return separator.join(translated)
  else:
   return translated[0]

for song in songs_list:
    formatted_song = {
        "id": id,
        "title" : traslate_value(song['title']),
        "artist" :  traslate_value(song['artist']),
        "genre" : traslate_value(song['genre']),
        "writer" : traslate_value(song['writer']),
        "music" : traslate_value(song['music']),
        "visits" : int(song['visits'].replace(",","")),
        "lyrics" : song['lyrics'].strip()
    }
    print(formatted_song)
    final_songs_list.append(formatted_song)
    id +=1

with open('sinhala_songs-processed.json' ,'w', encoding='utf-8') as outf:
  json.dump(final_songs_list,outf,indent=4,ensure_ascii=False)