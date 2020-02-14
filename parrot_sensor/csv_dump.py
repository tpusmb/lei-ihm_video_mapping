#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
GNU AFFERO GENERAL PUBLIC LICENSE
    Version 3, 19 November 2007
"""
from datetime import *
import csv

dateFormat = "%d-%b-%Y %H:%M:%S"
datas_directory = "datas/"
basename = "data_"
extension = ".csv"


def dump_all_flower_power(api, since="born", until="today"):
    sensor_data_sync = api.get_sensor_data_sync()
    for location in sensor_data_sync["locations"]:
        err = dump_flower_power(api, location, since, until)
        if err == -1:
            print "Your 'Since' date is after your 'Until' date !?"
            break


def dump_flower_power(api, location, since, until):
    until = datetime.today() if until == "today" else datetime.strptime(until, dateFormat)
    since = until - timedelta(days=7) if since == "born" else datetime.strptime(since, dateFormat)

    if since > until:
        return -1
    elif location['sensor']:
        # old name: location['sensor']['sensor_identifier'] + ".csv"
        filename = datas_directory + basename + location['plant_nickname'] + extension
        print "Dump " + filename
        print " From: " + str(since)[:19]
        print " To:   " + str(until)[:19]

        file_csv = csv.writer(open(filename, "wb"))
        # file_csv.writerow(["capture_datetime_utc", "fertilizer_level", "light", "soil_moisture_percent",
        #                   "air_temperature_celsius"])

        while since < until:
            samples_location = api.get_samples_location(location['location_identifier'], since,
                                                        since + timedelta(days=7))

            if len(samples_location["errors"]):
                print location['sensor']['sensor_identifier'], samples_location["errors"][0]["error_message"]
                continue

            for sample in samples_location['samples']:
                capture_datetime_utc = sample["capture_datetime_utc"].replace("T", " ").replace("Z", "")
                fertilizer_level = sample["fertilizer_level"]
                soil_moisture_percent = sample["soil_moisture_percent"]
                air_temperature_celsius = sample["air_temperature_celsius"]
                light = sample["light"]
                file_csv.writerow([location['plant_nickname'], capture_datetime_utc, fertilizer_level, light,
                                   soil_moisture_percent, air_temperature_celsius])

            since += timedelta(days=7)
        print
        return 0

if __name__ == "__main__":
    # Si on execute se script le chemin n'est plus le maime pour les fichiers de plantes
    datas_directory = "../datas/"
    import api_cloud

    client_id = "faubet.mael@gmail.com"
    client_secret = "7vhQGmU3BP0cmJhIamnH7Pyxr3yo8XoU6B4jOShVFK8ZtCdS"
    username = "speedbirds@hotmail.fr"
    password = "darkofthemoon3"

    connection = api_cloud.ApiCloud(client_id, client_secret)
    connection.login(username, password)
    dump_all_flower_power(connection)
