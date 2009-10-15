import heapq

'''
Library for determining connectivity.

Will start off simple, then get more convoluted.

Initial check is for direct hit mapping.

Could use quad-trees, R-trees, something like that later.

For now, just get something basic, but somewhat better than O(n**2) working.
We mitigate O(n**2) by having smaller buckets, e.g. (n/10) ** 2 == n**2 / 100.

Needs to support non-orthogonal lines, but doesn't need to be fast at them.


'''

def normalize(mylist):
    result = []
    for x1, y1, x2, y2, obj in mylist:
        x1, x2 = sorted(x1, x2)
        y1, y2 = sorted(y1, y2)
        result.append((x1, y1, x2, y2, obj))

def make_buckets(mylist, dimx, dimy, bucket_size):
    buckets = [[[] for y in range(0, dimy, bucket_size)] for x in range(0, dimx, bucket_size)]

    for item in mylist:
        x1, y1, x2, y2, obj = item
        assert x1 >= 0 and y1 >= 0
        for x in range(x1 // bucket_size, x2 // bucket_size + 1):
            for y in range(y1 // bucket_size, y2 // bucket_size + 1):
                buckets[x][y].append(item)

    for bucketlist in buckets:
        for bucket in bucketlist:
            yield bucket


def group_items(mylist, startindex, stopindex):
    if not mylist:
        return
    mylist = sorted(((obj[startindex], obj[stopindex], obj) for obj in mylist))
    result = []
    prev_x = mylist[0][0]
    for x1, x2, obj in mylist:
        if x1 != prev_x:
            yield result
            result = []
        result.append(obj)
        prev_x = x1
    yield result

def overlap_one_dimension(mylist, startindex, stopindex, push=heapq.heappush, pop=heapq.heappop):
    objheap = []
    for group in group_items(mylist, startindex, stopindex):
        x1 = group[0][startindex]
        while objheap and objheap[0][0] < x1:
            pop(objheap)
        for obj in group:
            push(objheap, (obj[stopindex], obj))
        if len(objheap) > 1:
            yield [x[1] for x in objheap]


def find_collisions(mylist, collision_set=None, normalized=False):
    ''' Assumes list of (x1, y1, x2, y2, obj) items
    '''
    x1_index, y1_index, x2_index, y2_index, obj_index = range(5)
    if collision_set is None:
        collision_set = set()
    if not normalized:
        mylist = normalize(mylist)

    for xlist in overlap_one_dimension(mylist, x1_index, x2_index):
        for ylist in overlap_one_dimension(xlist, y1_index, y2_index):
            for a in ylist:
                for b in ylist:
                    if a < b:
                        collision_set.add((a,b))
    return collision_set

def find_collisions_via_buckets(mylist, dimx=11000, dimy=85000, bucket_size=2000, normalized=False):
    ''' Assumes list of (x1, y1, x2, y2, obj) items
    '''
    if not normalized:
        mylist = normalize(mylist)
    collision_set = set()
    for bucket in make_buckets(mylist, dimx, dimy, bucket_size):
        find_collisions(bucket, collision_set, True)
    return collision_set
