# trivial_sequential.py
from lxml.html import parse
from urllib2 import urlopen

url = 'http://twistedmatrix.com' 

def title( url ):
    print parse( urlopen( url )).xpath( '/html/head/title' )[0].text

# let's download the page 30 times
[ title(url) for i in range(30) ]           # why a list comprehension? 
                                            # this will be clarified below ...


