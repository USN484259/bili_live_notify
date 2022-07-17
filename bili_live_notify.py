#!/usr/bin/env python3

import os
import sys
import time
import traceback
import requests
import tempfile
import webbrowser
from bilibili_api import live, user, sync
from gi.repository import Notify

script_name = os.path.basename(sys.argv[0])
print()
print(script_name + " by USN484259")

if len(sys.argv) < 2:
	print("Usage: " + script_name + " list_file [check_interval]")
	sys.exit(1)

dd_list = open(sys.argv[1]).readlines()

interval = 60
if len(sys.argv) > 2:
	interval = int(sys.argv[2])


live_status = {}
for l in dd_list:
	try:
		rid = int(l)
		live_status[rid] = 0
	except:
		print("WARN: unknown live room id " + l)

Notify.init(sys.argv[0])

def open_live_room(rid):
	print(rid)
	webbrowser.open("https://live.bilibili.com/" + str(rid))


def check_room(rid):
	cur_stat = live_status[rid]
	room = live.LiveRoom(rid)
	live_info = sync(room.get_room_play_info())
	print(live_info)
	if 1 == live_info.get("live_status") and 1 != cur_stat:
		usr = user.User(live_info.get("uid"))
		up_info = sync(usr.get_user_info())
		live_title = sync(room.get_room_info()).get("room_info").get("title")

		response = requests.get(up_info.get("face"))
		icon_file = tempfile.NamedTemporaryFile(delete=False)
		icon_file.write(response.content)
		icon_file.close()

		note = Notify.Notification.new(
			up_info.get("name") + " 开播了",
			live_title,
			icon_file.name
		)
		'''
		doesn't work for me, needs further review
		note.add_action(
			"action_click",
			"让我访问",
			open_live_room,
			rid
		)
		'''
		note.show()
		
	live_status[rid] = live_info.get("live_status")

while True:
	for rid in live_status.keys():
		try:
			check_room(rid)
		except:
			traceback.print_exc()

	time.sleep(interval)

