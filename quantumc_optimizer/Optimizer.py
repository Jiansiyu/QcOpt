import copy
import itertools
import logging
import multiprocessing

import networkx
from permutationsolver import PermutationSolver

quantumc_logger = logging.getLogger("QcOptimizer")

class QcOptimizer(object):
    '''

    '''
    def __init__(self,permutationrule):
        self.concurrent = -1 # use all the cores available
        self.qubit_num = 6   # number of QC qubit
        self.maxsolution= 5
        self.permutationsolver = PermutationSolver(max_n=self.qubit_num-1)  #initialize all  the permutation tables
        self.targetconnection =[]

    def validateconnectioncandidate(self, statearray):
        '''
        calculate the candidate of the result
        :param initialstate:
        :return:
        '''
        targetconnection = self.targetconnection
        def helper(state, array=[]):
            slow = 0
            fast = 1
            length = len(state)
            while fast < length:
                temp1 = [state[slow],state[fast]]
                temp2 = temp1[::-1]
                if temp1 in array:
                    array.remove(temp1)
                if temp2 in array:
                    array.remove(temp2)
                slow+=1
                fast+=1
            return array
        target = copy.deepcopy(targetconnection)
        for item in statearray:
            helper(item,target)
        if not target:
            return True
        else:
            return False

    def optimalstatesolver(self, initialstate,target):
        '''
        :param initialstate:
        :param target:
        :return:
        '''
        self.targetconnection = target
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        currentMaxsolution = 1
        # stack= self.permutationsolver.solve(initialstate,maxsolution=currentMaxsolution)
        stack = []
        permu_res = []
        print(stack)

        while not stack or stack.count(True) == 0:
            permu_res = self.permutationsolver.solve(initialstate,maxsolution=currentMaxsolution)
            stack = pool.map(self.validateconnectioncandidate,permu_res)
            print("Itering {}".format(currentMaxsolution))
            currentMaxsolution+=1
        pool.close()

        resultArray = []
        for item in permu_res:
            if self.validateconnectioncandidate(item):
                resultArray.append(item)
        print("nQubit: {}.   iteration :{}".format(self.qubit_num,currentMaxsolution-1))
        return currentMaxsolution-1, resultArray

    def fullconnectionsolver(self):
        '''
        solve the best result compare with fully connected circuit
        :return:
        '''
        fullconnection = [[x,y] for x,y in itertools.permutations([x for x in range(self.qubit_num)],2)]
        fullpossibleInitials = self.permutationsolver.getfullpossiblestates()
        quantumc_logger.info("total candiate initial states {}".format(len(fullpossibleInitials)))
        self.optimalstatesolver(initialstate=[x for x in range(self.qubit_num)],target=fullconnection)
        print(fullconnection)

if __name__ == '__main__':
    import cProfile
    with cProfile.Profile() as pr:
        a = QcOptimizer(None)
        a.fullconnectionsolver()
    pr.print_stats()
