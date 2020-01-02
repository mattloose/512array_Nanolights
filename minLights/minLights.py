"""minLights.py

A novelty script that interacts with MinKNOW, and LED Matrix Boards to provide customisable displays.
"""
# Core imports
import json
from google.protobuf.json_format import MessageToJson
import threading
import logging
import time
import grpc
import sys

# minLights imports

from PIL import Image
from PIL import ImageDraw,ImageFont
#from samplebase import SampleBase

from rgbmatrix import graphics

from rgbmatrix import RGBMatrix, RGBMatrixOptions

from minLights.arguments import get_parser
from minLights.load_rpc import fetch_devices, fetch_devices_2
from minLights.utils import print_args, hex2rgb, rgb2hex, chanlookup

import minLights.rpc as rpc
rpc._load()
import minLights.rpc.protocol_pb2 as protocol
import minLights.rpc.protocol_pb2_grpc as protocol_grpc
import minLights.rpc.manager_pb2 as manager
import minLights.rpc.manager_pb2_grpc as manager_grpc

log = logging.getLogger(__name__)


def parsemessage(message):
    return json.loads(MessageToJson(message, preserving_proto_field_name=True, including_default_value_fields=True))


class DeviceConnect():
    #def __init__(self, *args,**kwargs):
    #    super(DeviceConnect, self).__init__(*args,**kwargs)
        #self.detailsdict=dict()
    #    self.daemon=True
    def __init__(self,args,rpcconnection,minIONid,mylights):
        self.args = args
        log.info("Client established!")
        self.rpc_connection=rpcconnection
        self.mylights=mylights

        #Here we need to check if we are good to run against this version.
        self.version = self.rpc_connection.instance.get_version_info().minknow.full
        self.device_type = parsemessage(self.rpc_connection.instance.get_host_type())['host_type']
        #log.error(self.device_type)
        if str(self.device_type).startswith("PROMETHION"):
            log.warning(self.device_type)
            log.warning("This version of minLights may not be compatible with PromethION.")
            #sys.exit()
        #if str(self.version) != "3.3.13":
        if not str(self.version).startswith("3.3"):
            log.warning(self.version)
            log.warning("This version of minLights may not be compatible with the MinKNOW version you are running.")
            log.warning("As a consequence, lights monitoring MAY NOT WORK.")
            log.warning("If you experience problems, let us know.")
            #sys.exit()

        self.channels = parsemessage(self.rpc_connection.device.get_flow_cell_info())['channel_count']
        self.channelstatesdesc = parsemessage(self.rpc_connection.analysis_configuration.get_channel_states_desc())
        self.colourlookup = dict()
        for key in self.channelstatesdesc:
            for state in self.channelstatesdesc[key]:
                for porestate in state['states']:
                    colour = "#000000"
                    #print (porestate)
                    if "style" in porestate.keys():
                        colour = porestate['style'].get('colour')
                    #    print (porestate['style'].get('colour'))
                    else:
                        #print ("no colour found")
                        colour = "#000000"
                    if len(colour)< 1:
                        colour = "#000000"
                    self.colourlookup[porestate['name']]=hex2rgb(colour)
        self.channelstates = dict()
        for i in range(self.channels):
            self.channelstates[i+1]=None
        self.status = ""
        self.interval = 3 #we will poll for updates every 30 seconds.
        self.longinterval = 3 #we have a short loop and a long loop
        self.minIONid = minIONid
        self.computer_name = self.rpc_connection.instance.get_machine_id().machine_id
        self.minknow_version = self.rpc_connection.instance.get_version_info().minknow.full
        self.minknow_status = self.rpc_connection.instance.get_version_info().protocols
        self.disk_space_info = json.loads(
            MessageToJson(self.rpc_connection.instance.get_disk_space_info(), preserving_proto_field_name=True,
                          including_default_value_fields=True))
        self.flowcelldata = parsemessage(self.rpc_connection.device.get_flow_cell_info())


        try:
            self.acquisition_data = parsemessage(self.rpc_connection.acquisition.get_acquisition_info())
        except:
            #if self.args.verbose:
            log.debug("No active run")
            self.acquisition_data = {}


        runmonitorthread = threading.Thread(target=self.runmonitor, args=())
        runmonitorthread.daemon = True                            # Daemonize thread
        runmonitorthread.start()

        flowcellmonitorthread = threading.Thread(target=self.flowcellmonitor, args=())
        flowcellmonitorthread.daemon = True
        flowcellmonitorthread.start()

        runinforthread = threading.Thread(target=self.runinfo, args=())
        runinforthread.daemon = True  # Daemonize thread
        runinforthread.start()

        messagesmonitor = threading.Thread(target=self.getmessages, args=())
        messagesmonitor.daemon = True  # Daemonize thread
        messagesmonitor.start()

        #This is for future usage.
        #dutytimemonitorthread = threading.Thread(target=self.dutytimemonitor, args=())
        #dutytimemonitorthread.daemon = True
        #dutytimemonitorthread.start()

        newchannelstatethread = threading.Thread(target=self.newchannelstatemonitor, args=())
        newchannelstatethread.daemon = True
        newchannelstatethread.start()

        newhistogrammonitorthread = threading.Thread(target=self.newhistogrammonitor, args=())
        newhistogrammonitorthread.daemon = True
        newhistogrammonitorthread.start()

        #log.debug("All is well with connection.")
        self.first_connect()

    def disconnect_nicely(self):
        log.debug("Trying to disconnect nicely")
        try:
            self.minIONstatus["minKNOW_status"]="unplugged"
        except:
            log.debug("Couldn't unplug MinION from website.")


    def first_connect(self):
        """
        This function will run when we first connect to the MinION device.
        It will provide the information to minotour necessary to remotely control the minION device.
        :return:
        """
        log.debug("First connection observed")
        #log.debug("All is well with connection. {}".format(self.minIONid))
        for protocol in self.rpc_connection.protocol.list_protocols().ListFields()[0][1]:
            protocoldict = self.parse_protocol(protocol)
            #print (self.minion,protocoldict)
        if str(self.status).startswith("status: PROCESSING"):
            self.run_start()

    def parse_protocol(self,protocol):
        protocoldict=dict()
        flowcell = "N/A"
        kit = "N/A"
        basecalling = "N/A"
        try:
            kit = protocol.tags["kit"].ListFields()[0][1]
            flowcell = protocol.tags["flow cell"].ListFields()[0][1]
            basecalling = protocol.tags["base calling"].ListFields()[0][1]
        except:
            pass
        #print (protocol.name, protocol.identifier)
        protocoldict["identifier"]=protocol.identifier
        #protocoldict["name"]=protocol.name
        #print (protocol.name)
        if basecalling:
            basecalling="BaseCalling"
        else:
            basecalling="NoBaseCalling"
        protocoldict["name"]="{}/{}_{}_{}".format(protocol.name,flowcell,kit,basecalling)
        for tag in protocol.tags:
            try:
                protocoldict[tag]=protocol.tags[tag].ListFields()[0][1]
            except:
                pass
        return protocoldict

    def run_start(self):
        """
        This function will fire when a run first begins.
        It will drive the creation of a run.
        :return:
        """
        log.debug("run start observed")

        #We wait for 10 seconds to allow the run to start
        time.sleep(self.interval)
        try:
            self.runinformation = self.rpc_connection.acquisition.get_current_acquisition_run()

            #log.debug(self.runinfo_api)
            #log.debug(self.sampleid)
            #log.debug(self.runinformation)
            #log.debug("RUNID {}".format(self.runinformation.start_time))
            #log.debug(self.channelstatesdesc)
            #log.debug(self.channels)
            #log.debug("FLOWCELL DATA {}".format(self.get_flowcell_id()))
            #log.debug("trying to create run")
            #self.create_run(self.runinformation.run_id)
            #log.debug("run created!!!!!!!")
            #self.update_minion_run_info()
            #log.debug("update minion run info complete")

        except Exception as err:
            log.error("Problem:", err)




    def update_minion_run_info(self):
        '''
        payload = {
            "minION": str(self.minion["url"]),
            "minKNOW_current_script": str(self.rpc_connection.protocol.get_run_info().protocol_id),
            "minKNOW_sample_name": str(self.sampleid.sample_id),
            "minKNOW_exp_script_purpose": str(self.rpc_connection.protocol.get_protocol_purpose()),
            "minKNOW_flow_cell_id": self.get_flowcell_id(),
            "minKNOW_run_name": str(self.sampleid.sample_id),
            "run_id": str(self.runidlink),
            "minKNOW_version": str(self.rpc_connection.instance.get_version_info().minknow.full),
            "minKNOW_hash_run_id": str(self.runinformation.run_id),
            "minKNOW_script_run_id": str(self.rpc_connection.protocol.get_current_protocol_run().acquisition_run_ids[0]),
            "minKNOW_real_sample_rate": int(str(self.rpc_connection.device.get_sample_rate().sample_rate            )),
            "minKNOW_asic_id": self.flowcelldata['asic_id'],
            "minKNOW_start_time": self.runinformation.start_time.ToDatetime().strftime('%Y-%m-%d %H:%M:%S'),
            #"minKNOW_colours_string": str(self.rpc_connection.analysis_configuration.get_channel_states_desc()),
            "minKNOW_colours_string": str(MessageToJson(self.rpc_connection.analysis_configuration.get_channel_states_desc(), preserving_proto_field_name=True, including_default_value_fields=True)),
            "minKNOW_computer": str(self.computer_name),
        }

        contextinfo = parsemessage(self.rpc_connection.protocol.get_context_info())['context_info']
        for k, v in contextinfo.items():
            payload[k]=v

        ruinfo = parsemessage(self.rpc_connection.protocol.get_run_info())

        try:
            payload['experiment_id']=ruinfo['user_info']['protocol_group_id']
        except:
            payload['experiment_id']="Not Known"
        '''
        payload = "camel"
        #log.debug(">>>>>>>>", payload)

    def create_run(self, runid):
        log.debug(">>> inside create_run")

        #run = self.minotourapi.get_run_by_runid(runid)

        #log.debug(run)

        if not run:
            log.debug(">>> no run {}".format(runid))
            #
            # get or create a flowcell
            #

            if not flowcell:
                log.debug(">>> no flowcell")

            is_barcoded = False  # TODO do we known this info at this moment? This can be determined from run info.

            has_fastq = True  # TODO do we known this info at this moment? This can be determined from run info
            #log.debug(">>> before self.minotourapi.create_run")
            #log.debug("self.sampleid.sample_id",self.sampleid.sample_id)

            # createrun = requests.post(self.args.full_host+'api/v1/runs/', headers=self.header, json={"run_name": self.status_summary['run_name'], "run_id": runid, "barcode": barcoded, "is_barcoded":is_barcoded, "minION":self.minion["url"]})

            if not createrun:
                log.error("Houston - we have a problem!")



        log.debug("***** self.runid", self.runid)

    def run_live(self):
        """
        This function will update the run information to the server at a given rate during a live run.
        :return:
        """
        pass

    def run_stop(self):
        """
        This function will clean up when a run finishes.
        :return:
        """
        log.debug("run stop observed")

    def minknow_command(self):
        """
        This function will recieve commands for a specific minION and handle the interaction.
        :return:
        """
        pass

    def get_flowcell_id(self):
        if len(self.flowcelldata['user_specified_flow_cell_id']) > 0:
            #log.debug("We have a self named flowcell")
            return str(self.flowcelldata['user_specified_flow_cell_id'])
        else:
            #log.debug("the flowcell id is fixed")
            return str(self.flowcelldata['flow_cell_id'])


    def flowcellmonitor(self):
        while True:
            flowcellinfo = self.rpc_connection.device.stream_flow_cell_info()
            for event in flowcellinfo:
                #log.debug(event)
                self.flowcelldata = parsemessage(event)
                #log.debug(self.get_flowcell_id())

    def newhistogrammonitor(self):
        while True:
            histogram_stream = self.rpc_connection.statistics.stream_read_length_histogram(poll_time=60,wait_for_processing=True,read_length_type=0,bucket_value_type=1)

            try:
                for histogram_event in histogram_stream:
                    #print (parsemessage(histogram_event))
                    self.histogramdata = parsemessage(histogram_event)
                    if not str(self.status).startswith("status: PROCESSING"):
                        break
            except Exception as e:
                #print ("Histogram Problem: {}".format(e))
                pass
            time.sleep(self.interval)
            pass


    def newchannelstatemonitor(self):
        while True:
            channel_states = self.rpc_connection.data.get_channel_states(wait_for_processing=True, first_channel=1,
                                                                         last_channel=self.channels)
            try:
                for state in channel_states:
                    for channel in state.channel_states:#print (state)
                        self.channelstates[int(channel.channel)]=channel.state_name
                        #print (channel.channel, channel.state_name, chanlookup(channel.channel), self.colourlookup[channel.state_name])
                        #(x,y) = chanlookup(channel.channel)
                        #(r,g,b) = self.colourlookup[channel.state_name]
                        #self.mylights.point(x,15-y,r,g,b)
                if not str(self.status).startswith("status: PROCESSING"):
                    break
            except:
                pass
            #time.sleep(self.interval)
            pass

    def dutytimemonitor(self):
        while True:
            log.debug("Duty Time Monitor Running", self.status)
            #log.debug(str(self.status))
            while str(self.status).startswith("status: PROCESSING"):
                #log.debug("fetching duty time")
                dutytime = self.rpc_connection.statistics.stream_duty_time(wait_for_processing=True,step=60)
                if self.args.verbose:
                    for duty in dutytime:
                        log.debug(duty)
            time.sleep(1)


    def runmonitor(self):
        while True:
            status_watcher = rpc.wrappers.StatusWatcher(self.rpc_connection)
            msgs = rpc.acquisition_service
            while True:
                for status in status_watcher.wait():
                    #log.info(status)
                    self.status = status
                    if str(self.status).startswith("status: STARTING"):
                        self.run_start()
                    if str(self.status).startswith("status: FINISHING"):
                        self.run_stop()
                    #log.debug(status)

    def update_minion_status(self):
        #### This block of code will update live information about a minION
        ### We may not yet have a run to acquire - if so the acquisition_data will be empty.

        acquisition_data=dict()

        if len(self.acquisition_data)<1:
            acquisition_data['state']="No Run"
            currentscript = "Nothing Running"
        else:
            acquisition_data = self.acquisition_data
            currentscript = str(self.rpc_connection.protocol.get_run_info().protocol_id)

        if len(self.disk_space_info)<1:
            self.disk_space_info = json.loads(
                MessageToJson(self.rpc_connection.instance.get_disk_space_info(), preserving_proto_field_name=True,
                              including_default_value_fields=True))
            #log.debug(self.disk_space_info)


    def get_channel_states(self):
        return self.channelstates

    def update_minion_stats (self):
        asictemp = self.temperaturedata.minion.asic_temperature.value
        heatsinktemp = self.temperaturedata.minion.heatsink_temperature.value
        biasvoltage = int(self.bias_voltage)
        voltage_val = int(self.bias_voltage)#todo this likely is wrong
        voltage_value = biasvoltage #todo check this = probably wrong
        yield_val = self.acquisition_data['yield_summary']['selected_events']
        read_count = self.acquisition_data['yield_summary']['read_count']
        channelpanda = pd.DataFrame.from_dict(self.channelstates, orient='index', dtype=None)
        channeldict=dict()
        channeldict["strand"]=0
        channeldict["adapter"]=0
        channeldict["good_single"]=0
        channeldict["pore"]=0
        try:
            channelpandastates = channelpanda.groupby([0,]).size()
            #print (channelpandastates)
            #log.debug(channelpandastates)
            for state, value in channelpandastates.iteritems():
                #log.debug(state, value)
            #    print (state,value)
                channeldict[state]=value
            #print ("\n\n\n\n\n\n")
            instrand = 0 #channeldict["strand"]+channeldict["adapter"]
            openpore = 0 #channeldict["good_single"]+channeldict["pore"]
            meanratio = 0 #todo work out if we can still do this
        except:
            meanratio=0
            instrand=0
            openpore=0
            pass




    def runinfo(self):
        while True:
            #log.debug("Checking run info")
            try:
                self.acquisition_data = parsemessage(self.rpc_connection.acquisition.get_acquisition_info())
            except:
                #log.debug("No active run")
                self.acquisition_data ={}
            self.temperaturedata = self.rpc_connection.device.get_temperature()
            self.disk_space_info = json.loads(MessageToJson(self.rpc_connection.instance.get_disk_space_info(), preserving_proto_field_name=True, including_default_value_fields=True))
            if str(self.device_type).startswith("PROMETHION"):
                self.minion_settings = self.rpc_connection.promethion_device.get_device_settings()
            else:
                self.minion_settings = self.rpc_connection.minion_device.get_settings()
            self.bias_voltage = json.loads(MessageToJson(self.rpc_connection.device.get_bias_voltage(),preserving_proto_field_name=True,including_default_value_fields=True))['bias_voltage']

            try:
                self.runinfo_api = self.rpc_connection.protocol.get_run_info()
            except:
                log.debug("Run Info not yet known.")
            try:
                self.sampleid = self.rpc_connection.protocol.get_sample_id()
            except:
                log.debug("Sample ID not yet known.")
            #log.debug("running update minion status")
            self.update_minion_status()
            if str(self.status).startswith("status: PROCESSING"):
                self.runinformation = self.rpc_connection.acquisition.get_current_acquisition_run()
                #log.debug(self.runinformation)
                try:
                    #log.debug("running update minion stats")
                    if hasattr(self, 'runid'):
                        self.update_minion_stats()
                except Exception as err:
                    log.error("Problem updating stats to device.", err)
                    pass

            time.sleep(self.interval)

    def sendmessage(self,severitylevel,message):
        self.rpc_connection.log.send_user_message(severity=severitylevel, user_message=message)

    def getmessages(self):
        while True:
            messages = self.rpc_connection.log.get_user_messages(include_old_messages=True)

            for message in messages:
                log.info(message.user_message)
                '''
                payload = {"minion": self.minion["url"],
                           "message": message.user_message,
                           "run": "",
                           "identifier": message.identifier,
                           "severity": message.severity,
                           "timestamp": message.time.ToDatetime().strftime('%Y-%m-%d %H:%M:%S.%f')[:-3],
                           }

                if self.runidlink:
                    payload["run"] = self.runidlink

  #              messagein = self.minotourapi.create_message( payload, self.minion)
            '''



