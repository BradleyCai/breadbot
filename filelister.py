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
def relist(config_file, filesdir='bots/files', queuedir='bots/queue'):
    config = json.load(config_file)
    queuelist = os.listdir(queuedir)
    left = config['filelist'][:config['file_i']]
    right = set(config['filelist'][config['file_i']:])

    # Union queuelist, shuffle list, and update config file
    config['filelist'] = left + list(right.union(queuelist))
    shuffle(config['filelist'], config['file_i'])
    config_file.seek(0, 0)
    config_file.truncate()
    json.dump(config, config_file)

    for f in queuelist:
        src = os.path.join(queuedir, f)
        dst = os.path.join(filesdir, f)

        if os.path.exists(dst):
            print(f + ' is a duplicate. Not moved.')
        else:
            os.rename(src, dst)
            print(f + ' moved.')

# Removes a list of files from the filelist and filesdir
# The images that came before file_i are untouched and recorded in the filelist
# The images that came before file_i are still deleted from filesidr
# Reshuffles everything after file_i
def removefiles(config_file, files, filesdir='bots/files'):
    config = json.load(config_file)

    # Remove the files from disk
    for f in files:
        path = os.path.join(filesdir, f)

        if os.path.exists(path):
            os.remove(path)
            print(f + ' removed.')
        else:
            print(f + ' not found. Not removed.')

    config_name = os.path.basename(config_file.name)
    config_name = os.path.splitext(config_name)[0]
    initlist(config_name, \
        config['hook_id'], \
        config['hook_token'], \
        config['botsdir'], \
        config['filesdir'], \
        config['filelist'][:config['file_i']])

# Returns the next file name from the filelist and updates file_i
def getfile(config_file):
    config = json.load(config_file)

    if len(config['filelist']) == 0:
        raise IndexError('Filelist is empty.')

    if config['file_i'] >= len(config['filelist']):
        logging.warning('Ran out of files. Looping over from the beginning.')

    res = config['filelist'][config['file_i'] % len(config['filelist'])]
    config['file_i'] += 1
    config_file.seek(0, 0)
    config_file.truncate()
    json.dump(config, config_file)
    return res

# Shuffles a list past the file_i
def shuffle(l, file_i):
    l_len = len(l)
    for i in range(file_i, l_len - 2):
        j = random.randrange(i, l_len)
        l[i], l[j] = l[j], l[i]
    return l
