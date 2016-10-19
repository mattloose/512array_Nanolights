#!/usr/bin/python
# -*- coding: utf-8 -*-
from __future__ import division
import sys
import os
import re
import time
import errno
from socket import error as socket_error
import threading
import configargparse
import urllib2
import json
from ws4py.client.threadedclient import WebSocketClient
from thrift import Thrift
from thrift.transport import TTransport
from thrift.protocol import TCompactProtocol
import multiprocessing
import copy
import platform
import random
import struct
import hashlib


# Unbuffered IO
# sys.stdin = os.fdopen(sys.stdin.fileno(), 'w', 0) # MS
sys.stdout = os.fdopen(sys.stdout.fileno(), 'w', 1)  # MS
sys.stderr = os.fdopen(sys.stderr.fileno(), 'w', 0)  # MS

global OPER
OPER = platform.system()
if OPER == 'Windows':  # MS
    OPER = 'windows'
elif OPER == 'Darwin':
    OPER = 'osx'
else:
    OPER = 'linux'  # MS
print OPER  # MS

def hex2rgb(rgb):
    return struct.unpack('BBB', rgb.decode('hex'))

def rgb2hex(rgb):
    return struct.pack('BBB',*rgb).encode('hex')


config_file = script_dir = os.path.dirname(os.path.realpath('__file__'
        )) + '/' + 'minup_posix.config'
parser = \
    configargparse.ArgParser(description='interaction: A program to provide real time interaction for minION runs.'
                             , default_config_files=[config_file])
parser.add(
    '-ip',
    '--ip-address',
    type=str,
    dest='ip',
    required=True,
    default=None,
    help='The IP address of the minKNOW machine.',
    )
parser.add(
    '-v',
    '--verbose',
    action='store_true',
    help='Display debugging information.',
    default=False,
    dest='verbose',
    )
parser.add(
    '-r',
    '--ratio',
    action='store_true',
    help='This option prints the ratio of in strand to available.',
    default=False,
    dest='ratio',
    )
parser.add(
    '-n',
    '--no_lights',
    action='store_true',
    help='Inactivate lights for testing and development purposes.',
    default=False,
    dest='nolights',
)

args = parser.parse_args()

if args.nolights is False:
    import Image
    import ImageDraw,ImageFont
    from rgbmatrix import Adafruit_RGBmatrix


version = '0.1'  # 17th October 2016

### test which version of python we're using

###Machine to connect to address
global ipadd
ipadd = args.ip


def bytesto(bytes, to, bsize=1024):
    """convert bytes to megabytes, etc.
       sample code:
           print('mb= ' + str(bytesto(314575262000000, 'm')))
       sample output:
           mb= 300002347.946
    """

    a = {'k' : 1, 'm': 2, 'g' : 3, 't' : 4, 'p' : 5, 'e' : 6 }
    r = float(bytes)
    for i in range(a[to]):
        r = r / bsize

    return(r)

def _urlopen(url, *args):
    """Open a URL, without using a proxy for localhost.
    While the no_proxy environment variable or the Windows "Bypass proxy
    server for local addresses" option should be set in a normal proxy
    configuration, the latter does not affect requests by IP address. This
    is apparently "by design" (http://support.microsoft.com/kb/262981).
    This method wraps urllib2.urlopen and disables any set proxy for
    localhost addresses.
    """
    try:
        host = url.get_host().split(':')[0]
    except AttributeError:
        host = urlparse.urlparse(url).netloc.split(':')[0]
    import socket
    # NB: gethostbyname only supports IPv4
    # this works even if host is already an IP address
    addr = socket.gethostbyname(host)
    #if addr.startswith('127.'):
    #    return _no_proxy_opener.open(url, *args)
    #else:
    return urllib2.urlopen(url, *args)


def execute_command_as_string(data, host=None, port=None):
    host_name = host
    port_number = port
    url = 'http://%s:%s%s' % (host_name, port_number, '/jsonrpc')
    req = urllib2.Request(url, data=data,headers={'Content-Length': str(len(data)),'Content-Type': 'application/json'})
    ##print req
    try:
        f = _urlopen(req)
    except Exception, err:
        err_string = \
            'Fail to initialise mincontrol. Likely reasons include minKNOW not running, the wrong IP address for the minKNOW server or firewall issues.'
        #print err_string, err
    json_respond = json.loads(f.read())
    f.close()
    return json_respond



