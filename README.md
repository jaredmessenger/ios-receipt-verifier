ios-receipt-verifier
====================

Uses a [Heroku](http://www.heroku.com/) instance running a [Tornado Backend](http://www.tornadoweb.org/)
to verify iOS receipts from in-app-purchases   
For More info please read 
[Apple's Docs]
(http://developer.apple.com/library/ios/#documentation/NetworkingInternet/Conceptual/StoreKitGuide/VerifyingStoreReceipts/VerifyingStoreReceipts.html)

requires
-----------
1. Redis-To-Go:

        heroku addons:add redistogo:nano
        
2. NewRelic

        heroku addons:add newrelic:standard
        

Setup
-----------
```Shell
virtualenv venv --distribute --no-site-packages
source venv/bin/activate
pip install tornado

heroku create --remote server my-receipt-checker-app-name
heroku ps:scale web=1

git push server master
```
