#!/usr/bin/env python2.7

# FIXME this implementation does a couple very stupid things:
#   Counts every vote every time, instead of grouping identical votes
#   Recounts after every elimination, instead of just moving affected votes
# Same results either way, but it makes the code scale worse than it should

def getSeats(votes):
  seats = []
  seated = set()
  while True:
    next = getNextSeat(votes, seated)
    if len(next) == 0: break
    for cand in next: seated.add(cand)
    seats.append(next)
  return seats

def getNextSeat(votes, seated):
  eliminated = set()
  worst = set()
  while True:
    weights = getWeightsFor(votes, seated, eliminated)
    #print weights
    newWorst = getWorst(weights)
    if len(newWorst) == 0: break
    worst = newWorst
    for cand in worst:
      eliminated.add(cand)
      #break
  return map(str, sorted(list(worst)))

def getWeightsFor(votes, seated, eliminated):
  weights = dict()
  for votekey in votes:
    votetuple = votes[votekey]
    nvotes = votetuple[0]
    vote = votetuple[1]
    for rank in vote:
      for cand in rank:
        if cand in seated: continue
        if cand in eliminated: continue
        if cand in weights: continue
        weights[cand] = 0
    cands, weight = getCandidateAndWeight(vote, seated, eliminated)
    for cand in cands: weights[cand] += nvotes*weight
  return weights

def getWorst(weights):
  for cand in weights:
    minWeight = weights[cand]
    break
  worst = set()
  for cand in weights:
    weight = weights[cand]
    if weight < minWeight:
      minWeight = weight
      worst.clear()
    if weight == minWeight: worst.add(cand)
  return worst

def getCandidateAndWeight(vote, seated, eliminated):
  lastIdx = 0
  cands = set()
  s = len(seated)
  n = 0
  done = False
  for rank in vote:
    if len(cands): break
    for cand in rank:
      if cand in seated:
        n += 1
        continue
      if cand in eliminated: continue
      if len(cands): continue
      cands.add(cand)
  weight = float(1+s-n)/(1+s)
  return cands, weight

def loadVotes(path):
  import json
  with open(path, "r") as f: lines = f.readlines()
  votes_temp = []
  for line in lines:
    segs = line.split()
    count = int(segs[0])
    votetxt = " ".join(segs[1:])
    vote = json.loads(votetxt)
    votetup = (count, vote)
    votes_temp.append(votetup)
  cands = set()
  for votetup in votes_temp:
    for rank in votetup[1]:
      for cand in rank:
        cands.add(cand)
  votes = dict()
  for votetup in votes_temp:
    vote = votetup[1]
    isOK = True
    missing = cands.copy()
    for rank in vote:
      for cand in rank:
        if cand in missing: missing.remove(cand)
        else: isOK = False # Included the same candidate multiple times...
    #if len(missing): vote.append(list(missing))
    if isOK:
      count = votetup[0]
      votekey = str(vote)
      if votekey not in votes: votes[votekey] = (0, vote)
      oldtup = votes[votekey]
      assert vote == oldtup[1]
      newtup = (oldtup[0]+count, vote)
      votes[votekey] = newtup
  return votes

if __name__ == "__main__":
  import sys
  if len(sys.argv) != 2:
    print "No input file given"
    sys.exit()
  path = sys.argv[1]
  votes = loadVotes(path)
  print getSeats(votes)

