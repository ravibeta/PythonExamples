class Employee:
	def __init__(self, id, mgrId, name):
		self.id = id
		self.mgrId = mgrId
		self.name = name
    
# sample data
E = [Employee(1, 0, 'ABC'), Employee(2, 1, 'DEF'), Employee(3, 1, 'GHI')]

# method 1
def directReports(E, c, level):
	    c.level = level
	    Reports = [e for e in E if e.mgrId == c.id]
	    c.reports = Reports
	    print 'Name:' + c.name + ' Level:' + str(c.level) + ' Reports:' +"[{0}]".format(", ".join(str(r.name) for r in Reports))
	    all(directReports(E,report,level+1) for report in Reports)

all(directReports(E,c,0) for c in E if c.mgrId == 0)

# method 2
def directReportsBFS(E):
	Q = []
	level = 0
	[Q.append(e) for e in E if e.mgrId == 0]
	while (len(Q) > 0):
		c = Q.pop(0)
		if c is None:
			level = level + 1
			continue
		c.level = level;
		Reports = [e for e in E if e.mgrId == c.id]
		c.reports = Reports
		print 'Name:' + c.name + ' Level:' + str(c.level) + ' Reports:' +"[{0}]".format(", ".join(str(r.name) for r in Reports))
		Q.append(None)
		all(Q.append(report) for report in Reports)
		
directReportsBFS(E)	
