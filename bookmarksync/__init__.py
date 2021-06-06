"""Bookmark Sync top-level package."""
from bookmarksync.helpers import (
    load_bookmarks, save_bookmarks, load_tree, save_tree, reduce_tree, compare_trees  # noqa: F401
)

__version__ = '0.1.0'
__author__ = 'Jon Morris'
__author_email__ = 'jontwo@users.noreply.github.com'
__license__ = 'MIT'
