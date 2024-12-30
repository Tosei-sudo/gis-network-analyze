# codind: utf-8

import json
import hashlib

def point2Hash(point):
    return hashlib.md5(str(point).encode()).hexdigest()

import glob

features = []

for file in glob.glob('data/*.geojson'):
    with open(file, 'r') as f:
        data = json.load(f)
        features.extend(data['features'])

# with open('load.geojson', 'r') as f:
#     data = json.load(f)

class PointFeature:
    def __init__(self):
        self._point = None
        self.before = None
        self.hash = ""
    
    def setPoint(self, point):
        self._point = point
        self.hash = point2Hash(point)

    def toGeoJSON(self):
        return {
            "type": "Feature",
            "geometry": {
                "type": "Point",
                "coordinates": self._point
            },
            "properties": {
                "hash": self.hash,
                "before": self.before,
            }
        }

points = []

for feature in features:
    before = None
    if feature['geometry']['type'] == 'LineString':
        for point in feature['geometry']['coordinates']:
            pointFeature = PointFeature()
            
            pointFeature.setPoint(point)
            pointFeature.before = before
            
            points.append(pointFeature)
            
            before = pointFeature.hash
            
    elif feature['geometry']['type'] == 'MultiLineString':
        for line in feature['geometry']['coordinates']:
            for point in line:
                pointFeature = PointFeature()
                
                pointFeature.setPoint(point)
                pointFeature.before = before
            
                points.append(pointFeature)
                
                before = pointFeature.hash

geojson = {
    "type": "FeatureCollection",
    "features": [point.toGeoJSON() for point in points]
}

with open('points2.geojson', 'w') as f:
    json.dump(geojson, f)