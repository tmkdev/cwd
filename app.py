#!/bin/bash/python
from cwd import *
from cwd_checker import AlarmProcessor
"""
Bottle server. Run this to launch system and use default bottle server. It will bring up a instance of checker.
"""

if __name__ == '__main__':
    run_event = threading.Event()
    run_event.set()

    app.run(host='0.0.0.0', port=5000)
    time.sleep(2)

    ap = AlarmProcessor(name='AlarmProcessor', kwargs={'run_event': run_event})
    ap.start()


    try:
        while 1:
            time.sleep(.5)
    except KeyboardInterrupt:
        logging.critical("Keyboard Interrupt. Closing Threads")
        run_event.clear()
        ap.join()
        logging.critical("Threads closed. Exiting.")
        exit(1)
