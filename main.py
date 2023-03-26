from startup.process import *

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
