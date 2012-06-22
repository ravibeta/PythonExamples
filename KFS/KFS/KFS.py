import pickle
l = ['abc','defg','hijk','lmno','pqrs','tuvw','xyza','bcd','efg']
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
            print Ellipsis > 1
            print "The %(foo)s is %(bar)i." % {'foo': 'answer', 'bar':42} 
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



