# Chat Server
 this is a chat server that i built.
 
 server listens on port 9999.
 
 client connects to ip address and port which needs to be delivered from command line.
 
 on startup, client is required to enter username from keyboard / config file (assumed to have label **[USERNAME]** and key **username**)
 
 for simplicity, server echos each message received to all connected clients, but this can easily be changed through the send method
 
 if a client is inactive for 60 seconds he is disconnected from the server
