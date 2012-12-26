ios-receipt-verifier
====================

Simple Twisted server to verify iOS receipts from in-app-purchases   
For More info please read 
[Apple's Docs]
(http://developer.apple.com/library/ios/#documentation/NetworkingInternet/Conceptual/StoreKitGuide/VerifyingStoreReceipts/VerifyingStoreReceipts.html)

Local Setup
-----------
```Shell
virtualenv venv --distribute --no-site-packages
source venv/bin/activate
pip install -U twisted

heroku create --remote server --addons heroku-postgresql:dev ios-receipt-verification
heroku ps:scale web=1
```
