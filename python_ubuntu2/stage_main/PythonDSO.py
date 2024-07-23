#! /usr/bin/env python
# coding: utf-8
# Teledynelecroy VICP sample
# 2017/10/5 Fumiaki Sato
# This is only Python3
# $ Python3 PythonDSO.py

import struct
# import sys
import socket


class LecroyBinFormat:
    def __init__(self, wfdata):
        # Align start position
        for n in range(40):
            if wfdata[n] == 0x23 and wfdata[n+1] == 0x39:
                stp = n+11
        wfdata = wfdata[stp:]
        # Endian
        if struct.unpack('h', wfdata[34:34+2])[0] == 0:
            endian = '>'
        else:
            endian = '<'

        self.DESCRIPTOR_NAME = struct.unpack(
            endian+'16s', wfdata[0:16])[0].decode('UTF-8')
        self.TEMPLATE_NAME = struct.unpack(
            endian+'16s', wfdata[16:16+16])[0].decode('UTF-8')
        self.COMM_TYPE = struct.unpack(endian+'H', wfdata[32:32+2])[0]
        self.COMM_ORDER = struct.unpack(endian+'H', wfdata[34:34+2])[0]
        self.WAVE_DESCRIPTOR = struct.unpack(endian+'I', wfdata[36:36+4])[0]
        self.USER_TEXT = struct.unpack(endian+'I', wfdata[40:40+4])[0]
        self.RES_DESC = struct.unpack(endian+'I', wfdata[44:44+4])[0]
        self.TRIGTIME_ARRAY = struct.unpack(endian+'I', wfdata[48:48+4])[0]
        self.RIS_TIME_ARRAY = struct.unpack(endian+'I', wfdata[52:52+4])[0]
        self.RES_TIME_ARRAY = struct.unpack(endian+'I', wfdata[56:56+4])[0]
        self.WAVE_ARRAY_1 = struct.unpack(endian+'I', wfdata[60:60+4])[0]
        self.WAVE_ARRAY_2 = struct.unpack(endian+'I', wfdata[64:64+4])[0]
        self.RES_ARRAY_2 = struct.unpack(endian+'I', wfdata[68:68+4])[0]
        self.RES_ARRAY_3 = struct.unpack(endian+'I', wfdata[72:72+4])[0]
        self.INSTRUMENT_NAME = struct.unpack(
            endian+'16s', wfdata[76:76+16])[0].decode('UTF-8')
        self.INSTRUMENT_NUMBER = struct.unpack(endian+'I', wfdata[92:92+4])[0]
        self.TRACE_LABEL = struct.unpack(
            endian+'16s', wfdata[96:96+16])[0].decode('UTF-8')
        self.WAVE_ARRAY_COUNT = struct.unpack(endian+'I', wfdata[116:116+4])[0]
        self.PNTS_PER_SCREEN = struct.unpack(endian+'I', wfdata[120:120+4])[0]
        self.FIRST_VALID_PNT = struct.unpack(endian+'I', wfdata[124:124+4])[0]
        self.LAST_VALID_PNT = struct.unpack(endian+'I', wfdata[128:128+4])[0]
        self.FIRST_POINT = struct.unpack(endian+'I', wfdata[132:132+4])[0]
        self.SPARSING_FACTOR = struct.unpack(endian+'I', wfdata[136:136+4])[0]
        self.SEGMENT_INDEX = struct.unpack(endian+'I', wfdata[140:140+4])[0]
        self.SUBARRAY_COUNT = struct.unpack(endian+'I', wfdata[144:144+4])[0]
        self.SWEEPS_PER_ACQ = struct.unpack(endian+'I', wfdata[148:148+4])[0]
        self.POINTS_PER_PAIR = struct.unpack(endian+'H', wfdata[152:152+2])[0]
        self.PAIR_OFFSET = struct.unpack(endian+'H', wfdata[154:154+2])[0]
        self.VERTICAL_GAIN = struct.unpack(endian+'f', wfdata[156:156+4])[0]
        self.VERTICAL_OFFSET = struct.unpack(endian+'f', wfdata[160:160+4])[0]
        self.MAX_VALUE = struct.unpack(endian+'f', wfdata[164:164+4])[0]
        self.MIN_VALUE = struct.unpack(endian+'f', wfdata[168:168+4])[0]
        self.NOMINAL_BITS = struct.unpack(endian+'H', wfdata[172:172+2])[0]
        self.NOM_SUBARRAYT_COUNT = struct.unpack(
            endian+'H', wfdata[174:174+2])[0]
        self.HORIZ_INTERVAL = struct.unpack(endian+'f', wfdata[176:176+4])[0]
        self.HORIZ_OFFSET = struct.unpack(endian+'d', wfdata[180:180+8])[0]
        self.PIXEL_OFFSET = struct.unpack(endian+'d', wfdata[188:188+8])[0]
        self.TIMESTAMP_SEC = struct.unpack(endian+'d', wfdata[296:296+8])[0]
        self.TIMESTAMP_MIN = struct.unpack(endian+'B', wfdata[304:304+1])[0]
        self.TIMESTAMP_HOURS = struct.unpack(endian+'B', wfdata[305:305+1])[0]
        self.TIMESTAMP_DAYS = struct.unpack(endian+'B', wfdata[306:306+1])[0]
        self.TIMESTAMP_MONTHS = struct.unpack(endian+'B', wfdata[307:307+1])[0]
        self.TIMESTAMP_YEAR = struct.unpack(endian+'H', wfdata[308:308+2])[0]
        self.ACQ_DURATION = struct.unpack(endian+'f', wfdata[312:312+4])[0]
        self.RECORD_TYPE = struct.unpack(endian+'H', wfdata[316:316+2])[0]
        self.PROCESSING_DONE = struct.unpack(endian+'H', wfdata[318:318+2])[0]
        self.RIS_SWEEPS = struct.unpack(endian+'H', wfdata[322:322+2])[0]
        self.TIMEBASE = struct.unpack(endian+'H', wfdata[324:324+2])[0]
        self.VERT_COUPLING = struct.unpack(endian+'H', wfdata[326:326+2])[0]
        self.PROBE_ATT = struct.unpack(endian+'f', wfdata[328:328+4])[0]
        self.FIXED_VERT_GAIN = struct.unpack(endian+'H', wfdata[332:332+2])[0]
        self.BANDWIDTH_LIMIT = struct.unpack(endian+'H', wfdata[334:334+2])[0]
        self.VERTICAL_VERNIER = struct.unpack(endian+'f', wfdata[336:336+4])[0]
        self.ACQ_VERT_OFFSET = struct.unpack(endian+'f', wfdata[340:340+4])[0]
        self.WAVE_SOURCE = struct.unpack(endian+'H', wfdata[344:344+2])[0]
        if self.COMM_TYPE == 0:
            self.ad_value = struct.unpack(endian+str(self.WAVE_ARRAY_COUNT)+'b',
                                          wfdata[self.WAVE_DESCRIPTOR:self.WAVE_DESCRIPTOR+self.WAVE_ARRAY_COUNT])
        else:
            self.ad_value = struct.unpack(endian+str(self.WAVE_ARRAY_COUNT)+'h',
                                          wfdata[self.WAVE_DESCRIPTOR:self.WAVE_DESCRIPTOR+self.WAVE_ARRAY_COUNT*2])

    def view_description(self):
        print("DESCRIPTOR_NAME: "+self.DESCRIPTOR_NAME)
        print("TEMPLATE_NAME: "+self.TEMPLATE_NAME)
        print("COMM_TYPE: "+str(self.COMM_TYPE))
        print("COMM_ORDER: "+str(self.COMM_ORDER))
        print("WAVE_DESCRIPTOR: "+str(self.WAVE_DESCRIPTOR))
        print("USER_TEXT: "+str(self.USER_TEXT))
        print("RES_DESC: "+str(self.RES_DESC))
        print("TRIGTIME_ARRAY: "+str(self.TRIGTIME_ARRAY))
        print("RIS_TIME_ARRAY: "+str(self.RIS_TIME_ARRAY))
        print("RES_TIME_ARRAY: "+str(self.RES_TIME_ARRAY))
        print("WAVE_ARRAY_1: "+str(self.WAVE_ARRAY_1))
        print("WAVE_ARRAY_2: "+str(self.WAVE_ARRAY_2))
        print("RES_ARRAY_2: "+str(self.RES_ARRAY_2))
        print("RES_ARRAY_3: "+str(self.RES_ARRAY_3))
        print("INSTRUMENT_NAME: "+self.INSTRUMENT_NAME)
        print("INSTRUMENT_NUMBER: "+str(self.INSTRUMENT_NUMBER))
        print("TRACE_LABEL: "+self.TRACE_LABEL)
        print("WAVE_ARRAY_COUNT: "+str(self.WAVE_ARRAY_COUNT))
        print("PNTS_PER_SCREEN: "+str(self.PNTS_PER_SCREEN))
        print("FIRST_VALID_PNT: "+str(self.FIRST_VALID_PNT))
        print("LAST_VALID_PNT: "+str(self.LAST_VALID_PNT))
        print("FIRST_POINT: "+str(self.FIRST_POINT))
        print("SPARSING_FACTOR: "+str(self.SPARSING_FACTOR))
        print("SEGMENT_INDEX: "+str(self.SEGMENT_INDEX))
        print("SUBARRAY_COUNT: "+str(self.SUBARRAY_COUNT))
        print("SWEEPS_PER_ACQ: "+str(self.SWEEPS_PER_ACQ))
        print("POINTS_PER_PAIR: "+str(self.POINTS_PER_PAIR))
        print("PAIR_OFFSET: "+str(self.PAIR_OFFSET))
        print("VERTICAL_GAIN: "+str(self.VERTICAL_GAIN))
        print("VERTICAL_OFFSET: "+str(self.VERTICAL_OFFSET))
        print("MAX_VALUE: "+str(self.MAX_VALUE))
        print("MIN_VALUE: "+str(self.MIN_VALUE))
        print("NOMINAL_BITS: "+str(self.NOMINAL_BITS))
        print("NOM_SUBARRAYT_COUNT: "+str(self.NOM_SUBARRAYT_COUNT))
        print("HORIZ_INTERVAL: "+str(self.HORIZ_INTERVAL))
        print("HORIZ_OFFSET: "+str(self.HORIZ_OFFSET))
        print("PIXEL_OFFSET: "+str(self.PIXEL_OFFSET))
        print("TIMESTAMP_SEC: "+str(self.TIMESTAMP_SEC))
        print("TIMESTAMP_MIN: "+str(self.TIMESTAMP_MIN))
        print("TIMESTAMP_HOURS: "+str(self.TIMESTAMP_HOURS))
        print("TIMESTAMP_DYAS: "+str(self.TIMESTAMP_DAYS))
        print("TIMESTAMP_MONTHS: "+str(self.TIMESTAMP_MONTHS))
        print("TIMESTAMP_YEAR: "+str(self.TIMESTAMP_YEAR))
        print("ACQ_DURATION: "+str(self.ACQ_DURATION))
        print("RECORD_TYPE: "+str(self.RECORD_TYPE))
        print("PROCESSING_DONE: "+str(self.PROCESSING_DONE))
        print("RIS_SWEEPS: "+str(self.RIS_SWEEPS))
        print("TIMEBASE: "+str(self.TIMEBASE))
        print("VERT_COUPLING: "+str(self.VERT_COUPLING))
        print("PROBE_ATT: "+str(self.PROBE_ATT))
        print("FIXED_VERT_GAIN: "+str(self.FIXED_VERT_GAIN))
        print("BANDWIDTH_LIMIT: "+str(self.BANDWIDTH_LIMIT))
        print("VERTICAL_VERNIER: "+str(self.VERTICAL_VERNIER))
        print("ACQ_VERT_OFFSET: "+str(self.ACQ_VERT_OFFSET))
        print("WAVE_SOURCE: "+str(self.WAVE_SOURCE))

    def integer_waveform(self):
        return self.ad_value

    def scaled_waveform(self):
        scaled_wf = []
        for i in range(self.WAVE_ARRAY_COUNT):
            scaled_wf.append(
                self.ad_value[i]*self.VERTICAL_GAIN-self.VERTICAL_OFFSET)
        return scaled_wf

    def scaled_waveform_withtime(self):
        scaled_wf = []
        sample_tim = []
        for i in range(self.WAVE_ARRAY_COUNT):
            scaled_wf.append(
                self.ad_value[i]*self.VERTICAL_GAIN-self.VERTICAL_OFFSET)
            sample_tim.append(self.HORIZ_INTERVAL*i+self.HORIZ_OFFSET)
        swwt = [sample_tim, scaled_wf]
        return swwt


