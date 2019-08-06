from PySide2.QtWidgets import QListWidgetItem
import os
import numpy as np


class EnsayoPrensa(QListWidgetItem):

    def __init__(self, fname):
        super(EnsayoPrensa, self).__init__()
        self.fname = fname
        self.setText(os.path.split(fname)[1])

    def get_file_data(self):

        t, p, d, f, pm, v = np.genfromtxt(self.fname,
                                          dtype='float',
                                          usecols=(0, 1, 2, 3, 4, 5),
                                          unpack=True,
                                          comments='#'
                                          )
        return [t, p, d, f, pm, v]

    def get_displacement_xy(self):
        t, d = np.genfromtxt(self.fname,
                             dtype='float',
                             usecols=(0, 2),
                             unpack=True,
                             comments='#'
                             )
        return [t, d]

    def get_presure_xy(self):
        t, p = np.genfromtxt(self.fname,
                             dtype='float',
                             usecols=(0, 1),
                             unpack=True,
                             comments='#',

                             )
        return [t, p]

    def get_file_header(self):
        pass

    def get_file_footer(self):
        pass