class MinknowConnectRPC():
    def __init__(self,args,ip,mylights):
        self.ip = ip
        self.args = args
        log.debug("initialising minknow connection via rpc")
        self.mylights = mylights
        self.minIONdict=dict() #A dictionary to store minION connection data.
        devicemonitorthread = threading.Thread(target=self.devicemonitor, args=())
        devicemonitorthread.daemon = True  # Daemonize thread
        devicemonitorthread.start()

        lightfunctionthread = threading.Thread(target=self.lightchecker,args=())
        lightfunctionthread.daemon = True
        lightfunctionthread.start()

    def lightchecker(self):
        while True:
            #Loop through the list of MinIONs availble
            for minION in self.minIONdict:
                self.mylights.scrolling_write_text(minION)
                if "device_connection" in self.minIONdict[minION].keys():
                    self.mylights.scrolling_write_text(self.minIONdict[minION]["device_connection"].device_type,font_size=13,font_name=("minLights/fonts/7x13.bdf"))
                    self.mylights.scrolling_write_text(self.minIONdict[minION]["device_connection"].computer_name,font_size=13,font_name=("minLights/fonts/7x13.bdf"))
                    try:
                        print (self.minIONdict[minION]["device_connection"].flowcelldata)
                        for key in self.minIONdict[minION]["device_connection"].flowcelldata:
                            #print (key)
                            if isinstance(self.minIONdict[minION]["device_connection"].flowcelldata[key],str) and len(self.minIONdict[minION]["device_connection"].flowcelldata[key]) > 0:
                                self.mylights.scrolling_write_text("{}".format(self.minIONdict[minION]["device_connection"].flowcelldata[key]),font_size=13,font_name=("minLights/fonts/7x13.bdf"))
                    except Exception as err:
                        print ("Problem: {}".format(err))
                    #for line in self.mylights.scrolling_write_text(self.minIONdict[minION]["device_connection"].getflowcelldata()):
                    #    self.mylights.scrolling_write_text(line)

                    colourlookup = self.minIONdict[minION]["device_connection"].colourlookup
                    now = time.time()
                    prevchannel = dict()
                    while 1:
                        for channel in self.minIONdict[minION]["device_connection"].channelstates:
                            #print (now)
                            #print (channel,self.minIONdict[minION]["device_connection"].channelstates[channel])
                            (x,y) = chanlookup(channel)
                            (r,g,b) = colourlookup[self.minIONdict[minION]["device_connection"].channelstates[channel]]
                            if prevchannel.get(channel) != self.minIONdict[minION]["device_connection"].channelstates[channel]:
                                self.mylights.point(x,15-y,r,g,b)
                            prevchannel[channel] = self.minIONdict[minION]["device_connection"].channelstates[channel]
                            if time.time() > (now+60):
                                break
                        else:
                            continue
                        break

                    now = time.time()
                    print (self.minIONdict[minION]["device_connection"].histogramdata)
                    while 1:
                        scaled_hist = scale16(proc_hist_3(self.minIONdict[minION]["device_connection"].histogramdata['histogram_data']['buckets']))
                        self.mylights.matrix.Clear()
                        for idx, val in enumerate(scaled_hist):
                            # print(idx, val)
                            for i in range(15):
                                if i + 1 <= val:
                                    self.mylights.point(idx, 16 - (i + 1), 50, 50, 200)
                                else:
                                    self.mylights.point(idx, 16 - (i + 1), 0, 0, 0)
                            if time.time() > (now + 10):
                                break
                        else:
                            continue
                        break


    def devicemonitor(self):
        # -------------------------------------------------------------------------------
        # Connect to the running Manager instance:
        #
        # We can connect to minknow manager on port 9501.
        #
        channel = grpc.insecure_channel('{}:9501'.format(self.ip))
        stub = manager_grpc.ManagerServiceStub(channel)
        while True:
            # Send the list request
            list_request = manager.ListDevicesRequest()
            response = stub.list_devices(list_request)
            for device in response.active:
                #log.debug(device.name)
                deviceid = device.name
                if deviceid not in self.minIONdict:
                    self.minIONdict[deviceid] = dict()
                    self.minIONdict[deviceid]["state"] = "pending"
                if self.minIONdict[deviceid]["state"]!= "active":
                    log.info(device.ports)
                    self.minIONdict[deviceid]["grpc_port"] = device.ports.insecure_grpc
                    self.minIONdict[deviceid]["insecure_web"] = device.ports.insecure_web
                    log.debug(self.minIONdict[deviceid]["grpc_port"])
                    self.minIONdict[deviceid]["grpc_connection"] = rpc.Connection(
                        port=self.minIONdict[deviceid]["grpc_port"], host = self.args.host)

                    self.minIONdict[deviceid]["device_connection"] = DeviceConnect(self.args,
                                                                                   self.minIONdict[deviceid][
                                                                                       "grpc_connection"],
                                                                                   deviceid,self.mylights)
                    """
                    try:
                        self.minIONdict[deviceid]["device_connection"].connect()
                    except Exception as err:
                        
                        log.error("Problem connecting to device.", err)
                    """
                    self.minIONdict[deviceid]["state"]="active"
            time.sleep(5)

    def minIONnumber(self):
        return len(self.minIONdict)

    def get_minIONdetails(self):
        return (self.minIONdict)

    def disconnect_nicely(self):
        for device in self.minIONdict:
            log.info("Disconnecting {} from the server.".format(device))
            self.minIONdict[device]["device_connection"].disconnect_nicely()
        log.info("Stopped successfully.")

