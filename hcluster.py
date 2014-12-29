def tanimoto(v1, v2):
    c1, c2, shr = 0,0,0
    
    for i in range(len(v1)):
      if v1[i] != 0: c1 += 1 # in v1
      if v2[i] != 0: c2 += 1 # in v2
      if v1[i] != 0 and v2[i] != 0: shr += 1 # in both

    d = c1 + c2 - shr 
    if d == 0:
            d = 1

    return 1.0 - (float(shr)/d)

class bicluster:
    def __init__(self,vec,left=None,right=None,distance=0.0,id=None):
        self.left=left 
        self.right=right
        self.vec=vec
        self.id=id
        self.distance=distance

    def detail(self):
        print 'id = ' + str(self.id) + ' vec =' + repr(self.vec) + ' dist =' + str(self.distance)
        if self.left:
           self.left.detail()
        if self.right:
           self.right.detail()

def hcluster(rows,distance=tanimoto):
    distances={}
    currentclustid=-1
    
    # Clusters are initially just the rows
    clust=[bicluster(rows[i],id=i) for i in range(len(rows))]
    while len(clust)>1:
       lowestpair=(0,1)
       closest=distance(clust[0].vec,clust[1].vec)
       # loop through every pair looking for the smallest distance
       for i in range(len(clust)):
           for j in range(i+1,len(clust)):
               # distances is the cache of distance calculations
               if (clust[i].id,clust[j].id) not in distances:
                   distances[(clust[i].id,clust[j].id)]=distance(clust[i].vec,clust[j].vec)
               d=distances[(clust[i].id,clust[j].id)]
               if d<closest:
                  closest=d
                  lowestpair=(i,j)
       # calculate the average of the two clusters
       mergevec=[
       (clust[lowestpair[0]].vec[i]+clust[lowestpair[1]].vec[i])/2.0
       for i in range(len(clust[0].vec))]
     
       # create the new cluster
       left = None
#       if clust[lowestpair[0]].id < 0:
       left = clust[lowestpair[0]]
       right = None
#       if clust[lowestpair[1]].id < 0:
       right = clust[lowestpair[1]]
       newcluster=bicluster(mergevec,left=left,
                            right=right,
                            distance=closest,id=currentclustid)
       # cluster ids that weren't in the original set are negative
       currentclustid-=1
       del clust[lowestpair[1]]
       del clust[lowestpair[0]]
       clust.append(newcluster)
    return clust[0]

rows = [(1,0,0), (0,1,0), (0,0,1)]
hcluster(rows).detail()

#Courtesy: Book on Programming Collective Intelligence By Toby Segaran
