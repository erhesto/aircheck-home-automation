import requests
import logging
import itertools

from filelock import FileLock

import settings
from utils import handle_exceptions
from datatypes import Coordinates, PollutionType, PollutionTypeDangerLevel


# global headers accurate for all requests
headers = {'Accept': 'application/json', 'apikey': settings.AIRLY_API_KEY}

# TODO: Get coordinates from some api and pass as variable
coordinates = Coordinates(latitude=settings.LATITUDE, longitude=settings.LONGITUDE)



@handle_exceptions
def get_nearest_installations(coordinates: Coordinates, max_distance: int, max_results: int):
    params =  {
        'lat': coordinates.latitude, 
        'lng': coordinates.longitude, 
        'maxDistanceKM': max_distance,
        'maxResults': max_results,
    }
     
    return requests.get(f'{settings.API_URL}/installations/nearest', params=params, headers=headers)


@handle_exceptions
def get_measurement(installation_id: int):
    params = {
        'installationId': installation_id,
    }
    
    return requests.get(f'{settings.API_URL}/measurements/installation', params=params, headers=headers)


def get_pollution_types(measure):
    for m in measure:
        name, value = m['name'], m['value']
        if name in PollutionTypeDangerLevel.__members__.keys():
            yield PollutionType(name, value)


def check_status() -> bool:
    installations = get_nearest_installations(
        coordinates, 
        max_distance=settings.MAX_DISTANCE_KM, 
        max_results=settings.MAX_RESULTS
    )
    installation_ids = (installation['id'] for installation in installations)
    measurements = (get_measurement(id_) for id_ in installation_ids)  # TODO: maybe async? 
    pollution_measures = (get_pollution_types(measurement['current']['values']) for measurement in measurements)
    return all(pollution_measure.is_acceptable() for pollution_measure in itertools.chain.from_iterable(pollution_measures))


def main():
    all_is_good = check_status()
    
    with FileLock(f'{settings.OUTPUT_PATH}.lock') as lock:
        with open(settings.OUTPUT_PATH, 'w') as out_file:
            if not all_is_good or settings.DEBUG:
                out_file.write('1')


if __name__ == '__main__':
    main()

