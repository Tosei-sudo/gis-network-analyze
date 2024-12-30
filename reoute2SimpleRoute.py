# codind: utf-8

import json
import hashlib
import collections

def point2_hash(point):
    return hashlib.sha256(str(point).encode()).hexdigest()

with open('paths2.geojson', 'r') as f:
    data = json.load(f)

points = []
point_hash_map = {}
path_map = {}
endpoint_hash_map = {}

for feature in data['features']:
    coordinates = feature['geometry']['coordinates']
    
    for point in coordinates:
        point_hash = point2_hash(point)
        points.append(point_hash)
        
        point_hash_map[point_hash] = point
    
    start_point = coordinates[0]
    start_point_hash = point2_hash(start_point)
    
    end_point = coordinates[-1]
    end_point_hash = point2_hash(end_point)
    
    path_map[start_point_hash + end_point_hash] = coordinates
    
    endpoint_hash_map[end_point_hash] = start_point_hash

pointCount = collections.Counter(points)

del points

while(True):
    simplify_count = 0
    for (path_key, points) in path_map.items():
        start_point = points[0]
        start_point_hash = path_key[:64]
        
        end_point = points[-1]
        end_point_hash = path_key[64:]
        
        if pointCount[start_point_hash] <= 2:
            before_point_hash = endpoint_hash_map.get(start_point_hash)
            
            if before_point_hash is None:
                continue
            
            before_path_hash = before_point_hash + start_point_hash
            before_coordinates = path_map.get(before_path_hash)
            
            current_coordinates = path_map.get(start_point_hash + end_point_hash)
            
            if before_coordinates is None or current_coordinates is None:
                continue
            
            new_coordinates = before_coordinates + current_coordinates[1:]
            
            new_path_hash = before_point_hash + end_point_hash
            
            path_map[new_path_hash] = new_coordinates
            
            del path_map[before_point_hash + start_point_hash]
            del path_map[start_point_hash + end_point_hash]
            del endpoint_hash_map[start_point_hash]
            del pointCount[start_point_hash]
            
            endpoint_hash_map[end_point_hash] = before_point_hash
            
            simplify_count += 1
    print(simplify_count)
    if simplify_count == 0:
        break
            
with open('simplePaths2.geojson', 'w') as f:
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
            } for path in path_map.values()
        ]
    }, f)