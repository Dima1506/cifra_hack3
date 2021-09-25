from fastapi import FastAPI
from pydantic import BaseModel
from typing import Optional
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

import httpx

app = FastAPI()

origins = [
    "https://nostalgic-euclid-82608b.netlify.app",
    "https://localhost.tiangolo.com",
    "http://localhost",
    "http://localhost:3000",
]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class Coordinates(BaseModel):
    start_lan: str
    start_lag: str
    end_lan: str
    end_lag: str

    def create(start_lan, start_lag, end_lan, end_lag):
        self.start_lan =start_lan
        self.start_lag =start_lag
        self.end_lan = end_lan
        self.end_lag = end_lag

class TextAddress(BaseModel):
    from_a: str
    to: str

@app.post("/get_address")
def get_address(address:TextAddress):
    url = 'https://geocode-maps.yandex.ru/1.x?geocode='+address.from_a+'&apikey=c0d403ab-e5be-4049-908c-8122a58acf23&format=json&results=1'
    url2 = 'https://geocode-maps.yandex.ru/1.x?geocode='+address.to+'&apikey=c0d403ab-e5be-4049-908c-8122a58acf23&format=json&results=1'
    address1 = eval(httpx.get(url).text)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
    address2 = eval(httpx.get(url2).text)['response']['GeoObjectCollection']['featureMember'][0]['GeoObject']['Point']['pos'].split(' ')
    #t = eval('''{'start_lan':str(address1[0]),'start_lag':str(address1[1]),'end_lan':str(address2[0]), 'end_lag':str(address2[1])}''')
    cord = Coordinates(start_lan = str(address1[0]),start_lag =str(address1[1]),end_lan = str(address2[0]),end_lag=str(address2[1]))
    return get_route(cord)



def test_coordinate(start_point, end_point, promezh_point):
    return [0,2]


@app.post("/get_route")
def get_route(coordinate:Coordinates):
    url = 'http://62.84.117.254:5000/route/v1/driving/'+coordinate.start_lan+','+coordinate.start_lag+';'+coordinate.end_lan+','+coordinate.end_lag+'?geometries=geojson&alternatives=false&continue_straight=true'
    r = httpx.get(url)
    print(r.text)
    json_from_machine = eval(r.text)
    massive_coordinate = []
    massive_coordinate.append([float(coordinate.start_lan),float(coordinate.start_lag)])
    #print(json_from_machine['routes'][0]['duration'])
    massive_coordinate.extend(list(json_from_machine['routes'][0]['geometry']['coordinates']))
    massive_coordinate.append([float(coordinate.end_lan),float(coordinate.end_lag)])
    print(massive_coordinate)
    f = test_coordinate(start_point=[float(coordinate.start_lan),float(coordinate.start_lag)],
                                 end_point=[float(coordinate.end_lan),float(coordinate.end_lag)],
                                 promezh_point = list(json_from_machine['routes'][0]['geometry']['coordinates']))
    kkal = 2.548*json_from_machine['routes'][0]['duration']/60.0
    json_end = '{"type": "FeatureCollection","kkal":'+str(kkal)+',"features": [{"type": "Feature","properties": {"id": 1,"name": "youtube"},"geometry": {"type": "LineString","coordinates":'+str(massive_coordinate)+'}}]}'
    return JSONResponse(content=eval(json_end))
