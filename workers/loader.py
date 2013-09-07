import juggle

##################################################################
## Add all feeds from the file specified by the first parameter ##
## and add them to the 'feeds' queue.                           ##
##                                                              ##
## Not really a worker since it only runs periodically.         ##
##################################################################

feedsq = juggle.Queue('feeds')

with open(sys.arg[1]) as fp:
  feeds = [line.strip() for line in fp.readlines()]

  for feed in feeds:
    task = proto.Task()
    task.loc.url = feed
    feedsq.push(task)
