# bandwidth-client

Tool to test the bandwidth capabilities of a network. Client component.

## How do I run it?

Client is tested on a Raspberry Pi 4.

You will need Selenium WebDriver to run web tests.

Installation script coming soon. For now:

    $ pip install -r requirements.txt

Create a `.env` file with the server address:

```
SERVER_ADDRESS=my.server.ip.or.hostname.goes.here
```

Run it:

    $ python3 bandwidth_client.py

Now [install the server](https://github.com/techied/bandwidth-server)!