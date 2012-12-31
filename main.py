"""
Manages the 

twistd -y server.py -l protobuf.log
"""
import os
import json

from twisted.web.server import Site, NOT_DONE_YET
from twisted.web.resource import Resource
from twisted.internet import reactor
from twisted.internet.task import deferLater

import cgi
import urllib2

class BaseHandler(Resource):
    def validate_apple_respose(self, receipt_info, request):
        """
        Apple will return a json 
        """
        validation = dict()
        validation['valid_receipt'] = True
        if receipt_info['status'] != 0:
            validation['valid_receipt'] = False
            
        request.write(json.dumps(validation))
        request.finish()

class TestPage(Resource):
    """
    Page Visible to users to test receipts
    """
    def render_GET(self, request):
        return '<html><body><textarea name="receipt" rows=6 cols=40></textarea></body></html>'

    def render_POST(self, request):
        return ''
    
class ValidateReceipt(BaseHandler):
    """
    Production Receipt verification
    """       
    def render_POST(self, request):
        receipt_info = json.loads(request.content.read())
        d = deferLater(reactor, 1, self.send_receipt_to_apple, receipt_info)
        d.addCallback(self.validate_apple_respose, request)
        return NOT_DONE_YET
        
    def send_receipt_to_apple(self, receipt_info):
        """
        Send the data to apple
        """
        request = urllib2.Request('https://sandbox.itunes.apple.com/verifyReceipt')
        request.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(request, json.dumps(receipt_info))
        return json.loads(response.read())

class Sandbox(BaseHandler):
    """
    Used to test in-app-purchasing
    For info
    http://developer.apple.com/library/ios/#documentation/NetworkingInternet/Conceptual/StoreKitGuide/DevelopingwithStoreKit/DevelopingwithStoreKit.html#//apple_ref/doc/uid/TP40008267-CH103-SW1
    """
    def render_POST(self, request):
        receipt_info = json.loads(request.content.read())
        d = deferLater(reactor, 1, self.send_receipt_to_apple, receipt_info)
        d.addCallback(self.validate_apple_respose, request)
        return NOT_DONE_YET
        
    def send_receipt_to_apple(self, receipt_info):
        """
        Send the data to apple
        """
        request = urllib2.Request('https://sandbox.itunes.apple.com/verifyReceipt')
        request.add_header('Content-Type', 'application/json')
        response = urllib2.urlopen(request, json.dumps(receipt_info))
        return json.loads(response.read())
    
def main():
    """
    Main reactor that is constantly running listening on the port 
    on an evn variable Heroku Sets
    
    * Test Page is a way to copy and paste receipt info into a text area
    * Sandbox is for games in productions and not yet released
    """
    port = int(os.environ.get('PORT', 8880))
    root = Resource()
    root.putChild('', TestPage())
    root.putChild('sandbox', Sandbox())
    root.putChild('live', ValidateReceipt()), 
    factory = Site(root)
    reactor.listenTCP(port, factory)
    reactor.run()
    
if __name__ == '__main__':
    main()