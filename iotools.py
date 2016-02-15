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
        self.n = 0

    def __iter__(self):
        self.n = -1
        print "IterStart"
        return self

    def next(self):
        self.n += 1
        try:
            print "Iter " + str(self.n)
            return self.__getitem__(self.n)
        except EOFError:
            raise StopIteration
        #self.n += 1
        #print "Iter " + str(self.n)

    def __len__(self):
        if self.frameindex_complete == False:
            self._populate_frameindex()
        return len(self.frameindex)

    def _get_next_frame_start(self, seek=None, frame_length=None, preamble_length=None, marker=None):

        #throw exception if neither marker nor frame_length are specified
        if (marker is None) and (frame_length is None):
            raise ValueError("Missing required arguments: Either marker or frame_length required")

        #seek if specified
        if seek != None:
            self.filehandle.seek(seek)

        #skip preamble if specified
        if self.filehandle.tell() == self.frameindex[0]:
            if preamble_length != None:
                for _ in xrange(preamble_length):
                    if len(self.filehandle.readline()) == 0:
                        raise EOFError

        #read frame_length lines if specified and return position
        if frame_length != None:
            for _ in xrange(frame_length):
                if len(self.filehandle.readline()) == 0:
                    raise EOFError
            return self.filehandle.tell()

        #else read until marker occurs, return tell from line prior
        elif marker != None:
            line = ""
            last_tell = self.filehandle.tell()
            while marker not in line:
                line = self.filehandle.readline()
                if len(line) == 0:
                    raise EOFError
                last_tell = self.filehandle.tell()
            return last_tell

    def _read_preamble(self):
        # implement read preamble here
        return None

    def _get_frame_length(self):
        # implement get frame length here
        return None

    def _get_frame(self, seek=None, frame_length=None, marker=None, frame_number=None):

        #seek if specified
        if seek != None:
            self.filehandle.seek(seek)

        if frame_number in self.frameindex:
            self.filehandle.seek(self.frameindex[frame_number])

        #read frame_length lines if specified and return position
        if frame_length != None:
            for _ in xrange(frame_length):
                line = self.filehandle.readline()
                if len(line) == 0:
                    raise EOFError
                # parser code here

        #else read until marker occurs, return tell from line prior
        elif marker != None:
            line = ""
            while marker not in line:
                line = self.filehandle.readline()
                if len(line) == 0:
                    raise EOFError
                # parser code here

    def __getitem__(self, framenum=None):


        #deal with slices
        if type(framenum) == slice:
            collector = []
            for i in range(slice):
                collector.append(self.__getitem__(framenum=i))
            return collector

        #get frame length if unknown
        if self.framelength == 0:
            self.framelength = self._get_frame_length()

        #frame known and positive
        if framenum in self.frameindex:
            return self._get_frame(seek=self.frameindex[framenum], frame_length=self.framelength, frame_number=framenum)

        #frame unknown and positive
        elif framenum > -1:
            for i in xrange(framenum+1):
                if i == framenum:
                    return self._get_frame(seek=self.frameindex[framenum], frame_length=self.framelength, frame_number=framenum)
                elif i+1 in self.frameindex:
                    pass
                else:
                    self.frameindex[i+1] = self._get_next_frame_start(seek=self.frameindex[i], frame_length=self.framelength)
        #frame negative
        elif framenum < 0:
            #last frame unknown
            self._populate_frameindex()
            #last frame known
            return self._get_frame(seek=self.frameindex[len(self.frameindex) + framenum], frame_length=self.framelength)


    def _populate_frameindex(self):
        if self.frameindex_complete == False:
            i = 0
            try:
                while True:
                    if i+1 in self.frameindex:
                        pass
                    else:
                        self.frameindex[i+1] = self._get_next_frame_start(seek=self.frameindex[i], frame_length=self.framelength)
                    i += 1
            except EOFError:
                #remove highest index (end of file)
                del self.frameindex[max(self.frameindex.keys())]
                self.frameindex_complete = True

