import numpy as np

arr = [
    {
        "start": 0,
        "end": 20,
        "value": 1
    },
    {
        "start": 21,
        "end": 40,
        "value": 0
    },
    {
        "start": 41,
        "end": 50,
        "value": 1
    }
]
print(arr[-1]["end"])
class QuantumWell(object):
    def __init__(self, arr):
        self.arr = arr
        self.mesh_num = arr[-1]["end"]+1

    def makeQuantumWell(self):
        self.mesh = np.zeros(10)
        #self.mesh = np.linspace(0, self.arr[2]["end"], self.mesh_num)

        for material in self.arr:
            self.mesh[material["start"]:material["end"]] = material["value"]

        return self.mesh

quantum_well = QuantumWell(arr=arr)

mesh = quantum_well.makeQuantumWell()

print(mesh)