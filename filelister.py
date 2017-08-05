import os, random, shutil, json

def initlist(bot_name, hook_id, hook_token, used=[]):
    config = {'filelist': used + os.listdir('./bots/files'), 'hook_id': hook_id, 'hook_token': hook_token, 'file_i': len(used)}
    shuffle(config['filelist'], len(used))

    with open('./bots/{}.json'.format(bot_name), 'w') as config_file:
        json.dump(config, config_file)

def relist(config_file):
    config = json.load(config_file)
    queuelist = os.listdir('./bots/queue')

    # Concat queuelist, shuffle list, and update config file
    config['filelist'] = config['filelist'] + queuelist
    shuffle(config['filelist'], config['file_i'])
    config_file.seek(0, 0)
    config_file.truncate()
    json.dump(config, config_file)

    for f in queuelist:
        shutil.move('./bots/queue/' + f, './bots/files')

def getfile(config_file):
    config = json.load(config_file)
    if config['file_i'] == len(config['filelist']):
        return None
    res = config['filelist'][config['file_i'] % len(config['filelist'])]
    config['file_i'] += 1
    config_file.seek(0, 0)
    config_file.truncate()
    json.dump(config, config_file)
    return res

def shuffle(l, file_i):
    l_len = len(l)
    for i in range(file_i, l_len - 2):
        j = random.randrange(i, l_len)
        l[i], l[j] = l[j], l[i]
    return l
