import AtomEnsemble as ae

class XYZReader(object):

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
                atomproperties['velocity'] = [float(elements[4]), float(elements[5]), float(elements[6])]
            if len(elements) > 7:
                atomproperties['force'] = [float(elements[7]), float(elements[8]), float(elements[9])]
            if len(elements) > 10:
                atomproperties['mass'] = float(elements[10])
            if len(elements) > 11:
                atomproperties['charge'] = float(elements[11])
            if len(elements) > 12:
                atomproperties['molecule_index'] = int(elements[12])

            ensemble.append(ae.Atom(**atomproperties))
            self.intraframepos += 1

        self.intraframepos = 0
        self.framepos += 1
        self.frameindex[str(self.framepos)] = self.filehandle.tell()
        return ensemble