def update_run_scripts():
    get_scripts = \
        '{"id":"1", "method":"get_script_info_list","params":{"state_id":"status"}}'
    results = execute_command_as_string(get_scripts, ipadd, 8000)

    # #print get_scripts
    # for key in results.keys():
    #    #print "mincontrol:", key, results[key]

    scriptlist = list()
    for element in results['result']:

        # #print "Element", results["result"][element]

        for item in results['result'][element]:

            # #print "Item", item
            # #print item["name"]

            scriptlist.append("('runscript','all','" + item['name']
                              + "',1)")
    recipelist = ','.join(scriptlist)
    sqlinsert = \
        'insert into messages (message,target,param1,complete) VALUES %s' \
        % recipelist
    if args.verbose is True:
        print sqlinsert
    cursor.execute(sqlinsert)
    db.commit()


def send_message_port(message,port):
    message_to_send = \
        '{"id":"1", "method":"user_message","params":{"content":"%s"}}' \
        % message
    results=""
    try:
        results = execute_command_as_string(message_to_send, ipadd, port)
    except Exception, err:
        print "message send fail", err
    return results

def send_message(message):
    message_to_send = \
        '{"id":"1", "method":"user_message","params":{"content":"%s"}}' \
        % message
    results = execute_command_as_string(message_to_send, ipadd, 8000)
    return results

def startstop(command,minION):
    if OPER == "osx":
        p = os.popen('/Applications/MinKNOW.app/Contents/Resources/bin/mk_manager_client -i ' + minION + ' --' + command,"r")
        while 1:
            line = p.readline()
            if not line: break
            print line
    elif OPER == "windows":
        p = os.popen('C:\grouper\\binaries\\bin\\mk_manager_client.exe -i ' + minION + ' --' + command, "r")
        print 'C:\grouper\ \binaries\\bin\\mk_manager_client.exe -i ' + minION + ' --' + command, "r"
        while 1:
            line = p.readline()
            if not line: break
            print line
    elif OPER == "linux":
        print "!!!!!!!!!!!!!! Sorry cannot handle linux yet."
    else:
        print "!!!!!!!!!!!!!! Sorry - cannot recognise your operating system."

def commands(command):
    return {
        'getstaticdata' : '{"id":1,"method":"get_static_data","params":null}',
        'initialization_status' : '{"params": "null", "id": 5, "method": "initialization_status"}',
        'get_analysis_configuration' : '{"id":1,"method":"get_analysis_configuration","params":null}',
        'initialiseminion' : '{"params": {"command": "init_main_board", "parameters": []}, "id": 0, "method": "board_command_ex"}',
        'shutdownminion' : '{"params": {"state_id": "status", "value": "stop"}, "id": 0, "method": "set_engine_state"}',
        'startmessagenew' : '{"id":"1", "method":"user_message","params":{"content":"minoTour is now interacting with your run. This is done at your own risk. To stop minoTour interaction with minKnow disable upload of read data to minoTour."}}',
        'status':'{"id":"1", "method":"get_engine_state","params":{"state_id":"status"}}',
        'dataset':'{"id":"1", "method":"get_engine_state","params":{"state_id":"data_set"}}',
        'startrun' :'{"id":"1", "method":"start_script","params":{"name":"MAP_Lambda_Burn_In_Run_SQK_MAP005.py"}}',
        'stoprun' : '{"id":"1", "method":"stop_experiment","params":"null"}',
        'stopprotocol' : '{"id":"1", "method":"stop_script","params":{"name":"MAP_48Hr_Sequencing_Run.py"}}',
        'biasvoltageget' : '{"id":"1","method":"board_command_ex","params":{"command":"get_bias_voltage"}}',
        'bias_voltage_gain' : '{"id":"1","method":"get_engine_state","params":{"state_id":"bias_voltage_gain"}}',
        'bias_voltage_set' :'{"id":"1","method":"board_command_ex","params":{"command":"set_bias_voltage","parameters":"-120"}}',
        'machine_id' :'{"id":"1","method":"get_engine_state","params":{"state_id":"machine_id"}}',
        'machine_name' :'{"id":"1","method":"get_engine_state","params":{"state_id":"machine_name"}}',
        'sample_id' :'{"id":"1","method":"get_engine_state","params":{"state_id":"sample_id"}}',
        'flow_cell_id' : '{"id":"1","method":"get_engine_state","params":{"state_id":"flow_cell_id"}}',
        'user_error' :'{"id":"1","method":"get_engine_state","params":{"state_id":"user_error"}}',
        'sequenced_res' :'{"id":"1","method":"get_engine_state","params":{"state_id":"sequenced"}}',
        'yield_res' : '{"id":"1","method":"get_engine_state","params":{"state_id":"yield"}}',
        'current_script' : '{"id":"1","method":"get_engine_state","params":{"state_id":"current_script"}}',
        'get_scripts' : '{"id":"1", "method":"get_script_info_list","params":{"state_id":"status"}}',
        'disk_space' : '{"id":1,"method":"get_disk_space_info","params":null}',
        'sinc_delay' : '{"id":1,"method":"sinc_delay","params":null}',

    }[command]





