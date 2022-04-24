from requests import Response
from rich import print 
from constant import COLOR

def print_response(response:Response):
    if response.status_code != 200:
        COLOR = 'red'
        print()
