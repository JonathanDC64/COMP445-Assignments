import argparse
import get
import post
from urllib.parse import urlparse

#Help messages for httpc.py -help, httpc.py -get -help, httpc.py -post - help

HELP = """httpc is a curl-like application but supports HTTP protocol only.
Usage:
    httpc command [arguments]
The commands are:
    -get executes a HTTP GET request and prints the response.
    -post executes a HTTP POST request and prints the response.
    -help prints this screen."""
    
GET_HELP = """Usage: httpc.py -get [-v] [-h key:value] URL
Get executes a HTTP GET request for a given URL.
    -v Prints the detail of the response such as protocol, status, and headers.
    -h key:value Associates headers to HTTP Request with the format 'key:value'.
    -o output response to the specified file."""


POST_HELP = """Usage: httpc.py -post [-v] [-h key:value] [-d inline-data] [-f file] URL
Post executes a HTTP POST request for a given URL with inline data or
from file.
    -v Prints the detail of the response such as protocol, status, and headers.
    -h key:value Associates headers to HTTP Request with the format 'key:value'.
    -d string Associates an inline data to the body HTTP POST request.
    -f file Associates the content of a file to the body HTTP POST request.
    -o output response to the specified file.
    
Either [-d] or [-f] can be used but not both."""


#Arguments types for the command line argument parser
parser = argparse.ArgumentParser(add_help=False, usage='httpc.py (-get|-post) [-v] (-h "k:v")* [-d inline-data] [-f input_file] [-o output_file] URL')
parser.add_argument("-get", help="Executes a HTTP GET  request and prints the response.", action="store_true")
parser.add_argument("-post", help="Executes a HTTP POST request and prints the response.", action="store_true")
parser.add_argument("-help", help="Prints this screen.", action="store_true")
parser.add_argument("-v", help="Prints all the status, and its headers, then the contents of the response", action='store_true')
parser.add_argument("-h", help="Passes the headers value to your HTTP operation", action='append')
parser.add_argument("-d", help="Gives the user the possibility to associate the body of the HTTP Request with the inline data,")
parser.add_argument("-f", help="Send body data from file.")
parser.add_argument("-o", help="Write response to a file")
parser.add_argument("URL", help="Determines the targeted HTTP server. It could contain parameters of the HTTP operation.", default='', nargs='?')

#Get and validate the arguments
args = parser.parse_args()

#Input URL
url = args.URL

#Get data for post request if any exists
data = ''

#Get data from command line input
if args.d:
    data = args.d
#Get data from file
elif args.f:
    data = open(args.f).read()

#Output response to file if -o is specified    
output = None
if args.o:
    output = open(args.o,"w")
    
#Parse the input URL into their components
parsedurl = urlparse(url)

#URL protocol
scheme = parsedurl.scheme

#Host/Domain name
host = parsedurl.netloc

#Path of request
path = parsedurl.path

#Query parameters
query = parsedurl.query

#if there are query parameters, append them to the path for GET requests
if query:
    path = path + '?' + query

#Header options specified with -h (must be seperated with carriage return and new line)
header = ''
if args.h:
    header = '\r\n'.join(map(str,args.h))

#If the user inputed -help
help = args.help

#response object (type message)
response = None

#If the protocol of the url is not http or https, print error
if help == False and (scheme != 'http' and scheme != 'https'):
    parser.print_usage()
    print("URL must contain either http or https protocol")
#No post or get entered
elif help == False and args.get == False and args.post == False:
    parser.print_usage()
    print("You must specify either the -get or -post option")
else:
    #GET request
    if args.get:
        #If httpc.py -get -help
        if help:
            print(GET_HELP)
        else:
            response = get.get(host, path, header)
    #POST request
    elif args.post:
        #If httpc.py -post -help
        if help:
            print(POST_HELP)
        else:
            response = post.post(host, path, data, header)
    #If httpc.py -help print general help message
    elif help:
        parser.print_usage()
        print(HELP)    
    
    #Output the response
    if not help:
        #If -o is specified, output response to file
        if(args.o):
            #output verbose data
            if args.v:
                output.write(response.get_header() + "\r\n\r\n")
            output.write(response.get_body())
            output.close()
        #Output reponse to console
        else:
            #output verbose data
            if args.v:
                print(response.get_header())
            print(response.get_body())