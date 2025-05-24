from nyct_gtfs import NYCTFeed
import datetime, time
from flow import set_arrivals
import timeit
import logging

logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s %(levelname)s:%(message)s',
    filename='renderer.log',
    filemode='a'
)

def pull_data_to_flow(train_id, stop_id):
    while True:
        try:
            logging.info(f"Starting data fetch for train_id={train_id}, stop_id={stop_id}")
            arrivals=[]
            feeds = list(
                map(
                    lambda train: NYCTFeed(feed_specifier=train, fetch_immediately=False),
                    train_id
                )
            )
            for feed in feeds:
                feed.refresh()
                logging.info(f"Feed refreshed")
                trains = feed.filter_trips(headed_for_stop_id=stop_id)
                if trains:
                    for train in trains:
                        if train.departure_time> datetime.datetime.now():
                            arrivals.append([train.route_id, train.headsign_text.split('-')[0], train.departure_time])
                    logging.info(f"Found {len(trains)} trains for stop_id={stop_id}")
                else:
                    logging.info(f"No trains found for stop_id={stop_id}")
                    arrivals = [None, None]

            sorted_arrivals = sorted(arrivals, key=lambda x: x[2], reverse=False)
            logging.info(f"Sorted arrivals: {sorted_arrivals}")
            set_arrivals((sorted_arrivals + [None, None])[:2])
        except Exception as e:
            logging.error(f"Exception in pull_data_to_flow: {e}", exc_info=True)
        time.sleep(30)
