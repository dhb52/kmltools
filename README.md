# KML规划支撑工具
KML 传输规划支撑工具在传输规划方面，目前大部分规划人员、设计院在很大的程度上依赖于Google Earth工具（下称GE），利用GE进行图层绘制以及图层叠加。本次微网格规划工作中，也大量的使用了GE进行网格图层绘制。并使用Google Earth Pro（GE专业版）对每个网格的面积进行提取。然而GE Pro没有提供批量网格面积导出的功能，也就是说只能逐个网格获取，并手工输入到网格汇总表中。由于各个地市的网格数以百计，甚至达到几千个，这就造成的大量的人力浪费，也容易出现错误。

## 下载：[发行版](https://gitee.com/dhb52/kmltools/releases)

## 功能一：
面积计算计算多边形面积，单位为平方米，从结算结果测试分析，与Google Earth Pro的计算存在10平方米级别的差异。
应用场景：批量导出综合业务区、微网格的面积计算

## 功能二：
长度计算计算弧线、直线长度，单位为米，从结算结果测试分析，与Google Earth Pro的计算存在10米级别的差异。
应用场景：批量计算新建光缆、管道长度。

## 功能三：
点面计算批量计算点在多边形的归属关系
应用场景：计算点（4G站点、光交箱）在多边形（微网格、综合业务区）的归属关系。

## 功能四：
提取图层中的点信息。
应用场景：在图层上规划新增机房、站点，可以导出站点信息

## 功能五：
计算多边形重叠信息。
应用场景：验证网格区域是否存在重叠问题

# 二次开发
## step 1
create a virtual environment
```
python -m venv .venv
.\venv\Scripts\activate.bat
```

## step 2
install the requiements 
```
pip install -r requirements.txt
```

## step 3
generate the resource file
```
pyrcc5 resource.qrc -o rc_resource.py
```

## step 4
Bundle the app
```
pyinstaller -i app.ico -w kmltools.pyw
```
