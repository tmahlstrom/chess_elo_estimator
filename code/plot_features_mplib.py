from numpy.random import rand
import numpy as np
from scipy import stats
import csv
import os
import pandas as pd
import math
import ast
import json
from itertools import cycle, islice

from bokeh.core.properties import value
from bokeh.io import show, output_file
from bokeh.plotting import figure
from bokeh.models import HoverTool, FactorRange, ColumnDataSource

import matplotlib
import matplotlib.pyplot as plt
from matplotlib import cm
from matplotlib import rc
import seaborn as sns 
from matplotlib.colors import ListedColormap
import matplotlib.style as style
from matplotlib.patches import Patch
from matplotlib.font_manager import FontProperties
from matplotlib.colors import LinearSegmentedColormap

y_model_pred = []
y_elo_standard_pred = []


def main():
    df = pd.read_pickle('feature_df')
    print(df)
    plot_features(df)
    # axes = df.plot.bar(rot=0, subplots=True)
    # axes[1].legend(loc=2)
    # plt.show()
    #plot_model_validation(y_model_pred, y_elo_standard_pred)


def plot_features(df):

    style.use('seaborn-talk') 
    sns.set_style("white")
    sns.set_context("poster", font_scale=1.5,)
    font = {'fontname':'Adobe Hebrew'}
    bins = np.array([400 + 25 * x for x in range(150)])
    # font = {'family' : 'normal',
    #     'weight' : 'bold',
    #     'size'   : 22}

    #matplotlib.rc('font', **font)

    # set width of bar
    barWidth = 0.25
    
    # set height of bar
    bars1 = df['% best move'].values.tolist()
    bars1 = [x - 0.2 for x in bars1]
    bars2 = df['avg mid game strength'].values.tolist()
    bars2 = [x - 0.5 for x in bars2]

    bars3 = df['% blunders'].values.tolist()
    bars4 = df['std cp score'].values.tolist()
    bars4 = [(x - 0.1) *2 for x in bars4]
    #bars3 = [29, 3, 24, 25, 17]
    
    # Set position of bar on X axis
    r1 = np.arange(len(bars1))
    r2 = [x + barWidth for x in r1]
    #r3 = [x + barWidth for x in r2]
    
    # Make the plot
    plt.subplot(2, 1, 1)
    plt.bar(r1, bars1, color=[218.0/255,165/255.0,32.0/255], width=barWidth, linewidth = 1.5, edgecolor='black', label= '% chosen moves = best option')
    plt.bar(r2, bars2, color=[0, 51./255., 102./255.], width=barWidth, linewidth = 1.5, edgecolor='black', label='average mid-game choice rank')
    #plt.xlabel('', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(bars1))], df.index.tolist(), size = 20)
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=True)
    plt.yticks([])
    plt.ylabel('values scaled for viewing', fontsize=20, **font)
    plt.legend(loc = 2, prop={'size': 20, 'family':'Adobe Hebrew'}, labelspacing = 1.0)
    plt.margins(x=0.05)
    #plt.title("Several features used to train my models", fontweight='bold', size = 32)
    plt.title("Several features used to train my models", loc = 'center', y=0.99, bbox=dict(facecolor='white', edgecolor='black', boxstyle='square', linewidth = 1.0), fontsize=30, **font)

    #plt.bar(r3, bars3, color='#2d7f5e', width=barWidth, edgecolor='white', label='var3')
    plt.subplot(2, 1, 2)
    plt.bar(r1, bars3, color=[102./255., 0, 25./255.], width=barWidth, linewidth = 1.5, edgecolor='black', label='% chosen moves = blunder')
    plt.bar(r2, bars4, color=[85./255, 85./255, 85./255], width=barWidth, linewidth = 1.5, edgecolor='black', label='standard dev. of move strength')
    plt.legend(prop={'size': 20, 'family':'Adobe Hebrew'}, labelspacing = 1.0)

    #plt.xticks(ticks=None, labels=None)
    # Add xticks on the middle of the group bars
    plt.xlabel('Elo bins', fontsize=22, **font)
    plt.xticks([r + barWidth for r in range(len(bars1))], df.index.tolist(), size = 20)
    plt.tick_params(
        axis='x',          # changes apply to the x-axis
        which='both',      # both major and minor ticks are affected
        bottom=False,      # ticks along the bottom edge are off
        top=False,         # ticks along the top edge are off
        labelbottom=True)
    plt.yticks([])
    plt.ylabel('values scaled for viewing', fontsize=20, **font)
    plt.margins(x=0.05)


    # Create legend & Show graphic

    plt.show()



    # style.use('seaborn-talk') 
    # sns.set_style("white")
    # sns.set_context("poster", font_scale=1.5,)
    # font = {'fontname':'Adobe Hebrew'}
    # bins = np.array([400 + 25 * x for x in range(150)])

    # sns.distplot(y_elo_standard_pred, bins = bins, hist = True, kde=False, color = [102./255., 0, 25./255.],
    #         hist_kws = {"histtype"  : 'stepfilled', "alpha": 0.8},
    #         kde_kws = {'shade': True, 'linewidth': 1}, 
    #         label = 'standard system predictions')
    # sns.distplot(y_model_pred, bins = bins, hist = True, kde=False, color = [0, 51./255., 102./255.], 
    #         hist_kws = {"histtype"  : 'stepfilled', "alpha": 0.8},
    #         kde_kws = {'shade': True, 'linewidth': 1},  
    #         label = 'my model predictions')
    # sns.distplot(y_test, bins = bins, hist = True, kde=False, color = [218.0/255,165/255.0,32.0/255],
    #         hist_kws = {"histtype"  : 'stepfilled', "alpha": 0.4},
    #         kde_kws = {'shade': True, 'linewidth': 1}, label = 'target values')


    # # p = df.ix[:, df.columns.difference(exclude)].T.plot(kind='bar', stacked=True, color = colors, edgecolor = 'black', figsize=(16,8), grid = None, legend=False, linewidth = 1.5)
    # #plt.rcParams["font.size"] = 28
    # plt.minorticks_off()
    # #plt.setp(p, markerfacecolor='C0')
    # x_ticks_int = [1000, 1200, 1400, 1600, 1800, 2000, 2200, 2400]
    # x_ticks_str = [str(x) for x in x_ticks_int]
    
    # plt.xticks(x_ticks_int, x_ticks_str, rotation='horizontal', fontsize=14, fontname = 'Lucida Console')
    # plt.yticks([])
    # plt.title("Density of predicted vs target Elo values", loc = 'center', y=0.99, bbox=dict(facecolor='white', edgecolor='black', boxstyle='square', linewidth = 1.0), fontsize=30, **font)
    # plt.xlabel("Elo", fontsize=22, **font)
    # plt.ylabel("Density",labelpad= 20, fontsize=22, **font)
    # plt.xlim(900, 2500)
    # plt.ylim(0.0, 90)

    # # ax = plt.subplot(111)
    # # box = ax.get_position()
    # # ax.set_position([box.x0, box.y0, box.width * 0.8, box.height])
    
    # map_colors = [(0, 51./255., 102./255.), (.7, .6, .7), (102./255., 0, 25./255.)] 
    # cmap_name = 'my_custom_cmap'
    # cmap = LinearSegmentedColormap.from_list(cmap_name, map_colors, N=9)

    
    # legend_elements = [Patch(facecolor=[102./255., 0, 25./255., 0.8], edgecolor='black',
    #                     label='Standard Elo system', linewidth = 1.0),
    #                     Patch(facecolor= [0, 51./255., 102./255., 0.8], edgecolor='black',
    #                     label='My model predictions', linewidth = 1.0),
    #                     Patch(facecolor= [218.0/255,165/255.0,32.0/255, 0.4], edgecolor='black',
    #                     label='Actual values', linewidth = 1.0)]
    # plt.legend(handles=legend_elements, loc='center right',  prop={'size': 18, 'family':'Adobe Hebrew'}, labelspacing = 1.0)
    # #bbox_to_anchor=(1, 0.5),
    
    # # plt.legend(handles=legend_elements, loc='top')
    # plt.show()






