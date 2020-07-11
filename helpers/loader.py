import zipfile

from fastkml import geometry, kml


class _GeoPolygon:
    def __init__(self, name, path, coords):
        self.name = name
        self.path = path
        self.coords = coords


class _GeoPoint:
    def __init__(self, name, path, coord):
        self.name = name
        self.path = path
        self.coord = coord


class _GeoLine:
    def __init__(self, name, path, coords):
        self.name = name
        self.path = path
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
    new_path = path
    if not getattr(element, "features", None):
        return
    for feature in element.features():
        if isinstance(feature, kml.Folder):
            if not feature.name:
                feature.name = ""
            new_path = "/".join((path, feature.name))
        elif isinstance(feature, kml.Placemark):
            if feature_type == geometry.Polygon and isinstance(
                feature.geometry, feature_type
            ):
                coords = [(p[0], p[1]) for p in feature.geometry.exterior.coords]
                poly = _GeoPolygon(feature.name, path, coords)
                result.append(poly)
            elif feature_type == geometry.Point and isinstance(
                feature.geometry, feature_type
            ):
                point = _GeoPoint(feature.name, path, feature.geometry)
                result.append(point)
            elif feature_type == geometry.LineString and isinstance(
                feature.geometry, feature_type
            ):
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
