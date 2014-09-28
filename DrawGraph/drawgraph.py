# The following program lays out a graph with little or no crossing lines.
# Code samples taken from "Programming Collective Intelligence" by OReilly Media

from PIL import Image, ImageDraw
import math
import random

vertex = ['A','B','C','D','E']
links=[('A', 'B'),
('B', 'C'),
('C', 'D'),
('D', 'E'),
('E', 'A'),
('C', 'E'),
('A', 'D'),
('E', 'B')]
domain=[(10,370)]*(len(vertex)*2)

def randomoptimize(domain,costf):
    best=999999999
    bestr=None
    for i in range(1000):
        # Create a random solution
        r=[random.randint(domain[i][0],domain[i][1]) for i in range(len(domain))]
        # Get the cost
        cost=costf(r)
        # Compare it to the best one so far
        if cost<best:
            best=cost
            bestr=r
    return r

def annealingoptimize(domain,costf,T=10000.0,cool=0.95,step=1):
    # Initialize the values randomly
    vec=[float(random.randint(domain[i][0],domain[i][1]))
         for i in range(len(domain))]

    while T>0.1:
        # Choose one of the indices
        i=random.randint(0,len(domain)-1)
        # Choose a direction to change it
        dir=random.randint(-step,step)
        # Create a new list with one of the values changed
        vecb=vec[:]
        vecb[i]+=dir
        if vecb[i]<domain[i][0]: vecb[i]=domain[i][0]
        elif vecb[i]>domain[i][1]: vecb[i]=domain[i][1]

        # Calculate the current cost and the new cost
        ea=costf(vec)
        eb=costf(vecb)
        p=pow(math.e,(-eb-ea)/T)
        # Is it better, or does it make the probability
        # cutoff?
        if (eb<ea or random.random( )<p):
            vec=vecb

        # Decrease the temperature
        T=T*cool
    return vec

def crosscount(v):
    # Convert the number list into a dictionary of person:(x,y)
    loc=dict([(vertex[i],(v[i*2],v[i*2+1])) for i in range(0,len(vertex))])
    total=0

    # Loop through every pair of links
    for i in range(len(links)):
      for j in range(i+1,len(links)):

        # Get the locations
        (x1,y1),(x2,y2)=loc[links[i][0]],loc[links[i][1]]
        (x3,y3),(x4,y4)=loc[links[j][0]],loc[links[j][1]]
        
        den=(y4-y3)*(x2-x1)-(x4-x3)*(y2-y1)
        
        # den==0 if the lines are parallel
        if den==0: continue

        # Otherwise ua and ub are the fraction of the
        # line where they cross
        ua=((x4-x3)*(y1-y3)-(y4-y3)*(x1-x3))/den
        ub=((x2-x1)*(y1-y3)-(y2-y1)*(x1-x3))/den
        
        # If the fraction is between 0 and 1 for both lines
        # then they cross each other
        if ua>0 and ua<1 and ub>0 and ub<1:
            total+=1

    for i in range(len(vertex)):
        for j in range(i+1,len(vertex)):
          # Get the locations of the two nodes
          (x1,y1),(x2,y2)=loc[vertex[i]],loc[vertex[j]]

          # Find the distance between them
          dist=math.sqrt(math.pow(x1-x2,2)+math.pow(y1-y2,2))
          # Penalize any nodes closer than 50 pixels
          if dist<50:
            total+=(1.0-(dist/50.0))
    return total
		
def drawnetwork(loc):
    #create the image
    img = Image.new('RGB', (400,400),(255,255,255))
    draw=ImageDraw.Draw(img)
    #create the position dict
    pos=dict([(vertex[i],(loc[i*2],loc[i*2+1])) for i in range(0, len(vertex))])
    #Draw Links
    for (a,b) in links:
        draw.line((pos[a],pos[b]), fill=(255,0,0))
    #Draw vertex
    for (n,p) in pos.items():
        draw.text(p,n,(0,0,0))
    img.save('graph.jpg', 'JPEG')
    img.show()

sol=randomoptimize(domain,crosscount)
crosscount(sol)
sol=annealingoptimize(domain,crosscount,step=50,cool=0.99)
crosscount(sol)
drawnetwork(sol)