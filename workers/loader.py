import juggle, sys
# TODO: consider moving this behind the queue interface?
import proto.Task_pb2 as proto

##################################################################
## Add all feeds from the file specified by the first parameter ##
## and add them to the 'feeds' queue.                           ##
##                                                              ##
## Not really a worker since it only runs periodically.         ##
##################################################################

feedsq = juggle.Queue('feeds')

with open(sys.argv[1]) as fp:
  feeds = [line.strip() for line in fp.readlines()]

  for feed in feeds:
    task = proto.Task()
    task.content.location = feed
    task.content.type = proto.Location.WEB_URL

    feedsq.push(task)
