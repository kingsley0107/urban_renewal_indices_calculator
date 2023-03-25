# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
from utils.to_mercator import to_mercator
from config.static_vars import *


def aoi_area(path_block: str) -> gpd.GeoDataFrame:
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
