import networkx as nx
import matplotlib.pyplot as plt
import yaml
import os
import logging

quantum_logger = logging.getLogger("QuantumCircuit")
class ibmq_circuit(object):
    '''
    IBM Q Circuit
    '''
    def __init__(self,circuitname,circuityaml):
        self.circuit=None
        self.circuitname=circuitname
        self.circuitconnection=None
        self.circuitdescription=None
        self.circuitconfig = None
        self.circuitgraph = nx.Graph()
        self._loadcircuit(circuityaml)

    def _getgraph(self):
        circuitnode = []
        for item in self.circuitconnection:
            circuitnode.extend(item)
        circuitnode = list(set(circuitnode))
        self.circuitgraph.add_nodes_from(circuitnode)
        circuitconnection = [(cir[0],cir[1]) for cir in self.circuitconnection]
        self.circuitgraph.add_edges_from(circuitconnection)

    def _loadcircuit(self,circuityaml):
        '''
        Load the YAML file
        create networkX circuit according to its connection graph
        :param circuityaml: YAML file nmae that contains the circuit defination
        :return:
        '''
        yamlfullname = os.path.join(os.path.dirname(os.path.realpath(__file__)),"statics/circuit",circuityaml)
        if not os.path.isfile(yamlfullname):
            raise IOError("Can not Find Quamtum Circuit YAML define in path <{}>, \n "
                          "please check whether the YAML file have read permission!".format(yamlfullname))

        try:
            data_loader = self._readyaml(yamlfullname=yamlfullname)
            self.circuitconnection = data_loader["connection"]
            if not self.circuitname == data_loader["name"]:
                logging.warning("Circuit Name in YAML does not Match the Circuit Name in function !! "
                                "Overwrite with the name in YAML")
                self.circuitname = data_loader["name"]
            self.circuitconfig = data_loader
            self._getgraph()
        except Exception as e:
            quantum_logger.warning(str(e))

    def getnetwork(self):
        '''

        :return:
        '''
        return  self.circuitgraph

    def _readyaml(self,yamlfullname):
        '''
        :param yamlfullname:
        :return:
        '''
        try:
            with open(yamlfullname,'r') as stream:
                data_loader = yaml.safe_load(stream)
        except Exception as e:
            quantum_logger.warning(str(e))

        return  data_loader


    def savecircuit(self,saveyamlname):
        '''
        :return:
        '''

        if not isinstance(saveyamlname,str):
            pass

        if os.path.isfile(saveyamlname):
            pass

        try:
            with open(saveyamlname,'w', encoding='utf8') as outfile:
                yaml.dump(self._circuit,outfile,default_flow_style=False, allow_unicode=True)
        except IOError as e:
            quantum_logger.warning("{}".format(str(e)))
        except Exception as e:
            raise  e

    def draw(self):
        nx.draw(self.circuitgraph,with_labels=True)
        plt.title(self.circuitname)
        plt.show()


class ibmq_santiago(ibmq_circuit):
    '''

    '''
    def __init__(self):
        self.circuitname="ibmq_santiago"
        super(ibmq_santiago, self).__init__(circuitname=self.circuitname,
                                            circuityaml="{}.yaml".format(self.circuitname))


class ibmq_bogota(ibmq_circuit):
    '''

    '''
    def __init__(self):
        self.circuitname="ibmq_bogota"
        super(ibmq_santiago, self).__init__(circuitname=self.circuitname,
                                            circuityaml="{}.yaml".format(self.circuitname))


class ibmq_manila(ibmq_circuit):
    '''

    '''
    def __init__(self):
        self.circuitname="ibmq_manila"
        super(ibmq_santiago, self).__init__(circuitname=self.circuitname,
                                            circuityaml="{}.yaml".format(self.circuitname))


class ibmq_jakarta(ibmq_circuit):
    '''

    '''
    def __init__(self):
        self.circuitname="ibmq_jakarta"
        super(ibmq_santiago, self).__init__(circuitname=self.circuitname,
                                            circuityaml="{}.yaml".format(self.circuitname))


class ibmq_creater(ibmq_circuit):
    '''
    IBM Circuit Creater

    '''
    def __init__(self):
        self._circuit = None

    def create_circuit(self,name=None,company=None,connection=None,version=None):
        if not isinstance(name,str):
            pass

        if not isinstance(company,str):
            pass

        if not isinstance(connection,{list}):
            pass

        self._circuit = {
            'name':name,
            'company':company,
            'version':version,
            'connection':connection
                        }


if __name__ == '__main__':
    a = ibmq_santiago()
    print(a.circuitname)
    print(a.circuitconnection)
    a.draw()
