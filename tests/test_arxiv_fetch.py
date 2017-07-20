import sys
sys.path.append(".")
from dlmonitor.sources.arxivsrc import ArxivSource

if __name__ == '__main__':
    src = ArxivSource()
    src.fetch_new()
