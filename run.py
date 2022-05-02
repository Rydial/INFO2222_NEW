
#-----------------------------------------------------------------------------

import os
import sys
from bottle import run

#-----------------------------------------------------------------------------

import model
import view
import controller

#-----------------------------------------------------------------------------

def run_server():    
    '''
        run_server
        Runs a bottle server
    '''

    # Read Server Configurations from Server Config File
    config = {}

    with open("server.config") as file:
        for line in file:
            param, value = line.strip().split("=")
            config[param] = value

    # Run the Server
    run(
        host=config["host"],
        port=int(config["port"]),
        server=config["server"],
        keyfile=config["keyfile"],
        certfile=config["certfile"],
        reloader=int(config["reloader"]),
        debug=bool(config["debug"]))

#-----------------------------------------------------------------------------

def manage_db():
    '''
        Blank function for database support, use as needed
    '''
    return

#-----------------------------------------------------------------------------

# What commands can be run with this python file
# Add your own here as you see fit

command_list = {
    'manage_db' : manage_db,
    'server'       : run_server
}

# The default command if none other is given
default_command = 'server'

def run_commands(args):
    '''
        run_commands
        Parses arguments as commands and runs them if they match the command list

        :: args :: Command line arguments passed to this function
    '''
    commands = args[1:]

    # Default command
    if len(commands) == 0:
        commands = [default_command]

    for command in commands:
        if command in command_list:
            command_list[command]()
        else:
            print("Command '{command}' not found".format(command=command))

#-----------------------------------------------------------------------------

run_commands(sys.argv)