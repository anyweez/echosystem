import juggle, feedparser, time, datetime

############################################
## fetcher is responsible for retrieving all of the stories in a particular
## feed and storing them. Fetchers also fire off one new task per article 
## for labeling.
############################################ 

def clean_description(desc):
  if len(desc.split('<div')) > 1:
    return desc.split('<div')[0]
  else:
    return desc

feedq = juggle.Queue('feeds')
#labelq = juggle.Queue('labeling')
docstore = juggle.Docstore('news.docs')

print 'Awaiting feeds...'
# Fetch all articles for this feed.
while True:
  tasks = feedq.pop()
  print tasks

  if tasks is not None:
    # Juggle will only return one feed at this point, but the protocol supports sending
    # multiple tasks and this should be the assumption of clients. This *may* move into
    # the juggle lib later...haven't decided what's best yet.
    for task in tasks:
      url = task.content.location
      print 'Feed received:', url
      doc = feedparser.parse(url)

      print len(doc.entries)

      for story in doc.entries:
        print '%s <%s>' % (story.title, story.link)
	with urllib2.urlopen(story.link) as fp:
  	  body = fp.read()
        
	# TODO: Add some extra fields.
        doc = {
          'title': story.title,
	  'description': clean_description(story.description),
	  'published': story.published,
	  'source_url': url,
	  'retrieved': datetime.datetime.utcnow().strftime('%a, %d %b %Y %H:%M:%S GMT'),
	  # docid is added once the document is stored
        }

	doc['docid'] = docstore.store(doc, body)

        # Submit the article to the labeling queue. Then the fetcher's job is
	# complete!
#        article = proto.Task()
#        article.content.location = doc['docid']
#        article.content.type = proto.Task.Location.DOCUMENT
#        labelq.push(article)
  # TODO: Move this into jugglelib.
  else:
    time.sleep(5)
