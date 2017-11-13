import os, random, json, logging

'''
This python script (the 'filelister') is for creating 'filelists'. Filelists
are for managing a list of files that is associated with a server. The
'filelister' can initialize a new list, recreate a new list by adding a queue
to it, and grab a file from the list + update the list. The filelister can be
used both as a python library and as a commandline tool.
'''

# Creates a new shuffled initlist
# Can also be used to update the filelist (with config info, or files dir changes)
# "used" parameter is a list of already used files. Will update file_i to match
def initlist(bot_name, hook_id, hook_token, botsdir='bots', filesdir='bots/files', used=[]):
    config = { \
        'hook_id': hook_id, \
        'hook_token': hook_token, \
        'botsdir': botsdir, \
        'filesdir': filesdir, \
        'filelist': used + list(set(os.listdir(filesdir)).difference(used)), \
        'file_i': len(used)}
    shuffle(config['filelist'], len(used))

    with open(os.path.join(botsdir, bot_name + '.json'), 'w') as config_file:
        json.dump(config, config_file)

# Inserts a directory of files into the current filelist
def insertfiles(config_name, queuedir='bots/queue'):
    with open(config_name) as config_file:
        config = json.load(config_file)

    queuelist = os.listdir(queuedir)

    for f in queuelist:
        src = os.path.join(queuedir, f)
        dst = os.path.join(config['filesdir'], f)

        if os.path.exists(dst):
            print(f + ' is a duplicate. Not moved.')
        else:
            os.rename(src, dst)
            print(f + ' moved.')

    bot_name = os.path.basename(config_name)
    bot_name = os.path.splitext(bot_name)[0]
    initlist(bot_name, \
        config['hook_id'], \
        config['hook_token'], \
        config['botsdir'], \
        config['filesdir'], \
        config['filelist'][:config['file_i']])

# Removes a list of files from the filelist and filesdir
# The images that came before file_i are untouched and recorded in the filelist
# The images that came before file_i are still deleted from filesidr
# Reshuffles everything after file_i
def removefiles(config_name, removelist):
    with open(config_name) as config_file:
        config = json.load(config_file)

    # Remove the files from disk
    for f in removelist:
        path = os.path.join(config['filesdir'], f)

        if os.path.exists(path):
            os.remove(path)
            print(f + ' removed.')
        else:
            print(f + ' not found. Not removed.')

    bot_name = os.path.basename(config_name)
    bot_name = os.path.splitext(bot_name)[0]
    initlist(bot_name, \
        config['hook_id'], \
        config['hook_token'], \
        config['botsdir'], \
        config['filesdir'], \
        config['filelist'][:config['file_i']])

# Returns the next file name from the filelist and updates file_i
def getfile(config_name):
    with open(config_name) as config_file:
        config = json.load(config_file)

    if len(config['filelist']) == 0:
        raise IndexError('Filelist is empty.')

    if config['file_i'] >= len(config['filelist']):
        logging.warning('Ran out of files. Looping over from the beginning.')

    res = config['filelist'][config['file_i'] % len(config['filelist'])]
    config['file_i'] += 1

    with open(config_name, 'w') as config_file:
        json.dump(config, config_file)

    return res

# Shuffles a list past the file_i
def shuffle(l, file_i):
    l_len = len(l)
    for i in range(file_i, l_len - 2):
        j = random.randrange(i, l_len)
        l[i], l[j] = l[j], l[i]
    return l
