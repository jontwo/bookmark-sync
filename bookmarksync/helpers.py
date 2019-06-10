"""Helper module for Bookmark Sync."""

from lxml.etree import tostring
from lxml.html import HtmlElement
from lxml.html.soupparser import fromstring


def load_bookmarks(filepath):
    """Opens a bookmark html file, reads the contents and returns an lxml tree."""
    with open(filepath) as fp:
        tree = fromstring(fp.read())

    # strip DT and P tags
    return reduce_tree(tree)


def save_bookmarks(tree, filepath):
    """Saves an lxml tree to a bookmark html file."""
    def writenode(node, indent=0):
        spaces = ' ' * 4 * indent
        if node.tag == 'dl':
            fp.write("{}<DL><p>\n".format(spaces))
            for child in node.getchildren():
                writenode(child, indent + 1)
            fp.write("{}</DL>\n".format(spaces))
        else:
            fp.write("{indent}{dt}<{attrib}>{text}</{tag}>\n".format(
                indent=spaces,
                dt="<DT>" if indent else "",
                tag=node.tag.upper(),
                attrib=" ".join(
                    [node.tag.upper()]
                    + ['{}="{}"'.format(k.upper(), v) for k, v in node.attrib.items()]),
                text=node.text or "",
            ))
            for child in node.getchildren():
                writenode(child, indent + 1)

    with open(filepath, 'w') as fp:
        fp.write("""<!DOCTYPE NETSCAPE-Bookmark-file-1>
<!-- This is an automatically generated file.
     It will be read and overwritten.
     DO NOT EDIT! -->
""")
        # don't write the html tag, just its children
        for child in tree.getchildren():
            writenode(child)


def load_tree(filepath):
    """Opens a tree html file, reads the contents and returns an lxml tree."""
    with open(filepath) as fp:
        return fromstring(fp.read())


def save_tree(tree, filepath):
    """Saves an lxml tree to a tree html file."""
    with open(filepath, 'wb') as fp:
        fp.write(tostring(tree))


def reduce_tree(node):
    """Removes all but the important tags from a node and its children."""
    newnode = HtmlElement(attrib=node.attrib)
    newnode.tag = node.tag
    newnode.text = node.text
    for child in node.getchildren():
        newchild = reduce_tree(child)
        if child.tag.lower() in ('a', 'dl', 'h1', 'h3'):
            newnode.append(newchild)
        else:
            # we don't want this node, so get its children instead
            for grandchild in newchild.getchildren():
                newnode.append(grandchild)
    return newnode
