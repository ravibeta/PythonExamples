class Employee:
	def __init__(self, id, mgrId, name):
		self.id = id
		self.mgrId = mgrId
		self.name = name
    
# sample data
E = [Employee(1, 0, 'ABC'), Employee(2, 1, 'DEF'), Employee(3, 1, 'GHI')]


def directReportsBFS(E):
	Q = []
	level = 0
	[Q.append(e) for e in E if e.mgrId == 0]
	while (len(Q) > 0):
		c = Q.pop(0)
		if c is None:
			level = level + 1
			continue
		Reports = [e for e in E if e.mgrId == c.id]
		print 'Name:' + c.name + ' Level:' + str(level) + ' Reports:' +"[{0}]".format(", ".join(str(r.name) for r in Reports))
		Q.append(None)
		all(Q.append(report) for report in Reports)
		
directReportsBFS(E)	
