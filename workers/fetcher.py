import juggle, feedparser

############################################
## fetcher is responsible for retrieving all of the stories in a particular
## feed and storing them. Fetchers also fire off one new task per article 
## for labeling.
############################################ 

feedq = juggle.Queue('feeds')
#labelq = juggle.Queue('labeling')
docstore = juggle.Docstore('docs')

msg = feedq.pop()
print msg

# Fetch all articles for this feed.
while True:
  url = feedq.pop().loc.url
  doc = feedparser.parse(url)

  for story in doc['channel']['item']:
    print story['title']

    # TODO: Add some extra fields.
    doc = {
      'title': doc['feed']['title'],
      'filename': 'abcde123' # TODO: hash function
    }

    # Store the document in the shared document store.
    docstore.store(doc)

    # Submit the article to the labeling queue. Then the
    # fetcher's job is complete.
    story = proto.Task()
    story.loc.fSLoc = doc['filename']
    labelq.push(story)
