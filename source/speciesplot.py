import pandas as pd
import numpy as np
import datetime
from datetime import datetime as dt
from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
from matplotlib.collections import PatchCollection
from shapely.geometry import Point, Polygon, MultiPoint, MultiPolygon
from shapely.prepared import prep
import fiona
from descartes import PolygonPatch
import json
from osgeo import ogr

ld = pd.read_csv('rbnu_verbatim.csv')
ld['count'] = ld['individualCount']
ld['lat'] = ld['decimalLatitude']
ld['lon'] = ld['decimalLongitude']
del(ld['decimalLatitude'], ld['decimalLongitude'], ld['individualCount'])
ld['date'] = np.to_datetime(ld['date'])
keep = ['date', 'lat', 'lon', 'count']
ld = ld[keep]

# ecoregions map from http://www.fs.fed.us/rm/ecoregions/products/map-ecoregions-north-america/
shapefilename = '/home/jon/data/eco-na-shp/recode'
shp = fiona.open(shapefilename + '.shp')
coords = shp.bounds
shp.close

w, h = coords[2] - coords[0] - 260, coords[3] - coords[1]


m = Basemap(width=12000000, height=8000000,
            resolution='l', projection='laea',
            lat_1=35., lat_2=55, lat_0=45, lon_0=-107.)

_out = m.readshapefile(shapefilename, name='ecoregions', drawbounds=False, color='none', zorder=2)
df_map = pd.DataFrame({
    'poly': [Polygon(region) for region in m.ecoregions],
    'name': [region['ECOCODE'] for region in m.ecoregions_info]
})
mapped_points = [Point(m(mapped_x, mapped_y)) for mapped_x, mapped_y in zip(ld['lon'],
                 ld['lat'])]
all_points = MultiPoint(mapped_points)

region_polygons = prep(MultiPolygon(list(df_map['poly'].values)))
region_points = filter(region_polygons.contains, all_points)
