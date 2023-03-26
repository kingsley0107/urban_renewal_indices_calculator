# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
from utils.to_mercator import to_mercator
from config.static_vars import *


def road_dens_cal(raw_road: gpd.GeoDataFrame, block: gpd.GeoDataFrame) -> gpd.GeoDataFrame:
    """路网密度计算

    Args:
        raw_road (gpd.GeoDataFrame): 路网gdf
        block (gpd.GeoDataFrame): _description_

    Returns:
        gpd.GeoDataFrame: 新增一列
    """
    ori_crs = block.crs
    cols = block.columns.to_list()
    to_mercator(raw_road)
    to_mercator(block)
    block['block_area'] = block.area
    block['join_id'] = block.index

    overlap = gpd.overlay(raw_road, block)[['join_id', 'geometry']]
    overlap['road_len'] = overlap.length
    len = overlap.groupby(['join_id']).sum()[['road_len']]
    res = pd.merge(block, len, how='outer',
                   left_on='join_id', right_index=True)
    res['road_len_sum'] = res['road_len'].fillna(
        0).astype('float').round(2)
    res['road_density'] = (res['road_len_sum'] / 1000) / \
        (res['block_area']/1000000)
    res = res.to_crs(ori_crs)[cols+['road_density']]
    return res
