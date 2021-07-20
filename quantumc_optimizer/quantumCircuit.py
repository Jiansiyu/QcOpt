import networkx
import yaml
import os


class ibmq_circuit(object):

    def __init__(self,circuityaml=None):
        self._circuit=None
        self.circuitname=None
        self.circuitconnection=None
        self.circuitdescription=None
        if not circuityaml:
            self._loadcircuit(circuityaml)

    def _loadcircuit(self,circuityaml):
        '''
        Load the YAML file
        create networkX circuit according to its connection graph
        :param circuityaml: YAML file nmae that contains the circuit defination
        :return:
        '''
        yamlfullname = os.path.join(os.path.dirname(os.path.realpath(__file__)),circuityaml)
        if not os.path.isfile(yamlfullname):
            raise IOError("Can not Find Quamtum Circuit YAML define in path <{}>, \n "
                          "please check whether the YAML file have read permission!".format(yamlfullname))

    def getnetwork(self):
        pass

    def _readyaml(self):
        pass

    def savecircuit(self):
        pass

    def draw(self):
        pass


class ibmq_santiago(ibmq_circuit):
    def __init__(self):
        self.circuitname="ibmq_santiago"
        super(ibmq_santiago, self).__init__(circuityaml="{}.yaml".format(self.circuitname))


class ibmq_bogota(ibmq_circuit):
    def __init__(self):
        self.circuitname="ibmq_bogota"
        super(ibmq_santiago, self).__init__(circuityaml="{}.yaml".format(self.circuitname))
        pass


class ibmq_manila(ibmq_circuit):
    def __init__(self):
        self.circuitname="ibmq_manila"
        super(ibmq_santiago, self).__init__(circuityaml="{}.yaml".format(self.circuitname))


class ibmq_jakarta(ibmq_circuit):
    def __init__(self):
        self.circuitname="ibmq_jakarta"
        super(ibmq_santiago, self).__init__(circuityaml="{}.yaml".format(self.circuitname))



class ibmq_creater(ibmq_circuit):

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
    cui = ibmq_circuit()
    ibmq_santiago()
    with open('ibmq_santiago.yaml') as stream:
        data_loader = yaml.safe_load(stream)
    print(data_loader)