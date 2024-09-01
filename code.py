import requests
import datetime
def get_a_train_schedule(api_key):
    # URL for the MTA real-time feed
    MTA_URL = "https://api-endpoint.mta.info/Dataservice/mtagtfsfeeds/nyct%2Fgtfs-ace"

    headers = {
        'x-api-key': api_key
    }

    # Fetch data from MTA
    response = requests.get(MTA_URL, headers=headers)
    if response.status_code == 200:
        return response.content  # Return the raw content to be parsed later

a_train_data = get_a_train_schedule('https://data.ny.gov/resource/f462-ka72.json')

from google.transit import gtfs_realtime_pb2

def parse_gtfs_data(data, target_stop_id='A03S'):
    """
    Parse GTFS data to return information for a specific stop ID with readable timestamps.

    Args:
        data (bytes): The raw protobuf data from the GTFS feed.
        target_stop_id (str): The stop ID to filter for (default is '109').

    Returns:
        list: A list of trip updates for the specified stop ID with formatted timestamps.
    """
    feed = gtfs_realtime_pb2.FeedMessage()
    feed.ParseFromString(data)
    
    stop_updates = []

    for entity in feed.entity:
        if entity.HasField('trip_update'):
            trip_update = entity.trip_update
            
            for stop_time_update in trip_update.stop_time_update:
                if stop_time_update.stop_id == target_stop_id:
                    # Convert Unix timestamps to human-readable format
                    arrival_time = datetime.datetime.fromtimestamp(stop_time_update.arrival.time).strftime('%Y-%m-%d %H:%M:%S') if stop_time_update.HasField('arrival') else None
                    departure_time = datetime.datetime.fromtimestamp(stop_time_update.departure.time).strftime('%Y-%m-%d %H:%M:%S') if stop_time_update.HasField('departure') else None

                    stop_updates.append({
                        'trip_id': trip_update.trip.trip_id,
                        'route_id': trip_update.trip.route_id,
                        'stop_id': stop_time_update.stop_id,
                        'arrival': arrival_time,
                        'departure': departure_time
                    })
    
    return stop_updates

def find_closest_trains(stop_data):
    """
    Find the time differences and the two closest train times (arrival and departure) from now.

    Args:
        stop_data (list): A list of dictionaries containing trip updates for a specific stop ID with formatted timestamps.

    Returns:
        tuple: Two dictionaries with the closest train arrival and departure times from now.
    """
    current_time = datetime.datetime.now()
    time_diffs = []

    # Calculate time differences
    for entry in stop_data:
        if entry['arrival']:
            arrival_time = datetime.datetime.strptime(entry['arrival'], '%Y-%m-%d %H:%M:%S')
            time_diff = (arrival_time - current_time).total_seconds()

            if time_diff > 0:  # Only consider future trains
                time_diffs.append((time_diff, entry))

    # Sort the time differences to find the closest ones
    time_diffs.sort(key=lambda x: x[0])

    # Return the two closest train times based on time differences
    return time_diffs[:2] if time_diffs else []

# Example usage with previously fetched and parsed stop data
api_key = "YOUR_MTA_API_KEY"  # Replace with your actual API key
a_train_data = get_a_train_schedule(api_key)

if a_train_data:
    stop_data = parse_gtfs_data(a_train_data)
    closest_trains = find_closest_trains(stop_data)
    
    if closest_trains:
        print("The two closest trains are:")
        for time_diff, train in closest_trains:
            print(f"Trip ID: {train['trip_id']}, Route ID: {train['route_id']}, Arrival: {train['arrival']}, Departure: {train['departure']}, Time Difference: {time_diff} seconds")
    else:
        print("No upcoming trains found.")
else:
    print("Could not retrieve the A train schedule.")