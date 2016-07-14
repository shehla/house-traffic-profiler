import Queue
import statistics


class DelayController(object):
    def __init__(self, route_id, min_delay=30.0, max_delay=240.0, max_elements=5, THRESHOLD=3, STEP=30):
        self.route_id = route_id
        self.min_delay = min_delay
        self.max_delay = max_delay
        self.current_delay = min_delay
        self.queue = Queue()
        self.max_elements = max_elements
        self.THRESHOLD = THRESHOLD
        self.STEP = STEP

    def update_queue(travel_time):
        if self.queue.qsize() == self.max_elements:
            # remove the oldest record
            self.queue.get()
        # add the new record
        self.queue.put(travel_time)

    def adjust_delay(self):
        std_dev = statistics.pstdev(list(self.queue))
        mean = statistics.mean(list(self.queue))
        header = '*** DelayController:{0} mean:{1} std:{2} '.format(
            self.route_id,
            mean,
            std_dev,
        )
        if std_dev / mean * 100.0 > self.THRESHOLD:
            if self.current_delay - self.STEP >= self.min_delay:
                self.current_delay -= self.STEP
                header = '{0} HIGH ACTIVITY delay:{1}'.format(header, self.current_delay)
            else:
                header = '{0} MAXED out delay:{1}'.format(header, self.current_delay)

        if std_dev == 0.0:
            if self.current_delay + self.STEP <= self.max_delay:
                self.current_delay += self.STEP
                header = '{0} low activity delay:{1}'.format(header, self.current_delay)
            else:
                header = '{0} NO activity delay:{1}'.format(header, self.current_delay)
        print(header)
