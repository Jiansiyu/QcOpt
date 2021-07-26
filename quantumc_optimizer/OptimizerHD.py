'''
High Dimensional, High Efficient Solver
'''
import copy
import multiprocessing
import time

from quantumc_optimizer import quantumCircuit
import logging
import itertools

optlogger = logging.getLogger("OptimizerHD")

def checkStageRes(target, statesChain):
    '''
    for one single states, check the current whether is the candiate, if not return the update target

    :param runStack:
    :return:
    '''

    state = statesChain[-1]  # should only the last one need to update
    if not state:
        optlogger.warning("the getfinalstates initial state is empty!!")
        return (target, statesChain)

    if not target:
        return (True, statesChain)

    length = len(state)
    slow, fast = 0, 1
    while fast < length:
        paraA = [state[slow],state[fast]]
        paraB = paraA[::-1]
        if paraA in target:
            target.remove(paraA)
        if paraB in target:
            target.remove(paraB)
        slow += 1
        fast += 1
    if not target:
        return (True, statesChain)
    else:
        return (target, statesChain)



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
        possibleconnection = [sorted(x) for x in self.quantum_circuit.circuitconnection]
        possibleconnection = qc_circuit =list(k for k,_ in itertools.groupby(possibleconnection))

        for exchangerule in possibleconnection:
            indexA, indexB = exchangerule[0], exchangerule[1]
            temp = copy.deepcopy(initialstate)
            temp[indexB],temp[indexA] = temp[indexA], temp[indexB]
            result.append(temp)
        return  result

    def concurrentdfs(self, initailparam=()):
        '''
        :param initailstates: tuple input, target, the first initial states,
                               (target list, current initial, result list)
        :return: return the first element that satisfy the permutation rule
        '''
        if not  isinstance(initailparam, tuple):
            raise TypeError("Input \"InitialParam\" need to be tuple!!")

        if not initailparam:
            raise TypeError("The input of the concurrentdfs is None!!")

        target, initial = initailparam

        runStack = []  # (target, initial)
        runStack.append((target,initial))

        layerIndexer = 0
        starttime = time.time()
        while True:
            # need concurrent update the result
            layerIndexer += 1
            length = len(runStack)
            currentStage = runStack
            runStack = []  # empty the current stack, ready for the next level

            threadpool = multiprocessing.Pool(min(max(1,length),multiprocessing.cpu_count()))
            currentStageRes = threadpool.starmap(checkStageRes, currentStage)
            for item in currentStageRes:
                targetTemp, stateTemp = item
                if targetTemp == True:
                    return stateTemp
                else:
                    for nexttemp in self.getnext(stateTemp[-1]):
                        if nexttemp not in stateTemp:
                            nextBuffer = copy.deepcopy(stateTemp)
                            nextBuffer.append(nexttemp)
                            runStack.append((targetTemp,nextBuffer))
            threadpool.close()
            optlogger.warning("running layer: {}, \n\t total checked combinations : {}  \n\t  "
                           "concurrent thread : {} \n\t total time :{}".format(layerIndexer,length,self.nthread,time.time()-starttime))

    def solver(self):
        fullconnection = [[x, y] for x, y in itertools.permutations([x for x in range(self.n_qubit)], 2)]
        initialStates = [[x for x in range(self.n_qubit)]]
        result = self.concurrentdfs(initailparam=(fullconnection,initialStates))
        print(result)

if __name__ == '__main__':
    circuit = quantumCircuit.ibmq_santiago()
    opt = Optimizer(qcircuit=circuit)
    opt.solver()