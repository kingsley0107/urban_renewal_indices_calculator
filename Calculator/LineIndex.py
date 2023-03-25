# -*- coding: utf-8 -*-
import geopandas as gpd
import pandas as pd
from utils.to_mercator import to_mercator
from config.static_vars import *


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
