from fastkml import geometry

from . import _calculator


class PlacemarkWithPath:
    def __init__(self, name, path) -> None:
        self.name = name
        self.path = path


class Point(PlacemarkWithPath):
    def __init__(self, name, path, geom) -> None:
        super(Point, self).__init__(name, path)
        self.x, self.y = geom.coords[0][:2]


class LineString(PlacemarkWithPath):
    def __init__(self, name, path, geom) -> None:
        super(LineString, self).__init__(name, path)
        self.coords = [(p[0], p[1]) for p in geom.coords]

    @property
    def length(self) -> float:
        return _calculator.line_length(self.coords)


class Polygon(PlacemarkWithPath):
    def __init__(self, name, path, geom) -> None:
        super(Polygon, self).__init__(name, path)
        self.coords = [(p[0], p[1]) for p in geom.exterior.coords]

    @property
    def area(self) -> float:
        return _calculator.polygon_area(self.coords)

    def contains(self, point) -> bool:
        return _calculator.is_point_in_polygon(point.x, point.y, self.coords)

    def intersection_area(self, other) -> float:
        shapely_intersection_coords = _calculator.polygon_intersect(
            self.coords, other.coords
        )
        if shapely_intersection_coords is not None:
            area = _calculator.polygon_area(shapely_intersection_coords)
            return area
        else:
            return 0


class MultiPolygon(PlacemarkWithPath):
    def __init__(self, name, path, geom) -> None:
        super(MultiPolygon, self).__init__(name, path)
        # self.coords = [(p[0], p[1]) for p in geom.exterior.coords]
        self.polygons = []
        self.geom = geom
        for polygon_geom in self.geom.geoms:
            self.polygons.append(Polygon(name, path, polygon_geom))

    @property
    def area(self) -> float:
        tolal_area = 0.0
        for polygon in self.polygons:
            tolal_area += polygon.area

        return tolal_area

    def contains(self, point) -> bool:
        for polygon in self.polygons:
            if polygon.contains(point):
                return True

        return False

    def intersection_area(self, other) -> float:
        raise NotImplementedError


def placemark(name, path, geom) -> PlacemarkWithPath:
    """Factory method creating a [Point, LineString, Polygon]
    according to type of geometry
    """
    if isinstance(geom, geometry.Point):
        return Point(name, path, geom)
    elif isinstance(geom, geometry.LineString):
        return LineString(name, path, geom)
    elif isinstance(geom, geometry.Polygon):
        return Polygon(name, path, geom)
    elif isinstance(geom, geometry.MultiPolygon):
        return MultiPolygon(name, path, geom)
    else:
        raise TypeError("Not a Point, nor LineString, nor Polygon, nor MultiPolygon")
