import numpy as np
import geojson as gj
import json
from pyproj import Proj

import pandas as pd

from viktor import ViktorController
from viktor.views import GeoJSONResult
from viktor.views import GeoJSONView

from viktor.views import MapLine
from viktor.views import MapPoint
from viktor.views import MapResult
from viktor.views import MapView

# def load_roads(data):
#     with open(data) as f:
#         feauture = gj.load(f)

#     print(len(feauture['features']))

#     for i in len(feauture['features']):
#         line = MapLine();
#         for j in len(feauture['features']['coordinates'][0, 0, j]):
#             Mapline.append(MapPoint(feauture['features']['coordinates'][0, 0, j][0], feauture['features']['coordinates'][0, 0, j][1]))
#         line.




def convert_dataset(path):
    
    p_web = Proj(init='EPSG:3857')

    with open(path) as f:
        fc_in = json.load(f)
    
    fc_out = {'features': [],
        'type': 'FeatureCollection'}
    
    for feature in fc_in['features']:
        feature_out = feature.copy()
        new_coords = []
        # Project/transform coordinate pairs of each ring
        # (iteration required in case geometry type is MultiPolygon, or there are holes)

        for coordList in feature['geometry']['coordinates']:
            # unzip each coordinate pair, get first two elements and use pyproj to get it to the lat/long notation
            x2, y2 = p_web(*zip(*coordList))
            new_coords.append(list(zip(x2, y2)))
        
        print(new_coords)
        feature_out['geometry']['coordinates'] = new_coords
        # Append feature to output featureCollection
        fc_out['features'].append(feature_out)

        return fc_out




class Controller(ViktorController):

    ViktorController.label = 'mylabel'
    @GeoJSONView('GeoJSON view', duration_guess=1)
    def get_geojson_view(self, params, **kwargs):
        
        path = "data/unra_road_network.geojson"
        feature = convert_dataset(path)
            
        print(feature)
        return GeoJSONResult(feature)