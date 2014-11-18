# encoding: utf-8
from contextlib import contextmanager
from collections import namedtuple
import os
import tempfile
import subprocess

import cubicsuperpath
import simplepath
import simpletransform
import bezmisc
import cspsubdiv
import inkex
import platform


def execute_command(*popenargs, **kwargs):
    r"""Run command with arguments and return its output as a byte string.

    If the exit code was non-zero it raises a CalledProcessError.  The
    CalledProcessError object will have the return code in the returncode
    attribute and output in the output attribute.

    The arguments are the same as for the Popen constructor.  Example:

    >>> check_output(["ls", "-l", "/dev/null"])
    'crw-rw-rw- 1 root root 1, 3 Oct 18  2007 /dev/null\n'

    The stdout argument is not allowed as it is used internally.
    To capture standard error in the result, use stderr=STDOUT.

    >>> check_output(["/bin/sh", "-c",
    ...               "ls -l non_existent_file ; exit 0"],
    ...              stderr=STDOUT)
    'ls: non_existent_file: No such file or directory\n'
    """
    if 'stdout' in kwargs:
        raise ValueError('stdout argument not allowed, it will be overridden.')
    process = subprocess.Popen(stdout=subprocess.PIPE, *popenargs, **kwargs)
    output, unused_err = process.communicate()
    retcode = process.poll()
    if retcode:
        cmd = kwargs.get("args")
        if cmd is None:
            cmd = popenargs[0]
        raise subprocess.CalledProcessError(retcode, cmd, output=output)
    return output


def inkscape_command(*args):
    return execute_command(['inkscape'] + [str(arg) for arg in args])


def convert_command(*args):
    return execute_command(['convert'] + [str(arg) for arg in args])


@contextmanager
def tmp_file(ext, text=True):
    '''
        Create a temporary file to work on, pass it path, then remove it from the system.
        Example:

        with tmp_file(".txt") as tmp:
            print(tmp)
    '''
    fd, tmp = tempfile.mkstemp(ext, text=True)
    os.close(fd)
    try:
        yield tmp
    finally:
        try:
            os.remove(tmp)
        except OSError:
            pass


def print_(*arg):
    '''
        Print out debug message on fablab_debug.log in inkscape extension directory.
    '''
    f = open("fablab_debug.log", "a")
    for s in arg:
        s = str(unicode(s).encode('unicode_escape')) + " "
        f.write(s)
    f.write("\n")
    f.close()


def path_to_segments(node):
    '''
        Generator to convert a path node to an interator to 
        segmented paths (bezier curves broken to approximated 
        straights lines).
    '''
    mat = simpletransform.composeParents(node, [[1.0, 0.0, 0.0], [0.0, 1.0, 0.0]])
    d = node.get('d')

    if len(simplepath.parsePath(d)) == 0:
        return

    p = cubicsuperpath.parsePath(d)
    simpletransform.applyTransformToPath(mat, p)

    # p is now a list of lists of cubic beziers [ctrl p1, ctrl p2, endpoint]
    # where the start-point is the last point in the previous segment

    for sp in p:
        path = []
        subdivideCubicPath(sp, 0.2)  # TODO: smoothness preference
        for csp in sp:
            path.append([csp[1][0], csp[1][1]])
        yield path


def subdivideCubicPath(sp, flat, i=1):
    """
    Break up a bezier curve into smaller curves, each of which
    is approximately a straight line within a given tolerance
    (the "smoothness" defined by [flat]).

    This is a modified version of cspsubdiv.cspsubdiv().
    From Openscad plugins
    """

    while True:
        while True:
            if i >= len(sp):
                return

            p0 = sp[i - 1][1]
            p1 = sp[i - 1][2]
            p2 = sp[i][0]
            p3 = sp[i][1]

            b = (p0, p1, p2, p3)

            if cspsubdiv.maxdist(b) > flat:
                break

            i += 1

        one, two = bezmisc.beziersplitatt(b, 0.5)
        sp[i - 1][2] = one[1]
        sp[i][0] = two[2]
        p = [one[2], one[3], two[1]]
        sp[i:1] = [p]


class BaseEffect(inkex.Effect):
    def __init__(self):
        inkex.Effect.__init__(self)

    @contextmanager
    def as_tmp_svg(self):
        '''
            Work on a temporary .svg copy of this document.
            example :

            with self.as_tmp_svg as temp_svg:
                print tmp
        '''
        fd, tmp = tempfile.mkstemp(".svg", text=True)
        os.close(fd)
        self.document.write(tmp)
        try:
            yield tmp
        finally:
            try:
                os.remove(tmp)
            except(OSError):
                pass

    @contextmanager
    def reloaded_from_file(self, tmp):
        old_document = self.document
        self.parse(tmp)
        self.getposinlayer()
        self.getselected()
        self.getdocids()
        try:
            yield
        finally:
            self.document = old_document
            self.getposinlayer()
            self.getselected()
            self.getdocids()

    @contextmanager
    def inkscaped(self, arguments=[]):
        with self.as_tmp_svg() as tmp:
            ink_args = ["--file", tmp] + arguments + ["--verb=FileSave", "--verb=FileClose"]
            inkscape_command(*ink_args)
            with self.reloaded_from_file(tmp):
                yield tmp
