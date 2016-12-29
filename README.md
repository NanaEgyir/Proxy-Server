# Proxy Server #

## Description ##
This is a simple proxy server that provide basic functions such as 


- Using GET-Request
- Handling of objects like HTML pages, creating caches
- searching cache to determine if a request is available in the cache before sending request to original server
- Handling multiple requests through multi-threading 

Additionally this Proxy server is programmed to run in three modes (for debugging purposes):

1. **Silent mode:** Where little to no text is displayed in the console/terminal
2. **Verbose mode:** Where the program displays messages with the sole purpose of helping  the user to know where in the code to debug
3. **Threading mode:** A way to test for the multi-thread function of the proxy server

##Version##
0.1.0

##Usage##
1. configure your web browser and set it to 'localhost' or '127.0.0.1'
2. Run the server code on the terminal shell of your computer, making sure the following arguments are entered as follows: 
a. File path 
b. IP address 
c. Port number d. Mode: "--verbose" or "silent"
3. Open a tab on your configured web browser and enter any http://website. 


##Vendors##
[Andrew Ankrah](http://aankrah.com)

##License##
Python
