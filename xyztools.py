import AtomEnsemble as ae

class Reader(object):
    def __str__(self):
        ost = "Framelength: " + str(self.framelength) + "\nFrameindex: " + str(self.frameindex)
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

    def _get_frame(self, seek=None, frame_length=None, marker=None, frame_number=None):

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
            return self.get_frame(seek=self.frameindex[framenum], frame_length=self.framelength, frame_number=framenum)

        #frame unknown and positive
        elif framenum > -1:
            for i in xrange(framenum+1):
                if i == framenum:
                    return self.get_frame(seek=self.frameindex[framenum], frame_length=self.framelength, frame_number=framenum)
                elif i in self.frameindex:
                    pass
                else:
                    self.frameindex[i+1] = self._get_next_frame_start(seek=self.frameindex[i], frame_length = self.framelength, frame_number=framenum)

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

class XYZReader(Reader):

    def _get_frame_length(self):
        # implement get frame length here
        self.filehandle.seek(0)
        return int(self.filehandle.readline().strip())

    def _get_frame(self, seek=None, frame_length=None, marker=None, frame_number=None):

        #seek if specified
        if seek != None:
            self.filehandle.seek(seek)

        #read frame_length lines if specified and return position
        if frame_length != None:
            atomproperties = dict()
            ensemble = ae.AtomEnsemble()

            ensemble.filename = self.filehandle.name
            ensemble.framenumber = frame_number

            for i in xrange(frame_length):
                line = self.filehandle.readline().strip()
                if i == 1:
                    ensemble.boxvector=float(line)
                elif i > 1:
                    elements = line.split()
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

        return ensemble

class DLP2HReader(Reader):

    def __init__(self, fileobj=None):
        super.__init__(fileobj)
        _read_preamble()

    def _read_preamble(self):
        self.filehandle.seek(0)
        self.header = self.filehandle.readline().strip()

        elements = self.filehandle.readline().strip().split()
        self.trajectory_key = int(elements[0])
        self.periodic_key = int(elements[1])
        self.number_atoms = int(elements[2])

        self.frameindex[0] = self.filehandle.tell()

        self.framelength = (self.trajectory_key+2) * self.number_atoms

        if self.periodic_key:
            self.framelength += 4
        else:
            self.framelength += 1

    def _get_frame_length(self):
        # implement get frame length here
        if self.framelength == 0:
            self._read_preamble()
        return self.framelength

    def _get_frame(self, seek=None, frame_length=None, marker=None, frame_number=None):

        #seek if specified
        if seek != None:
            self.filehandle.seek(seek)

        #read frame_length lines if specified and return position
        if frame_length != None:
            atomproperties = dict()
            ensemble = ae.AtomEnsemble()

            ensemble.filename = self.filehandle.name
            ensemble.framenumber = frame_number

            atoms_start = 1
            if self.periodic_key > 0:
                atoms_start += 3
            atom_length = self.trajectory_key + 2
            atomproperties = dict()

            for i in xrange(frame_length):
                elements = self.filehandle.readline().strip().split()
                atom_position = (i - atom_start)%atom_length
                if i == 0:
                    ensemble.timestep = int(elements[1])
                    ensemble.time = float(elements[5])
                    if elements[0].strip() is not "timestep":
                        raise SyntaxError("Word timestep not found. Frame:" + str(frame_number) + ", Line:" + str(i))
                elif self.periodic_key and (i == 1):
                    ensemble.boxvector = float(elements[0])
                elif atom_position == 0:
                    atomproperties['element'] = elements[0]
                    atomproperties['mass'] = float(elements[2])
                    atomproperties['charge'] = float(elements[3])

                elif atom_position == 1:
                    atomproperties['velocity'] = [float(elements[0]), float(elements[1]), float(elements[2])]

                elif atom_position == 2:
                    atomproperties['force'] = [float(elements[0]), float(elements[1]), float(elements[2])]

                if atom_position == (atom_length-1):
                    ensemble.append(ae.Atom(**atomproperties))
                    atomproperties = dict()

            return ensemble

class Writer(object):

    def __init__(self, fileobj=None, overwrite=False):
        if type(fileobj) == str:
            if overwrite:
                self.filehandle = open(fileobj, "w")
            else:
                self.filehandle = open(fileobj, "a")
        elif type(fileobj) == file:
            self.filehandle = fileobj

    def __del__(self):
        if self.filehandle:
            self.filehandle.close()

    def write(self, frame=None, preamble=True):
        if frame:
            if type(frame) is list:
                self.write(frame=frame[0])
                for f in frame[1:]:
                    self.write(f, preamble=False)

            if preamble:
                self._write_global_preamble(frame)
            self._write_frame_preamble(frame)
            self._write_main(frame)

    def _write_global_preamble(self, frame=None):
        pass

    def _write_frame_preamble(self, frame=None):
        pass

    def _write_main(self, frame=None):
        pass
