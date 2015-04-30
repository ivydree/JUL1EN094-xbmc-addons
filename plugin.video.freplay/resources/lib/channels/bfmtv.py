#-*- coding: utf-8 -*-
import urllib,urllib2
import xml.dom.minidom
import json

title=['BFM TV']
img=['bfmtv']
readyForUse=True

def get_token():
  jsonFile=urllib2.urlopen('http://api.nextradiotv.com/bfmtv-android/4/').read()
  jsonParser= json.loads(jsonFile)
  return jsonParser['session']['token']
  
def list_shows(channel,param):  
  shows=[]
           
  shows.append( [channel,'TOUTACTU', "Toute l'actu en video".encode('utf-8'),'','shows'] )
  jsonFile=urllib2.urlopen('http://api.nextradiotv.com/bfmtv-android/4/%s/getMainMenu' % (get_token() )).read()
  jsonParser= json.loads(jsonFile)
  for menu in jsonParser['menu']['right'] :
    if menu['type']=='REPLAY':
      shows.append( [channel,menu['category'], menu['title'].encode('utf-8'),menu['image_url'].encode('utf-8'),'shows'] )
    
  return shows

def getVideoURL(channel,videoId):
  jsonFile=urllib2.urlopen('http://api.nextradiotv.com/bfmtv-android/4/%s/getVideo?idVideo=%s&quality=2' % (get_token() ,videoId)).read()
  jsonParser= json.loads(jsonFile)
  video_url=''
  quality=0
  for medium in jsonParser['video']['medias']:
    if medium['encoding_rate']>quality:
      quality=medium['encoding_rate']
      video_url=medium['video_url']
      
  return video_url
    
def search(channel,keyWord):
  return list_shows(channel,keyWord)

def list_videos(channel,show):
  videos=[] 
  
  if show=='TOUTACTU': 
    jsonFile=urllib2.urlopen('http://api.nextradiotv.com/bfmtv-android/4/%s/getLastVideosList?count=40&page=1' % (get_token() )).read()
  else:
    jsonFile=urllib2.urlopen('http://api.nextradiotv.com/bfmtv-android/4/%s/getVideosList?count=40&page=1&category=%s' % (get_token() ,show)).read()
  jsonParser= json.loads(jsonFile)
  for video in jsonParser['videos'] :
    videoId=video['video']   
    title=video['title'].encode('utf-8')      
    icon=video['image'].encode('utf-8')
    desc=video['description'].encode('utf-8')
    duration=video['video_duration_ms']/1000
    infoLabels={ "Title": title,"Plot":desc,"Duration": duration} 
    videos.append( [channel, videoId, title, icon,infoLabels,'play'] )     
    
  return videos

  