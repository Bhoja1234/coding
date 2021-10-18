# -*- coding: utf-8 -*-
"""
Created on Wed Sep 29 15:31:26 2021
@author: 伯雅
"""
import numpy as np
import json
import matplotlib.pyplot as plt

with open('./annotations.json','r',
          encoding = 'utf-8') as fp:
    a = json.load(fp)

# 画1号掩膜
Id = str('Q_%04d_L_10092020.jpg' %2)
x = a[Id]['all_points_x']
y = a[Id]['all_points_y']

# plt.plot(x, y, marker='o', markersize=3)
# plt.xlim(0,300)
# plt.ylim(0,300)
plt.plot(x,y, linewidth=3)
img = plt.imread('./images/%s' %Id)
plt.imshow(img)



def horizontal_lines_intersect(line1, line2):
    '''
    判断两水平线断经过竖直移动后，是否会相交，
    计算两条水平线段竖直距离是多少
    
    Parameters
    ----------
    line1 : [leftx, lefty, rightx, righty]
        线段1的左右端点.
    line2 : [leftx, lefty, rightx, righty]
        线段1的左右端点.

    Returns
    -------
    flag : 是否会相交
    HD : 两条水平线段的竖直距离

    '''
    HD = line1[1] - line2[1]
    # 情况1：line1完全在line2左边或者右边，
    # 即两条线段经过竖直移动后不会相交
    if(line1[2] <= line2[0]) or (line1[0] >= line2[2]):
        flag = 0
    # 其他情况经过竖直移动后均相交
    else:
        flag = 1
    
    return flag, HD

def point_horizontal_line(item, RPXY):
    '''
    根据图片右上角顶点坐标和物品宽度和高度，
    求出图片下端水平线段左右两端坐标

    Parameters
    ----------
    item : 图片[宽度，高度]
    RPXY : right point x/y
        图片右上角顶点坐标[x,y]

    Returns
    -------
    None.

    '''
    # 图片右下角顶点坐标
    RBPXY = np.array([RPXY[0], RPXY[1] - item[1]])
    # 图片左下角顶点坐标
    LBPXY = np.array([RPXY[0] - item[0], RPXY[1] - item[1]])
    return np.append(LBPXY, RBPXY)

def downHAtPoint(item, items, itemRP, RPNXY):
    '''
    图片item在箱子内任意位置可以下降的最大高度

    Parameters
    ----------
    item : 图片[宽度，高度]
    items : 各图片[宽度，高度]
    itemRP : 此图片右上角顶点坐标[x,y]
    RPNXY : 当前箱子内所有图片的右上角顶点坐标数组

    Returns
    -------
    物品item在箱子内任意位置可以下降的最大高度
    （如果能装入当前箱子，则downH为正数；否则为负数）

    '''
    bottomLine = point_horizontal_line(item, itemRP)
    RP_Num = RPNXY.shape[0]
    if RP_Num != 0:
        # 将RPNXY按照Y坐标降序排列
        sRPNXY = RPNXY[np.argsort(-RPNXY[:,2])] # 将RPNXY按照Y坐标降序排列
        sRBPNXY = sRPNXY
        # 将RPNXY按照Y坐标降序排列后的左上角顶点坐标
        sRBPNXY[:,1] = sRPNXY[:,1]- items[sRPNXY[:,0],0]
        # 物品按照Y坐标降序排列后，物品上端水平线段左右两端坐标[leftx,lefty,rightx,righty]
        topLine = np.append(sRBPNXY[:,1:3], sRPNXY[:,1:3])
        # 逐个遍历sRBPNXY中的物品
        alldownH = []; #储存所有满足相交条件的下降距离
        for i in range(len(RP_Num)):
            # 判断两条水平线段经过竖直移动后是否会相交，flag=1相交，flag=0不相交
            # 两条水平线段距离是多少，如果竖直移动后相交，HD为正数，反之为负数
            flag, HD = horizontal_lines_intersect(bottomLine, topLine[i,:])
            if flag and HD:
                alldownH.append(HD)
        # 如果不存在满足相交条件的物品，则直接下降到箱子最底端
        if alldownH is None:
            downH = itemRP[1] - item[1]
        else:
            # 如果存在满足相交条件的物品，则下降距离为alldownH中的最小值 
            downH = min(alldownH)
    else:
        # 此时箱子没有物品，物品直接下降到箱子底端
        downH = itemRP[1] - item[1]
    
    return downH

