from csv import unix_dialect, writer
from collections import Counter
from datetime import datetime as dt
from pathlib import Path

BASE_DIR = Path(__file__).absolute().parent.parent
RESULTS = 'results'
RESULTS_DIR = BASE_DIR / RESULTS
FILE_NAME = 'status_summary_{}.csv'
TIME_FORMAT = r'%Y-%m-%d_%H-%M-%S'


class PepParsePipeline:
    def open_spider(self, spider):
        self.counter = Counter()
        self.results = BASE_DIR / RESULTS
        self.results.mkdir(exist_ok=True)
        # RESULTS_DIR.mkdir(exist_ok=True)

    def process_item(self, item, spider):
        self.counter.update((item['status'],))
        return item

    def close_spider(self, spider):
        with open(
            self.results / FILE_NAME.format(dt.now().strftime(TIME_FORMAT)),
            'w'
        ) as f:
            writer(f, dialect=unix_dialect).writerows([
                ('Status', 'Number of PEPs'),
                *self.counter.items(),
                ('Total', sum(self.counter.values()))
            ])
