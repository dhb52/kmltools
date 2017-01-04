#!/usr/bin/env python
# coding: utf-8

# import sys
# reload(sys)
# sys.setdefaultencoding("utf-8")

import codecs

import os.path
import zipfile

import StringIO
from fastkml import kml
from fastkml import geometry
from geographiclib.geodesic import Geodesic


class GeoObj(object):
    def __init__(self, name, path, geo):
        self.name = name
        self.path = path 
        self.geo  = geo


class GeoPolygon:
    def __init__(self, name, path, coords):
        self.name = name
        self.path = path
        self.coords = coords


class GeoPoint:
    def __init__(self, name, path, coord):
        self.name = name
        self.path = path
        self.coord = coord


class GeoLine(object):
    def __init__(self, name, path, coords):
        self.name = name
        self.path = path
        self.coords = coords
        

 

def point_in_poly(x, y, poly):
    n = len(poly)
    inside = False

    p1x,p1y = poly[0]
    for i in range(n+1):
        p2x,p2y = poly[i % n]
        if y > min(p1y,p2y):
            if y <= max(p1y,p2y):
                if x <= max(p1x,p2x):
                    if p1y != p2y:
                        xints = (y-p1y)*(p2x-p1x)/(p2y-p1y)+p1x
                    if p1x == p2x or x <= xints:
                        inside = not inside
        p1x,p1y = p2x,p2y

    return inside


def find_features(result, element, feature_type, path = ""):
    if not getattr(element, 'features', None):
        return
    for feature in element.features():
        if isinstance(feature, kml.Folder):
            if feature.name == None: feature.name = ""
            path = '/'.join((path, feature.name))
        elif isinstance(feature, kml.Placemark):
            if feature_type == geometry.Polygon and isinstance(feature.geometry, feature_type):
                coords = [ (p[0], p[1]) for p in feature.geometry.exterior.coords ]
                poly = GeoPolygon(feature.name, path, coords)
                result.append(poly)
            elif feature_type == geometry.Point and isinstance(feature.geometry, feature_type):
                point = GeoPoint(feature.name, path, feature.geometry)
                result.append(point)
            elif feature_type == geometry.LineString and isinstance(feature.geometry, feature_type):
                line = GeoLine(feature.name, path, feature.geometry.coords)
                result.append(line)
        find_features(result, feature, feature_type, path)


# def _reproject(latitude, longitude):
#     """Returns the x & y coordinates in meters using a sinusoidal projection"""
#     from math import pi, cos, radians
#     earth_radius = 6371009 # in meters
#     lat_dist = pi * earth_radius / 180.0

#     y = [lat * lat_dist for lat in latitude]
#     x = [lng * lat_dist * cos(radians(lat)) 
#                 for lat, lng in zip(latitude, longitude)]
#     return x, y


# def area_of_polygon(coordinates):
#     """Calculates the area of an arbitrary polygon given its verticies"""
#     lon, lat = zip(*coordinates)

#     x, y = _reproject(lon, lat)

#     area = 0.0
#     for i in xrange(-1, len(x)-1):
#         area += x[i] * (y[i+1] - y[i-1])
    
#     return abs(area) / 2.0


# def polygon_area(coordinates):
#     from pyproj import Proj
#     from shapely.geometry import shape

#     lon, lat = zip(*coordinates)

#     pa = Proj("+proj=aea +lat_1=37.0 +lat_2=41.0 +lat_0=39.0 +lon_0=-106.55")
#     x, y = pa(lon, lat)
#     cop = {"type": "Polygon", "coordinates": [zip(x, y)]}
#     area = shape(cop).area

#     return area

def polygon_area(coordinates):
    from geographiclib.geodesic import Geodesic
    geod = Geodesic.WGS84
    #lon, lat = zip(*coordinates)
    p = geod.Polygon()
    for lon, lat in coordinates:
        p.AddPoint(lat, lon)  # AddPoint(lat, lon)
    _, _, area = p.Compute()
    return area


def _detect_enc(path):
    detector = UniversalDetector()
    for line in open(path).readlines():
        detector.feed(line)
        if detector.done: break

    detector.close()
    return detector.result['encoding']


def _read_kml_from_file(file_path):
    k = kml.KML()
    xml = None
    if file_path.lower().endswith('.kmz'):
        with zipfile.ZipFile(file_path, 'r') as zf:
            xml = zf.read("doc.kml")
    else:
        with open(file_path) as kmlFile:
            xml = kmlFile.read()

    k.from_string(xml)
    return k


def load_points(points_file):
    points = []
    k = _read_kml_from_file(points_file)
    find_features(points, k, geometry.Point)
    return points


def load_polygons(polygons_file):
    polygons = []
    k = _read_kml_from_file(polygons_file) 
    find_features(polygons, k, geometry.Polygon)
    return polygons


def load_lines(line_file):
    lines = []
    k = _read_kml_from_file(line_file) 
    find_features(lines, k, geometry.LineString)
    return lines
        

def load_data(points_file, polygons_file):
    points = load_points(points_file)
    polygons = load_polygons(polygons_file)
    return points, polygons


def points_inside_info(points, polygons):
    result = StringIO.StringIO()
    print >> result, "POINT NAME,POINT FOLDER,POLYGON NAME, POLYGON FOLDER"
    for point in points:
        x, y = point.coord.x, point.coord.y
        for poly in polygons:
            if point_in_poly(x, y, poly.coords):
                print >> result, "%s,%s,%s,%s" % (point.name, point.path, poly.name, poly.path)
    return result.getvalue()


def calc_poly_areas(polygons):
    result = StringIO.StringIO()
    print >> result, "NAME,FOLDER,AREA(m^2)"
    for a in polygons:
        area = polygon_area(a.coords)
        #print >> result, "%s,%d" % (a.name, area)
        print >> result, "%s,%s,%f" % (a.name, a.path, area)
    return result.getvalue()


def line_length(coords):
    geod = Geodesic.WGS84
    cnt = len(coords)
    length = 0.0
    for i in range(cnt-1):
        p1_lon, p1_lat, _ = coords[i]
        p2_lon, p2_lat, _ = coords[i+1]
        line = geod.Inverse(p1_lat, p1_lon, p2_lat, p2_lon)
        length += line['s12']

    return length


def calc_line_length(lines):
    result = StringIO.StringIO()
    print >> result, "NAME,FOLDER,LENGTH(m)"
    for a in lines:
        length = line_length(a.coords)
        print >> result, "%s,%s,%f" % (a.name, a.path, length)
    return result.getvalue()


if __name__ == '__main__':
    points, polygons = load_data('points.kml', 'areas.kml')
    print points_inside_info(points, polygons)
    print calc_poly_areas(polygons)




