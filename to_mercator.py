'''
degree to meter
'''
import inspect

import shapely.geometry
import shapely.geometry as gmt
import geopandas as gpd


def cal_utm(p):
    geo_classes = tuple([m[1] for m in inspect.getmembers(gmt, inspect.isclass)])
    # 计算投影带
    if type(p) in [int, float]:
        return int("326" + str(int(int(p) / 6) + 31))
    elif type(p) == gpd.GeoDataFrame:
        return cal_utm(p.geometry)
    elif type(p) == gpd.GeoSeries:
        return cal_utm(p.iloc[0])
    elif issubclass(type(p), geo_classes):
        x = (p.bounds[0] + p.bounds[2]) / 2
        return cal_utm(x)


#任意类型gpd.GeoSeries, gpd.GeoDataFrame转标准米制墨卡托
def to_mercator(geo):
    if type(geo) is gpd.GeoSeries:
        geo = geo.to_crs(4326)
        utm = cal_utm(geo)
        return geo.to_crs(utm)
    else:
        geo.to_crs(4326, inplace=True)
        utm = cal_utm(geo)
        geo.to_crs(utm, inplace=True)


def degree_meter_ratio(lng, lat):
    line = shapely.geometry.LineString([[lng, lat], [lng+0.001, lat+0.001]])
    len_degree = line.length
    geo = gpd.GeoSeries(line)
    geo = geo.set_crs(4326)
    geo_mc = to_mercator(geo)
    len_meter = geo_mc.iloc[0].length

    return round(len_meter / len_degree, 6)



if __name__ == '__main__':
    # gdf = get_gdf(cls='builtup_area', year=2022, adcode=name2code('xining'))
    # gdf_mc = to_mercator(gdf)

    print(degree_meter_ratio(125, 43))
