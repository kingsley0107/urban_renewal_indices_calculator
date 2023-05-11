中文版    [ENGLISH](./README.md)

# 城市更新指标计算器(v0.1.0) 

## 主要功能

- 以地块为单位的各类城市更新指标计算(覆盖率、密度、容积等)
- 高德POI部分类型正则筛选参考 (eg. 菜市场, 超市, 快递站点...)

## 数据样例

- ![城市地块](./img/blocks.jpg )
- ![建筑](./img/bd.jpg)
- ![POI](./img/poi.jpg)
- ![计算结果](./img/attributes.jpg)


## 模块介绍
## 1. Calculator.PointIndex
 -  以地块为单位的POI 覆盖率(1.菜市场Poi buffer300m，计算地块菜市场覆盖率)
    -   算法原理图示：
        -   ![data](./img/PoiIndex/cov/ori.jpg)
            <p align="center">
                <i>原始POI及地块数据.</i>
            </p>
        -   ![step1](./img/PoiIndex/cov/step1.jpg) 
            <p align="center">
                <i>根据POI生成缓冲区(重叠部分合并).</i>
            </p>
        -   ![step2](./img/PoiIndex/cov/step2.jpg) 
            <p align="center">
                <i>提取缓冲区与地块相交部分.</i>
            </p>            
        -   ![step3](./img/PoiIndex/cov/output.jpg) 
            <p align="center">
                <i>分别对地块进行缓冲区面积/地块总面积，计算得到结果.</i>
            </p>    
 -  地块内POI(buffer)数量 (如菜市场buffer 300m后，对所有地块计算含有菜市场缓冲区的数量
 (当不需要缓冲区时设置buffer为0.0001即可))
    -   算法原理图示：
            -   ![data2](./img/PoiIndex/cov/ori.jpg)
            <p align="center">
                <i>原始POI及地块数据.</i>
            </p>   
            -   ![step1](./img/PoiIndex/count/step1.jpg) 
            <p align="center">
                <i>根据POI生成缓冲区(重叠部分不再合并).</i>
            </p>
            -   ![step2](./img/PoiIndex/count/step2.jpg) 
            <p align="center">
                <i>提取缓冲区与地块相交部分(当一个地块被多个缓冲区覆盖时会出现有大量缓冲区重叠的区域).
                </i>
            </p>
            -   ![step3](./img/PoiIndex/count/output.jpg) 
            <p align="center">
                <i>提计算与地块相交的缓冲区数量，得到输出结果.</i>
            </p>
                <center></center>
## 2. Calculator.LineIndex
 -  以地块为单位的路网密度计算
    -   算法原理图示：
        -   ![data](./img/LineIndex/ori.jpg)
            <p align="center">
                <i>原始路网及地块数据.</i>
            </p>
        -   ![step1](./img/LineIndex/step1.jpg) 
            <p align="center">
                <i>提取与地块重叠的路网部分.</i>
            </p>
        -   ![step2](./img/LineIndex/output.jpg) 
            <p align="center">
                <i>计算(路网长度总和(km)/地块面积(km²)).</i>
            </p>

## 3. Calculator.AoiIndex
 -  以地块为单位的面数据指标计算
 -  覆盖率类参考POI
 -  building_floor_area地块建筑面积计算：
    -   算法原理图示：
        -   ![data](./img/AoiIndex/ori1.jpg)
            <p align="center">
                <i>原始建筑数据及地块数据.</i>
            </p>
        -   ![req](./img/AoiIndex/requirement.png)
            <p align="center">
                <i>建筑数据要求有一个代表高度的字段.</i>
            </p>
        -   ![step1](./img/AoiIndex/step1.jpg) 
            <p align="center">
                <i>提取与地块重叠的建筑部分(红色部分).</i>
            </p>
        -   ![step2](./img/AoiIndex/output.jpg) 
            <p align="center">
                <i>通过高度推算层数，再使用建筑占地面积*层数得到建筑面积.</i>
            </p>

## 使用说明书
### 1. 环境配置
-   python 3.x
-   geopandas

### 2. 数据准备
-   准备好数据文件，并且清楚数据坐标系

### 3. 配置config/static_vars.py
-   配置需要使用的数据路径，不需要引入的数据可以注释或不管

### 4. 修改完路径文件后在main.py运行对应函数
- POI覆盖率:执行poi_coverage()函数并输入对应参数
- POI数量:执行poi_count()函数并输入对应参数
- 路网密度:执行road_density()函数并输入对应参数
- AOI面积:执行aoi_area()函数并输入对应参数
- AOI覆盖率:执行aoi_coverage()函数并输入对应参数
- 建筑占地(屋顶)面积：执行building_roof_area()函数并输入对应参数
- AOI建筑面积：执行building_floor_area()函数并输入对应参数








## Concat:
Feel free to email me: kingsleyl0107@gmail.com



