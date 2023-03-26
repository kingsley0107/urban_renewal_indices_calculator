from Calculator.PointIndex import poi_coverage_cal, count_poi_with_buffer
from Calculator.AoiIndex import aoi_area_cal, aoi_coverage_cal, building_roof_area_cal, building_floor_area_cal
from Calculator.LineIndex import road_dens_cal
from config.static_vars import *
import geopandas as gpd


def poi_coverage(poi_path, block_path, buffer_distance, poi_type, output_path):
    points = gpd.read_file(poi_path)
    blocks = gpd.read_file(
        block_path)
    res = poi_coverage_cal(points, blocks, poi_type, buffer_distance)
    res.to_file(output_path, driver='GeoJSON')
    return res


def poi_count(poi_path, block_path,
              buffer_distance, poi_type, output_path):
    points = gpd.read_file(poi_path)
    blocks = gpd.read_file(
        block_path)
    res = count_poi_with_buffer(points, blocks, buffer_distance, poi_type)
    res.to_file(output_path, driver='GeoJSON')
    return res


def aoi_area(aoi_path, output_path):
    aoi = gpd.read_file(aoi_path)
    res = aoi_area_cal(aoi)
    res.to_file(output_path, driver='GeoJSON')
    return res


def aoi_coverage(aoi_path: str, block_path: str, aoi_type: str, threshold: int, output_path: str):
    aoi = gpd.read_file(aoi_path)
    block = gpd.read_file(block_path)
    res = aoi_coverage_cal(aoi, block, aoi_type, threshold)
    res.to_file(output_path, driver='GeoJSON')
    return res


def building_roof_area(bd_path: str, block_path: str, bd_type: str, output_path: str):
    bd = gpd.read_file(bd_path)
    block = gpd.read_file(block_path)
    res = building_roof_area_cal(bd, block, bd_type)
    res.to_file(output_path, driver='GeoJSON')


def building_floor_area(bd_path: str, block_path: str, bd_type: str, height_field, height_per_floor, output_path: str):
    bd = gpd.read_file(bd_path)
    block = gpd.read_file(block_path)
    res = building_floor_area_cal(bd, block, bd_type)
    res.to_file(output_path, driver='GeoJSON')


def road_density(road_path, block_path, output_path):
    road = gpd.read_file(road_path)
    block = gpd.read_file(block_path)
    res = road_dens_cal(road, block)
    res.to_file(output_path, driver='GeoJSON')


if __name__ == '__main__':
    # poi_coverage(poi_path, block_path, poi_buffer_dis, poi_type, output_path)
    # poi_count(poi_path, block_path,
    #           poi_buffer_dis, poi_type, output_path)
    # res = aoi_area(gpd.read_file(block_path))
    # aoi_coverage(aoi_path, block_path, '公园绿地', aoi_buffer_dis, output_path)
    # building_roof_area(bd_path, block_path, bd_type, output_path)
    building_floor_area(bd_path,
                        block_path, bd_type, height_field, height_per_floor, output_path)
    # road_density(road_path, block_path, output_path)
