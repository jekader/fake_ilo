#!/usr/bin/python

import libvirt,time
from socket import *
from ssl import *

def print_vm_status(vmname):
# connect to ovirt
    domains = { }
    conn = libvirt.open('qemu:///system')
#active domains
    active_ids = conn.listDomainsID()
    for id in active_ids:
        dom = conn.lookupByID(id)
        id_str = str(id)
        name = dom.name()
        domains[name] = dom
# inactive domains
    for name in conn.listDefinedDomains():
        dom = conn.lookupByName(name)
        domains[name] = dom
    if vmname in domains:
        if domains[vmname].isActive():
            return "on"
        else:
            return "off"
    else:
        return "NaN"

def set_vm_status(vmname,vmstatus):
# check if VM is already in desired status, just return result if yes
    if print_vm_status(vmname).lower() == vmstatus.lower():
        return vmstatus
    else:
#do actual fencing here
        if print_vm_status(vmname) in ('on','off'):
            conn = libvirt.open('qemu:///system')
            dom = conn.lookupByName(vmname)
            if vmstatus == "off":
                dom.destroy()
                return "off"
            if vmstatus == "on":
                dom.create()
                return "on"
        else:
#return error if VM not present
            return "NaN"

def logprint(msg):
    logfile = open('/var/log/fake_ilo.log','a')
    logline = time.strftime("[%Y-%m-%d %H:%M:%S] - ") + msg + "\n"
    logfile.write(logline)
    logfile.close()

#create socket
server_socket=socket(AF_INET, SOCK_STREAM)

username = ''
#Bind to an unused port on the local machine
server_socket.bind(('',1234))

#listen for connection
server_socket.listen (1)
tls_server = wrap_socket(server_socket, ssl_version=PROTOCOL_SSLv23, cert_reqs=CERT_NONE, server_side=True, keyfile='/etc/fake_ilo/server.key', certfile='/etc/fake_ilo/server.crt')

logprint('server started')

while True:
#accept connection
    connection, client_address= tls_server.accept()

#server is not finished
    finnished =False
    emptyresponse=0

#while not finished
    while not finnished:


    #send and receive data from the client socket
        data_in=connection.recv(1024)
        message=data_in.decode()

        if message=='quit':
            finnished= True
        else:
#login = VM name
            if message.find('USER_LOGIN') > 1:
                username=message.split()[3].replace('"', '')

            if message.find('xml') > 1:
                response='<RIBCL VERSION="2.0"></RIBCL>'
                data_out=response.encode()
                connection.send(data_out)
# return firmware version
            if message.find('GET_FW_VERSION') > 1:
                response='<GET_FW_VERSION\r\n FIRMWARE_VERSION="1.91"\r\n MANAGEMENT_PROCESSOR="2.22"\r\n />'
                data_out=response.encode()
                connection.send(data_out)
# get power status
            if message.find('GET_HOST_POWER_STATUS') > 1:
                response='HOST_POWER="' + print_vm_status(username) + '"'
                logprint('received status request for '+username+' from '+client_address[0]+':'+str(client_address[1])+' - responding  with: ' + print_vm_status(username))
                data_out=response.encode()
                connection.send(data_out)
# set power status
            if message.find('SET_HOST_POWER') > 1:
                power=message.split()[6].replace('"', '')
                response='HOST_POWER="' + set_vm_status(username,power) + '"'
                logprint('received fencing command for '+username+' from '+client_address[0]+':'+str(client_address[1])+' - requested status: '+power+ ', status after fencing is: ' + print_vm_status(username))
                data_out=response.encode()
                connection.send(data_out)
# filter out the rest
            else:
                if len(message) > 0:
                    do_nothing = 0
                else:
                    emptyresponse+=1
                if emptyresponse > 30:
                    finnished=True


#close the connection
connection.shutdown(SHUT_RDWR)
connection.close()

#close the server socket
server_socket.shutdown(SHUT_RDWR)
server_socket.close()
