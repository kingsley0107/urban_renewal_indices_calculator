# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
from to_mercator import to_mercator
import matplotlib.pyplot as plt
import matplotlib
matplotlib.rcParams['font.sans-serif'] = ['SimHei']   # 用黑体显示中文
matplotlib.rcParams['axes.unicode_minus'] = False     # 正常显示负号


FILTER_MAP = {
    '超市': """pois[(pois['type'].str.contains('超级市场')) | (pois['type'].str.contains('超市')) | ((pois['name_1'].str.contains('超市')) & (pois['common_type'].str.contains('便利店') == False) & (pois['type'].str.contains('购物相关场所')) & (pois['name_1'].str.contains('空压机') == False))]""",
    '便利店': """pois[(pois['type'].str.contains('便利店') & ~pois['type'].str.contains('超市')) | pois['common_type'].str.contains('便利店')]""",
    '菜市场': """pois[pois['type'].str.contains('综合市场;蔬菜市场') | (pois['type'].str.contains('综合市场;综合市场') & pois['name_1'].str.match('.*贸.*|.*市场.*')) | (pois['type'].str.contains('水产海鲜市场') & ~pois['type'].str.contains('餐饮') & ~pois['type'].str.contains('企业') & ~pois['type'].str.contains('生活服务场所') & ~pois['type'].str.contains('基地')) | (pois['type'].str.contains('农副产品市场') & ~pois['type'].str.contains('公司') & ~pois['type'].str.contains('餐饮') & ~pois['type'].str.contains('便利店'))]""",
    '快递站点': """pois[pois['type'].str.contains('物流速递') & pois['name_1'].str.match('.*驿站.*|.*蜂巢.*|.*丰巢.*|.*收寄.*|.*快递超市.*|.*柜.*|.*代.*')]""",
    '社区服务点': """pois[(pois['type'].str.contains("社区") | pois['name_1'].str.contains("社区活动") | pois['name_1'].str.contains("社区服务") | pois['name_1'].str.match(".*社区.*中心.*"))]""",
    '体育设施': """pois[(pois['type'].str.contains("乒乓球|篮球|健身|台球|游泳|溜冰|综合体育|羽毛|足球|跆拳道|高尔夫|运动场所|马术|钓鱼|垂钓") & pois['type'].str.startswith("体育休闲服务")) | (pois['type'].str.startswith("体育休闲服务") & pois['name_1'].str.contains("乒乓球|篮球|健身|台球|游泳|溜冰|综合体育|羽毛|足球|跆拳道|高尔夫|运动场所|马术|钓鱼|垂钓|活动广场|活动|文体|运动|步道"))]""",
    '便民服务设施': """pois[(pois['type'].str.contains('超级市场')) | (pois['type'].str.contains('超市')) | ((pois['name_1'].str.contains('超市')) & (pois['common_type'].str.contains('便利店') == False) & (pois['type'].str.contains('购物相关场所')) & (pois['name_1'].str.contains('空压机') == False)) | ((pois['type'].str.contains('便利店') & ~pois['type'].str.contains('超市')) | pois['common_type'].str.contains('便利店')) | (pois['type'].str.contains('物流速递') & pois['name_1'].str.match('.*驿站.*|.*蜂巢.*|.*丰巢.*|.*收寄.*|.*快递超市.*|.*柜.*|.*代.*')) | (pois['type'].str.contains('综合市场;蔬菜市场') | (pois['type'].str.contains('综合市场;综合市场') & pois['name_1'].str.match('.*贸.*|.*市场.*')) | (pois['type'].str.contains('水产海鲜市场') & ~pois['type'].str.contains('餐饮') & ~pois['type'].str.contains('企业') & ~pois['type'].str.contains('生活服务场所') & ~pois['type'].str.contains('基地')) | (pois['type'].str.contains('农副产品市场') & ~pois['type'].str.contains('公司') & ~pois['type'].str.contains('餐饮') & ~pois['type'].str.contains('便利店'))) | (pois['type'].str.contains("社区") | pois['name_1'].str.contains("社区活动") | pois['name_1'].str.contains("社区服务") | pois['name_1'].str.match(".*社区.*中心.*")) | ((pois['name_1'].str.contains("消防") & ~pois['type'].str.match(".*店|.*公司.*|.*企业.*|.*工厂.*|.*市场.*|.*购物.*")) | pois['type'].str.contains("消防")) | (pois['name_1'].str.contains("图书") | pois['type'].str.contains("图书")) | (pois['type'].str.contains("社区") | pois['name_1'].str.contains("社区活动") | pois['name_1'].str.contains("社区服务") | pois['name_1'].str.match(".*社区.*中心.*")) | (pois['type'].str.contains("厕") | pois['type'].str.contains("洗手") | pois['name_1'].str.match(".*厕.*|.*洗手.*"))]""",
    '充电站': """pois[(pois['name_1'].str.contains('充电站')) | (pois['type'].str.contains('充电站')) | (pois['common_type'].str.contains('充电站'))]""",
    '加油站': """pois[(pois['name_1'].str.contains('加油')) | (pois['type'].str.contains('加油')) | (pois['common_type'].str.contains('加油'))]""",
    '公交站': """pois[(pois['name_1'].str.contains('公交')) | (pois['type'].str.contains('公交')) | (pois['common_type'].str.contains('公交'))]""",
    '轨道站点': """pois[(pois['type'].str.contains('地铁站;地铁站'))]""",
    '绿地': 'aois',
    '屋顶面积': """aois""",
    '住宅': """aois[aois['common_type'].str.contains('住宅')]""",
    '商业建筑': """aois[aois['common_type'].str.contains('商场')]""",
    '工业建筑': """aois[aois['common_type'].str.contains('工业')]""",
    '酒店': """aois[aois['common_type'].str.contains('酒店')]""",
    '写字楼': """aois[aois['common_type'].str.contains('办公')]""",
    '学校': """aois[aois['common_type'].str.contains('学校')]""",
    '医院': """aois[aois['common_type'].str.contains('医院')]""",
    '建筑': """aois""",
    '企业': """pois[(pois['type'].str.contains('企业'))]"""
}


