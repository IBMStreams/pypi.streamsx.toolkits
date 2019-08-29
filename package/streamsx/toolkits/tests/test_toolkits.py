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
from datetime import time

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


