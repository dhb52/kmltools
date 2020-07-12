import zipfile

from fastkml import geometry, kml
from shapely.geometry import Point
from shapely.geometry.polygon import Polygon


class _GeoBase:
    def __init__(self, name, path) -> None:
        self.name = name
        self.path = path


class _GeoPolygon(_GeoBase):
    def __init__(self, name, path, coords) -> None:
        super(_GeoPolygon, self).__init__(name, path)
        self.coords = coords

    def contains(self, x, y) -> bool:
        points = [Point(p) for p in self.coords]
        poly = Polygon(points)
        return poly.contains(Point(x, y))


class _GeoPoint(_GeoBase):
    def __init__(self, name, path, coord) -> None:
        super(_GeoPoint, self).__init__(name, path)
        self.coord = coord


class _GeoLine(_GeoBase):
    def __init__(self, name, path, coords) -> None:
        super(_GeoPoint, self).__init__(name, path)
        self.coords = coords


def _load_kml(path) -> kml.KML:
    k = kml.KML()
    xml = None
    if path.lower().endswith(".kmz"):
        with zipfile.ZipFile(path, "r") as zf:
            xml = zf.read("doc.kml")
    else:
        with open(path, "rb") as kmlFile:
            xml = kmlFile.read()

    k.from_string(xml)
    return k


def _find_features(result, element, feature_type, path=""):
    """Recursively find feature by [feature_type]
    and add current path info to the current feature
    """
    new_path = path
    if not getattr(element, "features", None):
        return
    for feature in element.features():
        if isinstance(feature, kml.Folder):
            if not feature.name:
                feature.name = ""
            new_path = "/".join((path, feature.name))
        elif isinstance(feature, kml.Placemark) and isinstance(
            feature.geometry, feature_type
        ):
            if feature_type == geometry.Polygon:
                coords = [(p[0], p[1]) for p in feature.geometry.exterior.coords]
                poly = _GeoPolygon(feature.name, path, coords)
                result.append(poly)
            elif feature_type == geometry.Point:
                point = _GeoPoint(feature.name, path, feature.geometry)
                result.append(point)
            elif feature_type == geometry.LineString:
                line = _GeoLine(feature.name, path, feature.geometry.coords)
                result.append(line)

        _find_features(result, feature, feature_type, new_path)


def _load_feature_from_file(kml_file, featur_type):
    features = []
    k = _load_kml(kml_file)
    _find_features(features, k, featur_type)
    return features


def load_points(kml_file):
    return _load_feature_from_file(kml_file, geometry.Point)


def load_polygons(kml_file):
    return _load_feature_from_file(kml_file, geometry.Polygon)


def load_lines(kml_file):
    return _load_feature_from_file(kml_file, geometry.LineString)
