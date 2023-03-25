AMAP_FILTER_MAP = {
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