class HelpTheMinion(WebSocketClient):

#    def __init__(self,minIONdict):
#        self.minIONdict = minIONdict

    def opened(self):
        print "Connected to Master MinION Controller!"
        example.write_text("Connect!","white",3)
        example.showlight = True


    def initialiseminion():
        result = self.send(json.dumps({"params": "null", "id": 5, "method": "initialization_status"}))
        print result


    def received_message(self, m):
        ##print "message received!"
        for thing in ''.join(map(chr,map(ord,str(m)))).split('\n'):
            if len(thing) > 5:
                if thing[1:8] not in minIONdict:
                    #print "INITIALISING MINIONDICT"
                    minIONdict[thing[1:8]]=dict()
                print "minION ID:", thing[1:8]
                ##print map(ord,thing)
                minIONports =  map(lambda x:x-192+8000,filter(lambda x:x>190,map(ord,thing)))
                ##print minIONports
                if len(minIONports) > 0:
                    minIONdict[thing[1:8]]["state"]="active"
                    port = minIONports[0]
                    ws_longpoll_port = minIONports[1]
                    ws_event_sampler_port = minIONports[2]
                    ws_raw_data_sampler_port = minIONports[3]
                    minIONdict[thing[1:8]]["port"]=port
                    minIONdict[thing[1:8]]["ws_longpoll_port"]=ws_longpoll_port
                    minIONdict[thing[1:8]]["ws_event_sampler_port"]=ws_event_sampler_port
                    minIONdict[thing[1:8]]["ws_raw_data_sampler_port"]=ws_raw_data_sampler_port
        #            #print "port:",port
        #            #print "ws_longpoll_port:",ws_longpoll_port
        #            #print "ws_event_sampler_port:",ws_event_sampler_port
        #            #print "ws_raw_data_sampler_port:",ws_raw_data_sampler_port
                else:
                    #print "Tick tick tickett boo!"
                    minIONdict[thing[1:8]]["state"]="inactive"
        #            #print "minION not active"
                    minIONdict[thing[1:8]]["port"]=""
                    minIONdict[thing[1:8]]["ws_longpoll_port"]=""
                    minIONdict[thing[1:8]]["ws_event_sampler_port"]=""
                    minIONdict[thing[1:8]]["ws_raw_data_sampler_port"]=""

