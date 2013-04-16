# -*- coding: utf-8 -*-


def ReadXYZ(filename):
    """Read an XYZ file located at *filename* on disk
        Input:      Takes single-frame and multi-frame XYZ files
        Returns:    Array of dictionaries, one dictionary for each frame, starting with the first frame
                    Each dictionary contains the following keys:
                        comment:    (str) frame comment line
                        elements:   ([str, str, ...]) list of element labels, in order
                        coordinates:([[float, float, float], [float, float, float], ...) list of coordinate triples, in order
    """
    rootarray = []
    next_frame_start = 0
    next_comment_line = 1

    input_file = open(filename, "r")

    for num, line in enumerate(input_file):
        print line
        if num == next_frame_start:
            if line.strip() == "":
                next_frame_start += 1
            else:
                next_frame_start += (int(line.strip()) + 2)
                next_comment_line = num + 1
                rootarray.append({'elements': [], 'coordinates': [], 'comment': "" })
        elif num == next_comment_line:
            rootarray[-1]['comment'] = line.strip()
        else:
            elem = line.strip().split()
            rootarray[-1]['elements'].append(elem[0])
            rootarray[-1]['coordinates'].append([float(elem[1]),float(elem[2]),float(elem[3])])
    
    input_file.close()
    return rootarray


def WriteXYZ(data, filename, overwrite=False):
    """Write an XYZ file into a file *filename* on disk from *data*
        *data* is structured like the output of ReadXYZ
        *overwrite*: Will append to an existing file if False, otherwise it will overwrite any existing data
    """
    if overwrite == True:
        output_file = open(filename, "w")
    else:
        output_file = open(filename, "a")

    for frame in data:
        output_file.write(str(len(frame['elements'])) + '\n' + frame['comment'] + '\n')
        for element, coordinates in zip(frame['elements'], frame['coordinates']):
            output_file.write(element + " " + str(coordinates[0]) + " " + str(coordinates[1]) + " " + str(coordinates[2]) + "\n")
    
    output_file.close()




     
