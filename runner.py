import sys

from card_maker.card_maker import csv_reader

if __name__ == "__main__":
    batch = int(sys.argv[1])
    print(batch)
    csv_reader(batch)
