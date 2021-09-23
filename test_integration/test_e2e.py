import os
import signal
import time
from typing import Optional, Set

import pytest
from loguru import logger
from pytest_benchmark.fixture import BenchmarkFixture

# see https://github.com/seleniumbase/SeleniumBase
# https://seleniumbase.io/
from seleniumbase import BaseCase

from test_integration.tester_helper import find_next_free_port, get_website_address, start_frontend_dev_server

# Set in setup_module()
WEBSITE_ADDRESS = ''
# Remember which node processes to close
NEWLY_CREATED_NODE_PROCESSES: Set[int] = set()


def setup_module():
    # pylint: disable=W0603
    global WEBSITE_ADDRESS
    """
    See https://docs.pytest.org/en/6.2.x/xunit_setup.html
    """
    port = find_next_free_port()
    WEBSITE_ADDRESS = get_website_address(port)
    start_frontend_dev_server(port, NEWLY_CREATED_NODE_PROCESSES)


def teardown_module():
    # Stop frontend server

    # Soft kill
    for pid in NEWLY_CREATED_NODE_PROCESSES:
        logger.info(f'Killing {pid}')
        os.kill(pid, signal.SIGTERM)
    time.sleep(1)

    # Force kill
    for pid in NEWLY_CREATED_NODE_PROCESSES:
        logger.info(f'Force killing {pid}')
        try:
            os.kill(pid, signal.SIGKILL)
        except ProcessLookupError:
            pass


class MyTestClass(BaseCase):
    def test_basic_site_display(self):
        """ Check if HOME site is visible """
        self.open(WEBSITE_ADDRESS)
        self.assert_text('Hello world!')

    def test_shows_todos(self):
        """ Check if the to-do site is visible """
        self.open(WEBSITE_ADDRESS)
        self.click('#todo')
        self.assert_text('Unable to connect to server - running local mode')

    def test_add_todo(self):
        """ Add a new to-do entry """
        self.open(WEBSITE_ADDRESS)
        self.click('#todo')
        self.assert_text('Unable to connect to server - running local mode')
        test_text = 'my amazing test todo text'
        self.write('#newTodoInput', test_text)
        self.click('#submit1')
        self.assert_text(test_text)

    def test_example(self):
        url = 'https://store.xkcd.com/collections/posters'
        # Go to url
        self.open(url)
        # Type in input field "xkcd book"
        self.type('input[name="q"]', 'xkcd book')
        # Click the search icon to start searching
        self.click('input[value="Search"]')
        # Assert that there is a header with class "h3" which has text: "xkcd: volume 0"
        self.assert_text('xkcd: volume 0', 'h3')
        # Go to new url
        self.open('https://xkcd.com/353/')
        self.assert_title('xkcd: Python')
        self.assert_element('img[alt="Python"]')
        # Click on <a> element with rel="license"
        self.click('a[rel="license"]')
        # Assert that there is this text on the website visible
        self.assert_text('free to copy and reuse')
        # Click go_back
        self.go_back()
        # Click the "About" link
        self.click_link('About')
        # Assert that there is a header with class "h2" which has text: "xkcd.com"
        self.assert_exact_text('xkcd.com', 'h2')


class MyBenchClass(BaseCase):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.benchmark: Optional[BenchmarkFixture] = None

    @pytest.fixture(autouse=True)
    def setup_benchmark(self, benchmark):
        """
        Assign the benchmark to a class variable
        For more info see https://pytest-benchmark.readthedocs.io/en/latest/usage.html
        https://github.com/ionelmc/pytest-benchmark/blob/master/tests/test_with_testcase.py
        """
        self.benchmark = benchmark

    def basic_site_display(self):
        """ Check if HOME site is visible """
        self.open(WEBSITE_ADDRESS)
        self.assert_text('Hello world!')

    def test_bench_basic_site_display(self):
        """ Benchmark how fast the site loads """
        self.benchmark(self.basic_site_display)

    def add_todo(self):
        """ Add a new to-do entry """
        self.open(WEBSITE_ADDRESS)
        self.click('#todo')
        self.assert_text('Unable to connect to server - running local mode')
        test_text = 'my amazing test todo text'
        self.write('#newTodoInput', test_text)
        self.click('#submit1')
        self.assert_text(test_text)

    def test_bench_add_todo(self):
        """ Benchmark how fast a to-do can be added """
        self.benchmark(self.add_todo)


if __name__ == '__main__':
    setup_module()
    teardown_module()
