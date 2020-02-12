import socketio

sio = socketio.Client()


@sio.on('connect', namespace='/all-filings')
def on_connect():
    print("Connected to https://api.sec-api.io:3334/all-filings")


@sio.on('filing', namespace='/all-filings')
def on_filings(filing):
    print(filing)


sio.connect('https://api.sec-api.io:3334?apiKey=e58e22cf30545c49aac1fa0b2c42e1673bc1016ee1794e838c0a056ae2f31e11',
            namespaces=['/all-filings'])

sio.wait()