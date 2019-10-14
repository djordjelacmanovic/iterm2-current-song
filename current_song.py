#!/usr/bin/env python3
# coding=utf-8
# AppleScript based on https://gist.github.com/joshuaswilcox/7251527
import iterm2
from subprocess import Popen, PIPE

def get_current_song():
	get_song_applescript = """
	if application "Spotify" is running and application "Music" is not running then
		return "Spotify: " & spotify_status()
	else if application "Spotify" is running and application "Music" is running then
		--Get current states of Music and Spotify
		tell application "Music" to set MusicState to (player state as text)
		tell application "Spotify" to set spotifyState to (player state as text)
		if MusicState is "paused" and spotifyState is "paused" then
			return "Music: " & Music_status() & " / Spotify: " & spotify_status()
		else if MusicState is not "playing" and (spotifyState is "playing" or spotifyState is "paused") then
			return "Spotify: " & spotify_status()
		else if (MusicState is "playing" or MusicState is "paused") and spotifyState is not "playing" then
			return "Music: " & Music_status()
		else if MusicState is "stopped" and spotifyState is "stopped" then
			return "No Track Playing 😢"
		else
			return "Madman you be playin' 2 songs!!!"
		end if
	else if application "Music" is running and application "Spotify" is not running then
		return "Music: " & Music_status()
	else
		return "No music apps running"
	end if
	on spotify_status()
		tell application "Spotify"
			if player state is stopped then
				return "No Track Playing 😢"
			else
				set track_artist to artist of current track
				set track_name to name of current track
				set track_duration to duration of current track
				set seconds_played to player position
				set state to "▶️"
				if player state is paused then
					set state to "⏸"
				end if
				
				return state & " " & track_artist & " - " & track_name
			end if
		end tell
	end spotify_status
	on Music_status()
		tell application "Music"
			if player state is stopped then
				return "No Track Playing 😢"
			else
				set track_artist to artist of current track
				set track_name to name of current track
				set track_duration to duration of current track
				set seconds_played to player position
				set state to "▶️"
				if player state is paused then
					set state to "⏸"
				end if
			end if
		end tell
		return state & " " & track_artist & " - " & track_name
	end Music_status
	END
	"""
	p = Popen(['osascript', '-'], stdin=PIPE, stdout=PIPE, stderr=PIPE, universal_newlines=True)
	stdout, stderr = p.communicate(get_song_applescript)
	if stderr != "":
		raise Exception("Applescript error: " + stderr)
	return stdout.strip()

async def main(connection):
	component = iterm2.StatusBarComponent(
		short_description="Current song playing",
		detailed_description="Show the current song playing in iTunes or Spotify",
		exemplar="Spotify: ▶️ Danzig - Mother",
		update_cadence=1,
		identifier="dev.djordje.iterm-components.current-song",
		knobs=[])

	@iterm2.StatusBarRPC
	async def current_song_coroutine(knobs):
		current_song = get_current_song()
		return current_song

	await component.async_register(connection, current_song_coroutine)

iterm2.run_forever(main)
