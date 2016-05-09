# import os, io
import argparse
from utils.run_scan import run_scan_setup
from utils.run_match import run_match

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('-m', dest='mode', default=None)
    args = parser.parse_args()
    if args.mode and args.mode == 'run_scan':
        print("Default: Running Scan Mode")
        run_scan_setup(1)
    elif args.mode == 'run_match':
        run_match()
    else:
        print("Mode %s not found" % args.mode)

"""
/Users/abarger/.pyenv/versions/cardscan2/lib/python2.7/site-packages/sqlalchemy/engine/default.py:463: SAWarning: Unicode type received non-unicode bind param value.
  param.append(processors[key](compiled_params[key]))
"""
