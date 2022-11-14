import functools
from typing import List

from nredarwin.webservice import CallingPoint, DarwinLdbSession, ServiceItem

from traintimes.models import DepartureJson

MINUTES_IN_DAY = 1440


def combine_timetables(timetable_one: List[DepartureJson], timetable_two: List[DepartureJson]) -> List[DepartureJson]:
    timetable_one_iterator = iter(timetable_one)
    timetable_two_iterator = iter(timetable_two)

    # Interleave the two timetables, in order of actual departure time
    final_timetable = []

    next_one = None
    next_two = None

    while True:
        next_one = next_one or next(timetable_one_iterator, None)
        next_two = next_two or next(timetable_two_iterator, None)

        # If both "next" items are None we've reached the end of both iterables
        if next_one is None and next_two is None:
            break
        elif next_one is None:
            # If "next_one" is None, we've reached the end of the first iterable, just add items from the second
            final_timetable.append(next_two)
            next_two = None
        elif next_two is None:
            # If "next_two" is None, we've reached the end of the second iterable, just add items from the first
            final_timetable.append(next_one)
            next_one = None
        else:
            # Compare the actual departure times, inserting the soonest
            from_one = to_minutes(get_actual_from_time(next_one))
            from_two = to_minutes(get_actual_from_time(next_two))

            delta = from_one - from_two
            # Check for huge delta - this occurs near midnight as times roll over
            delta = handle_delta_near_midnight(delta)

            if delta < 0:
                final_timetable.append(next_one)
                next_one = None
            else:
                final_timetable.append(next_two)
                next_two = None

    return final_timetable


def handle_delta_near_midnight(original_delta: int) -> int:
    if original_delta < -700:
        return original_delta + MINUTES_IN_DAY
    elif original_delta > 700:
        return original_delta - MINUTES_IN_DAY
    else:
        return original_delta


def sort_timetable_comparison_function(departure_a: DepartureJson, departure_b: DepartureJson):
    minutes_a = to_minutes(get_actual_to_time(departure_a))
    minutes_b = to_minutes(get_actual_to_time(departure_b))
    minutes_delta = minutes_a - minutes_b
    # print("          A     B       A     B     D     D")
    # print("COMPARE", get_actual_to_time(departure_a), get_actual_to_time(departure_b),
    #       f"{minutes_a:5} {minutes_b:5} {minutes_delta:5} {handle_delta_near_midnight(minutes_delta):5}")

    return handle_delta_near_midnight(minutes_delta)


def sort_timetable(timetable: List[DepartureJson]) -> List[DepartureJson]:
    return sorted(timetable, key=functools.cmp_to_key(sort_timetable_comparison_function))


def get_timetable(darwin_client: DarwinLdbSession, destination) -> List[DepartureJson]:
    timetable = darwin_client.get_station_board("ECR", destination_crs=destination)
    services: List[ServiceItem] = timetable.train_services

    departures_json: List[DepartureJson] = []
    for service in services:
        departures_json.append(service_to_json(destination, service))

    # Sort the services based on estimated arrival time
    departures_json = sort_timetable(departures_json)

    return departures_json


def process_calling_points(destination_crs: str,
                           departure_json: DepartureJson,
                           subsequent_stops: List[CallingPoint]) -> None:
    for stop in subsequent_stops:
        if stop.crs != destination_crs:
            continue

        departure_json.to_crs = stop.crs
        departure_json.to_name = stop.location_name
        departure_json.to_scheduled_time = stop.st
        departure_json.to_estimated_time = stop.et or stop.at
        break


def service_to_json(destination_crs: str, service_item: ServiceItem) -> DepartureJson:
    departure_json = DepartureJson(
        service_item.std,
        service_item.etd,
        service_item.platform,
        service_item.length)

    subsequent_calling_point_lists: List = getattr(service_item, "subsequent_calling_point_lists")
    process_calling_points(destination_crs,
                           departure_json,
                           subsequent_calling_point_lists[0].calling_points)

    return departure_json


def get_actual_to_time(departure: DepartureJson) -> str:
    return get_actual_estimated_time(departure.to_scheduled_time, departure.to_estimated_time)


def get_actual_from_time(departure: DepartureJson) -> str:
    return get_actual_estimated_time(departure.from_scheduled_time, departure.from_estimated_time)


def to_minutes(time_string: str) -> int:
    time_parts = time_string.split(":")
    try:
        return (60 * int(time_parts[0])) + int(time_parts[1])
    except ValueError:
        return 0


def get_actual_estimated_time(scheduled, estimated) -> str:
    if estimated is None or estimated.lower() in ["on time", "cancelled", "delayed"]:
        return scheduled
    else:
        return estimated
