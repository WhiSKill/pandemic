import multiprocessing as mp
import snap
import Queue
from math import ceil

# multiprocessing library code from:
# http://eli.thegreenplace.net/2012/01/16/python-parallelizing-cpu-bound-tasks-with-multiprocessing
def mp_closeness(node_id_list, nprocs, G):
    def worker(node_id_list, out_q, G):
        """ The worker function, invoked in a process. 'nums' is a
            list of node_id's from a graph. The results are placed in
            a dictionary that's pushed to a queue.
        """
        outdict = {}
        for id in node_id_list:
            outdict[id] = snap.GetClosenessCentr(G, id)
        out_q.put(outdict)

    # Each process will get 'chunksize' nums and a queue to put his out
    # dict into
    out_q = Queue.Queue()
    chunksize = int(ceil(len(node_id_list) / float(nprocs)))
    procs = []

    for i in range(nprocs):
        p = mp.Process(
                target=worker,
                args=(node_id_list[chunksize * i:chunksize * (i + 1)],
                      out_q))
        procs.append(p)
        p.start()

    # Collect all results into a single result dict. We know how many dicts
    # with results to expect.
    resultdict = {}
    for i in range(nprocs):
        resultdict.update(out_q.get())

    # Wait for all worker processes to finish
    for p in procs:
        p.join()

    return resultdict

if __name__ == '__main__':
    mp_closeness(node_id_list, NUM_PROCS, G_snap)
