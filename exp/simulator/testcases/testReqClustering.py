from ..simulator import Simulator
from ..trace import Tracer

IMAGE_LAYER_MAPPING = {
        "Image01": ["Layer01", "Layer02"],
        "Image02": ["Layer02", "Layer03"],
        "Image03": ["Layer03", "Layer04"],
        "Image04": ["Layer05", "Layer06"],
        "Image05": ["Layer05"]
        }

class MyTracer(Tracer):
    def __init__(self):
        pass

    def layers_(self, image_name):
        assert(image_name in IMAGE_LAYER_MAPPING)
        return IMAGE_LAYER_MAPPING[image_name]
    
mySim = Simulator()
mySim.tr = MyTracer()

def testCase01():
    request_batch = [
                     (0, (["Image01"], 10)),
                     (0, (["Image03"], 10)),
                     (0, (["Image04"], 10)),
                     (0, (["Image02"], 10)),
                     (0, (["Image05"], 10))
                     ]
    req_batch_after_clustering = mySim.request_clustering(request_batch)
    print(req_batch_after_clustering)
    assert(req_batch_after_clustering == [
            (0, (["Image01"], 10)),
            (0, (["Image02"], 10)),
            (0, (["Image03"], 10)),
            (0, (["Image04"], 10)),
            (0, (["Image05"], 10))
            ])


if __name__ == "__main__":
    testCase01()