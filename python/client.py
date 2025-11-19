import os
import sys
import tftpy
import sqlite3
import argparse
import json
import socket

# Defensive programming
from enum import Enum
from typing import List

# Local Constants
CLIENT_JSON_FILE_NAME = "client.json"
DB_FILE_NAME          = "exercise.db"

DEFAULT_SERVER_IP_ADDR = "127.0.0.1"
DEFAULT_SERVER_CHECK_PORT = 2020

# Local Definitions
class ClientCmds(Enum):
    CHECK_CONNECTION = 'check'
    INPUT_ENTRY = 'ienter'
    STOP_INPUTS = 'stop'
    SEND = 'send'
    PRINT_DB = 'prdb'
    QUIT = 'quit'
    EXIT = 'exit'

class MainExitCodes(Enum):
    AFTER_TRANSFER = 0
    SIGINT = 1
    WITH_CMD = 2 # i.e., the exit REPL client cmd
    PRE_SERVER_RESPONSE = 3 # i.e., file transfer was done but response from
                            # server wasn't fully received

################################################################################
# Program Time!
################################################################################
def main():
    # Parse command-line arguments
    parser = argparse.ArgumentParser()
    # TODO: Address potential exceptions here from type mismatching
    parser.add_argument('-t', '--timeout',
                        type=int,
                        default=50,
                        help='TFTP message reception timeout in ms (default: 50ms)' )
    parser.add_argument('--transfer-db',
                        action='store_true',
                        help='The TFTP file transfer shall be on the SQLite DB file')
    parser.add_argument('--transfer-json',
                        action='store_true',
                        help='The TFTP file transfer shall be on the JSON file')
    parser.add_argument('--server-ip',
                        default=DEFAULT_SERVER_IP_ADDR,
                        help="Server's IPv4 address")
    parser.add_argument('--server-cc-port',
                        default=DEFAULT_SERVER_CHECK_PORT,
                        type=int,
                        help="Server's check connection port")
    args = parser.parse_args()
    print(args)

    # TODO: Confirm server's IP address is IPv4

    # Start up REPL CLI
    print('Starting up client CLI...')
    file_transfer_completed = False
    full_sequence_completed = False
    try:
        nreps = 0
        MAX_NREPS = 1_000_000 # Some max cap to prevent truly infinite looping
        while nreps < MAX_NREPS and not file_transfer_completed:
            nreps = nreps + 1

            print('> ', end='', flush=True)
            user_cmd = input().lower()

            match user_cmd:
                case ClientCmds.CHECK_CONNECTION.value:
                    # check_connection( args.server_ip, args.server_cc_port )
                    # check_connection( "192.168.0.25", args.server_cc_port )
                    check_connection( "127.0.0.1", args.server_cc_port )
                    # TODO

                case ClientCmds.INPUT_ENTRY.value:
                    print('Inputs for database.value:')
                    # TODO

                case ClientCmds.SEND.value:
                    print('Sending DB file...')
                    # TODO

                case ClientCmds.PRINT_DB.value:
                    print('Printing DB contents...')
                    # TODO

                case ClientCmds.QUIT.value | ClientCmds.EXIT.value:
                    print('Exiting REPL CLI...')
                    break

                case _:
                    print( f'Unknown command: {user_cmd}')

        assert nreps <= MAX_NREPS, f'Somehow, nreps passed {MAX_NREPS}... nreps: {nreps}'

        if file_transfer_completed:
            # Await for response from server on its DB...
            print('Awaiting on server for database printout...')
            # TODO
            full_sequence_completed = True

    except KeyboardInterrupt:
        print('\nUser ended session using SIGINT (Ctrl+C).')
        if not file_transfer_completed:
            sys.exit(MainExitCodes.SIGINT.value)

    # Begin TFTP transfer

    # Await response from server

    # Print server's response to console + file

    assert file_transfer_completed or (not file_transfer_completed and not full_sequence_completed), \
           "No way full sequence has been completed and file transfer hasn't!"

    print('')
    if not file_transfer_completed:
        print('No file transfer performed.')
        sys.exit(MainExitCodes.WITH_CMD.value)
    elif not full_sequence_completed:
        print("Failed to wait on server's complete response.")
        sys.exit(MainExitCodes.PRE_SERVER_RESPONSE.value)
    print('Full sequence completed. Congratulations.')
    sys.exit(MainExitCodes.AFTER_TRANSFER.value)


def check_connection( ip_addr:str,
                      port:int,
                      timeout:float = 5.0 ):
    """
    Checks a connection by making a socket.connect() call to the IP address and
    port passed in, sending a string, and then awaiting for one back.
    """
    with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
        print('Checking connection to server...')
        try:
            s.settimeout(timeout)
            # TODO: Catch exceptions
            # - TimeoutError
            s.connect( (ip_addr, port) )
            # TODO: Catch exceptions
            s.sendall(b"Marco!")
            # - InterruptedError
            data = s.recv(1024) # This will throw a ConnectionRefusedError /w
                                # errno @ 111 if there is nothing listening
            # TODO: Catch exceptions
            # - ConnectionRefusedError
            # - InterruptedError
            print(f"Received from the server: { data.decode() }")
            print("Connection should be good!")
        except:
            print(f"Unable to connect to desired IP address {ip_addr} at port {port}.")
            print(f"Timed out after {timeout} seconds or exception occurred.")

if __name__ == "__main__":
    main()
