# Voting Scripts

This repository contains a few scripts to test out some voting schemes, along with some example ballot counts (in a terrible format I threw together when transcribing vote counts from wikipedia examples).

## STV

[stv.py](src/stv.py) is to test voting system that uses ranked ballots, and gives results that seem to be consistent with single transferable vote systems.
In particular, in every test I've come up with, I seem to give the same results as STV using [Meek's method](https://en.wikipedia.org/wiki/Counting_single_transferable_votes#Meek) and the [Hagenbach-Bischoff quota](https://en.wikipedia.org/wiki/Hagenbach-Bischoff_quota).
The important thing to note is that it uses neither of these things explicitly--it doesn't even depend on specifying the number of seats to be filled.
It returns an ordered list of candidates (with the possibility of ties), which can be truncated to the desired number of seats, such that the last's determination happens to match the Meek+Hagenbach-Bischoff combination.
Only some relatively simple integer math is involved in the reweighing scheme, so it's slightly tedious but possible to use for hand counted ballots.

## Approval

[approval.py](src/approval.py) applies the reweighing scheme from above to get a sorted list of candidates from approval voting ballots.
So it's basically an approval voting system with proportional representation, hand countable, and the semantics don't depend on the number of seats being filled.

## Score

[score.py](src/score.py) generalizes the approval system above to use score voting, where scores must be mapped onto the range between 0 and 1 inclusive.
It uses floats out of convenience, so the implementation loses some precision, but it would work fine with rational numbers instead.
Since I don't have score voting ballots, this implementation takes the ranked votes and assigns some scores based on the ranking, just to test.

# The reweighing system

Each ballot has a weight applied equal to:

`1 + (seats filled so far) - (candidates seated so far of equal or higher rank than the highest unseated uneliminated candidate on this ballot)`, where the last term is replaced by total weight of all filled seats from this ballot in the case of the score voting scheme.
This could be renormalized by dividing by a factor of `1 + (filled seats)` if you want to remap weights to between 0 and 1, but that norm factor is omitted since it has no affect on the outcome.

Each voting system then loops over candidates and iteratively removes the candidate with the least support.
In the STV system, votes are then recounted ignoring the eliminated candidate.
The last remaining candidate (or tied subset of candidates) are then selected to fill the next steat.
The process then repeats to select the next candidate to seat, with new weights applied to all ballots based on the candidates seated so far.

I realize that's kind of a terrible explanation, but it's very little code, so I suggest just reading the source if you're interested enough to have made it to this point.

