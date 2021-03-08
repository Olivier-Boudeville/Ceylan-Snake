#!/usr/bin/env python

__title__       = 'This is the data module, which contains everything which is linked to data structure and management.'
__version__     = '0.1'
__author__      = 'Olivier Boudeville (olivier.boudeville@online.fr)'
__project__     = 'Ceylan'
__creationDate__= '2004, August 6'
__comments__    = ""
__source__      = 'None'
__doc__         = __title__ + '\n' + __comments__



# Import standard python modules:
import sys, types, string

# Import home-made modules:
import general_utils


class DataUtilsException(general_utils.GeneralUtilsException):
    """Base class for general_utils exceptions."""



class Node:
    """
    Nodes are trees: they can contain other nodes.
    Each node can carry a content, whose type is NodeContent.
    """

    def __init__(self, new_content=None):
        """Creates an empty node with no child node."""
        self.content = new_content
        self.children = []


    def __cmp__(self, other):
        return self.content != other.content


    def __repr__(self):
        """Returns a textual representation of the state of this node."""
        res = "Node has "
        if self.content:
            res += "content (%s)" % ( self.content, )
        else:
            res += "no content"
        res += " and it has "
        if self.children:
            res += "%s children" % ( len( self.children ), )
        else:
            res += "no child"

        return res


    def to_string(self, offset=0, next_offset=0, is_first_child=True):
        """
        Returns a stringified description of this tree.

        __ a __ b
           |_ c __ d __ e
                |_ f
                |_ g

        where:
         - offset is the current position where to write
         - next_offset is the position where children should begin
        """

        res= ""

        # The two branches must have the same length:
        #branch_first = 'x__x'
        #branch_next = 'y|_y'
        branch_first = ' __ '
        branch_next  = ' |_ '
        branch_last  = ''

        node_text = string.ljust('%s' % (self.content,), next_offset - offset + 1)

        if is_first_child:
            res += branch_first + node_text
        else:
            #res =  offset  * 'z' + branch_next + node_text
            res =  offset  * ' ' + branch_next + node_text

        if self.children:
            new_offset = offset + len(branch_first) + len(node_text)

            # Compute max child content total length:
            extra_len = 0
            for child in self.children:
                child_size = len( child.content )
                if child_size > extra_len:
                    extra_len = child_size
                new_next_offset = offset + len( branch_first ) + extra_len
            res += self.children[0].to_string( new_offset, new_next_offset, True )
            for c in self.children[1:]:
                res += '\n' + c.to_string( new_offset, new_next_offset, False )

            res += branch_last

        return res


        def add_child(self, child):
            """Adds a child to current node."""
            self.children.append(child)


        def remove_child(self, child):
            """Removes specified child; raises an exception if this child
            is not found."""
            self.children.remove(child)


        def remove_all_children(self):
            self.children = None


        def get_children(self):
            """Returns this node's children."""
            return self.children


        def set_content(self, node_content):
            """Sets a new content to current node, which must not have already
            a content."""
            if self.content:
                raise ValueError, "Node.set_content: content already assigned."
            self.content = node_content


        def get_content(self):
            """Returns this node's current content."""
            return self.content


        def drop_content(self):
            """Removes this node's content."""
            self.content = None


        def search_children(self, content):
            """Searches through node's children the first, if any, that has "
            specified content."""
            for c in self.children:
                if c.content == content:
                    return c
            return None


        def list_depth_first(self):
            """
            Walks the tree depth-first, returns the list of encountered nodes.
            """
            res = [self]
            for c in self.children:
                res += c.list_depth_first()
            return res
            #return [ self ] + c.list_depth_first() for c in self.children ]


        def list_by_height(self, first=True):
            """
            Walks the tree by increasing height, starting from root node, and
            returns the list of encountered nodes.
            """
            res = []
            if first:
                res = [ self ]
            res += self.children
            for c in self.children:
                res += c.list_by_height( False )
            return res


        def search_content(self, content):
            """
            Searches through internal content and then recursively through
            children for specified content.
            Returns the first node found having the content, if any, otherwise,
            returns None.
            content -> list of nodes
            """
            #output_device.debug( "Comparing target ('%s') with content '%s'." % (content, self.content))
            if content == self.content:
                return self
            else:
                for c in self.children:
                    res = c.search_content(content)
                    if res:
                        return res
                return None


        def search_path_to_content(self, content):
            """
            Returns, if possible, the path from the first found node whose
            content matches specified content to root node.
            """
            if content == self.content:
                #output_device.debug( "Content found for '%s'." % (self,) )
                return [ self ]
            else:
                #output_device.debug("Recursing from '%s'." % (self,))
                for child in self.children:
                    res = child.search_path_to_content(content)
                    if res:
                        res.append( self )
                        #output_device.debug( "Returning '%s'." % (res,) )
                        return res
                return None


        def display(self):
            """Displays this node."""
            print 'content  = %s' % (self.content,)
            print 'children = %s' % (self.children,)



class NodeExample(Node):

    def __init__(self, name=None):
        Node.__init__(self)
        self.content = name


if __name__ == "__main__":

    import startup
    #output_device = general_utils.screen_display()
    print __doc__

    a = NodeExample( 'a' )
    b = NodeExample( 'b' )
    c = NodeExample( 'c' )
    d = NodeExample( 'd' )
    e = NodeExample( 'e' )
    f = NodeExample( 'f' )
    g = NodeExample( 'g' )

    #__ a __ b
    #     |_ c __ d __ e
    #               |_ f
    #      |_ g

    a.add_child( b )
    a.add_child( c )
    c.add_child( d )
    d.add_child( e )
    d.add_child( f )
    a.add_child( g )

    print a.to_string()

    u = a.search_content( 'd' )
    print 'Searching for content d: %s' % ( u, )
    print

    path = a.search_path_to_content( 'd' )
    print 'Searching path from content d to root: '
    general_utils.display_list( path )
    print


    l = a.list_depth_first()
    print 'Listing content tree depth-first, starting from root node:'
    general_utils.display_list( l )
    print '(size of list: %s)' % ( len(l),)
    print

    m = a.list_by_height()
    print 'Listing content tree by increasing height, starting from root node:'
    general_utils.display_list( m )
    print '(size of list: %s)' % ( len(m),)
    print
