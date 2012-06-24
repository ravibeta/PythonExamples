import pickle
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
            print "The %(foo)s is %(bar)i." % {'foo': 'answer', 'bar':42} 
        def double(L):
            for x in L:
                yield x*2
        items = list(double([1,2,3,4,5]))
        print items
        r.closed

try:
    fi = FileRWTester()
    fi.ReadWrite()
except e:
   print e
else: 
   print "Read Write over"
finally:
    print "Done"