def vertical_lines_intersect(line1, line2):
    '''
    判断两竖直线断经过水平移动后，是否会相交，
    计算两条竖直线段水平距离是多少

    '''
    HD = line1[0] - line2[0]
    
    # 情况1：line1完全在line2上边或者下边，
    # 即两条线段经过竖直移动后不会相交
    if(line1[1] <= line2[3]) or (line1[3] >= line2[1]):
        flag = 0
    # 其他情况经过水平移动后均相交
    else:
        flag = 1
    
    return flag, HD

def point_vertical_line(item, RPXY):
    '''
    根据物品右上角顶点坐标和物品宽度和高度，
    求出物品左端竖直线段上下两端坐标[topx,topy,bottomx,bottomy]

    Parameters
    ----------
    item : 物品[宽度，高度]
    RPXY : 物品右上角顶点坐标[x,y]

    Returns
    -------
    None.

    '''
    LUPXY = np.append(RPXY[0] - item[0], RPXY[1])
    LBPXY = np.append(RPXY[0] - item[0], RPXY[1] - item[1])
    return np.append(LUPXY, LBPXY)

def leftWAtPoint(item,items,itemRP,RPNXY):
    '''
    计算在当前箱子中，物品item在箱子内任意位置可以向左移动的最大距离

    Parameters
    ----------
    item : 图片[宽度，高度]
    items : 各图片[宽度，高度]
    itemRP : 此图片右上角顶点坐标[x,y]
    RPNXY : 当前箱子内所有图片的右上角顶点坐标数组

    Returns
    -------
    物品item在箱子内任意位置可以向左移动的最大距离

    '''
    leftLine = point_vertical_line(item, itemRP)
    RP_Num = RPNXY.shape[0] # 箱子内物品数目
    if RP_Num != 0:
        # 将RPNXY按照X坐标降序排列
        sRPNXY = RPNXY[np.argsort(-RPNXY[:,1])] # 将RPNXY按照Y坐标降序排列
        sRBPNXY = sRPNXY
        sRBPNXY[:,2] = sRPNXY[:,2]- items[sRPNXY[:,0],1]
        rightLine = np.append(sRBPNXY[:,1:3], sRPNXY[:,1:3])
        allLeftW = []
        for i in range(len(RP_Num)):
            # 判断两条水平线段经过竖直移动后是否会相交，flag=1相交，flag=0不相交
            # 两条水平线段距离是多少，如果竖直移动后相交，HD为正数，反之为负数
            flag, HD = vertical_lines_intersect(leftLine, rightLine[i,:])
            if flag and HD:
                allLeftW.append(HD)
        if allLeftW is None:
            leftW = itemRP[1] - item[1]
        else:
            # 如果存在满足相交条件的物品，则下降距离为alldownH中的最小值 
            leftW = min(allLeftW)
    else:
        # 此时箱子没有物品，物品直接下降到箱子底端
        leftW = itemRP[1] - item[1]
    
    return leftW

def update_itemRP(itemRP,downH,leftW):
    itRPXY = np.zeros(2)
    itRPXY[1] = itemRP[1] - downH # y坐标
    itRPXY[0] = itemRP[0] - leftW # x坐标
    return itRPXY

def finalPos(item, items, itemRP, RPNXY):
    # 计算物品从当前位置向下向左移动后到最终位置后右上角顶点坐标
    while 1:
        downH = downHAtPoint(item, items, itemRP, RPNXY)
        leftW = 0 
        itemRP = update_itemRP(itemRP, downH, leftW)
        downH = 0
        leftW = leftWAtPoint(item, items, itemRP, RPNXY)
        itemRP = update_itemRP(itemRP, downH, leftW)
        if (downH == 0) and (leftW == 0):
            finalRP = itemRP
            break
    
    return finalRP

def overlap(item, items, itemRP, RPNXY):
    # 判断处于当前位置的物品在箱子中是否与其它物品有重合，
    # 有重合flagOL=1，反之flagOL=0
    flagOL = 0
    itemLBP = np.append(itemRP[0] - item[0],
                        itemRP[1] - item[1])
    A = np.append(itemLBP, itemRP)
    num = RPNXY.shape[0]
    if num > 0:
        for i in range(num):
            Sbx = items[RPNXY[i,0], 0] # 宽度
            Sby = items[RPNXY[i,0], 1] # 高度
            LBPXY = np.append(RPNXY[i,1] - Sbx,
                              RPNXY[i,2] - Sby)
            B = np.append(LBPXY, RPNXY[i,:])
            minx = max(A[0], B[0])
            miny = max(A[1], B[1])
            maxx = min(A[2], B[2])
            maxy = min(A[3], B[3])
            if (minx > maxx) or (miny > maxy):
                flagOL = 1
                break
            
    return flagOL


