import logging
import pprint

from linkedin_jobs_scraper import LinkedinScraper
from linkedin_jobs_scraper.events import Events, EventData, EventMetrics
from linkedin_jobs_scraper.query import Query, QueryOptions, QueryFilters
from linkedin_jobs_scraper.filters import TimeFilters, TypeFilters

from data_processing import stats, process_data

# Change root logger level (default is WARN)
logging.basicConfig(level=logging.INFO)


# Fired once for each successfully processed job
def on_data(data: EventData):
    # print(f'[ON_DATA] - {data.title} - {data.company} - {data.date} - {data.place} - data link: {data.link} - '
    #       f'{data.insights}  - company link: {data.company_link} - description: {len(data.description)}')
    process_data(data)


# Fired once for each page (25 jobs)
def on_metrics(metrics: EventMetrics):
    print('[ON_METRICS]', str(metrics))


def on_error(error):
    print('[ON_ERROR]', error)


def on_end():
    print('[ON_END]')


scraper = LinkedinScraper(
    chrome_executable_path='./chromedriver',  # Custom Chrome executable path (e.g. /foo/bar/bin/chromedriver)
    chrome_options=None,  # Custom Chrome options here
    headless=True,  # Overrides headless mode only if chrome_options is None
    max_workers=1,  # How many threads will be spawned to run queries concurrently (one Chrome driver for each thread)
    slow_mo=1,  # Slow down the scraper to avoid 'Too many requests 429' errors (in seconds)
    page_load_timeout=30  # Page load timeout (in seconds)
)

# Add event listeners
scraper.on(Events.DATA, on_data)
scraper.on(Events.ERROR, on_error)
scraper.on(Events.END, on_end)

queries = [
    Query(
        query='Backend Engineer',
        options=QueryOptions(
            locations=['Spain'],
            apply_link=True,  # Try to extract apply link (easy applies are skipped). Default to False.
            limit=400,
            filters=QueryFilters(
                relevance=None,
                time=TimeFilters.ANY,
                type=[TypeFilters.FULL_TIME, TypeFilters.INTERNSHIP],
                experience=None,
                remote=None
            )
        )
    ),
]

scraper.run(queries)
with open('job_stats_be_engineer_spain_400.json', 'w') as f:
    pp = pprint.PrettyPrinter(indent=4, stream=f)
    pp.pprint(stats)