class LecroyVICP:
    def __init__(self, ipadd):
        port = 1861
        self.sock = socket.socket()
        self.sock.connect((ipadd, port))

    def disconnect(self):
        self.sock.close()

    def writestring(self, cmdstr):
        cmdstr += '\n'
        cmdlen = len(cmdstr)
        sbuff = struct.pack(">Bbbbi"+str(cmdlen)+"s", 129,
                            1, 0, 0, cmdlen, cmdstr.encode("UTF-8"))
        self.sock.send(sbuff)

    def readstring(self, maxsize):
        temp = self.sock.recv(maxsize)
        datasize = len(temp)
        n = 0
        while datasize-1 > n:
            n += 4
            i = struct.unpack('>i', temp[n:n+4])[0]
            n += 4
            if n == 8:
                ret = temp[n:n+i]
            else:
                ret += temp[n:n+i]
            n += i
        return ret.decode('UTF-8')

    def readbinary(self, maxsize):
        beof = False
        lpout = False
        temp = []
        iseglength = 0
        lp = 0
        while lpout == False:
            if (len(temp) == 0):
                temp = self.sock.recv(maxsize)
            if len(temp) > 0:
                flg = temp[0] & 0x81
                if flg == 0x80:
                    beof = False
                    iseglength = struct.unpack('>i', temp[4:8])[0]
                    temp = temp[8:]
                elif flg == 0x81:
                    beof = True
                    iseglength = struct.unpack('>i', temp[4:8])[0]
                    temp = temp[8:]
                else:
                    print("unexpected data")
                    return
                while len(temp) < iseglength:
                    temp += self.sock.recv(maxsize)

                if len(temp) >= iseglength:
                    if lp == 0:
                        ret = temp[:iseglength]
                    else:
                        ret += temp[:iseglength]
                    lp += 1
                    temp = temp[iseglength:]
                    if beof == True:
                        lpout = True
        return ret

    def get_scaled_waveform(self, source_tr):
        self.writestring('CHDR OFF;CORD LO;CFMT DEF9,WORD,BIN')
        self.writestring(source_tr+':wf?')
        dat = self.readbinary(1000000)
        wf = LecroyBinFormat(dat)
        return wf.scaled_waveform()

    def get_scaled_waveform_withtime(self, source_tr):
        self.writestring('CHDR OFF;CORD LO;CFMT DEF9,WORD,BIN')
        self.writestring(source_tr+':wf?')
        dat = self.readbinary(1000000)
        wf = LecroyBinFormat(dat)
        return wf.scaled_waveform_withtime()

    def get_integer_waveform(self, source_tr):
        self.writestring('CHDR OFF;CORD LO;CFMT DEF9,WORD,BIN')
        self.writestring(source_tr+':wf?')
        dat = self.readbinary(1000000)
        wf = LecroyBinFormat(dat)
        return wf.integer_waveform()

    def get_byte_waveform(self, source_tr):
        self.writestring('CHDR OFF;CORD LO;CFMT DEF9,BYTE,BIN')
        self.writestring(source_tr+':wf?')
        dat = self.readbinary(1000000)
        wf = LecroyBinFormat(dat)
        return wf.integer_waveform()

    def get_parameter_value(self, source_tr, paramname):
        self.writestring('CHDR OFF;CORD LO')
        self.writestring(source_tr+':PAVA? '+paramname)
        return self.readstring(256)

    def store_hardcopy_to_file(self, imgtype, imgoption, filepath):
        self.writestring('CHDR OFF;CORD LO')
        self.writestring('HCSU DEV,'+imgtype+';HCSU PORT,NET')
        if imgoption != '':
            self.writestring('HCSU '+imgoption)
        self.writestring('SCDP')
        img = self.readbinary(1000000)
        f = open(filepath, 'wb')
        f.write(img)
        f.close

    def store_trc_to_file(self, source_tr, filepath):
        self.writestring('CHDR OFF;CORD LO;CFMT DEF9,WORD,BIN')
        self.writestring(source_tr+':wf?')
        dat = self.readbinary(1000000)
        for n in range(40):
            if dat[n] == 0x23 and dat[n+1] == 0x39:
                stp = n
        dat = dat[stp:]
        f = open(filepath, 'wb')
        f.write(dat)
        f.close


if __name__ == "__main__":
    # Please modify below argument to your dso ipaddress
    dso = LecroyVICP('192.168.1.100')

    # dso.store_hardcopy_to_file('BMP','','test3.bmp')

    # dso.writestring('*opc?')
    # b=dso.readstring(100)
    # print(b)

    # dso.writestring('C1:WF?')
    # dat=dso.readbinary(100000)

    dat = dso.get_parameter_value('C1', 'AMPL')

    # dat=dso.get_scaled_waveform_withtime('C1')

    # dso.store_trc_to_file('C1','/media/EAC7-E1B3/retval.trc')

    print(dat)
    dso.disconnect()
