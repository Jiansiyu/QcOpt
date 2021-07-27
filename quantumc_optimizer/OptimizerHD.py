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
            self.target_circuit = [[x, y] for x, y in list(itertools.combinations(range(self.n_qubit), 2))]
        else:
            self.target_circuit = target_circuit

        self.device_connection = [sorted(x) for x in self.device]
        self.device_connection = list(k for k, _ in itertools.groupby(self.device_connection))

        self.next_swap = {}

    def _formIndexKey(self, single_layout):
        '''
        :param keyarray:
        :return:
        '''
        return "".join(str(x) for x in single_layout)

    def _getNextSwap(self, firstLayout):
        next_level_candidate = []

        # calculate the next permuatation candidate
        key = self._formIndexKey(firstLayout)
        for physical_pair in self.device_connection:
            next_layout = copy.deepcopy(firstLayout)
            next_layout[physical_pair[0]], next_layout[physical_pair[1]] = next_layout[physical_pair[1]], next_layout[
                physical_pair[0]]
            next_level_candidate.append(next_layout)
        self.next_swap[key] = next_level_candidate

    def updateTarget(self, target, series_layout):
        last_layout = series_layout[-1]
        new_target = copy.deepcopy(target)
        for physical_pair in self.device_connection:
            gate = [last_layout[physical_pair[0]], last_layout[physical_pair[1]]]
            if gate in new_target:
                new_target.remove(gate)
        if not new_target:
            return True, series_layout
        return new_target, series_layout

    def findLayoutSolution(self, target, initial_layout):
        solution_space = [(target, initial_layout)]
        n_layers = 1
        starttime = time.time()

        while True:
            n_layers += 1
            n_pool = len(solution_space)
            threadpool = multiprocessing.Pool(min(max(1, n_pool), multiprocessing.cpu_count()))
            new_solution_space = threadpool.starmap(self.updateTarget, solution_space)
            threadpool.close()

            solution_space = []
            for item in new_solution_space:
                new_target, series_layout = item
                if new_target == True:
                    return series_layout
                else:
                    last_Layout = series_layout[-1]
                    last_Layout_key = self._formIndexKey(last_Layout)
                    if last_Layout_key not in self.next_swap.keys():
                        self._getNextSwap(last_Layout)
                    next_layout_candidates = self.next_swap[last_Layout_key]
                    for next_layout_candidate in next_layout_candidates:
                        next_series_layout = copy.deepcopy(series_layout)
                        if next_layout_candidate not in next_series_layout:
                            next_series_layout.append(next_layout_candidate)
                            solution_space.append((new_target, next_series_layout))

            optlogger.warning("running layer: {}, \n\t total checked combinations : {}  \n\t  "
                              "concurrent thread : {} \n\t total time :{}".format(n_layers, n_pool, self.n_thread,
                                                                                  time.time() - starttime))

    def solver(self):
        initial_layout = [[x for x in range(self.n_qubit)]]
        result = self.findLayoutSolution(self.target_circuit, initial_layout)
        return result


if __name__ == '__main__':
    hardware = quantumCircuit.ibmq_circuit("line_7")
    hardware.draw()
    solver = findsolution(hardware)
    print(solver.solver())
