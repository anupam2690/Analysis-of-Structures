'''
A Node class contents the number of a Profile's Node and coordinates
  _no  = node number
  _x[] = List of point coordinates
'''

#    |module     |item
from Base import Base

class Node(Base):
    # constructor
    #                  | node number
    #                      | node coordinate
    def __init__(self, no, x, y):
        Base.__init__(self)
        try:
            self._no  = int(no)
            self._x   = [float(x), float(y)]
        except Exception as e:
            self.appendlog(str(e))
            raise Exception ("*** Error: invalid node data!")

    # destructor
    def __del__(self):
        pass

    # print node data
    def listData(self):             # to print node data
        self.appendlog("> Node %d, x = %8.3f mm, y = %8.3f mm" % \
                       (self._no, self._x[0], self._x[1]))

