import numpy as np

def Apply_PBC(list coordinates, list pbc_vector):
    """Apply periodic boundary conditions
    Arguments:
        * coordinates
            list of an arbitrary number of vectors (lists of 3 floats) of atom coordinates
        * pbc_vector
            list of 3 vectors (lists of 3 floats) defining the unit cell boundary axes, in the form:
            [[ax, ay, az], [bx
    Returns:
        list of coordinates after folding into the unit cell. Element order relative to input coordinates is guaranteed to be preserved.
        
    Notes:
        elements that are farther apart from the box than one box length will be folded multiple times until they are inside the box."""

    covect = np.array(coordinates)
    pbcvect = np.array(pbc_vector)
    pbchalfvect = pbcvect * 0.5 

    outvect = []

    for c in covect:
        storevect = c
        if storevect[0] > pbchalfvect[0][0]:
            while storevect[0] > pbchalfvect[0][0]:
                storevect[0] -= pbcvect[0][0]
        elif storevect[0] < (-1.0 * pbchalfvect[0][0]):
            while storevect[0] < (-1.0 * pbchalfvect[0][0]):
                storevect[0] += pbcvect[0][0]

        if storevect[1] > pbchalfvect[1][1]:
            while storevect[1] > pbchalfvect[1][1]:
                storevect[1] -= pbcvect[1][1]
        elif storevect[1] < (-1.0 * pbchalfvect[1][1]):
            while storevect[1] < (-1.0 * pbchalfvect[1][1]):
                storevect[1] += pbcvect[1][1]

        if storevect[2] > pbchalfvect[2][2]:
            while storevect[2] > pbchalfvect[2][2]:
                storevect[2] -= pbcvect[2][2]
        elif storevect[2] < (-1.0 * pbchalfvect[2][2]):
            while storevect[2] < (-1.0 * pbchalfvect[2][2]):
                storevect[2] += pbcvect[2][2]

        outvect.append(storevect)

    return outvect


def Remove_PBC

