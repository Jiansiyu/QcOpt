import itertools
import logging

import networkx
from permutationsolver import PermutationSolver

quantumc_logger = logging.getLogger("QcOptimizer")

class QcOptimizer(object):
    '''

    '''

    def __init__(self,permutationrule):
        self.concurrent = -1 # use all the cores available
        self.qubit_num = 5   # number of QC qubit
        self.maxsolution= 5
        self.permutationsolver = PermutationSolver(max_n=self.qubit_num)  #initialize all  the permutation tables

    def _validateconnectioncandidate(self, initialstate):
        '''
        calculate the candidate of the result
        :param initialstate:
        :return:
        '''
        permuationsolution = self.permutationsolver.solve(initialstate,maxsolution=self.maxsolution)
        if not permuationsolution:
            quantumc_logger.warning("{}, there is no permutation solution candidate available ".format(__name__))
            return None

        result_stack = []
        for item in permuationsolution:
            pass

    def fullconnectionsolver(self):
        '''
        solve the best result compare with fully connected circuit
        :return:
        '''

        fullconnection = [[x,y] for x,y in itertools.permutations([x for x in range(5)],2)]
        fullpossibleInitials = self.permutationsolver.getfullpossiblestates()
        quantumc_logger.info("total candiate initial states {}".format(len(fullpossibleInitials)))

        # self._validateconnectioncandidate(fullpossibleInitials[0])

if __name__ == '__main__':
    a = QcOptimizer(None)
    a.fullconnectionsolver()
