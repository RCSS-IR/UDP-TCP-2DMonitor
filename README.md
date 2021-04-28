- ###Run server_side.py in the server
- ###Run client_side.py in the client
- ###Run ssh forwarding between server and client

##Example
The server is run on 6000/UDP in the server.
```
python server_side.py 127.0.0.1 6000 7000
```
Now you have to use ssh forwarding to connect the server and client
```
ssh -N -L 7000:localhost:8000 user@server_host
```
Then you should run the client_side.py on the client.
```
python client_side.py 7000 8000
```
Now you can run your monitor in 8000/udp.