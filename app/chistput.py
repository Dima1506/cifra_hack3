import json
import httpx
from geopy.distance import geodesic

fix_rast = 400

def get_new_route(start_point, end_point, promezh_point):
    cords = str(start_point[0])+','+str(start_point[1])+';'
    for i in promezh_point:
        cords+=str(i[0])+','+str(i[1])+';'
    cords+=str(end_point[0])+','+str(end_point[1])
    print('new_route'+cords)
    url = 'http://62.84.117.254:5000/route/v1/driving/'+cords+'?geometries=geojson&alternatives=false&continue_straight=true'
    r = eval(httpx.get(url).text)
    print(r)
    return list(r['routes'][0]['geometry']['coordinates'])


def good_point(point, mass_bad):
    it = 0.001
    ka1 = False
    ka2 = False
    while True:
        for j in mass_bad:
            if geodesic([point[0]+it, point[1]+it], j).meters < fix_rast:
                ka1 = True
                break
            if geodesic([point[0]-it, point[1]-it], j).meters < fix_rast:
                ka2 = True
                break
        if ka1 and ka2:
            it+=0.002
        elif ka1 == False:
            input("Press Enter to continue1...")
            return [round(point[0]+it,6), round(point[1],6)]
        elif ka2 == False:
            input("Press Enter to continue2...")
            return [round(point[0],6), round(point[1]+it,6)]



file = open('aqicn', 'r')
json_aqicn = eval(file.readline())
file.close()
mass_bad = []
mass_bad = [list(dict(i)['g'])[::-1] for i in json_aqicn['data']]

file = open('greenpeace', 'r')
json_greenpeace = eval(file.readline())
file.close()
mass_bad2 = [ [float(i[6].replace(',', '.')),float(i[7].replace(',', '.'))] for i in json_greenpeace['values'][1:]]
#print(mass_bad2)
mass_bad.extend(mass_bad2)

#print(mass_bad)
#mass_bad = [i[::-1] for i in mass_bad]
#print(mass_bad)
mass_good =[[37.57048,55.697537],[37.570105,55.697663],[37.571179,55.697057],[37.593623,55.709839],[37.597402,55.710021],[37.607276,55.71156],[37.622704,55.711276],[37.62281,55.706196],[37.630649,55.7053],[37.629897,55.705389],[37.629578,55.7045],[37.629667,55.70114],[37.634938,55.70083],[37.647058,55.698355],[37.655168,55.694809],[37.659488,55.695243],[37.662114,55.694108],[37.662237,55.693422],[37.651239,55.686402],[37.651766,55.68614],[37.655718,55.686434]]

print('ff'+str(good_point([37.661063, 55.809466], mass_bad)))

start_point = [37.57047268454096,55.69753308017714]
end_point =[37.65565733029608,55.686692650793695]
new_points = []
while True:
    ka = False
    for i in mass_good:
        for j in mass_bad:
            if geodesic(i, j).meters < fix_rast:
                point_ty = good_point(i, mass_bad)
                new_points.append(point_ty)
                print('new_points '+str(new_points))
                print('rast '+str(geodesic(i, j).meters))
                ka = True
                break
        if ka:
            break
    if ka:
        mass_good = get_new_route(start_point, end_point, new_points)
    if ka == False:
        break

print(new_points)
