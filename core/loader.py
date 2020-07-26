import zipfile

from fastkml import geometry, kml

from ._placemark import placemark


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
        if isinstance(feature, kml.Folder) or isinstance(feature, kml.Document):
            if not feature.name:
                feature.name = ""
            new_path = "/".join((path, feature.name))
        elif isinstance(feature, kml.Placemark) and isinstance(
            feature.geometry, feature_type
        ):
            pm = placemark(feature.name, path, feature.geometry)
            result.append(pm)

        _find_features(result, feature, feature_type, new_path)


def _load_feature_from_file(kml_file, featur_type) -> list:
    features = []
    k = _load_kml(kml_file)
    _find_features(features, k, featur_type)
    return features


def load_points(kml_file) -> list:
    return _load_feature_from_file(kml_file, geometry.Point)


def load_polygons(kml_file) -> list:
    return _load_feature_from_file(kml_file, geometry.Polygon)


def load_lines(kml_file) -> list:
    return _load_feature_from_file(kml_file, geometry.LineString)
