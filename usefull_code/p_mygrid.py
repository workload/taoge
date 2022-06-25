from shapely.geometry import Polygon, Point, MultiPoint  # 从哪些库中导入一些类
import geopandas as gpd  # 导入库，简称为包
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from geovoronoi import voronoi_regions_from_coords

def get_hex(shp, length, epsg_code):
    sh01 = gpd.read_file(shp)  # 读取上海市域界限
    sh01_m = sh01.to_crs(f'epsg:{epsg_code}')

    bds = [min(sh01_m.bounds.iloc[:,0]),min(sh01_m.bounds.iloc[:,1]),
       max(sh01_m.bounds.iloc[:,2]),max(sh01_m.bounds.iloc[:,3])]
       
    range_x = int((bds[2] - bds[0]) / length / 3) + 3
    range_y = int((bds[3] - bds[1]) / length / np.sqrt(3)) + 3

    ## 奇数列
    lst1y = []
    for i in range(-2, int(range_y)):
        delta = (2 * np.sqrt(length ** 2 - (length / 2) ** 2)) * i
        lst1y.append(delta + bds[1])
    lst1x = []
    for i in range(-2, int(range_x)):
        delta = (3 * length) * i
        lst1x.append(delta + bds[0])
    p1 = [[i1, i2] for i1 in lst1x for i2 in lst1y]

    lst2y = []
    for i in range(-2, int(range_y)):
        delta = (2 * np.sqrt(length ** 2 - (length / 2) ** 2)) * i + \
                np.sqrt(length ** 2 - (length / 2) ** 2)
        lst2y.append(delta + bds[1])
    lst2x = []
    for i in range(-2, int(range_x)):
        delta = 3 * length * i + 1.5 * length
        lst2x.append(delta + bds[0])
    p2 = [[i1, i2] for i1 in lst2x for i2 in lst2y]

    bds_area = MultiPoint([Point(i[0], i[1]) for i in p1] + [Point(i[0], i[1]) for i in p2]).bounds

    region_polys, region_pts = voronoi_regions_from_coords(np.array(p1 + p2),
                                                           Polygon(((bds_area[0], bds_area[1]),
                                                                    (bds_area[0], bds_area[3]),
                                                                    (bds_area[2], bds_area[3]),
                                                                    (bds_area[2], bds_area[1])
                                                                    )))

    pgs = gpd.GeoDataFrame({'hex_id': region_polys.keys(),
                            'geometry': region_polys.values()}, crs=f'epsg:{epsg_code}')

    dz = gpd.sjoin(pgs, sh01_m, predicate='intersects')
    dz = dz[['hex_id', 'geometry']]
    dz = dz.to_crs(epsg=4326)
    return dz

def get_fishnet(shp,divd,epsg_code):
    sh01 = gpd.read_file(shp,encoding = 'utf-8')
    sh01_m = sh01.to_crs(f'epsg:{epsg_code}')

    # 创建一个区域，后面再来切网格
    bds = [min(sh01_m.bounds.iloc[:,0]),min(sh01_m.bounds.iloc[:,1]),
    max(sh01_m.bounds.iloc[:,2]),max(sh01_m.bounds.iloc[:,3])]
    
    coord1 = bds[:2]
    coord3 = bds[2:]
    coord2 = (coord3[0],coord1[1])
    coord4 = (coord1[0],coord3[1])

    rectangle = Polygon([coord1,coord2,coord3,coord4])
    rectangle = gpd.GeoDataFrame([rectangle],columns=['geometry'])

    # 3创建渔网，网格划分
    def lng_lat(loc_all, divd):
    # 去提取经度纬度数值
        lngH = bds[2]
        lngL = bds[0]
        latH = bds[3]
        latL = bds[1]

        lng_lst = []
        lng_num = int((lngH - lngL)/divd) + 1
        for i in range(lng_num):
            lng = lngL + i*divd
            lng_lst.append(lng)

        lat_lst = []
        lat_num = int((latH - latL)/divd) + 1
        for i in range(lat_num):
            lat = latL + i*divd
            lat_lst.append(lat) 

        lat = lat_lst
        lng = sorted(lng_lst)

        lst = []
        for a in lat:
            for n in lng:
                lst.append('{},{}'.format(n, a))

        # 创建一个嵌套列表，便于后面进行坐标串组合
        lst1 = []
        for i in range(len(lat)):
            lst1.append(lst[i * len(lng):(i + 1) * len(lng)])

        # 坐标串组合
        lsta = []
        for a in range(0, len(lat) - 1):
            for n in range(0, len(lng) - 1):
                coords = (float(lst1[a][n].split(',')[0]),float(lst1[a][n].split(',')[1])),\
                         (float(lst1[a+1][n+1].split(',')[0]),float(lst1[a+1][n+1].split(',')[1]))
                lsta.append(coords)
        return lsta

    coords = rectangle['geometry'].bounds.values[0]
    loc_all = '{},{},{},{}'.format(coords[0],coords[3],coords[2],coords[1])

    nets = lng_lat(loc_all, divd)

    def getPolygon(coord1,coord3):
        coord1 = coord1
        coord3 = coord3
        coord2 = (coord3[0],coord1[1])
        coord4 = (coord1[0],coord3[1])

        rectangle = Polygon([coord1,coord2,coord3,coord4])

        return rectangle

    netfish = gpd.GeoDataFrame([getPolygon(i[0],i[1]) for i in nets],columns=['geometry'])
    # 4提取上海区域的网格

    ##### 网格需要先设置坐标系
    netfish = netfish.set_crs(epsg=epsg_code) # 设定初始的坐标系 WGS84
    netfish_wgs84 = netfish.to_crs(epsg=4326)
    dz = gpd.sjoin(netfish_wgs84,sh01,predicate='intersects')
    dz = dz[['geometry']]
    dz['net_id'] = np.array([i for i in range(len(dz))],dtype='int64')
    return dz

if __name__ == "__main__":
    shp = r'./basicSHP/sh01.shp' # 相对路径和绝对路径
    length = 1000
    epsg_code = 32651
    dz = get_hex(shp,length,epsg_code)