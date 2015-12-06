# Copyright (c) 2015, LE GOFF Vincent
# All rights reserved.

# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are met:

# * Redistributions of source code must retain the above copyright notice, this
#   list of conditions and the following disclaimer.

# * Redistributions in binary form must reproduce the above copyright notice,
#   this list of conditions and the following disclaimer in the documentation
#   and/or other materials provided with the distribution.

# * Neither the name of ytranslate nor the names of its
#   contributors may be used to endorse or promote products derived from
#   this software without specific prior written permission.

# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS "AS IS"
# AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT LIMITED TO, THE
# IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR A PARTICULAR PURPOSE ARE
# DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT HOLDER OR CONTRIBUTORS BE LIABLE
# FOR ANY DIRECT, INDIRECT, INCIDENTAL, SPECIAL, EXEMPLARY, OR CONSEQUENTIAL
# DAMAGES (INCLUDING, BUT NOT LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR
# SERVICES; LOSS OF USE, DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER
# CAUSED AND ON ANY THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY,
# OR TORT (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.

import io
import os
import sys
from textwrap import dedent
import unittest

try:
    from unittest import mock
except ImportError:
    import mock

from ytranslate.fsloader import FSLoader
from ytranslate.fsloader import os as fs_os

class TestFSLoader(unittest.TestCase):

    """Unittest for the FSLoader loader.

    This set of tests checks the features of the File System Loader
    (FSLoader) which is to loads the catalogs on the file system.
    In order to avoid testing the file system itself, access to it
    are 'mocked' by the 'mock' module ('unittest.mock' under Python
    3.3 and up).  You should install the 'mock' module with
    'pip install mock' if you're running Python 2.X.

    """

    def setUp(self):
        self.files = {}

    def open(self):
        """Return a mock of the open function."""
        address_open = "builtins.open"
        if sys.version_info.major == 2:
            address_open = "ytranslate.fsloader.open"

        return mock.patch(address_open, mock.mock_open())

    def mock_open(self, name, *args, **kwargs):
        """Open a mock file at the proper location.

        The match between file name and content is done in the 'files'
        dictionary.  A 'io.StringIO' object is returned.  This
        function serves as a substitute for 'open' in a test context.

        """
        name = name.replace(os.sep, "/")
        content = self.files.get(name, "")
        return io.StringIO(u"{}".format(content))

    @mock.patch.object(fs_os, "walk")
    def test_files(self, mock_walk):
        """Simple test with only files."""
        # Initialize the files
        self.files = {
                "test/en.yml": dedent("""\
                        new: New
                        view: View"""),
                "test/fr.yml": dedent("""\
                        new: Nouveau
                        view: Affichage"""),
        }

        with self.open() as mock_open:
            mock_open.side_effect = self.mock_open
            mock_walk.return_value = [
                ["test", [], ["en.yml", "fr.yml"]],
            ]

            # Creates the FSLoader object
            loader = FSLoader("unknown")
            loader.load()

            # Check the catalogs' proper loading
            self.assertEqual(len(loader.catalogs), 2)
            self.assertIn("en", loader.catalogs)
            self.assertIn("fr", loader.catalogs)

            # Check the catalog's content
            en = loader.catalogs["en"]
            fr = loader.catalogs["fr"]
            self.assertEqual(en.retrieve("new"), u"New")
            self.assertEqual(fr.retrieve("new"), u"Nouveau")
            self.assertEqual(en.retrieve("view"), u"View")
            self.assertEqual(fr.retrieve("view"), u"Affichage")
