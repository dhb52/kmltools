from geographiclib.geodesic import Geodesic


def polygon_area(coordinates):
    geod = Geodesic.WGS84
    p = geod.Polygon()
    for lon, lat in coordinates:
        p.AddPoint(lat, lon)
    _, _, area = p.Compute()
    return abs(area)


def line_length(coords):
    geod = Geodesic.WGS84
    cnt = len(coords)
    length = 0.0
    for i in range(cnt - 1):
        p1_lon, p1_lat, _ = coords[i]
        p2_lon, p2_lat, _ = coords[i + 1]
        line = geod.Inverse(p1_lat, p1_lon, p2_lat, p2_lon)
        length += line["s12"]
    return length


def point_in_poly(x, y, poly):
    n = len(poly)
    inside = False
    p1x, p1y = poly[0]
    for i in range(n + 1):
        p2x, p2y = poly[i % n]
        if y > min(p1y, p2y):
            if y <= max(p1y, p2y):
                if x <= max(p1x, p2x):
                    if p1y != p2y:
                        xints = (y - p1y) * (p2x - p1x) / (p2y - p1y) + p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x, p1y = p2x, p2y
    return inside
