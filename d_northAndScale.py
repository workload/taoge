# from mpl_toolkits.basemap import Basemap
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches


def add_north(ax, labelsize=16, loc_x=0.88, loc_y=0.85, width=0.05, height=0.13, pad=0.14,lw=1):
    """
    画一个比例尺带'N'文字注释
    主要参数如下
    :param ax: 要画的坐标区域 Axes实例 plt.gca()获取即可
    :param labelsize: 显示'N'文字的大小
    :param loc_x: 以文字下部为中心的占整个ax横向比例
    :param loc_y: 以文字下部为中心的占整个ax纵向比例
    :param width: 指南针占ax比例宽度
    :param height: 指南针占ax比例高度
    :param pad: 文字符号占ax比例间隙
    :return: None
    """
    minx, maxx = ax.get_xlim()
    miny, maxy = ax.get_ylim()
    ylen = maxy - miny
    xlen = maxx - minx
    left = [minx + xlen*(loc_x - width*.5), miny + ylen*(loc_y - pad)]
    right = [minx + xlen*(loc_x + width*.5), miny + ylen*(loc_y - pad)]
    top = [minx + xlen*loc_x, miny + ylen*(loc_y - pad + height)]
    center = [minx + xlen*loc_x, left[1] + (top[1] - left[1])*.4]
    triangle = mpatches.Polygon([left, top, center], ec='k',color='k',lw=lw)
    triangle2 = mpatches.Polygon([top, center,right], ec='k',color='none',lw=lw)
    ax.text(s='N',
            x=minx + xlen*loc_x,
            y=miny + ylen*(loc_y - pad + height),
            fontsize=labelsize,
            fontfamily='Times New Roman',
            horizontalalignment='center',
            verticalalignment='bottom')
    ax.add_patch(triangle)
    ax.add_patch(triangle2)

#########################################################################
# 绘制比例尺
def add_scalebar(ax,x, y, length,lw=1,fontsize=12,divd=12):
    """
    画一个比例尺带'N'文字注释
    主要参数如下
    :param ax: 要画的坐标区域 Axes实例 plt.gca()获取即可
    :param x: 起点x坐标
    :param y: 起点y坐标
    :param length: 一个刻度长度（米）
    :param lw: 线宽
    :param fs: 文字大小
    :return
    """
    ax.hlines(y=y, xmin=x, xmax=x+2*length, colors="black", ls="-", lw=lw, label='%d km' % (length))
    ax.vlines(x=x, ymin=y - length/20, ymax=y + length/20, colors="black", ls="-", lw=lw)
    ax.vlines(x=x+length,  ymin=y - length/20, ymax=y + length/20, colors="black", ls="-", lw=lw)
    ax.vlines(x=x+2*length, ymin=y - length/20, ymax=y + length/20, colors="black", ls="-", lw=lw)
    ax.text(x, y + length/divd, '0', ha='center',
            fontfamily='Times New Roman',fontsize=fontsize)
    ax.text(x+length, y + length/divd, '{:.0f}'.format(length/1000), ha='center',
            fontfamily='Times New Roman',fontsize=fontsize)
    ax.text(x+2*length, y + length/divd, '{:.0f} km'.format(2*length/1000), ha='center',
            fontfamily='Times New Roman',fontsize=fontsize)


if __name__ == "__main__":
    ## 调用
    #-----------添加指北针------------
    ax = plt.gca()
    add_scalebar(ax,91,-12.5,30)
    add_north(ax)
    plt.show()
