import os
import sys
import redis
import json
import logging

from tornado.web import RequestHandler, asynchronous
from tornado import httpclient, gen

redis_url  = os.getenv('REDISTOGO_URL', 'redis://localhost:6379')
redis_pool = redis.from_url(redis_url)

log = logging.getLogger('tornado.general')

class MainHandler(RequestHandler):
    @asynchronous
    @gen.engine
    def post(self, game_name):
        """
        Get the json data and send it to apple to be verified
        """       
        log.warn('Verifying receipt')
        content = json.loads(self.request.body)
        
        header  = {'Content-Type' : 'application/json'}
        
        request = httpclient.HTTPRequest('https://sandbox.itunes.apple.com/verifyReceipt',
                                         method='POST',
                                         headers=header,
                                         body=json.dumps(content))
        
        http_client = httpclient.AsyncHTTPClient()
        response = yield gen.Task(http_client.fetch, request)
        
        receipt_data = json.loads(response.body)
        
        if receipt_data['status'] != 0:
            self.set_status(403)
            
        else:
            log.warn('Saving Receipt %s' %game_name.lower)
            # try to add the receipt to the DB
            log.warn(receipt_data)
            if redis_pool.sadd(receipt_data['receipt']['bid'], receipt_data['receipt']['transaction_id']) :
                # To keep the Redis light and fast, expire the com.game
                # transactions after 5 days of inactivity
                redis_pool.expire(receipt_data['receipt']['bid'], 432000)
                
                # Increment the product for statistics
                redis_pool.zincrby(game_name.lower(), receipt_data['receipt']['product_id'], 1)
                
                log.warn('pool saved')
                
                self.set_status(200)
            else:
                self.set_status(403)
        
        self.finish()
        
    def get(self, game_name):
        """
        Display Analytics for a specific game
        """
        logging.info('Get game Name %s' %game_name)
        
        self.write(json.dumps(redis_pool.zrange(game_name.lower(), 0, 20, desc=True, withscores=True)))
        
        
class StatusCheckHandler(RequestHandler):
    """
    Request Handler for new relic to ping and check that the site is up
    """
    def get(self):
        self.set_status(200)
        self.write('online')
        
    def head(self):
        self.set_status(200)
        
        
        
        