POI_BUFFER_MAP = {
    '超市': 300,
    '便利店': 300,
    '菜市场': 300,
    '快递站点': 300,
    '社区服务点': 300,
    '体育设施': 300,
    '便民服务设施': 300,
    '充电站': 1000,
    '加油站': 1000,
    '公交站': 300,
    '轨道站点': 500,
    '企业': 0.0001

}

AOI_BUFFER_MAP = {
    '绿地': 500
}


def block_area(path_block: str) -> gpd.GeoDataFrame:
    """Calculate the area of blocks

    Args:
        path_block (str): 路径

    Returns:
        gpd.GeoDataFrame: blocks with 'block_area'
    """
    raw_blocks = gpd.read_file(path_block)[['id', 'object_id', 'geometry']]
    to_mercator(raw_blocks)
    raw_blocks['block_area'] = raw_blocks.area
    return raw_blocks


def poi_coverage(pois: gpd.GeoDataFrame, block: gpd.GeoDataFrame, poi_type: str, threshold: int = 300) -> gpd.GeoDataFrame:
    """POI覆盖率计算,根据传入的poi与threshold距离进行buffer

    Args:
        pois (gpd.GeoDataFrame): 传入geodataframe
        block (gpd.GeoDataFrame): 传入geodataframe
        poi_type (str): poi类别,具体类型对应POI_BUFFER_MAP与FILTER_MAP
        threshold (int, optional): buffer距离 Defaults to 300.

    Raises:
        Exception: POI类别错误

    Returns:
        gpd.GeoDataFrame: blocks新增一列poi_type_coverage
    """
    try:
        target_poi = eval(FILTER_MAP[poi_type])
    except KeyError:
        raise Exception(' INVALID POI TYPE ')
    buffer = gpd.GeoDataFrame(target_poi.buffer(
        threshold), columns=['geometry']).dissolve()
    overlap = gpd.overlay(block, buffer, how='intersection')
    overlap[poi_type+'覆盖率'] = round(overlap.area /
                                    overlap['block_area'], 4)*100
    result = pd.merge(block, overlap.drop(['block_area', 'geometry'], axis=1), on=[
                      'id', 'object_id'], how='outer')
    result[poi_type+'覆盖率'] = result[poi_type+'覆盖率'].fillna(0)
    return result


def aoi_coverage(aois: gpd.GeoDataFrame, block: gpd.GeoDataFrame, aoi_type: str, threshold: int = 500) -> gpd.GeoDataFrame:
    """AOI覆盖率计算，根据传入的AOI与threshold距离进行buffer

    Args:
        aois (gpd.GeoDataFrame): 传入geodataframe
        block (gpd.GeoDataFrame): 传入geodataframe
        aoi_type (str): AOI类别,具体类型对应AOI_BUFFER_MAP与FILTER_MAP
        threshold (int, optional): _description_. Defaults to 500.

    Raises:
        Exception: AOI类别错误

    Returns:
        gpd.GeoDataFrame: blocks新增一列aoi_type_coverage
    """
    try:
        target_aoi = eval(FILTER_MAP[aoi_type])
    except KeyError:
        raise Exception(' INVALID AOI TYPE ')
    buffer = gpd.GeoDataFrame(target_aoi.buffer(
        threshold), columns=['geometry']).dissolve()
    overlap = gpd.overlay(block, buffer, how='intersection')
    overlap[aoi_type+'覆盖率'] = round(overlap.area /
                                    overlap['block_area'], 4)*100
    result = pd.merge(block, overlap.drop(['block_area', 'geometry'], axis=1), on=[
                      'id', 'object_id'], how='outer')
    result[aoi_type+'覆盖率'] = result[aoi_type+'覆盖率'].fillna(0)
    return result


