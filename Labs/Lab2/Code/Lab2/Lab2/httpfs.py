import argparse
import http_server

parser = argparse.ArgumentParser(add_help=False, usage=' httpfs.py [-v] [-p PORT] [-d PATH-TO-DIR]')
parser.add_argument("-v", help="Prints debugging messages.", action='store_true')
parser.add_argument("-p", help="Specifies the port number that the server will listen and serve at.")
parser.add_argument("-d", help="Specifies the directory that the server will use to read/write requested files. Default is the current directory when launching the application.")

#Get and validate the arguments
args = parser.parse_args()

verbose = args.v

port = http_server.HTTP_PORT

if args.p:
    port = int(args.p)
    
directory = http_server.ROOT_DIRECTORY

if args.d:
    directory = args.d


http_server.run_server(http_server.LOCALHOST, port, verbose, directory)