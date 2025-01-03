import argparse
from datetime import datetime

def reformat_date(date_string):
    date_object = datetime.strptime(date_string, '%d/%m/%Y')
    return date_object.strftime('%Y-%m-%dT%H:%M:%SZ')

def main(start, end):
    if start != None:
        print("Argument 1:", reformat_date(start))
    if end != None:
        print("Argument 2:", reformat_date(end))

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="""Create models for users
    Ex. python test.py -s 19/03/2024 -e 19/07/2024""")
    parser.add_argument("-s", "--start_date", type=str, help="Start Date ex. '19/03/2024'")
    parser.add_argument("-e", "--end_date", type=str, help="End Date ex. '19/07/2024'")
    args = parser.parse_args()
    main(args.start_date, args.end_date)