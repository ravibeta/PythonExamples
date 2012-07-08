import pickle
import sys
import os

l = ('abc','defg','hijk','lmno','pqrs','tuvw','xyza','bcd','efg')
class FileRWTester:
     def ReadWrite(self):    
        name = raw_input("File name with path: ")
        with open(name,'w') as f:
            del f
        with open(name,'w') as f:
            pickle.dump(l,f)
        with open(name, 'r') as r:
            u = pickle.load(r)
            print u
            for word in u:
                print word
            for index,item in enumerate(l):
                print index, item
            print Ellipsis > 1
            positions = [[col + row * 3 for col in range(3)] for row in range(3)]
            print positions
            print "The %(foo)s is %(bar)i." % {'foo': 'answer', 'bar':42} 
        r.closed

class Property(object):
    def __init__(self, fget):
        self.fget = fget
 
    def __get__(self, obj, type):
        if obj is None:
            return self
        return self.fget(obj)

def print_args(function):
    def wrapper(*args, **kwargs):
        print 'Arguments:', args, kwargs
        return function(*args, **kwargs)
    return wrapper


'''
                5
        3           9
    2       4   7       10
1              6    8
'''
class Node:
    def __init__(self, data, l = None, r = None):
        self.l = l
        self.r = r
        self.data = data

    def __unicode__(self):
        return '%s' % self.data
    @Property 
    def value(self): 
        return self.data
     
n = []

for i in range(11):
    n.append(Node(i))

n[5].l = n[3]
n[5].r = n[9]
n[3].l = n[2]
n[3].r = n[4]
n[9].l = n[7]
n[9].r = n[10]
n[2].l = n[1]
n[7].l = n[6]
n[7].r = n[8]

@print_args
def dfs(tree):
    nodes = []
    if (tree != None):
        nodes.append(tree.data)
        nodes.extend(dfs(tree.l))
        nodes.extend(dfs(tree.r))
    return nodes

@print_args
def inorder(root):
    if root:
        for x in inorder(root.l):
            yield x
        yield root.data
        for x in inorder(root.r):
            yield x
i = []
m = inorder(n[5])
i.append(m.next())
i.append(m.send(Node(1)))
i.append(m.next())

@print_args
def indexall(t, value):
     pos = -1
     try:
         while True:
            pos = t.index(value, pos+1)
            yield pos
     except ValueError:
         pass




try:
    '''fi = FileRWTester()
    fi.ReadWrite()'''
    print dfs(n[5])
    print i
    for m in range(3):
        print m, i[m]
        if ( i == 3):
            break
    else:
        print("i was never 3")
    j = {'aaabbbccc':1, 'dddeeefff':2, 'ggghhhiii':3, 'dddeeefff':4, 'xxxyyyzzz':5}
    '''l = OrderedDict(sorted(j.items(), key  = lambda t:t[0]))'''
    h = sorted(j.items(),key = lambda t:t[0])
    print h
    args = (j.keys(), 'dddeeefff')
    ix = list(indexall(*args))
    print ix
    str = 'aaabbbcccdddeeefffggghhhiiidddeeefffxxxyyyzzz'
    ix2 = list(indexall(str,'d'))
    print ix2
    str2 = [x for x in str.capitalize() if x == 'A']
    print str2
    print str[::-1] 
    print str[::2]
    print str[1:5:2]
    j['mmmnnnooo'] = j.get('mmmnnnooo',6)
    print j
    for item in j.iteritems():
        print item
    print("The string is {foo} with {bar} letter".format(foo=str, bar=45)) 
    print os.listdir('c:\\a')
    def double(L):
        for x in L:
            yield x*2
    items = list(double([1,2,3,4,5]))
    print items

except :
   print "UnexpectedError:", sys.exc_info()[0]
else: 
   print "Read Write over"
finally:
    print "Done"

