# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
from utils.to_mercator import to_mercator
from config.static_vars import *


def aoi_area_cal(aois: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """Calculate the area of blocks

    Args:
        path_block (str): 路径

    Returns:
        gpd.GeoDataFrame: blocks with 'block_area'
    """
    ori_crs = aois.crs
    to_mercator(aois)
    aois['aoi_area'] = aois.area
    aois = aois.to_crs(ori_crs)
    return aois

# create buffer with geopandas


def aoi_coverage_cal(aois: gpd.GeoDataFrame, block: gpd.GeoDataFrame, aoi_type: str, threshold: int = 500) -> gpd.GeoDataFrame:
    """AOI覆盖率计算,根据传入的AOI与threshold距离进行buffer

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
    ori_crs = block.crs
    cols = block.columns.to_list()
    to_mercator(aois)
    to_mercator(block)
    block['join_id'] = block.index
    block['block_area'] = block.area
    buffer = gpd.GeoDataFrame(aois.buffer(
        threshold), columns=['geometry']).dissolve()
    overlap = gpd.overlay(block, buffer, how='intersection')[
        ['join_id', 'geometry', 'block_area']]
    overlap[aoi_type+'_coverage_rate'] = round(overlap.area /
                                               overlap['block_area'], 4)*100
    result = pd.merge(block, overlap.drop(['block_area', 'geometry'], axis=1), on=[
                      'join_id'], how='outer')
    result[aoi_type+'_coverage_rate'] = result[aoi_type +
                                               '_coverage_rate'].fillna(0)
    result = result.to_crs(ori_crs)[cols+[f'{aoi_type}_coverage_rate']]
    return result


def building_roof_area_cal(bd: gpd.GeoDataFrame, block: gpd.GeoDataFrame, bd_type: str = 'building') -> gpd.GeoDataFrame:
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
    ori_crs = block.crs
    to_mercator(bd)
    to_mercator(block)
    cols = block.columns.to_list()
    block['join_id'] = block.index

    overlap = gpd.overlay(block, bd[['geometry']])[['join_id', 'geometry']]
    overlap[f'{bd_type}_roof_area'] = overlap.area
    overlap = overlap.groupby(['join_id']).sum()[[f'{bd_type}_roof_area']]
    res = pd.merge(block, overlap, how='outer',
                   left_on='join_id', right_index=True)
    res[f'{bd_type}_roof_area'] = res[f'{bd_type}_roof_area'].fillna(
        0).astype(float).round(2)
    res = res.to_crs(ori_crs)[cols+[f'{bd_type}_roof_area']]
    return res


def building_floor_area_cal(bd: gpd.GeoDataFrame, block: gpd.GeoDataFrame, bd_type: str = 'building', height_field='height', height_per_floor=3) -> gpd.GeoDataFrame:
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
    ori_crs = block.crs
    to_mercator(bd)
    to_mercator(block)
    cols = block.columns.to_list()
    block['join_id'] = block.index

    bd['floor'] = (bd[height_field] // height_per_floor).astype(int)
    overlap = gpd.overlay(block, bd[['floor', 'geometry']])
    overlap['roof_area'] = overlap.area
    overlap[bd_type+'_floor_area'] = overlap['floor'] * overlap['roof_area']
    overlap = overlap.groupby('join_id').sum()[[bd_type+'_floor_area']]
    res = pd.merge(block, overlap, how='outer',
                   left_on='join_id', right_index=True)
    res[bd_type+'_floor_area'] = res[bd_type +
                                     '_floor_area'].fillna(0).astype(float).round(2)
    res = res.to_crs(ori_crs)[cols + bd_type +
                              '_floor_area']
    return res
