import AtomEnsemble as ae

class Reader(object):
    def __str__(self):
        ost = "framepos: " + str(self.framepos) + "\nframelength: " + str(self.framelength) + "\nFrameindex: " + str(self.frameindex)
        return ost


    def __init__(self, fileobj=None):
        if type(fileobj) == str:
            self.filehandle = open(fileobj)
        elif type(fileobj) == file:
            self.filehandle = fileobj

        self.framepos = 0
        self.intraframepos = 0
        self.framelength = 0
        self.frameindex = {0: 0}
        self.frameindex_complete = False

    def _get_next_frame_start(self, seek=None, frame_length=None, preamble_length=None, marker=None):

        #throw exception if neither marker nor frame_length are specified
        if (marker is None) and (frame_length is None):
            raise ValueError("Missing required arguments: Either marker or frame_length required")

        #seek if specified
        if seek != None:
            self.filehandle.seek(seek)

        #skip preamble if specified
        if self.filehandle.tell() = 0:
            if preamble_length != None:
                for i in xrange(preamble_length):
                    self.filehandle.readline()

        #read frame_length lines if specified and return position
        if frame_length != None:
            for i in xrange(frame_length):
                self.filehandle.readline()
            return self.filehandle.tell()

        #else read until marker occurs, return tell from line prior
        elif marker != None:
            line = ""
            last_tell = self.filehandle.tell()
            while marker not in line:
                line = self.filehandle.readline()
                last_tell = self.filehandle.tell()
            return last_tell

    def _read_preamble(self):
        # implement read preamble here
        return Null

    def _get_frame_length(self):
        # implement get frame length here
        return Null

    def _get_frame(self, seek=None, frame_length=None, marker=None):

        #seek if specified
        if seek != None:
            self.filehandle.seek(seek)

        #read frame_length lines if specified and return position
        if frame_length != None:
            for i in xrange(frame_length):
                self.filehandle.readline()
                # parser code here

        #else read until marker occurs, return tell from line prior
        elif marker != None:
            line = ""
            while marker not in line:
                line = self.filehandle.readline()
                # parser code here

    def __getitem__(self, framenum=None):
        print "fn" + str(framenum)
        print self.frameindex

        #deal with slices
        if type(framenum) = slice:
            collector = []
            for i in range(slice):
                collector.append(self.__getitem__(framenum=i))
            return collector

        #get frame length if unknown
        if self.framelength == 0:
            self.framelength = self._get_frame_length()

        #frame known and positive
        if framenum in frameindex:
            return self.get_frame(seek=self.frameindex[framenum], frame_length=self.framelength)

        #frame unknown and positive
        elif framenum > -1:
            for i in xrange(framenum+1):
                if i == framenum:
                    return self.get_frame(seek=self.frameindex[framenum], frame_length=self.framelength)
                elif i in self.frameindex:
                    pass
                else:
                    self.frameindex[i+1] = self._get_next_frame_start(seek=self.frameindex[i], frame_length = self.framelength)

        #frame negative
        elif framenum < 0:
            #last frame unknown
            if self.frameindex_complete == False:
                i = 0
                try:
                    while True:
                        if i in self.frameindex:
                            pass
                        else:
                            self.frameindex[i+1] = self._get_next_frame_start(seek=self.frameindex[i], frame_length = self.framelength)
                        i += 1
                except:
                    self.frameindex_complete = True
            #last frame known
            return self.get_frame(seek=self.frameindex[len(self.frameindex) - framenum], frame_length=self.framelength)

