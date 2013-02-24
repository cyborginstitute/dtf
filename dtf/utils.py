# Copyright 2012 Sam Kleinman
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
# http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

"""
:mod:`utils.py` is a module that provide a number of basic functions
for core :mod:`dtf` operations and functions.
"""

import os
import sys

def get_name(test):
    """
    Returns the base name of a file without the file extension.
    """
    return os.path.basename(test).split('.')[0]

def get_module_path(path):
    """
    :param string path: The location within the current directory of
                        a Python module.

    :returns: The full absolute path of the module.

    In addition to rendering an absolute path,
    :meth:`get_module_path()` also appends this path to ``sys.path``.
    """

    r = os.getcwd() + '/' + path
    sys.path.append(r)
    return r

def expand_tree(path, input_extension='yaml'):
    """
    :param string path: A starting path to begin searching for files.

    :param string input_extension: Optional. A filter.

    :returns: A list of paths starting recursively from the ``path``
              and only including those objects that end with the
              ``input_extensions.``

    :meth:`expand_tree()` returns a list of paths, filtered to
    """

    file_list = []
    for root, subFolders, files in os.walk(path):
        for file in files:
            f = os.path.join(root,file)
            if f.rsplit('.', 1)[1] == input_extension:
                file_list.append(f)

    return file_list
