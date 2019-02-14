

import xml.etree.ElementTree as ET
import json
import threading
import random
import sys

from time import sleep

from kafka import KafkaProducer, KafkaClient



# KAFKA params
KAFKA_HOST  = 'kafka:9092'
KAFKA_TOPIC = 'input.stream'

# Workers params
WORKERS = 10
SLEEP   = 0.4

#FILE = "/Users/J/github/wanderlust/producer/data/traces/1099780.gpx"

# File as 2nd input parameter
FILE = sys.argv[1]

# Kafka client 
producer = KafkaProducer(bootstrap_servers=KAFKA_HOST)


def main():
    
    # Variables
    workers = []
    points  = []
    
    # Get GPS points from file
    if ".gpx" in FILE:
        points = read_GPX_file(FILE)    
    
    # Start workers
    for i in range(WORKERS):
        
        uid = FILE + "-" + str(i)
        start_at = random.randrange( len(points) )
        
        t = threading.Thread( target=worker, args=(uid, points, start_at,) )
        t.start()
        workers.append(t)
        
        # Wait and repeat
        sleep(SLEEP)

    return



def worker(uid, points, start_at):
    
    for i in range(start_at, len(points)):
        points[i]['uid'] = uid      
        v = json.dumps( points[i])
        producer.send(KAFKA_TOPIC, v.encode("utf8"))
        
        print(v)
        
        # Wait and repeat
        sleep(SLEEP)
        
    return




def read_PLT_file(file_path):
    
    """
    Parse Geolife log files. The function returns all GPS points in the file
    as a list of dicts { 'lat', 'lon', 'alt', 'time' }.
    """
        
    # Read full file and remove header (first 6 lines)
    lines = open(file_path).read().split('\n')[6:]
    
    # Parse GPS points in file
    points = []
    for line in lines:
        
        # Line structure (lat, lon, ?, alt, days, date, time)
        w = line.split(',')
        
        # Ignore lines not respecting the format
        if(len(w) != 7):
            continue
        
        # Parse GPS points
        else:
            point = { 'lat': w[0], 'lon': w[1], 'alt': w[3], 'time': w[5]+'T'+w[6] }
            points.append(point)
        
    return points



    
def read_GPX_file(file_path):
    
    """
    Parse OpenStreetMaps GPX trace file. The function returns all GPX points in the file
    as a list of dicts { 'lat', 'lon', 'alt', 'time' }.
    """
    
    # Load full GPX file and prepare parser
    root = ET.parse(file_path).getroot()
    
    # Get file namespace (ex. http://www.topografix.com/GPX/1/1)
    gpx_ns  = root.tag[1:].split('}')[0]  # {namespace}xml_node

    # Parser namespace param
    NS = {'ns': gpx_ns}    

    # Parse GPX points
    points = []
    for pt in root.findall('ns:trk/ns:trkseg/ns:trkpt', NS):
        
        lat = pt.get('lat')
        lon = pt.get('lon')
        alt  = pt.find('ns:ele', NS).text
        time = pt.find('ns:time', NS).text
        
        point = { 'lat': lat, 'lon': lon, 'alt': alt, 'time': time }
        
        points.append( point )
    
    return points
        
main()        