#!/usr/bin/env python3
# -*- coding: utf-8 -*-
 
###
# Name: Julie Gardner-Hoag, Logan Gantner
# Student ID: 2299636, 2307470
# Email: gardnerh@chapman.edu, gantner@chapman.edu
# Course: CS510 Fall 2017
# Assignment: Classwork 6
###

from cplane_np import ArrayComplexPlane
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import numba as nb

class JuliaPlane(ArrayComplexPlane):
    """Class which inherits a complex grid and applies a "julia" type function to the grid, resulting in integer values.

    Args:
        c  (complex): the complex parameter associated with the applied julia function

    Attributes:
        plane (:obj:`list` of :obj:`list` of :obj:`complex`): A 2D list representing the current state of the
            complex grid (see __create_grid)
        fs (:obj:`list` of :obj:`function`): A list of all functions that have been applied to the plane since
            the latest refresh
        c: The complex parameter associated with the applied julia function

    Inherited methods:
        _ArrayComplexPlane__create_grid
        apply
        zoom
    """
    def __init__(self, c):
        self.c = c
        ArrayComplexPlane.__init__(self, -2, 2, 2000, -2, 2, 2000)
        self.apply(julia(c))

    def refresh(self, c):
        self.c = c
        self.fs = []
        self.plane = self._ArrayComplexPlane__create_grid()
        self.apply(julia(c))

    def toCSV(self, filename):
        """
        Creates the file 'filename' contain the plane specs and dataframe self.plane.
        Each of the seven parameters of the plane instance are store in a single row of width 2
           containing an identifier for the parameter followed by the parameter value.
        """
        spec_ids = ['xmin',    'xmax',    'ymin',    'ymax',    'xlen',    'ylen',    'c']
        specs =    [self.xmin, self.xmax, self.ymin, self.ymax, self.xlen, self.ylen, self.c]
        with open(filename + '.csv', 'w') as f:
            ### Store the specs
            for spec_id, spec in zip(spec_ids, specs):
                f.write('{},{}\n'.format(spec_id, spec))
            ### Store the self.plane dataframe
            self.plane.to_csv(f)

    def fromCSV(self, filename):
        """
        Imports dataframe and plane specs from filename.csv.
        This method should only be used for data stored using the toCSV method
           within this or child classes -- externally stored data may not be supported.
        If the filename entered does not exist, raises an exception
        """
        ### Try loading and storing data. Warn user if csv file does not exist
        try:
            ### Extract data from csv
            with open(filename, 'r') as f:
                specs = [f.readline().split(',')[1] for _ in range(7)]
                self.plane = pd.DataFrame.from_csv(f)
            ### Store all specs
            self.xmin, self.xmax, self.ymin, self.ymax = [float(c) for c in specs[:4]]
            self.xlen, self.ylen = [int(c) for c in specs[4:6]]
            self.c = complex(specs[-1])
        except FileNotFoundError:
            print('File "{}" could not be found'.format(filename))

    def show(self):
        """Plots a greyscale imshow of self.plane"""
        ax = plt.gca()
        plt.imshow(self.plane, cmap='hot')
        plt.colorbar()
        ax.invert_yaxis()
        ax.set_xticks([])
        ax.set_yticks([])
        plt.title('Julia Imshow Plot, Parameter c = {}'.format(self.c))

def julia(c, max=100):
    """
    Returns a function that determines the number of iterations required for |z(i)| >= 2, where
    z(i+1) = z(i)^2 + c.
    """
    @nb.vectorize([nb.int32(nb.complex128)])
    def func(z):
        n = 1
        while n < max:
            if abs(z) > 2:
                return n
            n += 1
            z = z**2 + c
        return 0
    return func









