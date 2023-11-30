from pycolonies import Colonies
from pycolonies import func_spec
from pycolonies import Workflow

colonies = Colonies("localhost", 50080)

colonyname = "4787a5071856a4acf702b2ffcea422e3237a679c681314113d86139461290cf4"
executorid = "3fc05cf3df4b494e95d6a3d297a34f19938f7daa7422ab0d4f794454133341ac" 
executor_prvkey = "ddf7f7791208083b6a9ed975a72684f6406a269cfa36f1b1c32045c0a71fff05"

def gen_nums(ctx={}):
    return 1, 2 

def reduce(*nums, ctx={}):
    total = 0
    for n in nums:
        total += n
    return total 

wf = Workflow(colonyname)
f = func_spec(func=gen_nums, 
              args=[], 
              colonyname=colonyname, 
              executortype="python",
              priority=200,
              maxexectime=100,
              maxretries=3,
              maxwaittime=100)
wf.add(f, nodename="gen_nums1", dependencies=[])

f = func_spec(func=gen_nums, 
              args=[], 
              colonyname=colonyname, 
              executortype="python",
              priority=200,
              maxexectime=100,
              maxretries=3,
              maxwaittime=100)
wf.add(f, nodename="gen_nums2", dependencies=[])

func_spec = func_spec(func=reduce, 
                             args=[], 
                             colonyname=colonyname, 
                             executortype="python",
                             priority=200,
                             maxexectime=100,
                             maxretries=3,
                             maxwaittime=100) 
wf.add(func_spec, nodename="reduce", dependencies=["gen_nums1", "gen_nums2"])

processgraph = colonies.submit(wf, executor_prvkey)
print("Workflow", processgraph["processgraphid"], "submitted")

# wait for the sum_list process
process = colonies.find_process("reduce", processgraph["processids"], executor_prvkey)
process = colonies.wait(process, 100, executor_prvkey)
print(process["out"][0])
