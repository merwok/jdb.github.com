# trivial_concurrent.py
from twisted.internet import reactor
from twisted.internet.defer import DeferredList, inlineCallbacks
from twisted.web.client import getPage
from lxml.html import fromstring

url = 'http://twistedmatrix.com'

@inlineCallbacks   # 1
def title( url ):
     html = yield getPage( url )            # 2 & 3 
     print fromstring( html ).xpath( '/html/head/title' )[0].text  # 4

DeferredList( 
     [ title( url ) for _ in range(30) ] 
  ).addCallback( lambda _:reactor.stop() )

reactor.run()
