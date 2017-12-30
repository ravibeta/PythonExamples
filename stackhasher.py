#! /usr/bin/python
import hashlib
hashes = {}
distinct_stacks = []
def hash(data): 
      # unix command md5sum
      # print("StackTrace with %s bytes and md5=%s" % (len(data),hashlib.md5(data).hexdigest()))
      return hashlib.md5(data).hexdigest()
      # StackTrace with 1244 bytes and md5=1f369406ec1243e5bc3aead95e97f380

# strip a stack before comparision, canonicalize if necessary:
def prepare(stk):
      if stk:
         lines = stk.split('\n')
         ret = [x.split('(')[0].strip().replace(" ","") for x in lines]
         if ret:
            return ret
      
      
def compare(stk1, stk2):
     lines1 = stk1.split('\n')
     lines2 = stk2.split('\n')
     if (len(lines1) == 0 or len(lines2) == 0):
        return false
     min = len(lines1)
     if len(lines2) < min:
         min = len(lines2)
     count = 0
     for i in range(min):
         line2 = lines2[i].split('(')[i].strip().replace(" ", "")
         line1 = lines1[i].split('(')[i].strip().replace(" ", "")
         if line1.lower() != line2.lower():
            return false
         if count > 2:
            return true
         count=count+1
         return False

def count(stk, hashes, distinct_stacks):
       prepared = prepare(stk)
       if prepared:
            prepared = '\n'.join(prepared)
            hashed = hash(prepared)
            if hashed in hashes:
               hashes[hashed] += 1
            else:
               distinct_stacks += [prepared]
               hashes[prepared] = 1
 
def parse(filename, hashes, distinct_stacks):
      with open(filename, 'r') as fin:
              lines = fin.readlines()
              for line in lines:
                    if "Exception:" in line:
                        stk = '\n'.join(line.split("at"))
                        count(stk, hashes, distinct_stacks)


###
>>> hashes = {}
>>> distinct_stacks = []
>>> stackhasher.parse('stacktrace.txt', hashes, distinct_stacks)
>>>
>>> hashes
{'com.devdaily.sarah.tests.TrySuccessFailure$AlsException:Bummer!\n': 1}
>>> distinct_stacks
['com.devdaily.sarah.tests.TrySuccessFailure$AlsException:Bummer!\n']
>>>
###
