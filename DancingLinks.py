class Node:
    def __init__(self, row, col):
        self.ROW = row
        self.COL = col
        self.HEAD = None
        self.LEFT = None
        self.RIGHT = None
        self.UP = None
        self.DOWN = None
 
    def detach(self):
        self.UP.DOWN = self.DOWN
        self.DOWN.UP = self.UP
        self.HEAD.SIZE -= 1
         
    def attach(self):
        self.DOWN.UP = self.UP.DOWN = self
        self.HEAD.SIZE += 1
 
class Head:
    def __init__(self, col):
        self.COL = col
        self.SIZE = 0
        self.LEFT = None
        self.RIGHT = None
        self.UP = None
        self.DOWN = None
 
    def detach(self):
        self.LEFT.RIGHT = self.RIGHT
        self.RIGHT.LEFT = self.LEFT
         
    def attach(self):
        self.RIGHT.LEFT = self.LEFT.RIGHT = self

class NodeIterator:
 
    def __init__(self, node, dir):
        self.start = node
        self.curr = node
        self.dir = dir
 
    def __iter__(self):
        return self
 
    def __next__(self):
        _next = self.move()
        if _next == self.start:
            raise StopIteration
        else:
            self.curr = _next
            return _next
 
    def move(self):
        if self.dir == "L":
            return self.curr.LEFT
        elif self.dir == "R":
            return self.curr.RIGHT
        elif self.dir == "U":
            return self.curr.UP
        elif self.dir == "D":
            return self.curr.DOWN
    

def createLeftRightLinks(rows):
        for row in rows:
            n = len(row)
            for j in range(n):
                row[j].RIGHT = row[(j + 1) % n]
                row[j].LEFT = row[(j - 1 + n) % n]
             
def createUpDownLinks(cols):
    for col in cols:
        n = len(col)
        for i in range(n):
            col[i].DOWN = col[(i + 1) % n]
            col[i].UP = col[(i - 1 + n) % n]
            if i != 0:
                col[i].HEAD = col[0]

class DancingMatrix:

    def __init__(self, mat):

        nrows = len(mat)
        ncols = len(mat[0])
        self.root = Head(-1)
        self.heads = [self.root] + [Head(j) for j in range(ncols)]
        self.rows = [[] for _ in range(nrows)]
        self.cols = [[head] for head in self.heads[1:]]

        createLeftRightLinks([self.heads])

        for i in range(nrows):
            for j in range(ncols):
                if mat[i][j] == 1:
                    node = Node(i, j)
                    self.rows[i].append(node)
                    self.cols[j].append(node)
                    self.cols[j][0].SIZE += 1
        
        createLeftRightLinks(self.rows)
        createUpDownLinks(self.cols)

class DancingLinks:

    def __init__(self, mat) -> None:
        self.dmat = DancingMatrix(mat)
        self.root = self.dmat.root
        self.solution = []
    
    def cover(self, col):
        col.detach()
        for row in NodeIterator(col, "D"):
            for cell in NodeIterator(row, "R"):
                cell.detach()
    
    def uncover(self, col):
        for row in NodeIterator(col, "U"):
            for cell in NodeIterator(row, "L"):
                cell.attach()
        col.attach()    

    def search(self, k):

        if self.root.RIGHT == self.root:
            print(f"Depth {k}: Found Solution")
            return True
        
        s = 9999999999
        col = None
        for head in NodeIterator(self.root, "R"):
            if head != self.root:
                if head.SIZE < s:
                    s = head.SIZE
                    col = head
        if s == 0:
            print(f"Depth {k}: S = 0")
            return False
        print(f"Depth {k}: Covering Column {col.COL}")
        self.cover(col)

        for row in NodeIterator(col, "D"):
            print(f"Depth {k}: Working on Row {row.ROW}")
            for cell in NodeIterator(row, "R"):
                print(f"Depth {k}: Covering Column {cell.HEAD.COL}")
                self.cover(cell.HEAD)

            if self.search(k+1):
                print(f"Depth {k}: Adding Solution {row.ROW}")
                self.solution.append(row.ROW)
                return True
            
            for cell in NodeIterator(row, "L"):
                print(f"Depth {k}: Uncovering Column {cell.HEAD.COL}")
                self.uncover(cell.HEAD)
        print(f"Depth {k}: Uncovering Column {col.COL}")
        self.uncover(col)
        return False
    

matrix_A = [[0,0,1,0,1,1,0],
        [1,0,0,1,0,0,1],
        [0,1,1,0,0,1,0],
        [1,0,0,1,0,0,0],
        [0,1,0,0,0,0,1],
        [0,0,0,1,1,0,1]]


import sys
import random

sys.setrecursionlimit(2000)
 
# Generate Random Exact Cover Problem
 
def rand_list(n):
    return [random.randint(0,1) for _ in range(n)]

def rand_matrix(n_col, n_row):
    
    r_mat = [rand_list(n_col) for _ in range(n_row)]
    
    n_set = random.randint(10, int(0.25*n_col))
    set_idx = list(set([random.randint(0, n_row) for _ in range(n_set)]))
    print(f"No of actual Set {len(set_idx)}")
    for i in set_idx:
        r_mat[i] = [0 for _ in range(n_col)]
    
    for i in range(n_col):
        rand_idx = random.choice(set_idx)
        r_mat[rand_idx][i] = 1
        
    return r_mat

print("Creating an Exact Cover Problem")
new_mat = rand_matrix(2048, 2048)

print("Creating Dancing Matrix")
dl = DancingLinks(new_mat)
print("Solving the Exact Cover Problem")
dl.search(0)  

print(dl.solution)
#for i in dl.solution:
    #print(new_mat[i])
