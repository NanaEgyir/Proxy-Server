#!/usr/bin/python  # This line is needed for script to run on mac
# *********************************************************
#                                                         *
#       ECE 5650: Computer Networks and Program           *
#             Project 3: Simple Proxy Server              *
#                  Fall 2016                              *
#            Student: Andrews K Ankrah                    *
#                                                         *
# *********************************************************

# ********************** About This Program ****************************************
#                                                                                  *
#   This is a python code for the proxy server.                                    *
#   The code was built on a skeleton code provide by the instructor.               *
#                                                                                  *
#   It is able to successfully connect to a host. Use the the GET- request         *
#   to get objects like HTML pages from the web host.                              *
#                                                                                  *
#   This proxy server is able to forward clients request to the web server.        *
#   It is also able to deliver a response message from the web server              *
#   and sends it to the client.                                                    *
#   It works for only http web servers.                                            *
#   It creates a cache.                                                            *
#                                                                                  *
#   Additional functionality include                                               *
#   1. Verbose mode: For debugging                                                 *
#   2. Silent Mode where messages are not printed                                  *
#   3. Supports multithreading                                                                               *
#   Details are discussed in the project report.                                   *
#                                                                                  *
# **********************************************************************************

# Importing required Modules
import socket
import sys
import thread
import traceback
import time
import threadine

#********************* CONSTANT VARIABLES **********************************
messages     = ""   # messages set to empty string
buff_size    = 4096 # Maximum  buffer size for the socket
threadNumber = 5    # Number of pending connections Ques to hold
threadCouter = 0    # Thread Counter



#**************************** Main Program ********************************
def main():
    if len(sys.argv) < 3:
        print '[Usage]     : "python ProxyServer.py server_ip"\n' \
              '[server_ip] : It is the IP Address of the Proxy Server\n' \
              '[Port Number]      : should be more than 1000\n' \
              '[Mode] : --verbose, silent or threading'
        sys.exit(2)

    #********************* CONSTANT VARIABLES *****************************
    server_ip    = sys.argv[1]       # host ip set to system input arg 1
    tcpSerPort   = int(sys.argv[2])  # Proxy Port number
    mode_type    = sys.argv[3]       # Program mode set system input arg 3

    # logic flow to assign values to the variable mode_type
    if mode_type == "silent":
        mode_type = "silent"  # Sets mode_type to silence
        print "\033[", 95, "m", "Silent Mode Activated", "...", "\033[0m" # Alerts user silent mode is activated

    elif mode_type == "--verbose":
        mode_type = "verbose"  # Sets mode type to verbose
        print "\033[", 95, "m", "Verbose Mode Activated", "...", "\033[0m" # Alerts the user verbose mode is activated

    elif mode_type == "threading":
        mode_type = "multithread"  # Sets mode type to verbose
        print "\033[", 95, "m", "Threading Mode Activated", "...", "\033[0m" # Alerts the user verbose mode is activated

    else:
        print '[Usage]     : "python ProxyServer.py server_ip"\n' \
              '[server_ip] : It is the IP Address of the Proxy Server\n' \
              '[Mode]      : --verbose or silent'  # Message to alert user about wrong entry
        sys.exit(2)  # Exit the code

    try:
        # Create a server socket, bind it to a port and start listening
        tcpSerSock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        printMessages(mode_type, "Starting Server")

        # Associate socket to host IP and port
        tcpSerSock.bind((server_ip, tcpSerPort))

        printMessages(mode_type, "Server is ready!\n Waiting for connection ... \n")

        # Listining for connecting request
        tcpSerSock.listen(threadNumber)

    except socket.error, (value, message):
        if tcpSerSock:
            tcpSerSock.close()
        print 'Could not open Socekt'
        sys.exit(1)

    while True:
        try:
            # Accept connection from client browser
            tcpCliSock, addr = tcpSerSock.accept()

            printMessages(mode_type, "Server is connected\n")

            # Creating thread to handle request
            thread.start_new_thread(proxy_thread, (mode_type, tcpCliSock, addr))

            #Testing thread
            if mode_type == "multithread":
                print "\033[", 90, "m", "Timer setted", "\033[0m"
                time.sleep(10)
            else:
                time.sleep(0)

        except:
            tcpSerSock.close()
            print "\n[*] Proxy server shutting down ...."
            sys.exit(1)

    #Close the socket and the server sockets
    tcpSerSock.close()

#************** END MAIN PROGRAM ************

# This is a function to print messages when in verbose mode
def printMessages(verbose_command, messages):
    if verbose_command == "verbose":
        colornum = 94
        print "\033[", colornum, "m", messages, "\033[0m"

