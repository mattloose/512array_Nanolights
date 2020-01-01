import os
import sys
import fnmatch
import platform
import shutil
import fileinput
import grpc


root_directory = os.path.dirname(os.path.realpath(__file__))
OPER = platform.system()
RPC_PATH = os.path.join("ont-python", "lib", "python2.7", "site-packages", "minknow", "rpc")


def _minknow_path(operating_system=OPER):
    return {
        "Darwin": os.path.join(os.sep, "Applications", "MinKNOW.app", "Contents", "Resources"),
        "Linux": os.path.join(os.sep, "opt", "ONT", "MinKNOW"),
        "Windows": os.path.join(os.sep, "C:\\\Program Files", "OxfordNanopore", "MinKNOW"),
    }.get(operating_system, None)


def _rpc_path(operating_system=OPER):
    return {
        "Windows": os.path.join("ont-python", "Lib", "site-packages", "minknow", "rpc")
    }.get(operating_system, RPC_PATH) 


PATCH_INIT = """

import platform
def _minknow_path(operating_system=platform.system()):
    return {
        "Darwin": os.path.join(os.sep, "Applications", "MinKNOW.app", "Contents", "Resources"),
        "Linux": os.path.join(os.sep, "opt", "ONT", "MinKNOW"),
        "Windows": os.path.join(os.sep, "C:\\\Program Files", "OxfordNanopore", "MinKNOW"),
    }.get(operating_system, None)
"""


def copyfiles(srcdir, dstdir, filepattern, module):
    def failed(exc):
        raise exc

    dstdir = os.path.join(root_directory, dstdir)
    for dirpath, dirs, files in os.walk(srcdir, topdown=True, onerror=failed):
        for file in fnmatch.filter(files, filepattern):
            shutil.copy2(os.path.join(dirpath, file), dstdir)
            editfile(
                os.path.join(dstdir, file),
                "minknow.{}".format(module),
                "minLights.{}".format(module),
            )
            editfile(
                os.path.join(dstdir, file),
                "minknow.paths.minknow_base_dir()",
                "_minknow_path()",
            )
            editfile(os.path.join(dstdir, file), "import minknow.paths", "")
            if file == "__init__.py":
                with open(os.path.join(dstdir, file), "a") as out:
                    out.write(PATCH_INIT)
        break  # no recursion


"""
def copyfiles(srcdir, dstdir, filepattern):
    def failed(exc):
        raise exc
    dstdir = os.path.join(root_directory,dstdir)
    for dirpath, dirs, files in os.walk(srcdir, topdown=True, onerror=failed):
        for file in fnmatch.filter(files, filepattern):
            shutil.copy2(os.path.join(dirpath, file), dstdir)
            editfile(os.path.join(dstdir, file), "minknow.rpc", "rpc")
        break # no recursion

"""

def editfile(filename,text_to_search,replacement_text):
    with fileinput.FileInput(filename, inplace=True) as file:
        for line in file:
            print(line.replace(text_to_search, replacement_text), end="")


    # Define a utility to search for a protocol in the list of returned protocols:
def find_protocol(protocols, flow_cell, kit, experiment_type):
    def has_tag(protocol, tag_name, tag_value):
        # Search each tag to find if it matches the requested tag
        for tag in protocol.tags:
            if (tag == tag_name and protocol.tags[tag].string_value == tag_value):
                return True
        return False

    # Search all protocols to find the one with matching flow cell and kit
    for protocol in protocols.protocols:
        if (has_tag(protocol, "flow cell", flow_cell) and
            has_tag(protocol, "kit", kit) and
            has_tag(protocol, "experiment type", "sequencing")):
            return protocol

    # Potentially an invalid script combination was requested?
    raise Exception("Protocol %s %s %s not found!" % (flow_cell, kit, experiment_type))
    
    
    # Define a utility to search for a protocol in the list of returned protocols:
def find_protocol2(protocols, flow_cell, kit, experiment_type, base_calling):
    def has_tag(protocol, tag_name, tag_value):
        # Search each tag to find if it matches the requested tag
        for tag in protocol.tags:
            if (tag == tag_name and protocol.tags[tag].string_value == tag_value):
                return True
        return False

    # Search all protocols to find the one with matching flow cell and kit
    for protocol in protocols.protocols:
        if (has_tag(protocol, "flow cell", flow_cell) and
            has_tag(protocol, "kit", kit) and
            has_tag(protocol, "experiment type", experiment_type) and
            has_tag(protocol, "base calling", base_calling)):
            return protocol

    # Potentially an invalid script combination was requested?
    raise Exception("Protocol %s %s %s not found!" % (flow_cell, kit, experiment_type))
    
    

