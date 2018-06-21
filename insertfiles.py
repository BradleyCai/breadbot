#!/usr/bin/env python3
import filelister
import subprocess

subprocess.run(['tar', '-xzf', 'queue.tar.gz'], stdout=subprocess.PIPE)
subprocess.run(['mv', 'home/bread/winhome/pictures/anime/queue', 'bots'])
filelister.insertfiles('bots/a2c.json')

