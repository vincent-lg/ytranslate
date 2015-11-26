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

"""Module containing the FSLoader class, described below."""


import os
import os.path
import sys

from ytranslate.catalog import Catalog
from ytranslate.loader import Loader

class FSLoader(Loader):

    """A file system loader of catalogs.

    This class represents a loader for YAML catalogs.  Catalogs
    are contained in files.  Directories are used to create a hierarchy
    of namespaces.  The root directory given in argument is the
    parent directory.  The directories contained in this root
    directory are recursively explored for catalog files.

    """

    def __init__(self, root_dir):
        self.root_dir = root_dir
        self.catalogs = {}
        self.selected_catalog = None

    def __repr__(self):
        return "<ytranslate.FSLoader (root={})>".format(repr(self.root_dir))

    def load(self):
        """Load the catalogs."""
        root_dir = self.root_dir
        len_root = len(os.path.split(root_dir))
        for base, dirs, files in os.walk(self.root_dir):
            fullbase = base
            for file in files:
                if len(file) > 4 and file.endswith(".yml"):
                    fullname = os.path.join(fullbase, file)
                    kwargs = {}
                    if sys.version_info.major == 3:
                        kwargs["encoding"] = "utf-8"

                    try:
                        file = open(fullname, "r", **kwargs)
                    except IOError as e:
                        raise ValueError("cannot load the {} file: " \
                                "{}".format(repr(fullname), e))
                    else:
                        data = file.read()

                    namespace = ".".join(fullname[:-4].split(
                            os.sep)[len_root + 1:])

                    parent = fullname.split(os.sep)[len_root]
                    if parent.endswith(".yml"):
                        parent = parent[:-4]

                    catalog = Catalog(fullname)
                    catalog.read_YAML(data)
                    if parent != namespace:
                        if parent not in self.catalogs:
                            self.catalogs[parent] = Catalog(parent)
                        parent = self.catalogs[parent]
                        parent.copy_from(catalog,
                                namespace=namespace)
                        parent.catalogs.append(catalog)
                    else:
                        self.catalogs[namespace] = catalog