class XYZReader(object):

    def __str__(self):
        ost = "framepos: " + str(self.framepos) + "\nframelength: " + str(self.framelength) + "\nFrameindex: " + str(self.frameindex)
        return ost


    def __init__(self, fileobj=None):
        if type(fileobj) == str:
            self.filehandle = open(fileobj)
        elif type(fileobj) == file:
            self.filehandle = fileobj

        self.framepos = 0
        self.intraframepos = 0
        self.framelength = 0
        self.frameindex = {0: 0}

    def __getitem__(self, framenum=None):
        print "fn" + str(framenum)
        print self.frameindex

        if self.framelength == 0:
            self.filehandle.seek(0)
            self.framelength = int(self.filehandle.readline().strip()) + 2
            self.filehandle.seek(0)
            self.framepos = 0

        try:
            self.filehandle.seek(self.frameindex[framenum])
            self.framepos = framenum
        except:
            for i in range(framenum-1, -1, -1):
                try:
                    self.filehandle.seek(self.frameindex[i])
                    self.framepos = i
                    for j in range(i+1, framenum):
                        for k in range(self.framelength):
                            self.filehandle.readline()
                        self.frameindex[j] = self.fileindex.tell()
                        self.framepos = j
                    break
                except:
                    pass

        self.intraframepos = 0
        ensemble = ae.AtomEnsemble()
        ensemble.filename = self.filehandle.name
        self.framelength = int(self.filehandle.readline().strip()) + 2
        ensemble.boxvector = float(self.filehandle.readline().strip())
        ensemble.framenumber = self.framepos
        self.intraframepos += 1

        while self.intraframepos < self.framelength:
            atomproperties = dict()
            elements = self.filehandle.readline().strip().split()
            atomproperties['element'] = elements[0]
            atomproperties['coordinate'] = [float(elements[1]), float(elements[2]), float(elements[3])]
            if len(elements) > 4:
                atomproperties['mass'] = float(elements[4])
            if len(elements) > 5:
                atomproperties['charge'] = float(elements[5])
            if len(elements) > 8:
                atomproperties['velocity'] = [float(elements[6]), float(elements[7]), float(elements[8])]
            if len(elements) > 11:
                atomproperties['force'] = [float(elements[9]), float(elements[10]), float(elements[11])]
            if len(elements) > 12:
                atomproperties['molecule_index'] = int(elements[12])

            ensemble.append(ae.Atom(**atomproperties))
            self.intraframepos += 1

        self.intraframepos = 0
        self.framepos += 1
        self.frameindex[str(self.framepos)] = self.filehandle.tell()
        return ensemble

class DLP2HReader(object):

    def __init__(self, fileobj=None):
        if type(fileobj) == str:
            self.filehandle = open(fileobj)
        elif type(fileobj) == file:
            self.filehandle = fileobj

        self.framepos = 0
        self.intraframepos = 0
        self.framelength = 0
        self.frameindex = {"0":0}

    def __getitem__(self, framenum=None):
        print "fn" + str(framenum)
        if framenum != None:
            print self.frameindex
            if framenum != self.framepos:
                if self.frameindex:
                    try:
                        self.filehandle.seek(self.frameindex[str(framenum)])
                    except:
                        if self.framepos > framenum:
                            self.filehandle.seek(0)
                            self.framepos = 0
                            self.intraframepos = 0

                        if self.intraframepos:
                            while self.intraframepos < self.framelength:
                                self.filehandle.readline()
                                self.intraframepos += 1
                            self.intraframepos = 0
                            self.framepos += 1

                        self.frameindex[str(self.framepos)] = self.fileindex.tell()

                        while self.framepos < framenum:
                            self.framelength = int(self.filehandle().strip()) +2
                            self.intraframepos += 1
                            while self.intraframepos < self.framelength:
                                self.filehandle.readline()
                                self.intraframepos += 1
                            self.intraframepos = 0
                            self.framepos += 1
                            self.frameindex[str(self.framepos)] = self.fileindex.tell()

        ensemble = ae.AtomEnsemble()
        ensemble.filename = self.filehandle.name
        self.framelength = int(self.filehandle.readline().strip())+2
        ensemble.boxvector = float(self.filehandle.readline().strip())
        ensemble.framenumber = self.framepos
        self.intraframepos += 2

        while self.intraframepos < self.framelength:
            atomproperties = dict()
            elements = self.filehandle.readline().strip().split()
            atomproperties['element'] = elements[0]
            atomproperties['coordinate'] = [float(elements[1]), float(elements[2]), float(elements[3])]
            if len(elements) > 4:
                atomproperties['mass'] = float(elements[4])
            if len(elements) > 5:
                atomproperties['charge'] = float(elements[5])
            if len(elements) > 8:
                atomproperties['velocity'] = [float(elements[6]), float(elements[7]), float(elements[8])]
            if len(elements) > 11:
                atomproperties['force'] = [float(elements[9]), float(elements[10]), float(elements[11])]
            if len(elements) > 12:
                atomproperties['molecule_index'] = int(elements[12])

            ensemble.append(ae.Atom(**atomproperties))
            self.intraframepos += 1

        self.intraframepos = 0
        self.framepos += 1
        self.frameindex[str(self.framepos)] = self.filehandle.tell()
        return ensemble