def scale16(hist):
    try:
        maxval = max(hist)
        scalehist=list()
        if maxval > 0:
            for i in hist:
                scalehist.append(int((i/maxval)*16))
            return scalehist
        else:
            return hist
    except:
        return hist

def proc_hist_3(histogram):
    binlist=list()
    binlength = len(histogram)
    try:
        for i in range(1,binlength):
            j = i*3 - 2
            if j <= binlength-1:
                binlist.append(int(histogram[j-1])+int(histogram[j])+int(histogram[j+1]))
            else:
                binlist.append(int(histogram[j-1])+int(histogram[j]))
        return  binlist
    except:
        return binlist

class myLightBoard():
    def __init__(self,args):
        # Build our lighting device.
        self.args=args
        self.options = RGBMatrixOptions()
        self.options.hardware_mapping = self.args.led_gpio_mapping
        self.options.rows = self.args.rows_led
        self.options.cols = self.args.cols_led
        self.options.chain_length = self.args.led_chain
        self.options.parallel = self.args.led_parallel
        # self.options.row_address_type = self.args.led_row_addr_type
        # self.options.multiplexing = self.args.led_multiplexing
        self.options.pwm_bits = self.args.led_pwm_bits
        self.options.brightness = self.args.led_brightness
        self.options.pwm_lsb_nanoseconds = self.args.led_pwm_lsb_nanoseconds
        # self.options.led_rgb_sequence = self.args.led_rgb_sequence
        # self.options.pixel_mapper_config = self.args.led_pixel_mapper
        if self.args.led_show_refresh:
            self.options.show_refresh_rate = 1
        if self.args.led_slowdown_gpio != None:
            self.options.gpio_slowdown = self.args.led_slowdown_gpio
        # if args.led_no_hardware_pulse:
        #    options.disable_hardware_pulsing = True

        self.matrix = RGBMatrix(options=self.options)
        self.scrolling_write_text("Lights Connected.", speed=0.01)


    def write_text_inst_two(self,message1,color1,message2,color2,font_name,font_name2):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        #color1 = graphics.Color(255, 255, 255)
        #color2 = graphics.Color(255, 255, 255)
        color1 = "Blue"
        color2 = "Green"
        #font1 = graphics.Font()
        #font1.LoadFont("minLights/fonts/5x7.bdf")
        font1 = ImageFont.load("minLights/fonts/4x6.pil")
        #font2 = graphics.Font()
        font2 = ImageFont.load("minLights/fonts/5x7.pil")
        #pos = 16
        #pos2 = 16
        #offscreen_canvas.Clear()
        #len = graphics.DrawText(offscreen_canvas,font1,pos,7,color1,message1)
        #len = graphics.DrawText(offscreen_canvas,font2,pos2,7,color2,message2)
        #offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)

        image = Image.new("1", (320, 200))
        image = image.convert("RGBA")
        draw = ImageDraw.Draw(image)
        x=32
        while True:
            draw.text((0,0), message1, font=font1, fill=color1)
            draw.text((0, 9), message2, font=font1, fill=color2)
            self.matrix.Clear()
        #self.matrix.SetImage(image.convert('RGB'))
            self.matrix.SetImage(image.convert('RGB'), x, 0)
            x-=1
            if x <= -320:
                break
            time.sleep(0.02)





    def scrolling_write_text(self,text,font_size=7,font_name=("minLights/fonts/5x7.bdf"),font_colour = graphics.Color(255, 255, 255), speed = 0.025):
        offscreen_canvas = self.matrix.CreateFrameCanvas()
        font = graphics.Font()
        font.LoadFont(font_name)
        pos = offscreen_canvas.width
        while True:
            offscreen_canvas.Clear()
            len = graphics.DrawText(offscreen_canvas, font, pos, font_size, font_colour,
                                    text)
            pos -= 1
            if (pos + len < 0):
                pos = offscreen_canvas.width
                break
            time.sleep(speed)
            offscreen_canvas = self.matrix.SwapOnVSync(offscreen_canvas)


    def point(self,x,y,r,g,b):
        self.matrix.SetPixel(x,y,r,g,b)





