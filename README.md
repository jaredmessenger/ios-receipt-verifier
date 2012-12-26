ios-receipt-verifier
====================

Uses a [Heroku](http://www.heroku.com/) instance running a [Twisted Site](http://twistedmatrix.com/trac/wiki)
to verify iOS receipts from in-app-purchases   
For More info please read 
[Apple's Docs]
(http://developer.apple.com/library/ios/#documentation/NetworkingInternet/Conceptual/StoreKitGuide/VerifyingStoreReceipts/VerifyingStoreReceipts.html)

Setup
-----------
```Shell
virtualenv venv --distribute --no-site-packages
source venv/bin/activate
pip install -U twisted

heroku create --remote server --addons heroku-postgresql:dev my-ios-receipt-verifier
heroku ps:scale web=1

git push server master
```
