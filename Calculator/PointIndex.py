# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
from utils.to_mercator import to_mercator
from config.static_vars import *


def poi_coverage_cal(pois: gpd.GeoDataFrame, block: gpd.GeoDataFrame, poi_type: str = '', buffer_distance: int = 300) -> gpd.GeoDataFrame:
    """
    POI覆盖率计算,根据传入的poi与buffer_distance距离进行buffer,分别计算buffer在每个地块中的覆盖率

    坐标系问题：
    1.代码会先将原始坐标转墨卡托(墨卡托投影坐标系)
    2.输出时再从墨卡托投影坐标系转回原坐标系

    必须搞清楚自己输入的是什么坐标，防止检查验证时摸不着头脑😈

    Args:
        pois (gpd.GeoDataFrame): Points of interest data.
        block (gpd.GeoDataFrame): Block data.
        poi_type (str, optional): Type of POI. Defaults to ''.
        buffer_distance (int, optional): Buffer distance around POI in meters. Defaults to 300.


    Returns:
        gpd.GeoDataFrame: blocks新增一列poi_type_coverage
    """
    # restore origin crs for final result
    block_ori_crs = block.crs
    block_cols = block.columns.to_list()

    # convert to projection coords
    to_mercator(pois)
    to_mercator(block)

    # add necessary fields
    block['join_id'] = block.index
    block['block_area'] = block.area

    others_col = [x for x in block.columns.to_list() if x not in [
        'join_id', 'block_area', 'geometry']]

    #   create buffer
    buffer = gpd.GeoDataFrame(pois.buffer(
        buffer_distance), columns=['geometry']).dissolve()

    # create intersection area and calculate its ratio with origin block
    overlap = gpd.overlay(block, buffer, how='intersection')
    overlap[f'{poi_type}_area'] = overlap['geometry'].area
    overlap[f'{poi_type}_coverage_rate'] = round(overlap[f'{poi_type}_area'] /
                                                 overlap['block_area'], 4)*100
    # merge based on 'join_id'
    result = pd.merge(block, overlap.drop(others_col+['geometry', 'block_area'], axis=1), on=[
                      'join_id'], how='outer')

    # data clean
    result[f'{poi_type}_coverage_rate'] = result[f'{poi_type}_coverage_rate'].fillna(
        0)
    result[f'{poi_type}_area'] = result[f'{poi_type}_area'].fillna(0)

    # edit here if you want to output anything.
    columns = block_cols + [f'{poi_type}_coverage_rate']
    result = result[columns]
    # Convert back to the original CRS
    result = result.to_crs(block_ori_crs)

    return result


def count_poi_with_buffer(pois: gpd.GeoDataFrame, block: gpd.GeoDataFrame,  threshold: int = 300, poi_type: str = 'new_type') -> gpd.GeoDataFrame:
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
    ori_crs = block.crs
    block_cols = block.columns.to_list()
    to_mercator(pois)
    to_mercator(block)
    block['uuuid'] = block.index

    buffer = gpd.GeoDataFrame(pois.buffer(
        threshold), columns=['geometry'])
    # counter = gpd.overlay(block, buffer, how='intersection').groupby(['uuuid']).count()[
    #     ['object_id']].rename(columns={'object_id': f'{poi_type}个数'})
    counter = gpd.overlay(block, buffer, how='intersection').groupby(['uuuid']).count()[
        [block.columns[0]]].rename(columns={block.columns[0]: f'{poi_type}_count'})
    result = pd.merge(block, counter, left_on='uuuid',
                      right_index=True, how='outer')
    columns = block_cols + [f'{poi_type}_count']
    result = result[columns]
    result[f'{poi_type}_count'] = result[f'{poi_type}_count'].fillna(
        0).astype('int')
    result = result.to_crs(ori_crs)
    return result
