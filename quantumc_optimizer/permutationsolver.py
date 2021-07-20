import itertools
import logging
import multiprocessing

permutation_logger = logging.getLogger(__name__)


class PermutationSolver(object):
    '''
    Permutation solution solver
    author: Siyu Jian (sj9va@virginia.edu) Physics Dept. of University of Virginia
    copy right @ Siyu Jian

    Input:
    max_n: the maximum element of the list start from 0, end with n [0,1,2,...,n]
    nthread: number of thread when calculate the permutation candidate
    '''

    def __init__(self,
                 max_n=5,
                 nthread=-1):
        '''
        :param max_n: the maximum element of the list start from 0, end with n [0,1,2,...,n]
        :param nthread: number of thread when calculate the permutation candidate
        '''
        self.max_n = max_n
        self.nthread = nthread
        self._permutationindexer()
        self.permutationtable = []
        self.permutationdic = {}

        # get the permutatin tables in in concurrent way
        self._permutationindexer()
        # start find the second indexer
        self._candidatesearcher()

    def _formIndexKey(self, keyarray):
        '''
        :param keyarray:
        :return:
        '''
        return "".join(str(x) for x in keyarray)

    def _getpermuationres(self, firstElement):
        '''
        :param firstElement:
        :return:
        '''
        candidate = []
        length = len(firstElement)

        slow = 0
        fast = 1

        key = self._formIndexKey(firstElement)
        while fast < length:
            element_temp = firstElement.copy()
            element_temp[slow], element_temp[fast] = element_temp[fast], element_temp[slow]
            candidate.append(element_temp)
            slow += 1
            fast += 1
        return {key: candidate}

    def _candidatesearcher(self):
        '''
        Get all the element that have only two different element in the permutations
        :return:
        '''
        pool = multiprocessing.Pool(multiprocessing.cpu_count())
        result = pool.map(self._getpermuationres, self.permutationtable)
        for item in result:
            self.permutationdic.update(item)

    def _permutationindexer(self):
        self.permutationtable = [list(x) for x in (itertools.permutations(range(self.max_n + 1), self.max_n + 1))]

    def solve(self, starter, maxsolution=5):
        '''
        Permutation solver

        :param starter: [required] List of start array
        :param maxsolution: [default = 5]  number of following arrays after the give array(included)
        :return: List of arrays(include the give array)
        '''
        if not starter:
            raise TypeError("Starter should not empty")

        if len(starter) != self.max_n + 1:
            raise TypeError("Starter array size should equal to max_n when initialize the instance")

        if maxsolution <= 0:
            raise TypeError("maxsolution should be >  0")

        stack = [[starter]]

        permunartionLevelIndexer = 1
        while permunartionLevelIndexer < maxsolution:
            permunartionLevelIndexer += 1
            length = len(stack)
            for _ in range(length):
                current = stack.pop(0)

                # get the last elememt
                lastIndex = current[-1]
                lastIndexKey = self._formIndexKey(lastIndex)

                for nextElement in self.permutationdic[lastIndexKey]:
                    current_temp = current.copy()
                    if nextElement not in current_temp:
                        current_temp.append(nextElement)
                        stack.append(current_temp)
        return stack

    def tester(self, array):
        print(self.permutationdic[self._formIndexKey(array)])


class DiagramSolver(object):
    '''
    Diaggram
    '''
    def __init__(self):
        pass


if __name__ == '__main__':
    solver = PermutationSolver(max_n=5)
    # solver.tester(array=[0,1,2,3,4,5])
    result = solver.solve([x for x in range(6)], maxsolution=5)
    for item in result:
        print(item)
    print(solver.__doc__)