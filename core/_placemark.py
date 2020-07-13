from fastkml import geometry


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


class Polygon(PlacemarkWithPath):
    def __init__(self, name, path, geom) -> None:
        super(Polygon, self).__init__(name, path)
        self.coords = [(p[0], p[1]) for p in geom.exterior.coords]


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
    else:
        raise TypeError("Not a Point, nor LineString, nor Polygon")
