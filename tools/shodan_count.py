"""Shared, credential-safe Shodan Count client and atomic JSON helpers."""
import email.utils
import json
import os
from pathlib import Path
import re
import time
from datetime import datetime, timezone
import urllib.error
import urllib.parse
import urllib.request

def now():
    return datetime.now(timezone.utc).isoformat(timespec='seconds')


def cli_config_dir(home=None):
    """Same location/precedence as installed shodan.cli.settings; no CLI dependency."""
    home = home or Path.home()
    return home/'.shodan' if (home/'.shodan').exists() else home/'.config/shodan'


def load_key(config_dir=None):
    key = os.environ.get('SHODAN_API_KEY', '').strip()
    if not key:
        try:
            key = ((config_dir or cli_config_dir())/'api_key').read_text().strip()
        except OSError:
            raise ValueError('Shodan CLI is not initialized; configure it or set SHODAN_API_KEY') from None
    if not key:
        raise ValueError('Empty Shodan API key')
    return key


def slugify(value):
    return re.sub(r'[^a-z0-9]+', '-', value.lower()).strip('-')[:60]


def read(path):
    try:
        return json.loads(path.read_text(encoding='utf-8'))
    except (FileNotFoundError, json.JSONDecodeError):
        return None


def save(path, value):
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + '.tmp')
    temporary.write_text(json.dumps(value, ensure_ascii=False, indent=1) + '\n', encoding='utf-8')
    temporary.replace(path)


def facet_meta(values, total):
    covered = sum(v['count'] for v in values)
    return dict(values_returned=len(values), covered=covered, remainder=max(total-covered, 0))


def country_query(query, cc):
    # Do not treat a country token inside a quoted banner string as a filter.
    tokens = re.findall(r'"(?:\\.|[^"\\])*"|[^\s]+', query)
    return query if f'country:{cc}' in tokens else f'{query} country:{cc}'


def compatible(record, query, facets):
    return bool(record and record.get('collection_status') == 'ok'
                and record.get('dork') == query and record.get('requested_facets') == facets)


class CountError(Exception):
    def __init__(self, message, fatal=False):
        super().__init__(message)
        self.fatal = fatal


class RequestBudget(Exception):
    pass


class CountClient:
    def __init__(self, key, interval=1.1, max_requests=None, opener=urllib.request.urlopen,
                 sleep=time.sleep, clock=time.monotonic):
        self.key, self.interval, self.max_requests = key, interval, max_requests
        self.opener, self.sleep, self.clock = opener, sleep, clock
        self.requests, self.last_start = 0, None

    def count(self, query, facets):
        parameters = urllib.parse.urlencode(dict(key=self.key, query=query, facets=facets))
        url = 'https://api.shodan.io/shodan/host/count?' + parameters
        for attempt in range(3):
            if self.max_requests is not None and self.requests >= self.max_requests:
                raise RequestBudget()
            if self.last_start is not None:
                self.sleep(max(0, self.interval - (self.clock() - self.last_start)))
            self.last_start = self.clock()
            self.requests += 1
            retry_after = 0
            try:
                with self.opener(url, timeout=40) as response:
                    data = json.load(response)
                if not isinstance(data, dict) or data.get('error'):
                    raise CountError('API returned an error response')
                total = data.get('total')
                if type(total) is not int or total < 0 or not isinstance(data.get('facets', {}), dict):
                    raise CountError('Invalid Count response')
                for values in data.get('facets', {}).values():
                    if not isinstance(values, list) or any(not isinstance(v, dict)
                        or type(v.get('value')) not in (str, int) or type(v.get('count')) is not int
                        or v['count'] < 0 for v in values):
                        raise CountError('Invalid facet response')
                return data
            except urllib.error.HTTPError as exc:
                exc.close()
                # Never log URLs, exception reprs or response bodies containing a key.
                if exc.code in (401, 403):
                    raise CountError(f'HTTP {exc.code}: check API key and account permissions', fatal=True) from None
                error = f'HTTP {exc.code}'
                if exc.code != 429 and exc.code < 500:
                    raise CountError(error) from None
                value = exc.headers.get('Retry-After', '') if exc.headers else ''
                try:
                    retry_after = max(0, float(value))
                except ValueError:
                    try:
                        retry_after = max(0, email.utils.parsedate_to_datetime(value).timestamp()-time.time())
                    except (TypeError, ValueError, OverflowError):
                        pass
            except (urllib.error.URLError, TimeoutError, OSError):
                error = 'Network request failed'
            except (json.JSONDecodeError, UnicodeError):
                error = 'Invalid JSON response'
            except CountError as exc:
                error = str(exc)
            if attempt < 2:
                self.sleep(max(retry_after, 3 * (attempt + 1)))
        raise CountError(error)