class DummyClient(WebSocketClient):
    #infodict = {}

    def __init__(self, *args,**kwargs):
        super(DummyClient, self).__init__(*args,**kwargs)
        print "Client established!"
        self.detailsdict=dict()
        self.daemon=True

    def opened(self):
        #print "Connection Success"
        ##print "Trying \"engine_states\":\"1\",\"channel_states\":\"1\",\"multiplex_states\":\"1\""
        self.send(json.dumps({'engine_states':'1','channel_states':'1','multiplex_states':'1','channel_info':'1'}))
        #self.send(json.dumps({'engine_states':'1','channel_states':'1','channel_info':'1'}))
        #self.send(json.dumps({'engine_states':'1','channel_states':'1'}))
        #self.send(json.dumps({'engine_states':'1'}))
        #self.send(json.dumps({'channel_info':'1','channel_states':'1'}))
        #self.send(transport.getvalue(), binary=True)

    def closed(self, code, reason="client disconnected for some reason"):
        print "socket",self.sock.fileno()
        print "Closed down", code, reason

    def received_message(self, m):
        if not m.is_binary:
            #print "****************** Non binary message"
            ##print type(m)
            if args.verbose is True: print m
            json_object = json.loads(str(m))
            for element in json_object:
                if element == "channel_info" and json_object[element] != "null":
                    #print "CHANNELINFO",json_object[element]
                    if "channels" in json_object[element].keys():
                        #if "state_group" in json_object[element]["channels"].keys():
                        for thing in json_object[element]["channels"]:
                            #print "****Channel*****"
                            (r,g,b) = (0,0,0)
                            #print colourlookup
                            state = "unknown"
                            if "state" in thing.keys():
                                state = thing["state"]
                                #print thing["state"],thing["state_group"],thing["name"],getx(int(thing["name"])),gety(int(thing["name"]))
                                try:
                                    #print thing
                                    (r,g,b) =  colourlookup[thing["state"]]
                                except:
                                    #print "not found",thing["state"]
                                    #print colourlookup
                                    state="undefined"
                                    (r,g,b) = (0,0,0)
                                #print thing,r,g,b
                            #elif "201" in thing.keys():
                            #    print "################################ NEW CHANNEL DESCRIPTORS?"
                            #    print thing
                            #else:
                            #    print "!!!!!!!!!!!!!Different data type seen"
                            #    print thing
                            #except:
                            #    print "no state"
                            (x,y) = chanlookup[int(thing["name"])]
                            example.logitem(int(thing["name"]),state)
                            example.point(x,y,r,g,b)
                    for element2 in json_object[element]:
                        if json_object[element][element2] != "null":
                            if element not in self.detailsdict:
                                self.detailsdict[element]=dict()
                                #print type(json_object[element][element2])
                            if json_object[element][element2] is not dict:
                                self.detailsdict[element][element2]=json_object[element][element2]


def get_run_scripts(port):
    get_scripts = \
        '{"id":"1", "method":"get_script_info_list","params":{"state_id":"status"}}'
    results = execute_command_as_string(get_scripts, ipadd, port)

    return results

    #print get_scripts
    for key in results.keys():
        print "mincontrol:", key, results[key]

    scriptlist = list()
    for element in results['result']:

        #print "Element", results["result"][element]

        for item in results['result'][element]:

            #print "Item", item
            #print item["name"]

            scriptlist.append("('runscript','all','" + item['name']
                              + "',1)")

class RepeatedTimer(object):
    def __init__(self,interval,function,*args,**kwargs):
        self._timer = None
        self.interval = interval
        self.function = function
        self.args = args
        self.kwargs = kwargs
        self.is_running = False
        self.start()

    def _run(self):
        self.is_running = False
        self.start()
        self.function(*self.args,**self.kwargs)

    def start(self):
        if not self.is_running:
            self._timer = threading.Timer(self.interval,self._run)
            self._timer.start()
            self.is_running = True

    def stop(self):
        self._timer.cancel()
        self.is_running = False