def count_poi_with_buffer(pois: gpd.GeoDataFrame, block: gpd.GeoDataFrame, poi_type: str, threshold: int = 300) -> gpd.GeoDataFrame:
    """计算block内的poi数量(buffer版poi)

    Args:
        pois (gpd.GeoDataFrame): _description_
        block (gpd.GeoDataFrame): _description_
        poi_type (str): _description_
        threshold (int, optional): _description_. Defaults to 300.

    Raises:
        Exception: _description_

    Returns:
        gpd.GeoDataFrame: blocks新增一列
    """
    try:
        target_poi = eval(FILTER_MAP[poi_type])
    except KeyError:
        raise Exception(' INVALID POI TYPE ')
    buffer = gpd.GeoDataFrame(target_poi.buffer(
        threshold), columns=['geometry'])
    counter = gpd.overlay(block, buffer, how='intersection').groupby(['id']).count()[
        ['object_id']].rename(columns={'object_id': f'{poi_type}个数'})
    result = pd.merge(block, counter, left_on='id',
                      right_index=True, how='outer')
    result[poi_type+'个数'] = result[poi_type+'个数'].fillna(0).astype('int')
    return result


def aoi_roof_area(aois: gpd.GeoDataFrame, block: gpd.GeoDataFrame, aoi_type: str) -> gpd.GeoDataFrame:
    """屋顶(基底)面积计算

    Args:
        aois (gpd.GeoDataFrame): 建筑gdf
        block (gpd.GeoDataFrame): _description_
        aoi_type (str): 建筑_type，参照FILTERMAP内的类型

    Raises:
        Exception: _description_

    Returns:
        gpd.GeoDataFrame: blocks新增一列
    """
    try:
        target_aoi = eval(FILTER_MAP[aoi_type])
    except KeyError:
        raise Exception(' INVALID AOI TYPE ')
    if not '屋顶面积' in aoi_type:
        aoi_type += '屋顶面积'
    if '绿地' in aoi_type:
        aoi_type = '绿地面积'
    overlap = gpd.overlay(block, target_aoi[['geometry']])[['id', 'geometry']]
    overlap[aoi_type] = overlap.area
    overlap = overlap.groupby(['id']).sum()[[aoi_type]]
    res = pd.merge(block, overlap, how='outer', left_on='id', right_index=True)
    res[aoi_type] = res[aoi_type].fillna(0).astype(float).round(2)
    return res


def aoi_floor_area(aois: gpd.GeoDataFrame, block: gpd.GeoDataFrame, aoi_type: str) -> gpd.GeoDataFrame:
    """建筑面积计算

    Args:
        aois (gpd.GeoDataFrame): 建筑gdf
        block (gpd.GeoDataFrame): _description_
        aoi_type (str): 建筑_type，参照FILTERMAP内的类型

    Raises:
        Exception: _description_

    Returns:
        gpd.GeoDataFrame: blocks新增一列
    """
    try:
        target_aoi = eval(FILTER_MAP[aoi_type])
    except KeyError:
        raise Exception(' INVALID AOI TYPE ')
    target_aoi['floor'] = (target_aoi['height'] // 3).astype(int)
    overlap = gpd.overlay(block, target_aoi[['floor', 'geometry']])
    overlap['面积'] = overlap.area
    overlap[aoi_type+'面积'] = overlap['floor'] * overlap['面积']
    overlap = overlap.groupby('id').sum()[[aoi_type+'面积']]
    res = pd.merge(block, overlap, how='outer', left_on='id', right_index=True)
    res[aoi_type + '面积'] = res[aoi_type +
                               '面积'].fillna(0).astype(float).round(2)
    return res


def road_dens(raw_road: gpd.GeoDataFrame, block: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """路网密度计算

    Args:
        raw_road (gpd.GeoDataFrame): 路网gdf
        block (gpd.GeoDataFrame): _description_

    Returns:
        gpd.GeoDataFrame: 新增一列
    """

    overlap = gpd.overlay(raw_road, block)[['id', 'geometry']]
    overlap['road_len'] = overlap.length
    len = overlap.groupby(['id']).sum()['road_len']
    res = pd.merge(block, len, how='outer', left_on='id', right_index=True)
    res['路网长度'] = res['road_len'].fillna(0).astype('float').round(2)
    res['路网密度'] = (res['路网长度'] / 1000) / (res['block_area']/1000000)
    return res