def fetch_protocols():
    dstRPC = "rpc"

    if not os.path.exists(os.path.join(root_directory, "rpc")):
        os.makedirs(os.path.join(root_directory, "rpc"))
    if not os.path.isfile(os.path.join(root_directory, "rpc", "__init__.py")):
        if _minknow_path() is not None:
            sourceRPC = os.path.join(_minknow_path(), _rpc_path())
        else:
            raise NotImplementedError("MinKNOW is not configured for this platform ({}) yet.".format(OPER))

        if os.path.exists(sourceRPC):
            copyfiles(sourceRPC, dstRPC, "*.py")
        else:
            raise ValueError("MinKNOW not found on this computer")


    sys.path.insert(0, os.path.join(root_directory, "rpc"))
    import rpc
    rpc._load()
    import rpc.protocol_pb2 as protocol
    import rpc.protocol_pb2_grpc as protocol_grpc
    import rpc.manager_pb2 as manager
    import rpc.manager_pb2_grpc as manager_grpc
    
    manager_channel = grpc.insecure_channel('localhost:9501')
    manager_stub = manager_grpc.ManagerServiceStub(manager_channel)
    
    list_devices_request = manager.ListDevicesRequest()
    list_devices_response = manager_stub.list_devices(list_devices_request)

    if len(list_devices_response.active) == 0:
        raise Exception("No devices found to start protocol on")

    # See 'list_devices.py' to find out more about available devices.
    device = list_devices_response.active[0]
    print("Using device %s using gRPC port %s" % (device.name, device.ports.insecure_grpc))
    
    #-------------------------------------------------------------------------------
    # Connect to the running MinKNOW instance:
    #
    # We can connect to a running MinKNOW instance on the local
    # computer (using port from above)
    #
    channel = grpc.insecure_channel('localhost:%s' % device.ports.insecure_grpc)
    stub = protocol_grpc.ProtocolServiceStub(channel)
    #-------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------
    # Find the protocols available on the running MinKNOW instance:
    #
    print("Listing protocols:")

    # Construct a list message to send to MinKNOW
    list_request = protocol.ListProtocolsRequest()
    # Send the message to MinKNOW and wait for a response
    available_protocols = stub.list_protocols(list_request)
    print("Found protocols: %s" % available_protocols)
    return available_protocols




def fetch_devices_2(ip):
    import minLights.rpc as rpc

    rpc._load()
    # Then import the generated api
    import minLights.rpc.manager_pb2 as manager
    import minLights.rpc.manager_pb2_grpc as manager_grpc

    # -------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------
    # Connect to the running Manager instance:
    #
    # We can connect to minknow manager on port 9501.
    #
    channel = grpc.insecure_channel('{}:9501'.format(ip))
    stub = manager_grpc.ManagerServiceStub(channel)
    # -------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------
    # Send the list request
    list_request = manager.ListDevicesRequest()
    response = stub.list_devices(list_request)
    # -------------------------------------------------------------------------------

    # -------------------------------------------------------------------------------
    # We can now iterate and find our required device
    # for device in response.active:
    #    print("Found device %s using gRPC port %s" % (device.name, device.ports.insecure_grpc))
    return (response)


def fetch_devices():
    dstRPC = "rpc"

    print (os.path.join(root_directory, "rpc"))

    if not os.path.exists(os.path.join(root_directory, "rpc")):
        os.makedirs(os.path.join(root_directory, "rpc"))
    if not os.path.isfile(os.path.join(root_directory, "rpc", "__init__.py")):
        if _minknow_path() is not None:
            sourceRPC = os.path.join(_minknow_path(), _rpc_path())
        else:
            raise NotImplementedError("MinKNOW is not configured for this platform ({}) yet.".format(OPER))

        if os.path.exists(sourceRPC):
            copyfiles(sourceRPC, dstRPC, "*.py", "rpc")
        else:
            raise ValueError("MinKNOW not found on this computer")

    sys.path.insert(0, os.path.join(root_directory, "rpc"))
    print ("we got here, {}".format(root_directory))
    import minLights.rpc as rpc

    rpc._load()
    # Then import the generated api
    import minLights.rpc.manager_pb2 as manager
    import minLights.rpc.manager_pb2_grpc as manager_grpc
    

    
    #-------------------------------------------------------------------------------


    #-------------------------------------------------------------------------------
    # Connect to the running Manager instance:
    #
    # We can connect to minknow manager on port 9501.
    #
    channel = grpc.insecure_channel('localhost:9501')
    stub = manager_grpc.ManagerServiceStub(channel)
    #-------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------
    # Send the list request
    list_request = manager.ListDevicesRequest()
    response = stub.list_devices(list_request)
    #-------------------------------------------------------------------------------

    #-------------------------------------------------------------------------------
    # We can now iterate and find our required device
    #for device in response.active:
    #    print("Found device %s using gRPC port %s" % (device.name, device.ports.insecure_grpc))
    return (response)
            
def load_rpc(port=8004):
    dstRPC = "rpc"

    if not os.path.exists(os.path.join(root_directory, "rpc")):
        os.makedirs(os.path.join(root_directory, "rpc"))
    if not os.path.isfile(os.path.join(root_directory, "rpc", "__init__.py")):
        if _minknow_path() is not None:
            sourceRPC = os.path.join(_minknow_path(), _rpc_path())
        else:
            raise NotImplementedError("MinKNOW is not configured for this platform ({}) yet.".format(OPER))

        if os.path.exists(sourceRPC):
            copyfiles(sourceRPC, dstRPC, "*.py", "rpc")
        else:
            raise ValueError("MinKNOW not found on this computer")

    sys.path.insert(0, os.path.join(root_directory, "rpc"))
    import rpc
    
    rpc._load()
    return rpc.Connection(port=port)

