#!/usr/bin/env python3

import os
import sys
import time
import traceback
import requests
import tempfile
import webbrowser
from bilibili_api import live, user, sync

import gi
gi.require_version('Notify', '0.7')
from gi.repository import Notify, GLib

script_name = os.path.basename(sys.argv[0])
print()
print(script_name + " by USN484259")
print("https://github.com/USN484259/bili_live_notify")

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
		rid = int(l.split()[0])
		live_status[rid] = 0
	except:
		print("WARN: unknown live room id " + l)

Notify.init(script_name)
pending_list = {}

def on_close(notification):
	pending_list.pop(notification, None)

def on_click(notification, action, rid):
	webbrowser.open("https://live.bilibili.com/" + str(rid), new = 1, autoraise = False)

def live_time_str(start_time):
	if start_time < 0:
		return ""
	live_time = time.time() - start_time
	if live_time < 0:
		return ""
	res = ""
	if live_time >= 3600:
		res = str(int(live_time / 3600)) + ':'

	live_time = live_time % 3600
	minute = int(live_time / 60)
	second = int(live_time % 60)

	res = res + "%02d:%02d" % (minute, second)
	return res

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

		notification = Notify.Notification.new(
			up_info.get("name") + " 开播了",
			live_time_str(live_info.get("live_time")) + '\t' + live_title,
			icon_file.name
		)

		notification.add_action(
			"default",
			"让我康康",
			on_click,
			rid
		)
		notification.connect("closed", on_close)
		notification.show()
		pending_list[notification] = None

	live_status[rid] = live_info.get("live_status")

def on_timer():
	try:
		for rid in live_status.keys():
			check_room(rid)
	except:
		traceback.print_exc()
	return True

main_loop = GLib.MainLoop()
on_timer()
GLib.timeout_add_seconds(interval, on_timer)
main_loop.run()

