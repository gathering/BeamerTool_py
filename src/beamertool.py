
import json
import argparse as ap
import UnicornAPI.api as api
import UnicornAPI.Auth


def main():
    parser=ap.ArgumentParser()
    parser.add_argument('offline', help="Offlinemode ", nargs=3)
    parser.add_argument('test', help="test auth and pull data", nargs=1)
    parser.add_argument('createshow', help="Creates a new show", nargs=1)
    args=parser.parse_args()
    print(args)

def authenitcate():
    return;

# do some work
def getCompos():

    return api.getComposFromUnicorn();


def parseCompos():
    return

def test():


if __name__=="__main__":
    main()