class XYZReader(Reader):

    def _get_frame_length(self):
        # implement get frame length here
        self.filehandle.seek(0)
        line = self.filehandle.readline()
        if len(line) == 0:
            raise EOFError
        return int(line.strip())+2

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
                if len(line) == 0:
                    raise EOFError
                if i == 1:
                    ensemble.boxvector = float(line)
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
        super(DLP2HReader, self).__init__(fileobj)
        self. _read_preamble()

    def _read_preamble(self):
        self.filehandle.seek(0)
        line = self.filehandle.readline()
        if len(line) == 0:
            raise EOFError

        if "timestep" in line:
            elements = line.strip().split()
            self.trajectory_key = int(elements[3])
            self.periodic_key = int(elements[4])
            self.number_atoms = int(elements[2])
            self.filehandle.seek(0)

        else:
            self.header = line.strip()

            line = self.filehandle.readline()
            if len(line) == 0:
                raise EOFError
            elements = line.strip().split()

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

        if frame_number != None:
            self.filehandle.seek(self.frameindex[frame_number])

        #read frame_length lines if specified and return position
        if frame_length != None:
            atomproperties = dict()
            ensemble = ae.AtomEnsemble()

            ensemble.filename = self.filehandle.name
            ensemble.framenumber = frame_number
            ensemble.header = self.header

            atoms_start = 1
            if self.periodic_key > 0:
                atoms_start += 3
            atom_length = self.trajectory_key + 2
            atomproperties = dict()

            for i in xrange(frame_length):
                line = self.filehandle.readline()
                if len(line) == 0:
                    raise EOFError
                elements = line.strip().split()
                atom_position = (i - atoms_start)%atom_length
                if i == 0:
                    if elements[0].strip() != 'timestep':
                        if frame_number != None:
                            zeropos = self.frameindex[frame_number-1]
                            self.frameindex = {0:zeropos}
                            print "HISTORY read reset"
                            return self._get_frame(seek, frame_length, marker, frame_number)
                        else:
                            raise SyntaxError("Word timestep not found. Frame:" + str(frame_number) + ", Line:" + str(i))
                    ensemble.timestep = int(elements[1])
                    ensemble.time = float(elements[5])
                elif self.periodic_key and (i < 4):
                    if i == 1:
                        ensemble.boxvector = float(elements[0])
                    else:
                        pass
                else:
                    if atom_position == 0:
                        atomproperties['element'] = elements[0]
                        atomproperties['mass'] = float(elements[2])
                        atomproperties['charge'] = float(elements[3])

                    elif atom_position == 1:
                        atomproperties['coordinate'] = [float(elements[0]), float(elements[1]), float(elements[2])]

                    elif atom_position == 2:
                        atomproperties['velocity'] = [float(elements[0]), float(elements[1]), float(elements[2])]

                    elif atom_position == 3:
                        atomproperties['force'] = [float(elements[0]), float(elements[1]), float(elements[2])]

                    if atom_position == (atom_length-1):
                        ensemble.append(ae.Atom(**atomproperties))
                        atomproperties = dict()

            return ensemble

class Writer(object):

    def __init__(self, fileobj=None, overwrite=False):
        if type(fileobj) == str:
            if overwrite:
                self.filehandle = open(fileobj, "w") #, 0)
            else:
                self.filehandle = open(fileobj, "a") #, 0)
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
            self.filehandle.flush()

    def _write_global_preamble(self, frame=None):
        pass

    def _write_frame_preamble(self, frame=None):
        pass

    def _write_main(self, frame=None):
        pass

class XYZWriter(Writer):

    def _write_global_preamble(self, frame=None):
        pass

    def _write_frame_preamble(self, frame=None):
        self.filehandle.write(str(len(frame['element'])) + "\n")
        if frame.boxvector:
            self.filehandle.write(str(frame.boxvector) + "\n")
        else:
            self.filehandle.write(frame.header + "\n")

    def _write_main(self, frame=None):
        for i in xrange(len(frame['element'])):
            self.filehandle.write(frame['element'][i])
            self.filehandle.write(" " + str(frame['coordinate'][i][0]) + " " + str(frame['coordinate'][i][1]) + " " + str(frame['coordinate'][i][2]))
            if 'mass' in frame:
                self.filehandle.write(" " + str(frame['mass'][i]))
            else:
                self.filehandle.write("\n")
                continue

            if 'charge' in frame:
                self.filehandle.write(" " + str(frame['charge'][i]))
            else:
                self.filehandle.write("\n")
                continue

            if 'velocity' in frame:
                self.filehandle.write(" " + str(frame['velocity'][i][0]) + " " + str(frame['velocity'][i][1]) + " " + str(frame['velocity'][i][2]))
            else:
                self.filehandle.write("\n")
                continue

            if 'force' in frame:
                self.filehandle.write(" " + str(frame['force'][i][0]) + " " + str(frame['force'][i][1]) + " " + str(frame['force'][i][2]))
            else:
                self.filehandle.write("\n")
                continue

            if 'molecule_index' in frame:
                self.filehandle.write(" " + str(frame['molecule_index'][i]))

            self.filehandle.write("\n")

class DLP2CWriter(Writer):

    def _write_global_preamble(self, frame=None):
        pass

    def _write_frame_preamble(self, frame=None):
        self.filehandle.write(frame.header + "\n")
        if 'force' in frame:
            self.filehandle.write("      2   ")
        elif 'velocity' in frame:
            self.filehandle.write("      1   ")
        else:
            self.filehandle.write("      0   ")

        if frame.boxvector:
            self.filehandle.write("      3   ")
        else:
            self.filehandle.write("      0   ")

        self.filehandle.write("{0:10d}{1:20.12f}".format(len(frame['element']), 0.0))

        if frame.boxvector:
            self.filehandle.write("\n{0:20.12f}{1:20.12f}{1:20.12f}\n{1:20.12f}{0:20.12f}{1:20.12f}\n{1:20.12f}{1:20.12f}{0:20.12f}".format(frame.boxvector, 0.0))

    def _write_main(self, frame=None):
        co = frame['coordinate']
        if 'velocity' in frame:
            vel = frame['velocity']
        if 'force' in frame:
            fo = frame['force']

        for i in xrange(len(frame['element'])):
            self.filehandle.write('\n{0:8s}{1:10d}'.format(frame['element'][i], i+1))
            #co = frame['coordinate'][i]
            self.filehandle.write('\n{0:20.12E}{1:20.12E}{2:20.12E}'.format(co[i][0], co[i][1], co[i][2]))

            if 'velocity' in frame:
                #vel = frame['velocity'][i]
                self.filehandle.write('\n{0:20.12E}{1:20.12E}{2:20.12E}'.format(vel[i][0], vel[i][1], vel[i][2]))
            else:
                continue
            if 'force' in frame:
                #fo = frame['force'][i]
                self.filehandle.write('\n{0:20.12E}{1:20.12E}{2:20.12E}'.format(fo[i][0], fo[i][1], fo[i][2]))
