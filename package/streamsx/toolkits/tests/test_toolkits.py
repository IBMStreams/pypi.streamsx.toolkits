# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

import streamsx.toolkits as toolkits

from streamsx.topology.topology import streamsx, Topology
from streamsx.topology.tester import Tester
from streamsx.topology.schema import StreamSchema
import streamsx.spl.toolkit as tk

import unittest
import os
import glob
import shutil
import uuid
from tempfile import gettempdir

##

class Test(unittest.TestCase):

    def test_get_github_toolkits(self):
        gh_tks = toolkits.get_github_toolkits()
        assert (gh_tks is not None), "Invalid result value"
        assert (isinstance(gh_tks, dict)), "dict type expected"
        print(gh_tks)

    def test_get_installed_packages(self):
        p = toolkits.get_installed_packages()
        assert (p is not None), "Invalid result value"
        assert (isinstance(p, dict)), "dict type expected"
        print(p)

    def test_get_pypi_packages(self):
        p = toolkits.get_pypi_packages()
        assert (p is not None), "Invalid result value"
        assert (isinstance(p, dict)), "dict type expected"
        print(p)

class TestDownloadToolkit(unittest.TestCase):
    @classmethod
    def tearDownClass(cls):
        # delete unpacked toolkits
        for d in glob.glob(gettempdir() + '/pypi.streamsx.nlp.tests-*'):
            if os.path.isdir(d):
                shutil.rmtree(d)
        for d in glob.glob(gettempdir() + '/com.ibm.streamsx.nlp*'):
            if os.path.isdir(d):
                shutil.rmtree(d)
        for d in glob.glob(gettempdir() + '/samples*'):
            if os.path.isdir(d):
                shutil.rmtree(d)

    def test_download_latest(self):
        topology = Topology()
        location = toolkits.download_toolkit('com.ibm.streamsx.nlp')
        print('\ntoolkit location: ' + location)
        streamsx.spl.toolkit.add_toolkit(topology, location)

    def test_download_samples(self):
        topology = Topology()
        location = toolkits.download_toolkit('samples', repository_name='streamsx.nlp')
        print('\nsamples location: ' + location)
        files = os.listdir(location)
        for name in files:
            print(name)

    def test_download_latest_with_repo(self):
        topology = Topology()
        location = toolkits.download_toolkit('com.ibm.streamsx.nlp', repository_name='streamsx.nlp')
        print('\ntoolkit location: ' + location)
        streamsx.spl.toolkit.add_toolkit(topology, location)

    def test_download_with_url(self):
        topology = Topology()
        url = 'https://github.com/IBMStreams/streamsx.nlp/releases/download/v1.9.0/streamsx.nlp.toolkits-1.9.0-20190404-1329.tgz'
        location = toolkits.download_toolkit('com.ibm.streamsx.nlp', url=url)
        print('\ntoolkit location: ' + location)
        streamsx.spl.toolkit.add_toolkit(topology, location)

    def test_download_latest_with_target_dir(self):
        topology = Topology()
        target_dir = 'pypi.streamsx.nlp.tests-' + str(uuid.uuid4()) + '/nlp-toolkit'
        location = toolkits.download_toolkit('com.ibm.streamsx.nlp', target_dir=target_dir)
        print('\ntoolkit location: ' + location)
        streamsx.spl.toolkit.add_toolkit(topology, location)

    def test_download_with_url_and_target_dir(self):
        topology = Topology()
        target_dir = 'pypi.streamsx.nlp.tests-' + str(uuid.uuid4()) + '/nlp-toolkit'
        url = 'https://github.com/IBMStreams/streamsx.nlp/releases/download/v1.9.0/streamsx.nlp.toolkits-1.9.0-20190404-1329.tgz'
        location = toolkits.download_toolkit('com.ibm.streamsx.nlp', url=url, target_dir=target_dir)
        print('\ntoolkit location: ' + location)
        streamsx.spl.toolkit.add_toolkit(topology, location)

