#!/usr/bin/env python3
import filelister

import unittest, os, shutil, json

class FileListerTests(unittest.TestCase):
    def setUp(self):
        self.botsdir = 'tests/bots'
        self.filesdir = 'tests/bots/files'
        self.queuedir = 'tests/bots/queue'
        if os.path.exists(self.filesdir):
            shutil.rmtree(self.filesdir)
        if os.path.exists(self.queuedir):
            shutil.rmtree(self.queuedir)
        shutil.copytree('tests/bots/test-files', self.filesdir)
        shutil.copytree('tests/bots/test-queue', self.queuedir)

        filelister.initlist('tests', 'test', 'test', botsdir=self.botsdir, filesdir=self.filesdir)

        self.config_name = os.path.join(self.botsdir, 'tests.json')
        with open(self.config_name) as config_file:
            self.config = json.load(config_file)
        self.config['filelist'].sort()

    def test_initlist(self):
        self.assertEqual(self.config['file_i'], 0)
        self.assertEqual(self.config['hook_id'], 'test')
        self.assertEqual(self.config['hook_token'], 'test')
        self.assertEqual(set(self.config['filelist']), set(os.listdir(self.filesdir)))

    def test_relist(self):
        with open(os.path.join(self.config_name), 'r+') as config_file:
            filelister.relist(config_file, filesdir=self.filesdir, queuedir=self.queuedir)
        with open(os.path.join(self.config_name)) as config_file:
            self.config = json.load(config_file)
        fileset = set(self.config['filelist'])

        self.assertEqual(len(os.listdir(self.queuedir)), 1)
        self.assertEqual(set(self.config['filelist']), set(os.listdir(self.filesdir)))

    def test_removefiles_all(self):
        self.remove = os.listdir('tests/bots/test-remove')
        with open(os.path.join(self.config_name), 'r+') as config_file:
            filelister.removefiles(config_file, self.remove, filesdir=self.filesdir)
        with open(os.path.join(self.config_name)) as config_file:
            self.config = json.load(config_file)

        self.assertEqual(self.config['file_i'], 0)
        self.assertEqual(len(os.listdir(self.filesdir)), 0)
        self.assertEqual(len(self.config['filelist']), 0)
        self.assertEqual(set(self.config['filelist']), set(os.listdir(self.filesdir)))

    def test_removefiles_all_mid_i(self):
        self.remove = os.listdir('tests/bots/test-remove')
        with open(os.path.join(self.config_name), 'r+') as config_file:
            self.config['file_i'] = 3
            json.dump(self.config, config_file)
        with open(os.path.join(self.config_name), 'r+') as config_file:
            filelister.removefiles(config_file, self.remove, filesdir=self.filesdir)
        with open(os.path.join(self.config_name)) as config_file:
            self.config = json.load(config_file)

        self.assertEqual(self.config['file_i'], 3)
        self.assertEqual(len(self.config['filelist']), 3)
        self.assertEqual(len(os.listdir(self.filesdir)), 0)

    def test_removefiles_mixed_mid_i(self):
        self.remove = os.listdir('tests/bots/test-remove-mixed')
        with open(os.path.join(self.config_name), 'r+') as config_file:
            self.config['file_i'] = 3
            json.dump(self.config, config_file)
        with open(os.path.join(self.config_name), 'r+') as config_file:
            filelister.removefiles(config_file, self.remove, filesdir=self.filesdir)
        with open(os.path.join(self.config_name)) as config_file:
            self.config = json.load(config_file)

        self.assertEqual(self.config['file_i'], 3)
        self.assertEqual(len(os.listdir(self.filesdir)), 5)
        self.assertEqual(len(self.config['filelist']), 6)
        self.assertTrue(set(self.config['filelist']) != set(os.listdir(self.filesdir)))

    def test_getfile(self):
        file_i = self.config['file_i']
        with open(os.path.join(self.config_name), 'r+') as config_file:
            img_name = filelister.getfile(config_file)
        with open(os.path.join(self.config_name)) as config_file:
            self.config = json.load(config_file)

        self.assertEqual(file_i + 1, self.config['file_i'])
        self.assertTrue(os.path.exists(os.path.join(self.filesdir, img_name)))

    def tearDown(self):
        shutil.rmtree(self.filesdir)
        shutil.rmtree(self.queuedir)
        os.remove(self.config_name)

if __name__ == '__main__':
    unittest.main()
