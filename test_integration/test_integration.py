import os
import signal
import time
from pathlib import Path
from typing import Set

from loguru import logger

# see https://github.com/seleniumbase/SeleniumBase
# https://seleniumbase.io/
from seleniumbase import BaseCase

from test_integration.tester_helper import (
    find_next_free_port,
    get_website_address,
    remove_leftover_files,
    start_backend_dev_server,
    start_frontend_dev_server,
    start_mongodb,
    start_postgres,
)

# Set in setup_module()
WEBSITE_ADDRESS = ''
# Remember which node processes to close
NEWLY_CREATED_PROCESSES: Set[int] = set()
CREATED_FILES: Set[Path] = set()


class MyTestClass(BaseCase):
    # pylint: disable=R0201
    def setup_method(self, _method):
        """ setup any state tied to the execution of the given method in a
        class.  setup_method is invoked for every test method of a class.
        """
        # pylint: disable=W0603
        global WEBSITE_ADDRESS
        """
        See https://docs.pytest.org/en/6.2.x/xunit_setup.html
        """
        free_frontend_port = find_next_free_port()
        free_backend_port = find_next_free_port(exclude_ports={free_frontend_port})
        WEBSITE_ADDRESS = get_website_address(free_frontend_port)
        start_frontend_dev_server(
            free_frontend_port,
            NEWLY_CREATED_PROCESSES,
            backend_proxy=f'http://localhost:{free_backend_port}',
        )
        start_backend_dev_server(free_backend_port, NEWLY_CREATED_PROCESSES, CREATED_FILES)
        start_mongodb()
        start_postgres()

    # pylint: disable=R0201
    def teardown_method(self, _method):
        """ teardown any state that was previously setup with a setup_method
        call.
        """
        # Stop frontend + backend server

        # Soft kill
        for pid in NEWLY_CREATED_PROCESSES:
            logger.info(f'Killing {pid}')
            os.kill(pid, signal.SIGTERM)
        time.sleep(1)

        # Force kill
        for pid in NEWLY_CREATED_PROCESSES:
            logger.info(f'Force killing {pid}')
            try:
                os.kill(pid, signal.SIGKILL)
            except ProcessLookupError:
                pass
        NEWLY_CREATED_PROCESSES.clear()

        # Remove files created by test
        remove_leftover_files(CREATED_FILES)
        CREATED_FILES.clear()

    def test_add_todo(self):
        """ Add a new to-do entry """
        self.open(WEBSITE_ADDRESS)
        self.assert_text('Hello world!')
        self.click('#todo')
        self.assert_text_not_visible('Unable to connect to server - running local mode')
        test_text = 'my amazing test todo text'
        self.assert_text_not_visible(test_text)
        self.write('#newTodoInput', test_text)
        self.click('#submit1')
        self.assert_text(test_text)
        self.assert_text_not_visible('Unable to connect to server - running local mode')

    def test_add_todo2(self):
        """ Add a new to-do entry, same as above """
        self.open(WEBSITE_ADDRESS)
        self.assert_text('Hello world!')
        self.click('#todo')
        self.assert_text_not_visible('Unable to connect to server - running local mode')
        test_text = 'my amazing test todo text'
        self.assert_text_not_visible(test_text)
        self.write('#newTodoInput', test_text)
        self.click('#submit1')
        self.assert_text(test_text)
        self.assert_text_not_visible('Unable to connect to server - running local mode')


if __name__ == '__main__':
    test = MyTestClass()
    test.setup_method('')
    test.test_add_todo()
    test.teardown_method('')
