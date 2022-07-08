#!/usr/bin/python

from tkinter import *
from tkinter import ttk
import requests


try:
    locale_file=open("location.txt")
    api_file=open("weather.api")
except:
    print("""
!!! Location/API details not found !!!
Place the appropriate files in the same folder as the program file
*API file name should be 'weather.api'
*Location file name should be 'location.txt'
""")
    exit()

loc_name,loc_code=[],[]
api=api_file.read()
api=api.strip()
for x in locale_file:
    x=x.strip()
    temp=x.split(":")
    loc_name.append(temp[0])
    loc_code.append(temp[1])

color0="#6f226f"
color1="#ff2222"
color2="#1c1c1c"
color3="#2222ff"
color4="#eeeeee"
color5="#cc0000"
color6="#0000cc"
color7="#55aa55"
color8="#5555ff"

nil = "<Not Found>"

class Forecast:
    def __init__(self,forecast_info):
        self.forecast=forecast_info['list'] or nil

class Geo:
    def __init__(self,geo_info):
        self.name=geo_info['name'] or nil
        self.lat=str(geo_info['lat']) or nil
        self.lon=str(geo_info['lon']) or nil
        self.country_code=geo_info['country'] or nil
        self.country_name=loc_name[loc_code.index(self.country_code)] or nil
        self.state=geo_info["state"] or nil
        
class Weather:
    def __init__(self,weather_info):
        self.main_weather=weather_info["weather"] or nil
        self.temp=weather_info["main"] or nil
        self.visibility=weather_info['visibility'] or nil
        self.wind=weather_info['wind'] or nil
        self.timezone_epoch=str(weather_info['timezone']) or nil
        self.time_convertion()
    
    def time_convertion(self):
        temp=str(int(self.timezone_epoch)/3600)
        hr_min=temp.split(".")
        min=str(int(float("0."+hr_min[-1])*60))
        self.timezone_actual=hr_min[0]+":"+min+"hrs (UTC)"

class Extract:
    def __init__(self,city_info):
        geo_info=requests.get("https://api.openweathermap.org/geo/1.0/direct?q="+city_info+"&limit=1&appid="+api)
        geo_info=geo_info.json()
        geo_info=geo_info[0]
        self.geo=Geo(geo_info)
        weather_info=requests.get('https://api.openweathermap.org/data/2.5/weather?lat='+self.geo.lat+'&lon='+self.geo.lon+'&appid='+api)
        weather_info=weather_info.json()
        self.weather=Weather(weather_info)
        forecast_info=requests.get('https://api.openweathermap.org/data/2.5/forecast?lat='+self.geo.lat+'&lon='+self.geo.lon+'&appid='+api)
        forecast_info=forecast_info.json()
        self.forecast=Forecast(forecast_info)
    
    def print_info(self):
        inner_frame.pack(expand=True,fill=BOTH,side=BOTTOM,padx=1,pady=1)
        Label(  lower_frame,
                text=" | Location: "+self.geo.name+"| State: "+self.geo.state+"| Country: "+self.geo.country_name+" ("+self.geo.country_code+")"+"| Latitude: "+self.geo.lat+"| Longitude: "+self.geo.lon+"| Timezone: "+self.weather.timezone_actual+"| ",
                background=color2,foreground=color4,justify=CENTER).pack(anchor="n",padx=2,pady=2,fill=X,side=TOP)
        weather_list=[]
        forecast=self.forecast.forecast
        for x in range(5):
            temp_list=[]
            while True:
                temp_forecast=forecast.pop(0)
                dt_forecast=temp_forecast["dt_txt"].split()
                temp1=forecast[0]
                dt1=temp1["dt_txt"].split()
                if dt_forecast[0]<dt1[0]:
                    temp_list.append(temp_forecast)
                    break
                temp_list.append(temp_forecast)
            weather_list.append(temp_list)
        
        for day_index in range(5):
            weather_day = weather_list.pop(0)
            full_info=""
            num=1
            for x in weather_day:
                date_time=x["dt_txt"].split()
                weather_main=x["weather"][0]["main"]
                weather_description=x["weather"][0]["description"]
                weather_humidity=x["main"]["humidity"]
                temp=x["main"]["feels_like"]-273.15
                date_list=date_time[0].split("-")
                date_list.reverse()
                date_info=date_list[0]+"/"+date_list[1]+"/"+date_list[2]
                full_info+="\n\n"+str(num)+") Time:"+date_time[1][:-3]+"\nWeather: "+weather_main+" ("+weather_description+")\nTemp: "+str(temp)[:4]+"*C, Humidity: "+str(weather_humidity)+"%"
                num+=1
            Label(day_list[day_index],text="Date:"+date_info+full_info,justify=CENTER,foreground=color4,background=color2).pack(anchor="n",side=TOP)
        for day in day_list:
            day.pack(anchor="nw",side=LEFT,expand=True,fill=BOTH,pady=2,padx=1) 

