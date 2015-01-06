import accounts
import praw
import sys
import datetime
import random

def login():
	r.login(username, password)

r = praw.Reddit('lmao-bot by /u/Xwerve and /u/liquidized')
username = accounts.lmao_bot_user
password = accounts.lmao_bot_pass
login()

key_phrase_list = ['ay', 'ayy', 'ayyy', 'ayyyy', 'ayyyyy', 'ayyyyyy', 'ayyyyyyyy', 'ayyyyyyyyy', 'ayyyyyyyyyy', ' ay', 'ay ', 'ayy ', ' ayy']
the_phrase_list = ['ayy lmao', 'ayylmao', 'ayy lamo']
empty = ['']*100

banned_subreddits_list = 	['askreddit', 'teenagers', 'nfl', 'pcmasterrace', 'globaloffensive', 'globaloffensivetrade', \
					      	'suicidewatch', 'depression', 'whowouldwin', 'dota2', 'mildlyinteresting', 'me_irl', 'csgobetting',
					      	'ayylmao', 'nba', 'circlejerk', 'csgolounge']
ok_subs = 'all'
banned_responders_list = [username, 'ayy_lmao_bot', 'AutoModerator']

# uses dictionaries because they are faster to search through
banned_responders = dict(zip(banned_responders_list, empty))
key_phrase = dict(zip(key_phrase_list, empty))
the_phrase = dict(zip(the_phrase_list, empty))
banned_subreddits = dict(zip(banned_subreddits_list, empty))

#list of random posts
random_strings = 	['[ayy lmao](https://www.youtube.com/watch?v=OZ1-yNTWXj4)', \
					'[ayy lmao](http://www.reddit.com/r/ayylmao)', \
					'[ayy lmao](http://i.imgur.com/Y5ycwfM.jpg)', \
					'[ayy lmao](http://38.media.tumblr.com/431a57f56e81ff699ede2dd9ee84e942/tumblr_n900iqw4hD1tnkm5to1_500.gif)^(seizure warning)', \
					'[ayy lmao](http://i.imgur.com/PXr5x64.jpg)', \
					'[ayy lmao](http://i.imgur.com/EYX5BQb.png)', \
					'[ayy lmao](http://imgur.com/80ivZjn)', \
					'[ayy lmao](http://i0.kym-cdn.com/photos/images/original/000/632/613/42d.jpg)', \
					'[ayy lmao](http://25.media.tumblr.com/db0b336c4acf2713ba1a27853b6c1cfd/tumblr_mverfjZl7t1qkgh4go1_500.jpg)', \
					'[ayy lmao](http://i2.kym-cdn.com/photos/images/newsfeed/000/861/112/ee8.gif)', \
					'[ayy lmao](http://i0.kym-cdn.com/photos/images/newsfeed/000/827/015/5e3.png)']



#keeps track of recent comments
comment_ids = {}
#cannot post to same thread 3 times as a courtesy
link_ids = {}

def trytoreply(response):
	try:
		if str(comment.subreddit).lower() in banned_subreddits:
			print("Comment found in banned subreddit: " + str(comment.subreddit) + " by " + str(comment.author))
		elif comment.link_id not in link_ids:
			comment_ids[str(comment.id)] = ''
			link_ids[comment.link_id] = 1
			comment.reply(response)
			print('Commented on ' + str(comment) + ' posted by ' + str(comment.author) + ' in ' + str(comment.subreddit) + ' at ' + str(datetime.datetime.now().time()))
		else:
			comment_ids[str(comment.id)] = ''
			if link_ids[comment.link_id] >= 3:
				print("Posted too much in " + str(comment.link_title) + " in " + str(comment.subreddit))
			else:
				link_ids[comment.link_id] += 1
				comment.reply(response)
				print('Commented on ' + str(comment) + ' posted by ' + str(comment.author) + ' in ' + str(comment.subreddit) + ' at ' + str(datetime.datetime.now().time()))
	except:
		print('Could not reply to ' + str(comment.author) + ' in ' + str(comment.subreddit))


for comment in praw.helpers.comment_stream(r, ok_subs, limit=None, verbosity=0):
	#pops ids off of stack to not take up too much memory
	if len(comment_ids) > 100:
		comment_ids.popitem()
	if len(link_ids) > 100:
		link_ids.popitem()
	#skips banned or unreasonable subreddits
	else:
		#iterates through comment and post lists that it has gathered in order to see if they contain key words
		if str(comment).lower() in key_phrase and str(comment.author) not in banned_responders and str(comment.id) not in comment_ids:
			trytoreply('lmao')
		if (str(comment).lower()[:8] or str(comment).lower()[1:9]) in the_phrase and str(comment.author) not in banned_responders and str(comment.id) not in comment_ids:
			random_reply = random.choice(random_strings)
			trytoreply(random_reply)