class ThreadingExample(object):
    """ Threading example class
    The run() method will be started and it will run in the background
    until the application exits.
    """

    def __init__(self, interval=3):
        """ Constructor
        :type interval: int
        :param interval: Check interval, in seconds
        """
        self.interval = interval
        self.channel_data = dict()
        self.showlight = False
        for i in chanlookup:
            self.channel_data[i]=dict()
        # Rows and chain length are both required parameters:
        if args.nolights is False: self.matrix = Adafruit_RGBmatrix(16, 1)
        # use a bitmap font
        if args.nolights is False: self.font = ImageFont.load("rpi-rgb-led-matrix/fonts/4x6.pil")
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        """ Method that runs forever """
        while True:
            if self.showlight is True:
                if args.ratio is False:
                    self.flash_state_summary()
                else:
                    self.ratio_summary()
            #if args.verbose is True:
            if args.verbose is True: print self.get_state_summary()
            if args.verbose is True: print time.time()
            time.sleep(0.5)
            pass

    def ratio_summary(self):
        summary = self.get_state_summary()
        strand = 0
        single = 0
        if "strand" in summary.keys():
            strand = int(summary["strand"])
        if "good_single" in summary.keys():
            single = int(summary["good_single"])
            print "Seen Good Single", single
        total = strand+single
        if strand == 0:
            percentage = 0
        else:
            percentage = (total/strand)*100
        print total, "%.1f" % percentage, "%"
        #self.write_text_inst(str(summary),"blue")


    def flash_state_summary(self):
        for key,value in self.channel_data.items():
            #print key,value
            (r,g,b) = (0,0,0)
            try:
                (r,g,b) =  colourlookup[value["state"]]
            except:
                pass
            (x,y) = chanlookup[int(key)]
            self.point(x,y,r,g,b)



    def get_state_summary(self):
        state_dict = dict()
        for key, value in self.channel_data.items():

            #print value,type(value)
            try:
                if value["state"] in state_dict:
                    state_dict[value["state"]] += 1
                else:
                    state_dict[value["state"]] = 1
            except:
                pass
            #print(key, len([item for item in value if item]))
        return state_dict

    def logitem(self,channel,state):
        self.channel_data[channel]["state"]=state

    def point(self,x,y,r,g,b):
        if args.nolights is False:
            self.matrix.SetPixel(x,y,r,g,b)
        else:
            if args.verbose is True:
                print "would do:",x,y,r,g,b

    def write_text_inst(self,message,color):
        if args.nolights is False:
            image = Image.new("1",(320,200))
            image = image.convert("RGBA")
            draw = ImageDraw.Draw(image)
            draw.text((0,0),message,font=self.font,fill=color)
            self.matrix.Clear()
            self.matrix.SetImage(image.im.id,1,0)

    def write_text(self,message,color,showtime):
        if args.nolights is False:
            image = Image.new("1",(320,200))
            image = image.convert("RGBA")
            draw = ImageDraw.Draw(image)
            draw.text((0,0),message,font=self.font,fill=color)
            self.matrix.Clear()
            self.matrix.SetImage(image.im.id,1,0)
            time.sleep(showtime)
            self.matrix.Clear()

    def write_time(self,color):
        if args.nolights is False:
            timestring=time.strftime("%H:%M:%S", time.gmtime())
            image = Image.new("1",(320,200))
            image = image.convert("RGBA")
            draw = ImageDraw.Draw(image)
            draw.text((0,0),timestring,font=self.font,fill=color)
            #self.matrix.Clear()
            self.matrix.SetImage(image.im.id,0,0)
            #time.sleep(showtime)
            #self.matrix.Clear()





def getx(value):
    value = value-1
    xval=31-((value - (value % 4))/4 % 32)
    return xval


def gety(value):
    value = value-1
    ad36 = value % 4
    ab37 = (value - ad36)/4
    ad37 = (ab37 % 32)
    ab38 = ((ab37-ad37)/32)
    ad38 = (ab38 % 4)
    ag38 = (ad36+(4*ad38))
    yval=(15 - ag38)
    return yval