y_model_pred = [1500.5618168962362, 1496.7201318909686, 1451.7689212111468, 1620.5188818836882, 1514.381035497736, 1547.495837542127, 1533.2345235648957, 1595.5002791228028, 1598.785197300402, 1639.273123259164, 1649.727844925884, 1597.2111387064074, 1674.9143544107135, 1709.730977889894, 1589.494965455724, 1431.081869129433, 1521.391070401386, 1454.5952079842043, 1077.5581401813233, 1576.6844961753561, 1605.5589097920233, 1548.6249037362088, 1698.9255802548726, 1516.8248753882665, 1462.3118183480121, 1507.1863034019016, 1515.1066003641574, 1599.134180333874, 1562.6112273009244, 1632.606027525182, 1636.26342569943, 1631.8119497232924, 1325.6403125884192, 1530.4253971469639, 1476.483726954302, 1620.1346607909948, 1395.021300706066, 1387.1120539420444, 1495.1561937830465, 1582.5977397876802, 1663.6976183387903, 1401.7588140462278, 1627.6145087066877, 1548.4213167179985, 1563.0523487445716, 1591.074969797587, 1792.8882989901222, 1695.9111187364638, 1657.395974518438, 1550.8496604201885, 1466.829383476179, 1530.5898421724337, 1615.2892986760278, 1652.1482404281332, 1580.4105852037962, 1669.1404115802047, 1509.3607820616794, 1511.3987496680052, 1780.6190437575156, 1576.4756679154364, 1643.8879970445266, 1596.6214901066364, 1555.7169002177975, 1663.2512661785993, 1797.6270608624643, 1275.4849739418792, 1249.0789834079992, 1723.6827152250496, 1621.8565956296018, 1640.0933743654973, 1340.1256572639231, 1599.73347256197, 1450.0871526228034, 1738.9700647129926, 1397.9502268540934, 1597.0916133267565, 1639.188973976265, 1643.0789778524716, 1469.0882038536233, 1711.8473959534754, 1710.6244135812285, 1766.2189264330714, 1354.166807040016, 1742.9191366901928, 1656.813439171675, 1656.4802632475491, 1581.5472346745846, 1605.4326405793556, 1262.2587735595946, 1388.4500970050199, 1574.4464875837325, 1542.368329243655, 1462.6185878488604, 1701.70032793744, 1762.3032706018537, 1431.7292692778326, 1503.2298346609764, 1686.3577301130551, 1733.661686769307, 1617.700350505046, 1668.1095587048421, 1669.2939596352298, 1570.6530962603085, 1561.811805950251, 1730.060750386044, 1468.4395564640986, 1508.4696464922365, 1282.92100373808, 1509.3280839057466, 1653.5147957835472, 1637.4004603970334, 1795.1474529039815, 1105.375590554999, 1578.5308816385602, 1500.6938748506773, 1758.3537384917554, 1690.2296903779177, 1598.2565231390947, 1475.3310241938836, 1584.2559894636668, 1452.518241289372, 1670.8907644969279, 1662.150471978718, 1710.4698109999167, 1466.6178359796966, 1543.9082647950959, 1634.121540029521, 1737.3781888874123, 1630.4951379266588, 1713.1353270921218, 1316.3479397693795, 1485.6948448097592, 1470.9616964109416, 1572.6613188679544, 1457.4668769888879, 1523.5422662996336, 1566.475185531975, 1646.7620286050023, 1625.0768233333872, 1567.9397332493174, 1412.4322273361545, 1514.6963490801681, 1610.6010107388204, 1730.1781612482023, 1662.6977103217291, 1602.0649710967757, 1530.2721795291955, 1424.8895890777283, 1747.4590215718201, 1579.9879498386695, 1473.938294585624, 1676.0501897035672, 1585.5558554200225, 1267.1539663814585, 1454.1817080300139, 1549.1909895376466, 1471.9537290157616, 1385.6933844651126, 1723.7258275769148, 1781.2972244479852, 1622.6169094024142, 1697.306505854452, 1651.3727599563772, 1628.9544615133877, 1428.4752769222305, 1565.155064363172, 1633.1195749494075, 1379.9423078841194, 1604.125913485573, 1552.538764216938, 1496.2699070363126, 1430.770626835571, 1607.451136190077, 1491.401263284645, 1583.8906427523361, 1575.9975660961209, 1539.9925499341127, 1666.6802356280289, 1462.6783054602022, 1568.3947814127591, 1692.9240278468394, 1583.830385479205, 1840.451708805093, 1488.489945217365, 1645.7338565374682, 1642.480505538726, 1607.350008920126, 1626.6868090743646, 1626.5713224485003, 1955.0500529721025, 1787.8714559933112, 1559.1271545489233, 1655.499646543856, 1590.486342866457, 1650.3872387314195, 1506.2136588614896, 1640.167437315175, 1402.3382492386609, 1705.0744238476195, 1697.7803391382279, 1478.6037964559184, 1671.1075049662288, 1649.084898365615, 1461.579662068033, 1661.9436155064366]
y_elo_standard_pred = [1588, 1587, 1526, 1585, 1567, 1568, 1573, 1576, 1565, 1589, 1591, 1576, 1581, 1569, 1551, 1530, 1577, 1546, 1521, 1548, 1558, 1546, 1592, 1532, 1564, 1564, 1584, 1530, 1577, 1533, 1534, 1537, 1529, 1576, 1578, 1547, 1581, 1532, 1550, 1568, 1581, 1576, 1591, 1538, 1574, 1543, 1558, 1578, 1540, 1592, 1575, 1586, 1557, 1589, 1582, 1590, 1541, 1567, 1553, 1591, 1540, 1566, 1568, 1591, 1552, 1529, 1523, 1591, 1573, 1592, 1522, 1564, 1538, 1540, 1564, 1549, 1587, 1589, 1563, 1575, 1572, 1597, 1564, 1568, 1551, 1565, 1568, 1566, 1573, 1563, 1593, 1542, 1572, 1596, 1585, 1533, 1561, 1573, 1531, 1536, 1562, 1566, 1586, 1536, 1547, 1528, 1523, 1563, 1574, 1554, 1569, 1548, 1562, 1556, 1581, 1543, 1547, 1535, 1545, 1575, 1564, 1585, 1590, 1594, 1577, 1540, 1568, 1589, 1549, 1573, 1568, 1538, 1548, 1579, 1534, 1528, 1575, 1568, 1595, 1555, 1536, 1567, 1571, 1535, 1556, 1596, 1522, 1577, 1555, 1550, 1530, 1551, 1547, 1553, 1554, 1586, 1548, 1576, 1558, 1597, 1589, 1575, 1547, 1579, 1544, 1585, 1536, 1565, 1542, 1577, 1530, 1549, 1555, 1521, 1579, 1583, 1552, 1557, 1521, 1573, 1559, 1587, 1558, 1547, 1570, 1556, 1585, 1580, 1593, 1570, 1556, 1595, 1597, 1546, 1594, 1525, 1582, 1532, 1552, 1552, 1530, 1593, 1554, 1536, 1526]
y_test = [1604, 1669, 1366, 1681, 1345, 1807, 1562, 1553, 1318, 1924, 1965, 1500, 1529, 1311, 1806, 1435, 1524, 1482, 1303, 1781, 1906, 1405, 1807, 1315, 1226, 1248, 1362, 1542, 1510, 1322, 1593, 1466, 1274, 1536, 1301, 1580, 1681, 1462, 1626, 1343, 1405, 1451, 1746, 1505, 1483, 1419, 1951, 1790, 1591, 1827, 1600, 1790, 1866, 1640, 1678, 1835, 1386, 1260, 1827, 1901, 1560, 1700, 1444, 1961, 1771, 1201, 1153, 1969, 1024, 1792, 1100, 1534, 1465, 1571, 1231, 1842, 1704, 1783, 1160, 1491, 1889, 2279, 1300, 1371, 1710, 1374, 1405, 1346, 1435, 1180, 1828, 1598, 1279, 1875, 1832, 1026, 1156, 1643, 1513, 1380, 1360, 1135, 1582, 1485, 1783, 1500, 1380, 1280, 1597, 1825, 1370, 1822, 1090, 1895, 1720, 1577, 1682, 1586, 1592, 1476, 1204, 1776, 1983, 1767, 1575, 1618, 1348, 1837, 1863, 1497, 1281, 1533, 1670, 1578, 1709, 1290, 1738, 1542, 1821, 1927, 1451, 1285, 1430, 1460, 1944, 1956, 990, 1733, 1928, 1739, 1358, 1800, 1747, 1813, 1774, 1646, 1703, 1530, 2041, 2066, 1951, 1494, 1966, 1545, 1450, 1573, 1542, 1012, 1465, 1685, 1390, 1509, 1914, 1027, 1669, 1580, 1674, 1981, 1092, 1569, 2008, 1658, 1850, 1527, 1388, 1866, 1754, 1637, 1846, 1373, 1652, 1925, 1964, 1589, 2080, 1501, 1578, 1427, 1842, 1629, 1374, 1877, 1843, 1491, 1317]





if __name__ == '__main__':
    main()