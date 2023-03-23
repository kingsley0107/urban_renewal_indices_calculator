
# -*- coding: utf-8 -*-
from IndexCalculator import *
from tqdm import tqdm
import warnings
warnings.filterwarnings('ignore')


def calculate_indicators(raw_poi_path: str, path_block: str, raw_aoi_green_path: str, raw_aoi_path: str, path_raw_road: str):
    """计算函数

    Returns:
        _type_: block
    """

    block = block_area(path_block)
    raw_poi = gpd.read_file(raw_poi_path)
    raw_aoi_green = gpd.read_file(raw_aoi_green_path)
    raw_aoi = gpd.read_file(raw_aoi_path)
    raw_road = gpd.read_file(path_raw_road)[['geometry']]

    to_mercator(block)
    to_mercator(raw_poi)
    to_mercator(raw_aoi_green)
    to_mercator(raw_aoi)
    to_mercator(raw_road)

    #   1.计算POI覆盖率
    print("*********   POI_COVERAGE   *********")
    for poi_type in tqdm(['超市', '便利店', '菜市场', '快递站点', '社区服务点', '体育设施', '便民服务设施', '充电站', '加油站', '公交站', '轨道站点']):
        res = poi_coverage(raw_poi, block, poi_type,
                           threshold=POI_BUFFER_MAP[poi_type])
        target_column = res[res.columns[-1]]
        block[target_column.name] = target_column.values
    #   uncomment if interrupt here
    #   return block

    #   2.计算AOI覆盖率
    print("*********   AOI_COVERAGE   *********")
    for aoi_type in tqdm(['绿地']):
        res = aoi_coverage(raw_aoi_green, block, aoi_type,
                           threshold=AOI_BUFFER_MAP[aoi_type])
        target_column = res[res.columns[-1]]
        block[target_column.name] = target_column.values
    #   uncomment if interrupt here
    #   return block

    #   3.计算POI个数
    print("*********   POI_COUNT   *********")
    for poi_type in tqdm(['充电站', '加油站', '企业']):
        res = count_poi_with_buffer(
            raw_poi, block, poi_type, POI_BUFFER_MAP[poi_type])
        target_column = res[res.columns[-1]]
        block[target_column.name] = target_column.values
    #   uncomment if interrupt here
    #   return block

    #   4.计算屋顶面积
    print("*********   AOI_ROOF_AREA   *********")
    for aoi_type in tqdm(['屋顶面积', '住宅', '商业建筑', '工业建筑']):
        res = aoi_roof_area(raw_aoi, block, aoi_type)
        target_column = res[res.columns[-1]]
        block[target_column.name] = target_column.values
    #   uncomment if interrupt here
    #   return block

    for aoi_type in tqdm(['绿地']):
        res = aoi_roof_area(raw_aoi_green, block, aoi_type)
        target_column = res[res.columns[-1]]
        block[target_column.name] = target_column.values
    #   uncomment if interrupt here
    #   return block

    #   5.计算建筑面积
    print("*********   AOI_FLOOR_AREA   *********")
    for aoi_type in tqdm(['住宅', '商业建筑', '酒店', '写字楼', '学校', '医院', '工业建筑', '建筑']):
        res = aoi_floor_area(raw_aoi, block, aoi_type)
        target_column = res[res.columns[-1]]
        block[target_column.name] = target_column.values
    #   uncomment if interrupt here
    #   return block

    # 6.建筑密度、容积率及路网密度
    block['建筑密度'] = block['屋顶面积'] / block['block_area']
    block['容积率'] = block['建筑面积'] / block['block_area']
    res = road_dens(raw_road, block)
    target_column = res[res.columns[-1]]
    block[target_column.name] = target_column.values
    return block


if __name__ == '__main__':
    # 数据读取&坐标转换
    raw_poi_path = r'./poi.geojson'
    path_block = r'./raw_block.geojson'
    raw_aoi_green_path = r'./green_space_aoi.geojson'
    raw_aoi_path = r'./buildings.geojson'
    path_raw_road = r'./road/ctl_1984.shp'

    #   function
    block = calculate_indicators(raw_poi_path=raw_poi_path, path_block=path_block,
                                 raw_aoi_green_path=raw_aoi_path, raw_aoi_path=raw_aoi_path, path_raw_road=path_raw_road)

    #   output
    block.to_file(r'./verify/result.geojson', driver='GeoJSON')
