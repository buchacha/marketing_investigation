import requests 
from PIL import Image
from io import BytesIO
from PIL import ImageFont
from PIL import ImageDraw 
import os
import re

class Place:
	name=''
	rating=''
	website=''
	
	def __init__(self, nam='', rat='', web=''):
		self.name=nam
		self.rating=rat
		self.website=web

symbols = (u"абвгдеёжзийклмнопрстуфхцчшщъыьэюяАБВГДЕЁЖЗИЙКЛМНОПРСТУФХЦЧШЩЪЫЬЭЮЯ",u"abvgdeejzijklmnoprstufhzcss_y_euaABVGDEEJZIJKLMNOPRSTUFHZCSS_Y_EUA")

tr = {ord(a):ord(b) for a, b in zip(*symbols)}
# api-endpoint 

def update_progress(progress):
    fill_chars=int(progress/5)
    print ('\r[{0}{1}] {2}%'.format('#'*(fill_chars), ' '*(20-fill_chars), progress), end="")
    
def clean_string(name):
	regex = re.compile('[^0-9a-zA-Zа-яА-Я]')
	#First parameter is the replacement, second parameter is your input string
	return regex.sub('', name)
	
key="AIzaSyBDgfs58nqW-HOv9aIFnMhhhsMd1H62eLcd8I"
URL = "https://maps.googleapis.com/maps/api/geocode/json?key="+key
  
# location given here 

location = input("enter location (e.g \"moscow\"): ")
if location=="":
	location="moscow"

#location = "new york"
# defining a params dict for the parameters to be sent to the API 

PARAMS = {'address':location} 

# sending get request and saving the response as response object 

r = requests.get(url = URL, params = PARAMS) 

# extracting data in json format 

data = r.json() 
# extracting latitude, longitude and formatted address  
# of the first matching location 

latitude = data['results'][0]['geometry']['location']['lat'] 

longitude = data['results'][0]['geometry']['location']['lng'] 

formatted_address = data['results'][0]['formatted_address'] 

# printing the output 

print("Latitude:%s\nLongitude:%s\nFormatted Address:%s"
      %(latitude, longitude,formatted_address)) 
      
keyword=input("type in keyword (cafe): ")

if keyword=="":
	keyword="cafe"

radius=input("type in radius (1000 m): ")

if radius=="":
	radius="1000"

URL="https://maps.googleapis.com/maps/api/place/nearbysearch/json?location="+str(latitude)+","+str(longitude)+"&fields=name,place_id,photo_reference&radius="+radius+"&keyword="+keyword+"&key="+key

r = requests.get(url = URL) 

# extracting data in json format 

data = r.json() 
#font = ImageFont.truetype("sans-serif.ttf", 16)

n=len(data['results'])
if n>0:
	dir="/storage/emulated/0/"+location+"_"+keyword+"_"+radius
	if not os.path.exists(dir):
		os.makedirs(dir)
	n_cur=0
	for res in data['results']:
		n_cur=n_cur+1
		update_progress(round(n_cur/n*100))
		rating=str(res['rating'])
		id=res['place_id']
		try:
			photo_reference=res['photos'][0]['photo_reference']
			URL="https://maps.googleapis.com/maps/api/place/photo?maxwidth=400&photoreference="+photo_reference+"&key="+key
			r = requests.get(url = URL) 
			i = Image.open(BytesIO(r.content))
		
			URL="https://maps.googleapis.com/maps/api/place/details/json?place_id="+id+"&fields=website&key="+key
			r = requests.get(url = URL)
			data=r.json()
			text=""
			try:
				text=data['result']['website']
			except KeyError:
				print()
				print(res['name']+" doesn't provide website")
	
			draw = ImageDraw.Draw(i)
			draw.rectangle((20, 20, 350, 70), outline='black', fill='white')
			draw.text((30, 30), res['name'].translate(tr)+"\n"+rating, fill='black')
			
			i.save(dir+"/"+clean_string(res['name']).translate(tr)+".png")
		except KeyError:
			print(res['name']+"doesn't provide photos")
		except UnicodeError:
			print('\n'+res['name'].translate(tr)+"has non inicode chars. Isn't saved :(.")
else:
	print("нет объектов с заданными параметрами")
