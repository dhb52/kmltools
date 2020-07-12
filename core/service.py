from io import StringIO

import openpyxl
from fastkml import geometry, kml, styles
from shapely.geometry import LineString as ShapelyLineString
from shapely.geometry import Polygon as ShapelyPolygon
from shapely.geometry.polygon import Polygon as ShapelyPolygonType

from . import _calculator as calculator


def calc_poly_areas(polygons):
    result = StringIO()
    result.write("名称,所在目录,面积(平方)\n")
    for a in polygons:
        area = calculator.polygon_area(a.coords)
        result.write("%s,%s,%f\n" % (a.name, a.path, area))
    return result.getvalue()


def points_inside_info(points, polygons) -> str:
    result = StringIO()
    result.write("点名称,经度,纬度,点所在目录,多边形名称,多边形所在目录\n")
    for point in points:
        x, y = point.coord.x, point.coord.y
        for poly in polygons:
            # if calculator.point_in_poly(x, y, poly.coords):
            if poly.contains(x, y):
                result.write(
                    "%s,%f,%f,%s,%s,%s\n"
                    % (point.name, x, y, point.path, poly.name, poly.path)
                )
    return result.getvalue()


def calc_poly_areas(polygons) -> str:
    result = StringIO()
    result.write("名称,所在目录,面积(平方)\n")
    for a in polygons:
        area = calculator.polygon_area(a.coords)
        result.write("%s,%s,%f\n" % (a.name, a.path, area))
    return result.getvalue()


def calc_line_length(lines) -> str:
    result = StringIO()
    result.write("名称,所在目录,长度(米)\n")
    for a in lines:
        length = calculator.line_length(a.coords)
        result.write("%s,%s,%f\n" % (a.name, a.path, length))
    return result.getvalue()


def calc_polygon_intersection_area(polygons) -> str:
    result = StringIO()
    result.write("多边形1,多边形1所在目录,多边形2,多边形2所在目录,重叠面积(平方)\n")
    for i, p1 in enumerate(polygons):
        shapely_p1 = ShapelyPolygon(p1.coords)
        for p2 in polygons[i+1:]:
            shapely_p2 = ShapelyPolygon(p2.coords)
            inter = None
            try:
                inter = shapely_p1.intersection(shapely_p2)
            except:
                pass
            if isinstance(inter, ShapelyPolygonType):
                area = calculator.polygon_area(inter.exterior.coords)
                if area > 0:
                    result.write(
                        "%s,%s,%s,%s,%f\n"
                        % (p1.name, p1.path, p2.name, p2.path, area)
                    )

    return result.getvalue()


def points_to_csv(points) -> str:
    result = StringIO()
    result.write("名称,经度,纬度,点所在目录\n")
    for point in points:
        result.write(
            "%s,%f,%f,%s\n" % (point.name, point.coord.x, point.coord.y, point.path)
        )
    return result.getvalue()

def link_points_kml(excel_path, kml_path) -> None:
    wb = openpyxl.load_workbook(excel_path)
    ws = wb.active
    kml_obj = kml.KML()
    lstyle = styles.LineStyle(color="ff00c500", width=2.0)
    style = styles.Style(styles=[lstyle])
    folder = kml.Folder(name="批量连线", styles=[style])

    kml_obj.append(folder)
    for row in ws.iter_rows(min_row=2, max_col=6, values_only=True):
        p1_name, p1_x, p1_y, p2_name, p2_x, p2_y = row
        p1_x, p1_y, p2_x, p2_y = (
            float(p1_x),
            float(p1_y),
            float(p2_x),
            float(p2_y),
        )
        if p1_x != p2_x and p1_y != p2_y:
            line = ShapelyLineString([(p1_x, p1_y, 0), (p2_x, p2_y, 0)])
            p = kml.Placemark(name=f"{p1_name}<->{p2_name}", styles=[style])
            p.geometry = line
            folder.append(p)
    kmlstr = kml_obj.to_string(prettyprint=True)
    with open(kml_path, "w") as out:
        out.write(kmlstr)
    wb.close()


def save_excel_template(excel_path) -> None:
    wb = openpyxl.Workbook()
    ws = wb.active
    rows = (
        ("点1名称", "经度", "纬度", "点2名称", "经度", "纬度"),
        ("潮州市", 116.622604, 23.65695, "枫溪镇", 116.606779, 23.64921),
        ("潮州市", 116.622604, 23.65695, "湘桥区", 116.628632, 23.674536),
        ("潮州市", 116.622604, 23.65695, "古巷镇", 116.574761, 23.661714),
        ("潮州市", 116.622604, 23.65695, "东丽湖新村", 116.665511, 23.662787),
        ("潮州市", 116.622604, 23.65695, "下水头村", 116.630906, 23.623607),
        ("潮州市", 116.622604, 23.65695, "潮州市", 116.622604, 23.65695),
    )
    for row in rows:
        ws.append(row)
    wb.save(excel_path)
    wb.close()
