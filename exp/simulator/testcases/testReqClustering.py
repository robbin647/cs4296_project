from ..simulator import Simulator
from ..trace import Tracer

IMAGE_LAYER_MAPPING = {
        "Image01": ["Layer01", "Layer02"],
        "Image02": ["Layer02", "Layer03"],
        "Image03": ["Layer03", "Layer04"],
        "Image04": ["Layer05", "Layer06"],
        "Image05": ["Layer05"],
        "Image06": ["Layer01", "Layer02", "Layer03"],
        "Image07": ["Layer03", "Layer04", "Layer05", "Layer06"],
        "Image08": ["Layer02", "Layer03", "Layer05", "Layer06"],
        "Image09": ["Layer01", "Layer04", "Layer05"],
        "Image10": ["Layer04", "Layer06"]
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
                     (0, (["Image05"], 10)),
                     (0, (["Image09"], 10)),
                     (0, (["Image10"], 10)),
                     (0, (["Image06"], 10)),
                     (0, (["Image07"], 10)),
                     (0, (["Image08"], 10))
                     ]
    req_batch_after_clustering = mySim.request_clustering(request_batch, TOP_LAYER_RATIO=1.0)
    print(req_batch_after_clustering)
    assert(req_batch_after_clustering == [
            (0, (['Image03'], 10)), 
            (0, (['Image04'], 10)), 
            (0, (['Image05'], 10)), 
            (0, (['Image10'], 10)), 
            (0, (['Image07'], 10)), 
            (0, (['Image08'], 10)), 
            (0, (['Image01'], 10)), 
            (0, (['Image02'], 10)), 
            (0, (['Image06'], 10)), 
            (0, (['Image09'], 10))
            ])

def testCase02(): #prove it can handle requests with multiple images
    request_batch = [
                     (0, (["Image01"], 10)),
                     (0, (["Image03"], 10)),
                     (0, (["Image04"], 10)),
                     (0, (["Image02"], 10)),
                     (0, (["Image05"], 10)),
                     (0, (["Image09", "Image10"], 10)),
                     (0, (["Image10"], 10)),
                     (0, (["Image06"], 10)),
                     (0, (["Image07"], 10)),
                     (0, (["Image08"], 10))
                     ]
    req_batch_after_clustering = mySim.request_clustering(request_batch, TOP_LAYER_RATIO=1.0)
    print(req_batch_after_clustering)
    assert(req_batch_after_clustering == [
            (0, (['Image03'], 10)), 
            (0, (['Image04'], 10)), 
            (0, (['Image05'], 10)), 
            (0, (['Image09', 'Image10'], 10)),
            (0, (['Image10'], 10)), 
            (0, (['Image07'], 10)), 
            (0, (['Image08'], 10)), 
            (0, (['Image01'], 10)), 
            (0, (['Image02'], 10)), 
            (0, (['Image06'], 10)), 
            ])

if __name__ == "__main__":
    testCase01()
    testCase02()