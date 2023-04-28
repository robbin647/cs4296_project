import sys
# You need the following two lines to make subsequent imports working!
# if '/home/tianxia/depsched/exp/simulator' not in sys.path:
#     sys.path.insert(1, '/home/tianxia/depsched/exp/simulator')

from ..schedule import Scheduler
from ..trace import Tracer

class MyTracer(Tracer):
    def __init__(self):
        pass

    def image_size(self, image_name):
        IMAGE_SIZE_TABLE={
                "Image01": 50000,
                "Image02": 55000,
                "Image03": 35000
                }
        assert(image_name in IMAGE_SIZE_TABLE)
        return IMAGE_SIZE_TABLE[image_name]
    
    def layers_(self, image_name):
        IMAGE_LAYER_MAPPING = {
                "Image01": ["Layer01", "Layer03"],
                "Image02": ["Layer02", "Layer03"],
                "Image03": ["Layer03"]
                }
        assert(image_name in IMAGE_LAYER_MAPPING)
        return IMAGE_LAYER_MAPPING[image_name]
    
    def layer_size(self, layer):
        LAYER_SIZE_TABLE={
                "Layer01": 15000 ,
                "Layer02": 20000,
                "Layer03": 35000
                }
        assert(layer in LAYER_SIZE_TABLE)
        return LAYER_SIZE_TABLE[layer]

tracer = MyTracer()

def testCase1():
    mySched = Scheduler(tracer, dep_th=0.1)
    mySched.visit_sequence = [0, 1, 2] ## must make sure the node is traversed sequentially for this test to work

    req = (["Image01"], 10)
    nodes = [
            [{"Image03": [0, 0, 0, False]}, {"Layer03": [0, 0, 0, False]}, 35000, 40000, 1, 2, {}, 5000],
            [{"Image03": [0,0,0,False]}, {"Layer03": [0,0,0,False]}, 35000, 50000, 0, 2, {}, 15000],
            [{"Image01": [0,0,0,False]}, {"Layer01": [0, 0, 0, False], "Layer03": [0,0,0,False]}, 50000, 50000, 1, 2, {}, 0]
            ]

    # use dep sched: should give result = 
    selected_node = mySched.schedule(req, nodes,
            sched="dep", lb_ratio=0)
    
    print("testCase01: dep: ", selected_node)
    assert(selected_node == 3)

    # use compromising sched: should give result = 
    selected_node = mySched.schedule(req, nodes,
            sched="compromising-dep", lb_ratio=0)
    
    assert(selected_node == 2)


if __name__ == '__main__':
    testCase1()
