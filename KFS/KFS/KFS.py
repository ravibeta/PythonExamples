f = open('/tmp/workfile','w')
print f
f.write('Hello World\n')
f.close()
with open('/tmp/workfile', 'r') as r:
	for line in r:
		print line
r.closed
