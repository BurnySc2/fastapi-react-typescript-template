import os
import random
import signal
import subprocess
import time
from pathlib import Path
from typing import Optional

import pytest
from pytest_benchmark.fixture import BenchmarkFixture
from seleniumbase import BaseCase

# see https://github.com/seleniumbase/SeleniumBase
# https://seleniumbase.io/

WEBSITE_IP = 'http://localhost'
WEBSITE_PORT = f'{random.randint(10_000, 65_535)}'
WEBSITE_ADDRESS = f'{WEBSITE_IP}:{WEBSITE_PORT}'
WEBSERVER_PROCESS: Optional[subprocess.Popen] = None


def generate_css_file():
    frontend_folder = Path(__file__).parent.parent / 'frontend'
    index_css_path = frontend_folder / 'src' / 'index.css'

    # If it already exists, skip generation of file
    # pylint: disable=R1732
    if index_css_path.is_file():
        return

    # Start compilation of index.css
    _tailwind_css_process = subprocess.Popen(['npm', 'run', 'tailwind:prod'], cwd=frontend_folder)

    # Wait for tailwindcss to compile index.css file
    wait_seconds = 0
    while not index_css_path.is_file():
        wait_seconds += 1
        if wait_seconds > 30:
            break
        time.sleep(1)


def start_frontend_dev_server():
    # pylint: disable=W0603
    global WEBSERVER_PROCESS

    env = os.environ.copy()
    # Set port for dev server
    env['PORT'] = WEBSITE_PORT
    # Don't open frontend in browser
    env['BROWSER'] = 'none'

    # pylint: disable=R1732
    generate_css_file()

    frontend_folder = Path(__file__).parent.parent / 'frontend'
    WEBSERVER_PROCESS = subprocess.Popen(['npx', 'react-scripts', 'start'], cwd=frontend_folder, env=env)

    # Give it some time to create dev server
    time.sleep(3)


# pylint: disable=W0613
def setup_module(_module):
    # pylint: disable=W0603
    """
    See https://docs.pytest.org/en/6.2.x/xunit_setup.html
    """
    start_frontend_dev_server()


# pylint: disable=W0613
def teardown_module(_module):
    # pylint: disable=W0603
    global WEBSERVER_PROCESS
    """ teardown any state that was previously setup with a call to
    setup_class.
    """
    if WEBSERVER_PROCESS is not None:
        time.sleep(0.1)
        os.kill(WEBSERVER_PROCESS.pid, signal.SIGTERM)
        time.sleep(0.1)
        if WEBSERVER_PROCESS.poll() is None:
            os.kill(WEBSERVER_PROCESS.pid, signal.SIGKILL)
        time.sleep(0.1)

    WEBSERVER_PROCESS = None


class MyTestClass(BaseCase):
    def test_basic_site_display(self):
        """ Check if HOME site is visible """
        self.open(WEBSITE_ADDRESS)
        self.assert_text('some text')

    # def test_shows_todos(self):
    #     """ Check if the to-do site is visible """
    #     self.open(WEBSITE_ADDRESS)
    #     self.click("#changedata")
    #     self.assert_text("Unable to connect to server")

    # TODO fix test by adding offline-functionality so that it adds items even though server is not responding, or include starting server in e2e tests
    # def test_add_todo(self):
    #     """ Add a new to-do entry """
    #     self.open(WEBSITE_ADDRESS)
    #     self.click("#todo")
    #     test_text = "my amazing test todo text"
    #     self.write("#newTodoInput", test_text)
    #     self.click("#submit1")
    #     self.assert_text(test_text)

    # def test_example(self):
    #     url = "https://store.xkcd.com/collections/posters"
    #     # Go to url
    #     self.open(url)
    #     # Type in input field "xkcd book"
    #     self.type('input[name="q"]', "xkcd book")
    #     # Click the search icon to start searching
    #     self.click('input[value="Search"]')
    #     # Assert that there is a header with class "h3" which has text: "xkcd: volume 0"
    #     self.assert_text("xkcd: volume 0", "h3")
    #     # Go to new url
    #     self.open("https://xkcd.com/353/")
    #     self.assert_title("xkcd: Python")
    #     self.assert_element('img[alt="Python"]')
    #     # Click on <a> element with rel="license"
    #     self.click('a[rel="license"]')
    #     # Assert that there is this text on the website visible
    #     self.assert_text("free to copy and reuse")
    #     # Click go_back
    #     self.go_back()
    #     # Click the "About" link
    #     self.click_link("About")
    #     # Assert that there is a header with class "h2" which has text: "xkcd.com"
    #     self.assert_exact_text("xkcd.com", "h2")


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
        self.assert_text('some text')

    def test_bench_basic_site_display(self):
        """ Benchmark how fast the site loads """
        self.benchmark(self.basic_site_display)

    # def add_todo(self):
    #     """ Add a new to-do entry """
    #     self.open(WEBSITE_ADDRESS)
    #     self.click("#todo")
    #     test_text = "my amazing test todo text"
    #     self.write("#newTodoInput", test_text)
    #     self.click("#submit1")
    #     self.assert_text(test_text)

    # def test_bench_add_todo(self):
    #     """ Benchmark how fast a to-do can be added """
    #     self.benchmark(self.add_todo)
