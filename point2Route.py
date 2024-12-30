# codind: utf-8

import json
import hashlib

def point2Hash(point):
    return hashlib.md5(str(point).encode()).hexdigest()

with open('points2.geojson', 'r') as f:
    data = json.load(f)

pointHashMap = {}

paths = []

for feature in data['features']:
    point = feature['geometry']['coordinates']
    pointHash = feature['properties']['hash']
    
    pointHashMap[pointHash] = point

for feature in data['features']:
    point = feature['geometry']['coordinates']
    pointHash = feature['properties']['before']
    
    if pointHash is not None:
        paths.append([point, pointHashMap.get(pointHash)])

with open('paths2.geojson', 'w') as f:
    json.dump({
        "type": "FeatureCollection",
        "features": [
            {
                "type": "Feature",
                "geometry": {
                    "type": "LineString",
                    "coordinates": path
                },
                "properties": {
                    
                }
            } for path in paths
        ]
    }, f)
    