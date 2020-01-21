# coding=utf-8
# Licensed Materials - Property of IBM
# Copyright IBM Corp. 2019

import streamsx.toolkits as toolkits
from streamsx.toolkits.tests.x509_certs import TRUSTED_CERT_PEM, PRIVATE_KEY_PEM, CLIENT_CERT_PEM, CLIENT_CA_CERT_PEM

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
import random
import string
import OpenSSL

##

def _write_text_file(text):
    """write 'text' into a generated filename in temp directory.
    Args:
        text(str) the text to write
    Returns:
        str: the filename
    """
    filename = os.path.join(gettempdir(), 'pypi.streamsx.toolkits.test-pem-' + ''.join(random.choice(string.digits) for _ in range(20)) + '.pem')
    f = open(filename, 'w')
    try:
        f.write (text)
        return filename
    finally:
        f.close()


class TestCreateJKSStore(unittest.TestCase):
    def setUp(self):
        self.ca_crt_file = _write_text_file (TRUSTED_CERT_PEM)
        self.client_ca_crt_file = _write_text_file (CLIENT_CA_CERT_PEM)
        self.client_crt_file = _write_text_file (CLIENT_CERT_PEM)
        self.private_key_file = _write_text_file (PRIVATE_KEY_PEM)
    
    def tearDown(self):
        if os.path.isfile(self.ca_crt_file):
            os.remove(self.ca_crt_file)
        if os.path.isfile(self.client_ca_crt_file):
            os.remove(self.client_ca_crt_file)
        if os.path.isfile(self.client_crt_file):
            os.remove(self.client_crt_file)
        if os.path.isfile(self.private_key_file):
            os.remove(self.private_key_file)

        for storetype in ['truststore', 'keystore']:
            for f in glob.glob(os.path.join(gettempdir(), storetype) + '-*.jks'):
                try:
                    os.remove(f)
                    print ('file removed: ' + f)
                except:
                    print('Error deleting file: ', f)

    def test_create_truststore_single(self):
        store_filename = os.path.join(gettempdir(), 'truststore-' + ''.join(random.choice(string.digits) for _ in range(20)) + '.jks')
        toolkits.create_truststore(TRUSTED_CERT_PEM, store_filepath=store_filename)
        assert os.path.isfile(store_filename)

    def test_create_truststore_list(self):
        store_filename = os.path.join(gettempdir(), 'truststore-' + ''.join(random.choice(string.digits) for _ in range(20)) + '.jks')
        toolkits.create_truststore([TRUSTED_CERT_PEM, CLIENT_CA_CERT_PEM], store_filepath=store_filename, store_passwd=None)
        assert os.path.isfile(store_filename)

    def test_create_truststore_single_file(self):
        store_filename = os.path.join(gettempdir(), 'truststore-' + ''.join(random.choice(string.digits) for _ in range(20)) + '.jks')
        toolkits.create_truststore(self.ca_crt_file, store_filepath=store_filename, store_passwd="abcdef")
        assert os.path.isfile(store_filename)

    def test_create_truststore_file_list(self):
        store_filename = os.path.join(gettempdir(), 'truststore-' + ''.join(random.choice(string.digits) for _ in range(20)) + '.jks')
        toolkits.create_truststore([self.ca_crt_file, self.client_ca_crt_file], store_filepath=store_filename, store_passwd="abcdef")
        assert os.path.isfile(store_filename)

    def test_ValueError_create_truststore_empty_list(self):
        self.assertRaises(ValueError, toolkits.create_truststore, trusted_cert=[], store_filepath="/irrelevant", store_passwd="irrelevant")

    def test_create_keystore(self):
        store_filename = os.path.join(gettempdir(), 'keystore-' + ''.join(random.choice(string.digits) for _ in range(20)) + '.jks')
        toolkits.create_keystore(CLIENT_CERT_PEM, PRIVATE_KEY_PEM, store_filepath=store_filename)
        assert os.path.isfile(store_filename)

    def test_create_keystore_files(self):
        store_filename = os.path.join(gettempdir(), 'keystore-' + ''.join(random.choice(string.digits) for _ in range(20)) + '.jks')
        toolkits.create_keystore(self.client_crt_file, self.private_key_file, store_filepath=store_filename, store_passwd="sdfghj")
        assert os.path.isfile(store_filename)

    def test_create_keystore_crt_file_not_exists(self):
        self.assertRaises(OpenSSL.crypto.Error, toolkits.create_keystore, "/tmp/not/existing.crt", self.private_key_file, store_filepath="/doesnotmatter.jks")

    def test_create_keystore_key_file_not_exists(self):
        self.assertRaises(OpenSSL.crypto.Error, toolkits.create_keystore, self.client_crt_file, "/tmp/not/existing.key",store_filepath="/doesnotmatter.jks")


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

