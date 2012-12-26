ios-receipt-verifier
====================

Simple Twisted server to verify iOS receipts from in-app-purchases

Local Setup
-----------
```Shell
virtualenv venv --distribute --no-site-packages
source venv/bin/activate
pip install -U twisted

heroku create --remote server --addons heroku-postgresql:dev ios-receipt-verification
```
