'''
High Dimensional, High Efficient Solver
'''
import multiprocessing
import itertools
from quantumc_optimizer import quantumCircuit
import logging


optlogger = logging.getLogger("OptimizerHD")
class Optimizer(object):
    '''
    High Dimension Quantum Qubit Solver
    '''
    def __init__(self,nthread = -1, qcircuit=None, initialpermutation=None, targetqcircuit=None):
        '''

        :param nthread:  number of concurrent thread used in the calculation -1. will use all the thread avaible
        :param qcircuit: quantum circuit object
        :param initialpermutation: The initial permutation used for search
        '''
        self.nthread = nthread
        if self.nthread == -1:
            self.nthread = multiprocessing.cpu_count()

        self.qunatum_circuit = qcircuit
        # used for the connection rule
        if not qcircuit:
            self.qunatum_circuit = quantumCircuit.ibmq_santiago()
        # load the number of qubite, it works
        self.n_qubit = self.qunatum_circuit.n_qubit


if __name__ == '__main__':
    opt = Optimizer()