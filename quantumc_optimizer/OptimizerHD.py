'''
High Dimensional, High Efficient Solver
'''
import copy
import multiprocessing
from quantumc_optimizer import quantumCircuit
import logging


optlogger = logging.getLogger("OptimizerHD")
class Optimizer(object):
    '''
    High Dimension Quantum Qubit Solver High Efficiency concurrent Solver


    author: Siyu Jian (sj9va@virginia.edu)
               ***************
               *** Go Hoos ***
               ***************
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
        else:
            self.nthread = nthread

        self.qunatum_circuit = qcircuit
        # used for the connection rule
        if not qcircuit:
            self.quantum_circuit = quantumCircuit.ibmq_santiago()
        else:
            self.quantum_circuit = qcircuit
        self.n_qubit = self.qunatum_circuit.n_qubit

        self.threadPool = multiprocessing.Pool(self.nthread)

        print("===> {}".format(self.quantum_circuit.circuitconnection))


    def getnext(self,initialstate = []):
        '''
        Given the initial state, calculate all the next states
        :param initialstate: the initial states need to calculate
        :return: list if next level states
        '''
        result = []
        for exchangerule in self.qunatum_circuit.circuitconnection:
            indexA, indexB = exchangerule[0], exchangerule[1]
            temp = copy.deepcopy(initialstate)
            temp[indexB],temp[indexA] = temp[indexA], temp[indexB]
            result.append(temp)
        return  result


    def getfinalstates(self,initialparams=()):
        '''

        :param initialparams: target, states
        :return:
        '''

        target, state = initialparams
        if not state:
            optlogger.warning("{} the getfinalstates initial state is empty!!".format(__class__))
            return  target
        if not target:
            return []

        length = len(initialparams)

        slow, fast = 0, 1

        while fast < length:
            paraA = state[slow]
            paraB = state[fast]
            if [paraA, paraB] in target:
                target.remove([paraA,paraB])
            if [paraB,paraA] in target:
                target.remove([paraB,paraA])
            slow += 1
            fast += 1

        return target

    def concurrentdfs(self,initailparam=()):
        '''
        :param initailstates: tuple input, target, the first initial states,
                               (target list, current initial, result list)
        :return: return the first element that satisfy the permutation rule
        '''
        if not initailparam:
            raise TypeError("The input of the concurrentdfs is None!!")

        target, initial, resultstack = initailparam

        # concurrent DFS
        if not target:
            return resultstack

        for nextRes in self.getnext(initial):
            if nextRes not in resultstack:
                pass


    def solver(self):
        pass
if __name__ == '__main__':
    circuit = quantumCircuit.ibmq_santiago()
    opt = Optimizer(qcircuit=circuit)
    circuit.draw()