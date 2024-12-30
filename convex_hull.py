# coding: utf-8
import numpy as np
import json

def polar_angle(p0, p1):
    """2点間の偏角を計算"""
    diff = p1 - p0
    return np.arctan2(diff[1], diff[0])

def distance(p0, p1):
    """2点間の距離を計算"""
    diff = p1 - p0
    return np.sqrt(diff[0] ** 2 + diff[1] ** 2)

def graham_scan(points):
    """Graham Scan アルゴリズムによる凸包計算"""
    points_np = np.array(points)
    
    # 1. 最も下かつ左の点を基準点にする
    min_point_idx = np.argmin(points_np[:, 1] + points_np[:, 0] * 1e-6)
    base_point = points_np[min_point_idx]
    
    # 2. 偏角でソートし、偏角が同じ場合は距離でソート
    sorted_points = sorted(points_np, key=lambda p: (polar_angle(base_point, p), distance(base_point, p)))
    
    # 3. 凸包を構築
    hull = []
    for point in sorted_points:
        while len(hull) > 1 and np.cross(
            hull[-1] - hull[-2], point - hull[-1]) <= 0:
            hull.pop()
        hull.append(point)
    
    return np.array(hull)

if __name__ == '__main__':
    # 入力データの読み込み
    with open('points.geojson', 'r') as f:
        data = json.load(f)

    p_list = [feature['geometry']['coordinates'] for feature in data['features']]
    
    # 凸包計算
    convex_hull = graham_scan(p_list)

    # GeoJSON形式で結果を保存
    with open('convex_hull2.geojson', 'w') as f:
        json.dump({
            "type": "FeatureCollection",
            "features": [
                {
                    "type": "Feature",
                    "geometry": {
                        "type": "Polygon",
                        "coordinates": [convex_hull.tolist()]
                    },
                    "properties": {}
                }
            ]
        }, f)
