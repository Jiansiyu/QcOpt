import cProfile
import copy
import itertools
import multiprocessing
import time
import logging
import quantumCircuit

optlogger = logging.getLogger("BFsearch")


class findsolution(object):
    def __init__(self, device, target_circuit=None, n_thread=-1):
        self.hardware = device
        self.device = self.hardware.circuitconnection
        self.n_qubit = self.hardware.n_qubit

        self.n_thread = n_thread
        if self.n_thread == -1:
            self.n_thread = multiprocessing.cpu_count()
        else:
            self.n_thread = n_thread

        if not target_circuit:
            self.target_circuit = itertools.combinations(range(self.n_qubit), 2)
        else:
            self.target_circuit = target_circuit

        self.device_connection = [sorted(x) for x in self.device]
        self.device_connection = tuple(tuple(k) for k, _ in itertools.groupby(self.device_connection))

        self.next_swap = {}
        self._getNextSwapDict()

    def _getNextSwap(self, firstLayout):
        '''
        get all next layout for all possible swaps
        :param firstLayout: a tuple
        :return: a dic
        '''
        next_level_candidate = []

        # calculate the next permuatation candidate
        for physical_pair in self.device_connection:
            next_layout = list(firstLayout)
            next_layout[physical_pair[0]], next_layout[physical_pair[1]] = next_layout[physical_pair[1]], next_layout[
                physical_pair[0]]
            next_level_candidate.append(tuple(next_layout))
        return {firstLayout: next_level_candidate}

    def _getNextSwapDict(self):
        all_layout = itertools.permutations(range(self.n_qubit))
        threadpool = multiprocessing.Pool(self.n_thread)
        result = threadpool.map(self._getNextSwap, all_layout)
        for item in result:
            self.next_swap.update(item)
        threadpool.close()

    def updateTarget(self, target, series_layout):
        '''
        update the target based on the last layout
        :param target: a tuple of tuple
        :param series_layout: a tuple of tuple
        :return: next level or True when target has no element
        '''
        last_layout = series_layout[-1]
        new_target = list(target)
        for physical_pair in self.device_connection:
            gate = (last_layout[physical_pair[0]], last_layout[physical_pair[1]])
            if gate in new_target:
                new_target.remove(gate)
        if not new_target:
            print('the result layout is', series_layout)
            print('the length is',len(series_layout))
            return [(True, series_layout)]
        else:
            next_level = []
            next_layout_candidates = self.next_swap[last_layout]
            for next_layout_candidate in next_layout_candidates:
                next_series_layout = list(series_layout)
                if next_layout_candidate not in next_series_layout:
                    next_series_layout.append(next_layout_candidate)
                    next_series_layout = tuple(next_series_layout)
                    next_level.append((tuple(new_target), next_series_layout))

        return next_level

    def findLayoutSolution(self, target, initial_layout):
        solution_space = [(target, initial_layout)]
        n_layers = 1
        starttime = time.time()

        while True:
            n_layers += 1
            n_pool = len(solution_space)
            threadpool = multiprocessing.Pool(min(n_pool, multiprocessing.cpu_count()))
            new_solution_space = threadpool.starmap(self.updateTarget, solution_space)
            threadpool.close()
            solution_space = []

            for item in new_solution_space:
                solution_space.extend(item)
            for new_target, series_layout in solution_space:
                if new_target == True:
                    return series_layout

            optlogger.warning("running layer: {}, \n\t total checked combinations : {}  \n\t  "
                              "concurrent thread : {} \n\t total time :{}".format(n_layers, n_pool, self.n_thread,
                                                                                  time.time() - starttime))

    def solver(self):
        initial_layout = (tuple(range(self.n_qubit)),)
        result = self.findLayoutSolution(self.target_circuit, initial_layout)
        return result