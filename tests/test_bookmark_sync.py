"""Bookmark Sync test module."""

import os
import tempfile
import unittest
from lxml.html.soupparser import fromstring
import bookmarksync as bs


class BookmarkSyncTests(unittest.TestCase):
    @classmethod
    def setUp(cls):
        cls.data_dir = os.path.join(os.path.dirname(__file__), 'data')
        cls.bkm_file = os.path.join(cls.data_dir, 'bookmark1.html')
        cls.bkm_file2 = os.path.join(cls.data_dir, 'bookmark2.html')
        cls.tree1 = fromstring(
            '<html><h1>Bookmarks Menu</h1><dl><h3 add_date="1518129521"'
            ' last_modified="1518129615">Subfolder</h3><dl><a add_date="1518129612" '
            'href="http://www.sub.level.html" last_modified="1518129612">Sub level link</a>'
            '</dl><a add_date="1518129612" href="http://www.top.level.html" last_modified'
            '="1518129612">Top level link</a></dl></html>'
        )

    def assertNodeEqual(self, first, second, msg=None):
        self.assertEqual(first is None, second is None, msg)
        if first is None and second is None:
            return
        msg = '{}/{}'.format(msg, first.tag) if msg else 'for node {}'.format(first.tag)
        self.assertEqual(first.tag, second.tag, msg)
        self.assertEqual(first.text, second.text, msg)
        self.assertDictEqual(dict(first.attrib), dict(second.attrib), msg)
        children1 = first.getchildren()
        children2 = second.getchildren()
        self.assertEqual(len(children1), len(children2), msg)
        for child1, child2 in zip(children1, children2):
            self.assertNodeEqual(child1, child2, msg)

    @staticmethod
    def file_to_string(filepath):
        with open(filepath) as fp:
            return fp.read()

    def test_load_bookmarks(self):
        expected = self.tree1

        actual = bs.load_bookmarks(self.bkm_file)

        self.assertNodeEqual(actual, expected)

    def test_save_bookmarks(self):
        expected = """<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
<H1>Bookmarks Menu</H1>
<DL><p>
    <DT><H3 ADD_DATE="1518129521" LAST_MODIFIED="1518129615">Subfolder</H3>
    <DL><p>
        <DT><A ADD_DATE="1518129612" HREF="http://www.sub.level.html" LAST_MODIFIED="1518129612">
Sub level link</A>
    </DL>
    <DT><A ADD_DATE="1518129612" HREF="http://www.top.level.html" LAST_MODIFIED="1518129612">
Top level link</A>
</DL>
"""
        tree = bs.reduce_tree(fromstring(expected))

        with tempfile.TemporaryDirectory() as fpd:
            filepath = os.path.join(fpd, 'merged.html')
            bs.save_bookmarks(tree, filepath)
            actual = self.file_to_string(filepath)

        self.assertEqual(actual, expected)

    def test_reduce_tree(self):
        expected = fromstring(
            '<html><h1>Bookmarks</h1><dl><dl><h3>Heading</h3></dl></dl><a>link</a></html>'
        )
        tree = fromstring(
            '<html><h1>Bookmarks</h1><dl><div><dt><dl><span><h3>Heading</h3></dl></dl>'
            '<p><a>link</a></html>'
        )
        actual = bs.reduce_tree(tree)

        self.assertNodeEqual(actual, expected)
