import os
import shutil
import tempfile
from os.path import dirname, isdir, realpath


def _convert_path(path):
    """Given a Unix path, convert it for the current platform.
    """
    return os.sep.join(path.split('/'))


def _convert_paths(paths):
    """Given a tuple of Unix paths, convert them for the current platform.
    """
    return tuple([_convert_path(p) for p in paths])


def _get_tempdir():
    """Return a temporary directory we can use for our fixture.
    """
    return os.path.realpath(os.path.join(tempfile.gettempdir()))


class FilesystemFixture(object):

    def __init__(self, root=None):
        self.root = root if root is not None else _get_tempdir()


    def mk(self, *treedef):
        """Given a treedef, build a filesystem fixture in self.root.

        treedef is a sequence of strings and tuples. If a string, it is interpreted
        as a path to a directory that should be created. If a tuple, the first
        element is a path to a file, the second is the contents of the file. We do
        it this way to ease cross-platform testing.

        """
        for item in treedef:
            if isinstance(item, basestring):
                path = _convert_path(item.lstrip('/'))
                path = os.sep.join([self.root, path])
                os.makedirs(path)
            elif isinstance(item, tuple):
                filepath, contents = item
                path = _convert_path(filepath.lstrip('/'))
                path = os.sep.join([self.root, path])
                parent = dirname(path)
                if not isdir(parent):
                    os.makedirs(parent)
                file(path, 'w').write(contents)


    def resolve(self, path=''):
        """Given a relative path, return an absolute path under self.root.

        The incoming path is in UNIX form (/foo/bar.html). The outgoing path is in
        native form, with symlinks removed.

        """
        path = os.sep.join([self.root] + path.split('/'))
        return realpath(path)


    def remove(self):
        """Remove the filesystem fixture at self.root.
        """
        if isdir(self.root):
            shutil.rmtree(self.root)
