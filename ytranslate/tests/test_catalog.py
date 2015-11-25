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

import unittest

from ytranslate.catalog import Catalog

# Documents
SIMPLE_DOC = """
file: Fichier
edit: Édition
view: Affichage
connection:
    connected: Connecté
    connecting: Connexion en cours
    error: Connexion impossible
""".strip()

class TestCatalog(unittest.TestCase):

    """Unittest for the Catalog class.

    This set of unittests is to ensure the proper building of
    catalogs using YAML documents.

    """

    def test_simple_structure(self):
        """Test to read and create the proper structure."""
        catalog = Catalog("test")
        catalog.read_YAML(SIMPLE_DOC)
        self.assertEqual(catalog.messages, {
            'file': u'Fichier',
            'edit': u'Édition',
            'view': u'Affichage',
            'connection.connected': u'Connecté',
            'connection.connecting': u'Connexion en cours',
            'connection.error': u'Connexion impossible',
        })

    def test_write_dictionary(self):
        """Test to read and retrive the nested structure."""
        catalog = Catalog("test")
        catalog.read_YAML(SIMPLE_DOC)
        dictionary = catalog.write_dictionary()
        self.assertEqual(dictionary, {
            'file': u'Fichier',
            'edit': u'Édition',
            'view': u'Affichage',
            'connection': {
                'connected': u'Connecté',
                'connecting': u'Connexion en cours',
                'error': u'Connexion impossible',
            },
        })
        print catalog.write_YAML()