if __name__ == '__main__':

    global chanlookup
    chanlookup ={1:(31,0),2:(31,1),3:(31,2),4:(31,3),5:(31,4),6:(31,5),7:(31,6),8:(31,7),9:(30,0),10:(30,1),11:(30,2),12:(30,3),13:(30,4),14:(30,5),15:(30,6),16:(30,7),17:(29,0),18:(29,1),19:(29,2),20:(29,3),21:(29,4),22:(29,5),23:(29,6),24:(29,7),25:(28,0),26:(28,1),27:(28,2),28:(28,3),29:(28,4),30:(28,5),31:(28,6),32:(28,7),33:(31,15),34:(31,14),35:(31,13),36:(31,12),37:(31,11),38:(31,10),39:(31,9),40:(31,8),41:(30,15),42:(30,14),43:(30,13),44:(30,12),45:(30,11),46:(30,10),47:(30,9),48:(30,8),49:(29,15),50:(29,14),51:(29,13),52:(29,12),53:(29,11),54:(29,10),55:(29,9),56:(29,8),57:(28,15),58:(28,14),59:(28,13),60:(28,12),61:(28,11),62:(28,10),63:(28,9),64:(28,8),65:(3,0),66:(3,1),67:(3,2),68:(3,3),69:(3,4),70:(3,5),71:(3,6),72:(3,7),73:(2,0),74:(2,1),75:(2,2),76:(2,3),77:(2,4),78:(2,5),79:(2,6),80:(2,7),81:(1,0),82:(1,1),83:(1,2),84:(1,3),85:(1,4),86:(1,5),87:(1,6),88:(1,7),89:(0,0),90:(0,1),91:(0,2),92:(0,3),93:(0,4),94:(0,5),95:(0,6),96:(0,7),97:(3,15),98:(3,14),99:(3,13),100:(3,12),101:(3,11),102:(3,10),103:(3,9),104:(3,8),105:(2,15),106:(2,14),107:(2,13),108:(2,12),109:(2,11),110:(2,10),111:(2,9),112:(2,8),113:(1,15),114:(1,14),115:(1,13),116:(1,12),117:(1,11),118:(1,10),119:(1,9),120:(1,8),121:(0,15),122:(0,14),123:(0,13),124:(0,12),125:(0,11),126:(0,10),127:(0,9),128:(0,8),129:(7,0),130:(7,1),131:(7,2),132:(7,3),133:(7,4),134:(7,5),135:(7,6),136:(7,7),137:(6,0),138:(6,1),139:(6,2),140:(6,3),141:(6,4),142:(6,5),143:(6,6),144:(6,7),145:(5,0),146:(5,1),147:(5,2),148:(5,3),149:(5,4),150:(5,5),151:(5,6),152:(5,7),153:(4,0),154:(4,1),155:(4,2),156:(4,3),157:(4,4),158:(4,5),159:(4,6),160:(4,7),161:(7,15),162:(7,14),163:(7,13),164:(7,12),165:(7,11),166:(7,10),167:(7,9),168:(7,8),169:(6,15),170:(6,14),171:(6,13),172:(6,12),173:(6,11),174:(6,10),175:(6,9),176:(6,8),177:(5,15),178:(5,14),179:(5,13),180:(5,12),181:(5,11),182:(5,10),183:(5,9),184:(5,8),185:(4,15),186:(4,14),187:(4,13),188:(4,12),189:(4,11),190:(4,10),191:(4,9),192:(4,8),193:(11,0),194:(11,1),195:(11,2),196:(11,3),197:(11,4),198:(11,5),199:(11,6),200:(11,7),201:(10,0),202:(10,1),203:(10,2),204:(10,3),205:(10,4),206:(10,5),207:(10,6),208:(10,7),209:(9,0),210:(9,1),211:(9,2),212:(9,3),213:(9,4),214:(9,5),215:(9,6),216:(9,7),217:(8,0),218:(8,1),219:(8,2),220:(8,3),221:(8,4),222:(8,5),223:(8,6),224:(8,7),225:(11,15),226:(11,14),227:(11,13),228:(11,12),229:(11,11),230:(11,10),231:(11,9),232:(11,8),233:(10,15),234:(10,14),235:(10,13),236:(10,12),237:(10,11),238:(10,10),239:(10,9),240:(10,8),241:(9,15),242:(9,14),243:(9,13),244:(9,12),245:(9,11),246:(9,10),247:(9,9),248:(9,8),249:(8,15),250:(8,14),251:(8,13),252:(8,12),253:(8,11),254:(8,10),255:(8,9),256:(8,8),257:(15,0),258:(15,1),259:(15,2),260:(15,3),261:(15,4),262:(15,5),263:(15,6),264:(15,7),265:(14,0),266:(14,1),267:(14,2),268:(14,3),269:(14,4),270:(14,5),271:(14,6),272:(14,7),273:(13,0),274:(13,1),275:(13,2),276:(13,3),277:(13,4),278:(13,5),279:(13,6),280:(13,7),281:(12,0),282:(12,1),283:(12,2),284:(12,3),285:(12,4),286:(12,5),287:(12,6),288:(12,7),289:(15,15),290:(15,14),291:(15,13),292:(15,12),293:(15,11),294:(15,10),295:(15,9),296:(15,8),297:(14,15),298:(14,14),299:(14,13),300:(14,12),301:(14,11),302:(14,10),303:(14,9),304:(14,8),305:(13,15),306:(13,14),307:(13,13),308:(13,12),309:(13,11),310:(13,10),311:(13,9),312:(13,8),313:(12,15),314:(12,14),315:(12,13),316:(12,12),317:(12,11),318:(12,10),319:(12,9),320:(12,8),321:(19,0),322:(19,1),323:(19,2),324:(19,3),325:(19,4),326:(19,5),327:(19,6),328:(19,7),329:(18,0),330:(18,1),331:(18,2),332:(18,3),333:(18,4),334:(18,5),335:(18,6),336:(18,7),337:(17,0),338:(17,1),339:(17,2),340:(17,3),341:(17,4),342:(17,5),343:(17,6),344:(17,7),345:(16,0),346:(16,1),347:(16,2),348:(16,3),349:(16,4),350:(16,5),351:(16,6),352:(16,7),353:(19,15),354:(19,14),355:(19,13),356:(19,12),357:(19,11),358:(19,10),359:(19,9),360:(19,8),361:(18,15),362:(18,14),363:(18,13),364:(18,12),365:(18,11),366:(18,10),367:(18,9),368:(18,8),369:(17,15),370:(17,14),371:(17,13),372:(17,12),373:(17,11),374:(17,10),375:(17,9),376:(17,8),377:(16,15),378:(16,14),379:(16,13),380:(16,12),381:(16,11),382:(16,10),383:(16,9),384:(16,8),385:(23,0),386:(23,1),387:(23,2),388:(23,3),389:(23,4),390:(23,5),391:(23,6),392:(23,7),393:(22,0),394:(22,1),395:(22,2),396:(22,3),397:(22,4),398:(22,5),399:(22,6),400:(22,7),401:(21,0),402:(21,1),403:(21,2),404:(21,3),405:(21,4),406:(21,5),407:(21,6),408:(21,7),409:(20,0),410:(20,1),411:(20,2),412:(20,3),413:(20,4),414:(20,5),415:(20,6),416:(20,7),417:(23,15),418:(23,14),419:(23,13),420:(23,12),421:(23,11),422:(23,10),423:(23,9),424:(23,8),425:(22,15),426:(22,14),427:(22,13),428:(22,12),429:(22,11),430:(22,10),431:(22,9),432:(22,8),433:(21,15),434:(21,14),435:(21,13),436:(21,12),437:(21,11),438:(21,10),439:(21,9),440:(21,8),441:(20,15),442:(20,14),443:(20,13),444:(20,12),445:(20,11),446:(20,10),447:(20,9),448:(20,8),449:(27,0),450:(27,1),451:(27,2),452:(27,3),453:(27,4),454:(27,5),455:(27,6),456:(27,7),457:(26,0),458:(26,1),459:(26,2),460:(26,3),461:(26,4),462:(26,5),463:(26,6),464:(26,7),465:(25,0),466:(25,1),467:(25,2),468:(25,3),469:(25,4),470:(25,5),471:(25,6),472:(25,7),473:(24,0),474:(24,1),475:(24,2),476:(24,3),477:(24,4),478:(24,5),479:(24,6),480:(24,7),481:(27,15),482:(27,14),483:(27,13),484:(27,12),485:(27,11),486:(27,10),487:(27,9),488:(27,8),489:(26,15),490:(26,14),491:(26,13),492:(26,12),493:(26,11),494:(26,10),495:(26,9),496:(26,8),497:(25,15),498:(25,14),499:(25,13),500:(25,12),501:(25,11),502:(25,10),503:(25,9),504:(25,8),505:(24,15),506:(24,14),507:(24,13),508:(24,12),509:(24,11),510:(24,10),511:(24,9),512:(24,8)}
    global minIONdict
    global minIONdict_test
    global minIONclassdict
    global statedict
    global statesummarydict
    #global example
    global colourlookup
    colourlookup=dict()
    minIONdict=dict()
    minIONdict_test=dict()
    minIONclassdict=dict()
    statedict=dict()
    statesummarydict=dict()
    minwsip = "ws://"+ args.ip + ":9500/"
    example = ThreadingExample()


    global lights
    lights = False
    global helper
    print minwsip
    helper = HelpTheMinion(minwsip)
    try:
        helper.connect()
    except Exception, err:
        print "Error",err
        print "We guess you have not got minKNOW running on your computer at the ip address specified. Please try again."
        example.showlight=False
        example.write_text("Bye Bye!","red",3)
        print "bye bye"
        sys.exit()
    ringtone = 0

    try:
    #if 1:
        while 1:
            active = 0
            inactive = 0
            for minION in minIONdict:
                print minION
                if minIONdict[minION]["state"]=="active":
                    active += 1
                    if minION not in minIONclassdict:
                        minIONclassdict[minION]=dict()
                    if "connected" not in minIONclassdict[minION]:
                        connectip = "ws://"+ args.ip + ":"+str(minIONdict[minION]["ws_longpoll_port"])+"/"
                        minIONclassdict[minION]["class"]=DummyClient(connectip)
                    try:
                    #if 1:
                        if "connected" not in minIONclassdict[minION]:
                            try:
                            #if 1:
                                minIONclassdict[minION]["class"].connect()
                                #print "GETTTING THE GOOD STUFF"
                                results = execute_command_as_string(commands('get_analysis_configuration'), ipadd,minIONdict[minION]["port"])
                                #print results["result"]["channel_states"]
                                for thing in results["result"]["channel_states"]:
                                    temp_dict = results["result"]["channel_states"][thing]
                                    #print temp_dict
                                    if "style" in temp_dict.keys():
                                        #print temp_dict["name"],temp_dict["style"]["colour"]
                                        colourlookup[temp_dict["name"]]=hex2rgb(temp_dict["style"]["colour"].lstrip('#'))
                                        #print hex2rgb(temp_dict["style"]["colour"].lstrip('#'))
                                    else:
                                        colourlookup[temp_dict["name"]]=hex2rgb("000000")
                                #print colourlookup
                                scriptresult = execute_command_as_string(commands('get_scripts'), ipadd,minIONdict[minION]["port"])
                                print scriptresult
                                lights=True
                                minIONdict[minION]["channelstuff"]=results["result"]["channel_states"]
                            except Exception, err:
                                print "Connection failed", err
                            minIONclassdict[minION]["connected"]="True"

                    except:
                        print "Connection Error"
                    try:
                        #print "GETTTING THE GOOD STUFF"
                        results = execute_command_as_string(commands('get_analysis_configuration'), ipadd,minIONdict[minION]["port"])
                        #print results["result"]["channel_states"]
                        for thing in results["result"]["channel_states"]:
                            temp_dict = results["result"]["channel_states"][thing]
                        #    print temp_dict
                            if "style" in temp_dict.keys():
                        #        print temp_dict["name"],temp_dict["style"]["colour"]
                                colourlookup[temp_dict["name"]]=hex2rgb(temp_dict["style"]["colour"].lstrip('#'))
                        #        print hex2rgb(temp_dict["style"]["colour"].lstrip('#'))
                            else:
                                colourlookup[temp_dict["name"]]=hex2rgb("000000")
                        #print colourlookup
                        lights=True
                        minIONdict[minION]["channelstuff"]=results["result"]["channel_states"]
                    except:
                        print "Ho Hum"
                else:
                    inactive += 1
            time.sleep(5)
    except (KeyboardInterrupt,Exception) as err:
        print "ctrl-c detected at top level",err
        example.showlight = False
        example.write_text("Bye Bye!","red",3)
        print "bye bye"
        sys.exit()