def search_info():
    global details
    city_info=city.get()
    loading.pack_forget()
    warning_empty.pack_forget()
    warning_error.pack_forget()
    success.pack_forget()
    if not city_info:
        warning_empty.pack()
        return
    try:
        loading.pack()
        for widgets in lower_frame.winfo_children():
            widgets.pack_forget()
        for b in day1.winfo_children(),day2.winfo_children(),day3.winfo_children(),day4.winfo_children(),day5.winfo_children():
            for x in b:
                x.destroy()
        root.update()
        details=Extract(city_info)
        loading.pack_forget()
        details.print_info()
        success.pack()
    except:
        loading.pack_forget()
        warning_error.pack()

root = Tk()
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
root.title("Weather Search")
root.attributes("-fullscreen",True)
root.resizable(False,False)
root.config(background=color2)

style = ttk.Style()
style.configure("Custom.TLabel",background=color4,relief=FLAT)

upper_frame=Frame(root,width=200,height=10,bg=color2)
upper_frame.pack_configure(padx=2,pady=2,side=TOP,fill=X)
upper_frame.pack()

close=Button(upper_frame,text="X",font=("Sans Bold",7),background=color1,foreground=color4,border=0,activebackground=color5,activeforeground=color4,command=root.destroy)
close.pack(pady=0,padx=0,ipady=0,anchor="ne",side=RIGHT)

title=Label(upper_frame,text="                              World Weather Search                              ",font=("Sans Bold",17),background=color0,foreground=color4,justify=CENTER)
title.pack(pady=5,anchor="n",side=TOP)

city_text = ttk.Label(upper_frame,text="Enter the City name:",font=("Arial",11),background=color2,foreground=color4)
city_text.pack(anchor="n",padx=50,side=TOP)


display=''
city = ttk.Entry(upper_frame,font=("Arial",10),style="Custom.TLabel",textvariable=display,justify=CENTER)
city.focus()
city.pack(ipadx=50,pady=5,padx=10,after=city_text,anchor="n")

search=Button(upper_frame,text="Search!",font=("Arial",10),background=color3,foreground=color4,borderwidth=0,justify=CENTER,activebackground=color6,activeforeground=color4,takefocus=True,command=search_info)
search.pack(after=city,padx=10,pady=10,anchor="n")

lower_frame=Frame(root,width=1000,height=700,bg=color0)
lower_frame.pack_configure(after=upper_frame,padx=1,pady=1,expand=True,fill=BOTH)
lower_frame.pack()

inner_frame=Frame(lower_frame,width=1000,height=700,background=color0)

day1=Frame(inner_frame,background=color2)
day2=Frame(inner_frame,background=color2)
day3=Frame(inner_frame,background=color2)
day4=Frame(inner_frame,background=color2)
day5=Frame(inner_frame,background=color2)

day_list=[day1,day2,day3,day4,day5]

warning_error=Label(upper_frame,text="Oops! Something went wrong! Try again with a Valid Input or check the Network Connection!",background=color2,foreground=color1,font=("Arial",10))
warning_empty=Label(upper_frame,text="Input is Empty! Enter a Location name to search",background=color2,foreground=color1,font=("Arial",10))
loading=Label(upper_frame,text="Please wait! Loading...",background=color2,foreground=color8,font=("Arial",10))
success=Label(upper_frame,text="Search Successful!",background=color2,foreground=color7,font=("Arial",10))

root.bind("<Key-Return>",lambda x: search_info())

root.mainloop()