#*********************** Proxy Thread function *************
# This function handles the request from the browser
#***********************************************************
def proxy_thread(mode_type, tcpCliSock, addr):

    global  threadCouter

    threadCouter+=1

    #Getting  request from client browser and setting to variable request
    request = tcpCliSock.recv(buff_size)

    # Printing message from Server
    request_header = "HTTP REQUEST:"
    printMessages(mode_type, request_header)  # Prints the header


    # Extract the filename from the given message for caching
    cache_header = "Extracts From GET Request:"

    # Getting the first line of the get request
    first_line = request.split('\n')[0]

    # Getting the URL of the request
    url = first_line.split(' ')[1]

    #for i in range(0, len(BLOCKED))

    printMessages(mode_type, first_line)  # Prints the get request info

    print "\033[", 92, "m","Thread", "\t", threadCouter, "\t", url, "\t", "started at time","\t",str(time.time()), "\033[0m"

    printMessages(mode_type, cache_header)
    # Printing the URL of the requested page
    printMessages(mode_type, 'URL: ' + url + "\n")

    # find the webserver and port
    http_pos = url.find("://")  # find pos of ://

    if (http_pos == -1):
        filename = url
    else:
        filename = url[(http_pos + 3):]  # get the rest of url

    port_pos = filename.find(":")  # find the port pos (if any)

    # Find end of the web server
    webserver_pos = filename.find("/")
    if webserver_pos == -1:
        webserver_pos = len(filename)

    webserver = ""
    port = -1

    if (port_pos == -1 or webserver_pos < port_pos):
        port = 80
        webserver = filename[:webserver_pos]
    else:
        port = int((filename[(port_pos + 1):])[:webserver_pos - port_pos - 1])
        webserver = filename[:port_pos]

    #Modifying file name to ensure it is properly saved
    # Replaces all "/" with "."
    fileName_modefied = filename.replace("/", ".")


    # Ensuring the file is saved in the same path as the this py file
    filetouse = "/" + fileName_modefied

    printMessages(mode_type, "Searching for  " + filetouse + " in Cache...\n")


    # Initializing the presence of file to false
    fileExist = "false"

    try:
        # Check whether the file exists in the cache
        f = open(filetouse[1:], "r")
        saved_data = f.readlines()

        # Setting fileExist to true
        fileExist = "true"

        # Setting the search results message to a variable
        cache_search_result_1 = 'Web page object ' + request.split()[1] + ' is already in cache! \n'

        # Printing the search result from the cache
        printMessages(mode_type, cache_search_result_1)

        for i in range(0, 4):
            printMessages(mode_type,"[*]"+ saved_data[i])

        # ProxyServer finds a cache hit and generates a response message
        tcpCliSock.send("HTTP/1.0 200 OK\r\n")
        tcpCliSock.send("Content-Type:text/html\r\n")


        if mode_type == "silent":
            #Response message when server is in silent mode
            print "Client request granted"
        else:
            # Printing the http response from cache
            printMessages(mode_type, "HTTP Response From Cache: to "+ url)
        for i in range(0, 4):
            printMessages(mode_type, "[*]" + saved_data[i])
            #print"\n"


        for i in range(0, len(saved_data)):
            tcpCliSock.send(saved_data[i])

    # Error handling for file not found in cache
    except IOError:
        # Printing the file to use in the console
        printMessages(mode_type, "File " + filetouse + " is not in the proxy server's chache\n")

        # Setting message to tell user the proxy server is searching
        # the requested page from the origin server.
        searching_message = "Sending the object request "

        # Printing the searching_message to the terminal
        printMessages(mode_type, searching_message + url + "to origin server...\n")

        if fileExist == "false":
            # Create a socket on the Proxy server
            socket_message = "Creating socket on Proxy Server \n"

            printMessages(mode_type, socket_message)

            # Extracting the host name from the file name
            hostn = filename.replace("www.", "", 1).split('/')[0]

            printMessages(mode_type, "Connecting to host " + hostn +" ...\n")

            try:
                #create a socket to connect to the webserver
                c = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

                # Connect to the socket to port 80
                c.connect((hostn, 80))

                port_message = "Proxy server is now connected to the host "

                printMessages(mode_type, port_message + hostn + "\n")

                # Create a temporary file on this socket and ask port 80
                # for the file requested by the client
                fileobj = c.makefile('r', 0)
                fileobj.write("GET " + "http://" + filename + " HTTP/1.0\n\n")

                printMessages(mode_type, "Cache file successfully created for " + filename + "\n")

                # Read the response into buffer
                buff = fileobj.readlines()

                if mode_type == "silent":
                    # Response message when server is in silent mode
                    print "Client request granted\n"
                else:
                    # Response when server is in verbose mode
                    printMessages(mode_type, "HTTP Response From Server to " + url + "\n")
                    for i in range(0, 4):
                        printMessages(mode_type, "[*]" + buff[i])
                    print "\n"

                # Create a new file in the cache for the requested file.
                # Also send the response in the buffer to client socket
                # and the corresponding file in the cache
                tmpFile = open(fileName_modefied, "wb")
                for i in range(0, len(buff)):
                    tmpFile.write(buff[i])
                    tcpCliSock.send(buff[i])


                print "\033[", 91, "m", "Thread", "\t", threadCouter, "\t", url, "\t", "closed at time", "\t", str(
                    time.time()), "\033[0m"
                #print "\033[", 93, "m", "Thread", "\t", threadCouter, "\t", "is releasing the lock", "\033[0m"

                #tLock.release()

            except:
                request_type_message = 'Illegal request'
                printMessages(mode_type, request_type_message)

        else:
            # HTTP response message for file not found
            file_not_found_msg = 'File Not Found! Make sure file is saved in the same directory as the py file'

            printMessages(mode_type, file_not_found_msg)
    print "\033[", 91, "m", "Thread", "\t", threadCouter, "\t", url, "\t", "closed at time", "\t", str(
        time.time()), "\033[0m"


if __name__ == '__main__':

    main()

