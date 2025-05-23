from nyct_gtfs import NYCTFeed
import datetime, time
from flow import set_arrivals
import timeit


def pull_data_to_flow(train_id, stop_id):
    while True:
        arrivals=[]
        feeds = list(
            map(
                lambda train: NYCTFeed(feed_specifier=train, fetch_immediately=False),
                train_id
            )
        )
        for feed in feeds:
            feed.refresh()
            trains = feed.filter_trips(headed_for_stop_id=stop_id)
            if trains:
                for train in trains:
                    if train.departure_time> datetime.datetime.now():
                        arrivals.append([train.route_id, train.headsign_text.split('-')[0], train.departure_time])
            else:
                arrivals = [None, None]

        sorted_arrivals = sorted(arrivals, key=lambda x: x[2], reverse=False)
        print(sorted_arrivals)
        set_arrivals((sorted_arrivals + [None, None])[:2])
        time.sleep(30)
