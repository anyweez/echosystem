import juggler, time, echos

######################################
## labeler scans a document and tags it with mid's for countries that are
## referenced in the document. It then scores the countries based on their
## relevance to the article.
######################################

labelq = juggler.Queue('labeling')
docstore = juggler.Docstore('news.docs')

while True:
  tasks = labelq.pop()

  if tasks is not None:
    for task in tasks:
      locations = {}
      docid = task.content.location
      meta, body = docstore.load(docid)

      # TODO: build this
      text = echos.bodytext(body)
      # TODO: build this. Returned list should not have any duplicates.
      tokens = echos.tokenize(text)

      # Labeling all of the identifying tokens.
      for token in tokens:
        label = labeler.query(token)

	if label is not None:
          weight = echos.weigh(token, text)
	  
	  if locations.has_key(label):
	    locations[label].append( (token, weight) )
	  else:
            locations[label] = [ (token, weight) ]

      # Scoring. Currently just a sum.
      # Eventually: weigh location mentions by how often they are usually mentioned.
      top_loc = None
      top_score = None
      # If any other geo labels already exist, clear them.
      meta['geo'] = {}

      for location in locations.keys():
	meta['geo'][location] = sum([ t[1] for t in locations[location] ])

      # Save the new annotations.
      # TODO: Make sure docstore's 'save' == 'update'
      docstore.save(meta, body)

  # TODO: move this into jugglerlib
  else:
    time.sleep(5)
