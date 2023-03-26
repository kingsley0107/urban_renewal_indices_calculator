

################################################配置区域开始################################################
# 不需要的部分可以注释掉
# 1.poi路径
poi_path = (r'./数据/points/supermarket_ori.geojson')
# 2.poi buffer距离
poi_buffer_dis = 300
# 3.poi 类型
poi_type = 'supermarket'
# 4.建筑数据路径
bd_path = (r'./数据/industrial_building.geojson')
# 5.建筑类型
bd_type = 'industrial'
# 6.建筑面积指定高度字段，多少米算一层
height_field = 'height'
height_per_floor = 3
# 7.AOI路径
aoi_path = r'./数据/公园绿地aoi.geojson'
# 8.AOI buffer距离
aoi_buffer_dis = 500
# 9. 路网路径
road_path = r'./数据/路网数据/ctl_1984.shp'
# 10.地块路径
block_path = r'./数据/aois/raw_blocks.geojson'
# 11.输出路径
output_path = r'./output.geojson'
################################################配置区域结束################################################
