from geographiclib.geodesic import Geodesic
from shapely.geometry import Polygon as ShapelyPolygon


def polygon_area(coords) -> float:
    geod = Geodesic.WGS84
    p = geod.Polygon()
    for coord in coords:
        x, y = coord
        p.AddPoint(y, x)
    _, _, area = p.Compute()
    return abs(area)


def line_length(coords) -> float:
    geod = Geodesic.WGS84
    cnt = len(coords)
    length = 0.0
    for i in range(cnt - 1):
        p1_x, p1_y = coords[i]
        p2_x, p2_y = coords[i + 1]
        line = geod.Inverse(p1_y, p1_x, p2_y, p2_x)
        length += line["s12"]
    return length


def is_point_in_polygon(x, y, polygon_coords) -> bool:
    """url: https://stackoverflow.com/questions/36399381/whats-the-fastest-way-of-checking-if-a-point-is-inside-a-polygon-in-python
    """
    n = len(polygon_coords)
    inside = False
    p1x, p1y = polygon_coords[0]
    for i in range(n + 1):
        p2x, p2y = polygon_coords[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    xints = None
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or (xints is not None and x <= xints):
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside


def polygon_intersect(polygon1_coords, polygon2_coords):
    shapely_p1 = ShapelyPolygon(polygon1_coords)
    shapely_p2 = ShapelyPolygon(polygon2_coords)
    inter = None
    try:
        inter = shapely_p1.intersection(shapely_p2)
    except:
        pass
    if isinstance(inter, ShapelyPolygon):
        return inter.exterior.coords
    else:
        return None
