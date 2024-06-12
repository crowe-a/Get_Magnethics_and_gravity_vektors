import numpy as np
import json
from geomag import geomag
import datetime

def main(k):
    start_time = datetime.datetime.now()
    
    def calculate_magnetic_field(latitude, longitude, altitude):
        gm = geomag.GeoMag()
        mag_field = gm.GeoMag(latitude, longitude, altitude)
        return {
            'x': mag_field.bx,
            'y': mag_field.by,
            'z': mag_field.bz,
            'total_intensity': mag_field.bh,
            'declination': mag_field.dec,
            'inclination': mag_field.dip
        }

    def yercekimi_vetor(latitude, longitude, altitude):
        a = 6378137.0
        f = 1 / 298.257223563
        b = a * (1 - f)
        R = np.sqrt(latitude**2 + longitude**2 + altitude**2)
        G = 6.67430e-11
        M = 5.9722e24
        g = G * M / R**2
        g_vector = -g * np.array([latitude, longitude, altitude]) / R
        return g_vector

    # Koordinatları ve yükseklikleri tanımla
    latitude_start, latitude_end = -90, 90
    longitude_start, longitude_end = -180, 180
    altitude = 1200

    data = {}
    index = 0
    flag = 0
    for lat in np.arange(latitude_start, latitude_end, 0.000449 * k):  # 50 metre aralık için yaklaşık 0.000449 derece
        for lon in np.arange(longitude_start, longitude_end, 0.000449 * k):
            mag_field = calculate_magnetic_field(lat, lon, altitude)
            gravity_vector = yercekimi_vetor(lat, lon, altitude)
            
            data[str(index)] = [
                (np.linalg.norm(gravity_vector), gravity_vector[0], gravity_vector[1], gravity_vector[2]),
                (mag_field['total_intensity'], mag_field['x'], mag_field['y'], mag_field['z'])
            ]
            index += 1
        flag += 1
        print(flag)

    # JSON dosyasına yaz
    with open('gravity_magnetic_data3.json', 'w') as f:
        json.dump(data, f, indent=4)  # Pretty-print JSON with an indent of 4 spaces,intend=4 her kayıttan sonra bi alt satırdan devam ettiriyor.
        stop_time = datetime.datetime.now() - start_time
        print(stop_time)

main(1000)