def main():
    extra_args = ()
    """
    extra_args = (
        (
            "--toml",
            dict(
                metavar="TOML",
                required=True,
                help="TOML file specifying experimental parameters",
            ),
        ),
    )"""
    parser, args = get_parser(extra_args=extra_args, file=__file__)

    logging.basicConfig(
        level=logging.DEBUG,
        format=args.log_format,
        filename=args.log_file,
        filemode="w",
    )

    # define a Handler that writes INFO messages or higher to the sys.stderr
    console = logging.StreamHandler()
    console.setLevel(logging.INFO)

    # set a format which is simpler for console use
    formatter = logging.Formatter(args.log_format)
    console.setFormatter(formatter)

    # add the handler to the root logger
    logging.getLogger("").addHandler(console)

    # Start by logging sys.argv and the parameters used
    logger = logging.getLogger("MinLights")
    logger.info(" ".join(sys.argv))
    print_args(args, logger=logger)


    mylights = myLightBoard(args)

    #For each IP we want to set up a class to contain it and all its devices.

    devices = MinknowConnectRPC(args,args.host,mylights)

    try:

        while True:
            #log.info(devices.minIONnumber())
            #log.info(devices.get_minIONdetails())
            for minION, values in devices.get_minIONdetails().items():
                #log.info(minION)

                #log.info(values.keys())

                if "device_connection" in values.keys():
                    log.info(values['device_connection'].computer_name)
            time.sleep(1)

    except KeyboardInterrupt:

        devices.disconnect_nicely()





