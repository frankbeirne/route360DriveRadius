import json
import argparse
from r360_py.util.TravelOptions import TravelOptions
from r360_py.util.Configuration import Configuration
from r360_py.rest.polygon.PolygonService import PolygonService
from r360_py.util.enum.PolygonSerializationType import PolygonSerializationType
from r360_py.util.enum.TravelType import TravelType

def source(arg):
    # For simplity, assume arg is a pair of integers
    # separated by a comma. If you want to do more
    # validation, raise argparse.ArgumentError if you
    # encounter a problem.
    return [float(x) for x in arg.split(';')]


parser = argparse.ArgumentParser(description="Query the Route360° Polygon service in python", formatter_class=argparse.ArgumentDefaultsHelpFormatter)

parser.add_argument("--serviceUrl",        type=str,    help="The URL of the Route360° API endpoint.")
parser.add_argument("--serviceKey",        type=str,    help="Your personal key for the API.")
parser.add_argument("--travelType",        type=str,    help="The travel type for the request: car, walk, bike or transit")
parser.add_argument("--travelTimes",       type=int,    help="The travel time in seconds as a list of integers.", nargs="+")
parser.add_argument("--time",              type=int,    help="The time in seconds of the day: 1.30 p.m. = 13 * 3600 + 30 * 60 = 48600 (transit only)", default=43200)
parser.add_argument("--date",              type=int,    help="The date in the format YYYYMMDD, e.g.: 20160727 for the 27th of July 2016 (transit only)", default=20162707)
parser.add_argument("--polygonSerializer", type=str,    help="The serializer for the polygons: json or geojson", default="geojson")
parser.add_argument("--source",            type=source, help="The source as doubles (lat,lng) separated by ';'.")
parser.add_argument("--buffer",            type=int,    help="The buffer (in meter) that should be generated around the polygons. (max 500m)", default=None)
parser.add_argument("--simplify",          type=int,    help="The threshold (in meter) that should be used for Douglas-Puecker (before buffering, max 500m).", default=None)
parser.add_argument("--srid",              type=int,    help="The target SRID (Spatial Reference System Identifier), all that are supported via PostGIS.", default=None)
parser.add_argument("--quadrantSegments",  type=int,    help="The number of quadrant segements (max 8), see: http://postgis.net/docs/ST_Buffer.html.", default=None)
parser.add_argument("--outputDir",         type=str,    help="The path where to write the output files")
parser.add_argument("--outputFilename",    type=str,    help="The the name of the file to write to")

args = parser.parse_args()

travelOptions = TravelOptions();
travelOptions.addSource({ "id": str(args.source[0]) + ";" + str(args.source[1]), "lat" :  args.source[0],  "lng" :  args.source[1], "tm" : {  args.travelType : {
        "date" : args.date, "time" : args.time
    }}})
travelOptions.setServiceKey(args.serviceKey)
travelOptions.setTravelTimes(args.travelTimes)
travelOptions.setServiceUrl(args.serviceUrl)
travelOptions.setMinPolygonHoleSize(10000000)
travelOptions.setTravelDate(args.date)
travelOptions.setTravelDate(args.time)
travelOptions.setBufferMeter(args.buffer)
travelOptions.setSimplifyMeter(args.simplify)
travelOptions.setSrid(args.srid)
travelOptions.setQuadrantSegments(args.quadrantSegments)
travelOptions.setTravelType(TravelType.parse(args.travelType))
travelOptions.setPolygonSerializationType(PolygonSerializationType.parse(args.polygonSerializer))

polygon = PolygonService().getPolygons(travelOptions)

f = open(args.outputDir + args.outputFilename, 'w')
f.write(json.dumps(polygon["data"]))