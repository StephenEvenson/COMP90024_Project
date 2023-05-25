#
# Part of Assignment 2 - COMP90024
#
# Cluster and Cloud Computing - Team 72
#
# Authors:
#
#  - Juntao Lu (Student ID: 1290513)
#  - Runtian Zhang (Student ID: 1290379)
#  - Jiahao Shen (Student ID: 1381187)
#  - Yuchen Liu (Student ID: 1313394)
#  - Jie Shen (Student ID: 1378708)
#
# Location: Melbourne
#
import json

import requests


class PHNAPI:
    def __init__(self, phn_memory_file):
        self.base_url = "https://app.dmap.io/api/data-gis"
        self.access_token = "guest"
        with open(phn_memory_file, 'r') as f:
            self.phn_memory = json.load(f)

    def get_phn_by_bbox(self, bbox, dataType="boundary", dataset="PHN_boundaries_AUS_May2017_V7 (DOH)", zoomLevel=10,
                        mapOptBndAcc=2, mapOptMarkerGrouping=0):

        bbox_key = json.dumps(bbox)

        if bbox_key in self.phn_memory:
            return self.phn_memory[bbox_key]

        boundsSouthWestLng = bbox[0]
        boundsSouthWestLat = bbox[1]
        boundsNorthEastLng = bbox[2]
        boundsNorthEastLat = bbox[3]

        url = f"{self.base_url}?dataType={dataType}&dataset={dataset}&zoomLevel={zoomLevel}&boundsSouthWestLat={boundsSouthWestLat}&boundsSouthWestLng={boundsSouthWestLng}&boundsNorthEastLat={boundsNorthEastLat}&boundsNorthEastLng={boundsNorthEastLng}&mapOptBndAcc={mapOptBndAcc}&mapOptMarkerGrouping={mapOptMarkerGrouping}"

        headers = {
            "Accept": "*/*",
            "Accept-Encoding": "gzip, deflate, br",
            "Accept-Language": "en-US,en;q=0.9,zh-CN;q=0.8,zh;q=0.7",
            "Content-Type": "application/json; charset=utf-8",
            "Datatheme": "au.gov.health.PHNLocator",
            "Map-Config": "fRd",
            "Origin": "https://maps.healthmap.com.au",
            "Referer": "https://maps.healthmap.com.au/",
            "Sec-Ch-Ua": "\"Google Chrome\";v=\"113\", \"Chromium\";v=\"113\", \"Not-A.Brand\";v=\"24\"",
            "Sec-Ch-Ua-Mobile": "?0",
            "Sec-Ch-Ua-Platform": "\"Windows\"",
            "Sec-Fetch-Dest": "empty",
            "Sec-Fetch-Mode": "cors",
            "Sec-Fetch-Site": "cross-site",
            "Time-Zone": "Australia/Sydney",
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) "
                          "Chrome/113.0.0.0 Safari/537.36",
            "X-Access-Token": "guest",
        }

        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                res = response.json()
                if res['success'] and len(res['gisBoundaries']['rows']) > 0:
                    nameOther = res['gisBoundaries']['rows'][0]['nameOther']
                    self.phn_memory[bbox_key] = nameOther
                    return nameOther
                else:
                    return None
            else:
                return None
        except Exception as e:
            print('Error: ', e)
            return None
