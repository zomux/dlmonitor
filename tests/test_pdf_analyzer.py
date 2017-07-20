import sys
sys.path.append(".")
from dlmonitor.analyzer import PDFAnalyzer
from argparse import ArgumentParser

if __name__ == '__main__':
    ap = ArgumentParser()
    ap.add_argument("path")
    args = ap.parse_args()

    print (PDFAnalyzer().run(args.path))
