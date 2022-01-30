# ac-clock
An IRL version of the Animal Crossing clock.

Currently really only works as a CLI with minimal stdout, since packaging as an application takes significant overhead.
Think of this as a "quick and dirty" implementation of the clock system with multiprocess synchronization to achieve the bell tower effect.

Note: This only works for mac as it requires `afplay`

How to create a packaged version:
1. `pip install -r requirements.txt`
2. `pyinstaller main.py --onefile`
3. To run, `./dist/main`, or give the main file to someone without Python
    Note, make sure that video_logs_default.json is in the same directory as main.

How to run straight from python file:
1. `pip install -r requirements.txt`
2. `python3 main.py`
