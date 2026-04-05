import sys
from os import getcwd, path
from argparse import Namespace

sys.path.insert(0, getcwd())

import ai_imager.web_interface as web

web.app_data_dir = path.join(getcwd(), "contents")

args = Namespace(
    key=None,
    key_path=None,
    cookie_file=None,
    debug=False,
    thread=True,
    host=True,
)

web.API(
    args=args,
    port=5000,
    debug=False,
    host=True,
    threaded=True,
)
