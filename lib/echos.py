from bs4 import BeautifulSoup

# 1) These functions
# 2) Labeler service
# 3) MongoDB metadata storage
# 4) Basic UI
# 5) Basic web service to power UI

# Accepts a bunch of HTML and outputs as much of the relevant article text as
# possible. Ideally this will include caption text.
def bodytext(html):
  bs = BeautifulSoup(html)  
  return bs.get_text()

# Accepts a bunch of text and generates a list of unique tokens from it. The
# token list can be unigrams and bigrams for now.
def tokenize(text, unique=True):
  unigrams = text.split(' ')
  bigrams = zip(unigrams[:-1], unigrams[1:])
  
  unigrams.extend(bigrams)
  if unique:
    return list(set(unigrams))
  else:
    return unigrams

# For the provided token, generate a weight between [0, 1]. Two thoughts for how
# to do this now: (1) count # of occurrences and (2) weigh by where it occurs in
# the doc, closer to the beginning is higher score.
def weight(target, text):
  # TODO: No need to do this every time, though we do need repetition in this list.
  tokens = tokenize(text, unique=False)

  locs = []
  # Check the unigrams list.
  if len(target) == 1:
    unigrams = [token for token in tokens if len(token) == 1]
    locs = [i for i, token in enumerate(unigrams) if token == target]
  # Otherwise check the bigrams list.
  else:
    bigrams = [token for token in tokens if len(token) == 2]
    locs = [i for i, token in enumerate(bigrams) if token == target]

  # Get the importance of each mention. Simple linear formula now...could be way smarter.
  raw_weights = [1.0 - (loc / count) for loc in locs]

  return sum(raw_weights)
