#!/bin/bash
set -e

iterm_autolaunch_dir="$HOME/Library/Application Support/iTerm2/Scripts/AutoLaunch"
mkdir -p "$iterm_autolaunch_dir"
script=$(realpath current_song.py)
cd "$iterm_autolaunch_dir" && ln -s $script ./