from csv import QUOTE_NONE, unix_dialect, writer
from collections import defaultdict
from datetime import datetime as dt

from .settings import BASE_DIR, RESULTS

FILE_NAME = 'status_summary_{}.csv'
TIME_FORMAT = r'%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:
    counter = defaultdict(int)

    def open_spider(self, spider):
        self.results = BASE_DIR / RESULTS
        self.results.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        self.counter[item['status']] += 1
        return item

    def close_spider(self, spider):
        with open(
            self.results / FILE_NAME.format(dt.now().strftime(TIME_FORMAT)),
            'w'
        ) as f:
            writer(f, dialect=unix_dialect, quoting=QUOTE_NONE).writerows([
                ('Status', 'Number of PEPs'),
                *self.counter.items(),
                ('Total', sum(self.counter.values()))
            ])
