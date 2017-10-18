#!/usr/bin/env python3
# -*- coding: utf-8 -*-

###
# Name: Julie Gardner-Hoag, Logan Gantner
# Student ID: 2299636, 2307470
# Email: gardnerh@chapman.edu, gantner@chapman.edu
# Course: CS510 Fall 2017
# Assignment: Classwork 6
###

from abscplane import AbsComplexPlane
import numpy as np
import pandas as pd

class ArrayComplexPlane(AbsComplexPlane):
    """Class containing a complex grid equipped with methods designed to easily edit grid values simultaneously

    Args:
        xmin (float): the grid's min real value
        xmax (float): the grid's max real value
        xlen   (int): the number of points spanning [xmin, xmax]
        ymin (float): the grid's min imag value
        ymax (float): the grid's max imag value
        ylen   (int): the number of points spanning [ymin, ymax]

    Attributes:
        plane (:obj:`list` of :obj:`list` of :obj:`complex`): A 2D list representing the current state of the
            complex grid (see __create_grid)
        fs (:obj:`list` of :obj:`function`): A list of all functions that have been applied to the plane since
            the latest refresh
    """
    def __init__(self, xmin, xmax, xlen, ymin, ymax, ylen):
        self.xmin  = xmin
        self.xmax  = xmax
        self.xlen  = xlen
        self.ymin  = ymin
        self.ymax  = ymax
        self.ylen  = ylen

        self.plane = self.__create_grid()
        ### An ordered list of functions that have been applied to the plane points
        self.fs    = []

    def __create_grid(self):
        rx = np.linspace(self.xmin, self.xmax, self.xlen)
        ry = np.linspace(self.ymin, self.ymax, self.ylen)
        x,y = np.meshgrid(rx,ry)
        grid = x + y*1j

        col_names = ['x'+str(i+1) for i in range(self.xlen)]
        row_names = ['y{0}*i'.format(str(i+1)) for i in range(self.ylen)]
        grid = pd.DataFrame(grid, index=row_names, columns=col_names)

        return grid

    def refresh(self):
        """Removes all functions from self.fs and restores self.plane to its unmodified grid values"""
        self.fs = []
        self.plane = self.__create_grid()

    def apply(self, f):
        """
        Given a single-argument function f, replaces all points z in self.plane with f(z).
        Also adds the applied function to list self.fs
        """
        ### Use pandas' applymap method to modify all plane points using f
#         self.plane = self.plane.applymap(f)
        self.plane = f(self.plane)
        ### Store the applied function for future reference
        self.fs.append(f)

    def zoom(self,xmin,xmax,xlen,ymin,ymax,ylen):
        """Redefines the grid based on new dimensions, then reapplies all functions from self.fs to the grid"""
        self.xmin  = xmin
        self.xmax  = xmax
        self.xlen  = xlen
        self.ymin  = ymin
        self.ymax  = ymax
        self.ylen  = ylen
        ### Reset the grid
        self.plane = self.__create_grid()

        ### Apply all functions from self.fs to the new grid.
        for f in self.fs:
            self.plane = self.plane.applymap(f)
    
    
    
    
    
    
    
    
    
    
    
