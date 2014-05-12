class Employee:
	def __init__(self, id, mgrId, name):
		self.id = id
		self.mgrId = mgrId
		self.name = name
    
# sample data
#E = [Employee(1, 0, 'ABC'), Employee(2, 1, 'DEF'), Employee(3, 1, 'GHI')]
E = [Employee(1, 1, 'ABC'), Employee(4,4,'IJK'), Employee(2, 1, 'DEF'), Employee(5,4,'MNO'), Employee(3, 1, 'GHI')]

def directReportsBFS(E,s):
	Q = []
	level = 0
	Q.append(s)
	while (len(Q) > 0):
		c = Q.pop(0)
		if c is None:
			level = level + 1
			continue
		Reports = [e for e in E if e.mgrId == c.id and e.mgrId != e.id]
		print 'Name:' + c.name + ' Level:' + str(level) + ' Reports:' +"[{0}]".format(", ".join(str(r.name) for r in Reports))
		Q.append(None)
		all(Q.append(report) for report in Reports)


[directReportsBFS(E,e) for e in E if e.mgrId == e.id]
