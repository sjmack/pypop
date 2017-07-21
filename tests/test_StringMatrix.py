import base
import subprocess
import hashlib
import unittest
import pytest
from PyPop.Utils import StringMatrix, appendTo2dList

def new_matrix():
    return StringMatrix(3, ['A', 'B', 'C'])

class StringMatrixTest(unittest.TestCase):
    def test_new(self):
        # check everything is zero upon first assignment
        A_matrix = new_matrix()
        assert A_matrix['A'] == [[0, 0], [0, 0], [0, 0]]
        assert A_matrix['B'] == [[0, 0], [0, 0], [0, 0]]
        assert A_matrix['C'] == [[0, 0], [0, 0], [0, 0]]

    def test_assign(self):
        # test assignment
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        assert A_matrix['A'] == [[0, 0], [0, 0], [0, 0]]
        assert A_matrix['B'] == [['B0', 'B0'], ['B1', 'B1'], [0, 0]]
        assert A_matrix['C'] == [[0, 0], [0, 0], [0, 0]]

    def test_copy(self):
        # check copies are independent
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')

        B_matrix = A_matrix.copy()
        B_matrix[0,'A'] = ('A0', 'A0')
        B_matrix[1,'A'] = ('A1', 'A2')

        # B should be changed
        assert B_matrix['A'] == [['A0', 'A0'], ['A1', 'A2'], [0, 0]]
        assert B_matrix['B'] == [['B0', 'B0'], ['B1', 'B1'], [0, 0]]
        assert B_matrix['C'] == [[0, 0], [0, 0], [0, 0]]
    
        # A should be unchanged and have nothing the A column
        assert A_matrix['A'] == [[0, 0], [0, 0], [0, 0]]
        assert A_matrix['B'] == [['B0', 'B0'], ['B1', 'B1'], [0, 0]]
        assert A_matrix['C'] == [[0, 0], [0, 0], [0, 0]]

    def test_submatrix_one_locus(self):
        # test subMatrix, get all data at locus 'A'
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        A_matrix[0, 'A'] = ('A0', 'A0')
        A_matrix[1, 'A'] = ('A1', 'A2')
        assert A_matrix['A'] == [['A0', 'A0'], ['A1', 'A2'], [0, 0]]

    def test_submatrix_two_locus(self):
        # test subMatrix, get all data for b at locus 'A:B'
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        A_matrix[0, 'A'] = ('A0', 'A0')
        A_matrix[1, 'A'] = ('A1', 'A2')
        assert A_matrix['A:B'] == [['A0', 'A0', 'B0', 'B0'], ['A1', 'A2', 'B1', 'B1'], [0, 0, 0, 0]]

    def test_filterout(self):
        # filterOut all rows that contain 'B1'
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        A_matrix[0, 'A'] = ('A0', 'A0')
        A_matrix[1, 'A'] = ('A1', 'A2')
        B_list = A_matrix.filterOut('A:B:C', 'B1') # do the filter
        assert B_list == [['A0', 'A0', 'B0', 'B0', 0, 0], [0, 0, 0, 0, 0, 0]]

    def test_append(self):
        # append a string to each allele
        A_matrix = new_matrix()
        A_matrix[0, 'B'] = ('B0', 'B0')
        A_matrix[1, 'B'] = ('B1', 'B1')
        A_matrix[0, 'A'] = ('A0', 'A0')
        A_matrix[1, 'A'] = ('A1', 'A2')

        assert appendTo2dList(A_matrix['A:B:C'], appendStr=':') == [['A0:', 'A0:', 'B0:', 'B0:', '0:', '0:'], ['A1:', 'A2:', 'B1:', 'B1:', '0:', '0:'], ['0:', '0:', '0:', '0:', '0:', '0:']]

        assert A_matrix['A'] == [['A0', 'A0'], ['A1', 'A2'], [0, 0]]
        assert A_matrix['B'] == [['B0', 'B0'], ['B1', 'B1'], [0, 0]]
        assert A_matrix['C'] == [[0, 0], [0, 0], [0, 0]]