import Queue
import time
import statistics


class DelayController(object):
    def __init__(self, route_id, min_delay=30.0, max_delay=240.0, max_elements=5, THRESHOLD=3, STEP=30):
        self.route_id = route_id
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.current_delay = min_delay
        self.queue = Queue.Queue()
        self.max_elements = max_elements
        self.THRESHOLD = THRESHOLD
        self.run_at = time.time()

    #def is_time_to_run(self):
    #    if time.time() >= self.run_at:
    #        time_in_mins = get_time(route['from'], route['to'], model)
    #        self.update_queue(time_in_mins)
    #        self.run_at += self.current_delay
    #        return True

    def update_queue(self, travel_time):
        if self.queue.qsize() == self.max_elements:
            # remove the oldest record
            self.queue.get()
        # add the new record
        self.queue.put(travel_time)
        self.adjust_delay()

    def adjust_delay(self):
        std_dev = statistics.pstdev(list(self.queue.queue))
        mean = statistics.mean(list(self.queue.queue))
        header = '*** DelayController:{0} mean:{1} std:{2} '.format(
            self.route_id,
            mean,
            std_dev,
        )
        if std_dev / mean * 100.0 > self.THRESHOLD:
            if self.current_delay / 2 >= self.min_delay:
                self.current_delay /= 2.0
                header = '{0} HIGH ACTIVITY delay:{1}'.format(header, self.current_delay)
            else:
                self.current_delay = self.min_delay
                header = '{0} MAXED out delay:{1}'.format(header, self.current_delay)

        if std_dev == 0.0:
            if self.current_delay * 2.0 <= self.max_delay:
                self.current_delay *= 2.0
                header = '{0} low activity delay:{1}'.format(header, self.current_delay)
            else:
                self.current_delay = self.max_delay
                header = '{0} NO activity delay:{1}'.format(header, self.current_delay)
        print(header)
