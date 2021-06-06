"""Bookmark Sync main module."""

import argparse
import os
from xmldiff.main import patch_tree
from bookmarksync.helpers import load_bookmarks, save_bookmarks, save_tree, diff_trees


def main():
    """Runs bookmark sync main method.

    TODO
    options
    - create new merged.html
    - compare existing merged.html with new bookmarks.html
    - compare and save
    - store all intermediate diffs (by datestamp? diff time or modified time?)
    - apply each diff since last sync
    """
    args = parse_args()
    if args.bookmark_file:
        new_bkm = load_bookmarks(args.bookmark_file)
        sync_file = args.sync_file
        if not os.path.dirname(sync_file):
            sync_file = os.path.join(os.path.dirname(os.path.abspath(args.bookmark_file)),
                                     sync_file)
        try:
            old_bkm = load_bookmarks(sync_file)
        except IOError:
            save_tree(new_bkm, sync_file)
            return
        diff = diff_trees(new_bkm, old_bkm)
        output_file = None
        if args.save_file:
            output_file = args.save_file
        elif args.overwrite_file:
            output_file = args.bookmark_file
        if output_file:
            updated_bkm = patch_tree(diff, old_bkm)
            save_bookmarks(updated_bkm, output_file)
        else:
            print(diff)


def parse_args():
    """Creates parser and reads args."""
    parser = argparse.ArgumentParser(description='Utility to sync exported bookmark files')
    parser.add_argument('--bookmark_file', '-b', type=os.path.expanduser,
                        help='Compare bookmark file to the current sync file.')
    parser.add_argument('--save_file', '-s', type=os.path.expanduser,
                        help='Save the compared bookmarks to a new bookmark file.')
    parser.add_argument('--overwrite_file', '-o', action='store_true',
                        help='Save the compared bookmarks to the input bookmark file.')
    parser.add_argument('--sync_file', '-y', type=os.path.expanduser, default='merged.html',
                        help='Sync file to store current bookmarks. (default: %(default)s in '
                        'same directory as bookmark file). This will be created if it does not '
                        'exist.')
    return parser.parse_args()
