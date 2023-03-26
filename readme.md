中文版         

# 城市更新指标计算器(03.25更新 施工状态)

### 主要功能

- 地块指标计算 （离散地块 eg.城市内部地块等AOI数据）
- 高德POI类型筛选 (eg. 菜市场, 超市, 快递站点...)

### 模块介绍
#### 1. Calculator.PointIndex
 -  地块内POI Buffer覆盖率(如菜市场Poi buffer300m后，对所有地块进行菜市场覆盖率计算)
 -  地块内POI(buffer)数量 (如菜市场buffer 300m后，对所有地块计算含有菜市场缓冲区的数量
 (当不需要缓冲区时设置buffer为0.0001即可))

 #### 2. Calculator.AoiIndex
 - AOI 占地面积 (如地块面积)
 - 地块内AOI Buffer覆盖率

### 数据样例

- ![城市地块](./img/blocks.jpg )
- ![计算结果](./img/attributes.jpg)
- ![建筑](./img/bd.jpg)
- ![POI](./img/poi.jpg)

### 涵盖指标 (持续施工中)

| 指标名称 | 计算方法 | 数据来源 |
| :-----| ----: | :----: |
| 生活服务设施覆盖率 | buffer 300m | 高德POI |
| 超市覆盖率 | buffer 300m | 高德POI |
| 便利店覆盖率 | buffer 300m | 高德POI |
| 菜市场覆盖率 | buffer 300m | 高德POI |
| 快递站点覆盖率 | buffer 300m | 高德POI |
| 社区服务点覆盖率 | buffer 300m | 高德POI |
| 便民服务设施覆盖率 | buffer 300m | 高德POI |
| 体育设施覆盖率 | buffer 300m | 高德POI |
| 充电站覆盖率 | buffer 1000m | 百度充电桩查询 |
| 充电桩数量 | buffer 1000m后count | 百度充电桩查询 |
| 加油站覆盖率 | buffer 1000m | 百度加油站查询 |
| 公园绿地覆盖率 | 点位buffer300m，面积buffer500m | 高德poi，百度aoi |
| 轨道站点覆盖率 | buffer 500m | 高德POI |
| 公交站点覆盖率 | buffer 300m | 高德POI |
| 绿地面积 | 地块内，绿地面积占比 | 高德poi，百度aoi |
| 居住小区数量 | buffer 300m后count | 链家小区 |
| 企业数量 | 地块内企业数量 | 爱企查 |
| 屋顶面积 | 地块内屋顶面积 |  |
| 住宅屋顶面积 |  |  |r
| 容积率 |  |  |
| 路网密度 | 地块内道路总长度/地块面积 | osm+qq |
