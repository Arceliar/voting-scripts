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
  weights = getWeightsFor(votes, seated)
  best = getBest(weights)
  return map(str, sorted(list(best)))

def getWeightsFor(votes, seated):
  weights = dict()
  for votekey in votes:
    votetuple = votes[votekey]
    nvotes = votetuple[0]
    vote = votetuple[1]
    scores = getScores(vote, seated)
    for cand in scores:
      if cand not in weights: weights[cand] = 0.
      weights[cand] += nvotes*scores[cand]
  return weights

def getBest(weights):
  maxWeight = 0
  best = set()
  for cand in weights:
    weight = weights[cand]
    if weight > maxWeight:
      maxWeight = weight
      best.clear()
    if weight == maxWeight: best.add(cand)
  #print "Best:", best, "with score:", maxWeight
  #print "All:", weights
  return best

def getScores(vote, seated):
  lastIdx = 0
  scores = dict()
  s = len(seated)
  n = 0.
  for cand in vote:
    if cand in seated: n += vote[cand]
    else: scores[cand] = vote[cand]
  weight = float(1+s-n) #/ float(1+s) # The denominator has no effect on the result, it's just to normalize
  for cand in scores: scores[cand] *= weight
  return scores

def loadVotes(path):
  import json
  with open(path, "r") as f: lines = f.readlines()
  votes_temp = []
  for line in lines:
    segs = line.split()
    count = int(segs[0])
    votetxt = " ".join(segs[1:])
    voteList = json.loads(votetxt)
    vote = dict()
    for idx in xrange(len(voteList)):
      # FIXME i don't have scores in my voting files, so i make some up
      # Assigning a score of 1 is equivalent to approval voting
      # Score distribution has a large effect on the result
      score = 1. - float(idx)/len(voteList)
      #score = .99**idx
      for cand in voteList[idx]:
        vote[cand] = score
    votetup = (count, vote)
    votes_temp.append(votetup)
  cands = set()
  for votetup in votes_temp:
    for cand in votetup[1]:
      cands.add(cand)
  votes = dict()
  for votetup in votes_temp:
    vote = votetup[1]
    for cand in cands:
      if cand not in vote: vote[cand] = 0.
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

