"""The linkedlist module provides support for rendering linked lists.

linkedlist module provides a wrapper for your LinkedList nodes useful for
explanation and the Forwardlist class which is useful for application.

- The LinkedListNode class is used to represent a node.
- The LinkedList class is used to store the head pointer.
- The ForwardList class is a complete implementation of singly linked list

These three classes can be directly imported from the toolkit:

    >>> llnode = ARgorithmToolkit.LinkedListNode(algo,7)
    >>> ll = ARgorithmToolkit.LinkedList("llnode",algo,llnode)
    >>> fl = ARgorithmToolkit.ForwardList("fl",algo)
"""

from ARgorithmToolkit.utils import ARgorithmHashable, ARgorithmStructure, State, StateSet, ARgorithmError
from ARgorithmToolkit.encoders import serialize

class LinkedListNodeState:
    """This class is used to generate states for various actions performed on
    the ``ARgorithmToolkit.linkedlist.LinkedListNode`` object.

    Attributes:

        name (str) : Name of the variable for whom we are generating states
        _id (str) : id of the variable for whom we are generating states
    """

    def __init__(self,name:str,_id:str):
        self.name = name
        self._id = _id

    def llnode_declare(self,value,_next,comments=""):
        """Generates the `llnode_declare` state when a new node is created.

        Args:
            value : The value stored in the linkedlist node
            next (LinkedListNode): The next pointer
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `llnode_declare` state
        """
        state_type = "llnode_declare"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "value" : value,
            "next" : _next.name if _next else "none"
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def llnode_iter(self,value,_next,last_value=None,comments=""):
        """Generates the `llnode_iter` state when a node is accessed or its
        value is changed.

        Args:
            value : The value stored in the linkedlist node
            next (LinkedListNode): The next pointer
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `llnode_iter` state
        """
        state_type = "llnode_iter"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "value" : value,
            "next" : _next.name if _next else "none"
        }
        if not(last_value is None):
            state_def["last_value"] = last_value
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def llnode_next(self,value,_next,last_next,comments=""):
        """Generates the `llnode_next` state when the next pointer changes.

        Args:
            value : The value stored in the linkedlist node
            next (LinkedListNode): The next pointer
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `llnode_next` state
        """
        state_type = "llnode_next"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "value" : value,
            "next" : _next.name if _next else "none",
            "last_next" : last_next.name if last_next else "none"
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def llnode_delete(self,comments=""):
        """Generates the `llnode_delete` state when a node is deleted.

        Args:
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `llnode_delete` state
        """
        state_type = "llnode_delete"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

@serialize
class LinkedListNode(ARgorithmStructure, ARgorithmHashable):
    """The LinkedListNode class is an implementation of a Linked list Node for
    which we store states. Unlike other data structure classes, in which we
    have to give a name to the instance, we dont have to provide name in the
    LinkedListNode Class.

    Attributes:
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of LinkedListNode Class
        value: The value stored in the node
        next (LinkedListNode): The reference to next node

    Raises:
        ARgorithmError: Raised if algo is not of type StateSet

    Example:

        >>> llnode = ARgorithmToolkit.LinkedListNode(algo,7)
        >>> llnode.value = 10
        >>> temp = = ARgorithmToolkit.LinkedListNode(algo,7)
        >>> temp.next = llnode
        >>> llnode = temp
    """

    def __init__(self,algo:StateSet,value=None,comments=""):
        self.name = str(id(self))
        self._id = str(id(self))
        try:
            assert isinstance(algo,StateSet)
            self.algo = algo
        except AssertionError as e:
            raise ARgorithmError("algo should be of type StateSet") from e

        self.state_generator = LinkedListNodeState(self.name, self._id)

        self._flag = False
        self.value = value
        self.next = None
        self._flag = True

        state = self.state_generator.llnode_declare(
            self.value,self.next,comments
        )
        self.algo.add_state(state)

    def __setattr__(self,key,value):
        """The __setattr__ function is overriden to listen to state changes in
        the value of node or the next attribute.

        Raises:
            ARgorithmError: Raised if next pointer is not type None or LinkedListNode
        """
        if key == 'next' and value:
            assert isinstance(value,LinkedListNode) , ARgorithmError("next should be of type None or LinkedListNode")
        last_value = None
        last_next = None
        if key == 'value' and self._flag:
            last_value = self.value
        elif key == 'next' and self._flag:
            last_next = self.next
        self.__dict__[key] = value
        if key == 'next' and self._flag:
            if last_next or self.next:
                state = self.state_generator.llnode_next(
                    value=self.value,
                    _next=self.next,
                    last_next=last_next,
                    comments="next pointer updated"
                )
                self.algo.add_state(state)
        elif key == 'value' and self._flag:
            state = self.state_generator.llnode_iter(
                value=self.value,
                _next=self.next,
                last_value=last_value,
                comments="value updated"
            )
            self.algo.add_state(state)

    def __del__(self):
        """The __del__ function is overriden is there to listen to node
        deletion."""
        state = self.state_generator.llnode_delete(
            "Node was deleted"
        )
        self.algo.add_state(state)

    def __str__(self):
        return f"LinkedListNode({self.value}) at {self.name}"

    def __repr__(self):
        return f"LinkedListNode({self.value}) at {self.name}"

class LinkedListState:
    """This class is used to generate states for various actions performed on
    the ``ARgorithmToolkit.linkedlist.LinkedList`` object.

    Attributes:

        name (str) : Name of the variable for whom we are generating states
        _id (str) : id of the variable for whom we are generating states
    """
    def __init__(self,name:str,_id:str):
        self.name = name
        self._id = _id

    def ll_declare(self,head,comments=""):
        """Generates the `ll_declare` state when a new linkedlist is created.

        Args:
            head (LinkedListNode): The head pointer
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `ll_declare` state
        """
        state_type = "ll_declare"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "head" : head.name if head else "none"
        }
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

    def ll_head(self,head,last_head=None,comments=""):
        """Generates the `ll_head` state when linkedlist head is changed.

        Args:
            head (LinkedListNode): The head pointer
            comments (str, optional): Comments for descriptive purpose. Defaults to "".

        Returns:
            State: Returns the `ll_head` state
        """
        state_type = "ll_head"
        state_def = {
            "id" : self._id,
            "variable_name" : self.name,
            "head" : head.name if head else "none"
        }
        if not (last_head is None):
            state_def["last_head"] = last_head
        return State(
            state_type=state_type,
            state_def=state_def,
            comments=comments
        )

@serialize
class LinkedList(ARgorithmStructure, ARgorithmHashable):
    """The LinkedList class is used to just store the head of the linked list.

    This class is useful when programmer want to program his own List class using
    the nodes. Only contains head attribute and no methods

    Attributes:
        name (str): The name given to the linkedlist
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of LinkedList Class
        head (LinkedListNode): The referece to head of linkedlist

    Raises:
        ARgorithmError: Raised if algo is not of type StateSet

    Example:

        >>> ll = ARgorithmToolkit.LinkedList("llnode",algo)
        >>> llnode = ARgorithmToolkit.LinkedListNode(algo,7)
        >>> ll.head = llnode
    """

    def __init__(self,name:str,algo:StateSet,head=None,comments=""):

        assert isinstance(name,str) , ARgorithmError("Name should be of type string")
        self.name = name
        self._id = str(id(self))
        try:
            assert isinstance(algo,StateSet)
            self.algo = algo
        except AssertionError as e:
            raise ARgorithmError("algo should be of type StateSet") from e
        self.state_generator = LinkedListState(self.name, self._id)

        self._flag = False
        if head:
            assert self.algo == head.algo, ARgorithmError("The head node belongs to a different StateSet")
        self.head = head
        self._flag = True

        state = self.state_generator.ll_declare(self.head,comments)
        self.algo.add_state(state)

    def __setattr__(self,key,value):
        """The __setattr__ function is overriden to listen to state changes in
        the head.

        Raises:
            ARgorithmError: Raised if head pointer is not type None or LinkedListNode
        """
        last_head = None
        if key == 'head' and value:
            assert isinstance(value,LinkedListNode) , ARgorithmError("next should be of type None or LinkedListNode")
        if key == 'head' and self._flag:
            last_head = self.head._id if self.head else "none"
        self.__dict__[key] = value
        if key == 'head' and self._flag:
            state = self.state_generator.ll_head(self.head,last_head=last_head, comments="head pointer shifts")
            self.algo.add_state(state)

    def __str__(self):
        return f"LinkedList(head at {self.head})"

    def __repr__(self):
        return f"LinkedList(head at {self.head})"

class ForwardListIterator:
    """This class is a generator that is returned each time an ForwardList has
    to be iterated.

    Yields:
        Value of ForwardList Node

    Raises:
        AssertionError: If not declared with an instance of ARgorithmToolkit.linkedlist.ForwardList
    """
    def __init__(self,forwardlist):
        assert isinstance(forwardlist,ForwardList)
        self._curr = forwardlist.head

    def __next__(self):
        if self._curr:
            data = self._curr.value
            self._curr = self._curr.next
            return data
        raise StopIteration

class ForwardList(LinkedList):
    """The ForwardList class is proper implementation of singly linked list.

    The difference between LinkedList and ForwardList class is that ForwardList
    is a ready implementation of singly linked list. In the LinkedList class the
    programmer will have to make their own methods.

    Attributes:
        name (str): The name given to the linkedlist
        algo (ARgorithmToolkit.utils.StateSet): The stateset that will store the states generated by the instance of ForwardList Class
        head (LinkedListNode): The referece to head of linkedlist
        size (int): Number of nodes i.e size of list

    Raises:
        ARgorithmError: Raised if algo is not of type StateSet

    Example:

        >>> fl = ARgorithmToolkit.ForwardList("fl",algo)
    """

    def __init__(self,name:str,algo:StateSet,comments=""):
        super().__init__(name,algo,comments="")
        self.size = 0

    def __len__(self):
        """overloads the len() operator to return size of list.

        Returns:
            int: size of list

        Example:

            >>> fl = ARgorithmToolkit.ForwardList("fl",algo)
            >>> fl.push_front(1)
            >>> fl.size()
            1
        """
        return self.size

    def insert(self,value,index=0):
        """Insert node with given value at particular index. If index is not
        given,insert at front.

        Args:
            value : The value to be inserted
            index (int, optional): The index where value has to inserted . Defaults to 0.

        Example:

            >>> fl = ARgorithmToolkit.ForwardList("fl",algo)
            >>> fl.insert(2)
            >>> fl.insert(4)
            >>> fl.insert(3,1)
            >>> fl
            ForwardList([4, 3, 2])
        """
        if self.size == 0 or index == 0:
            self.push_front(value)
        elif self.size < index:
            temp = self.head
            while temp.next:
                temp = temp.next
            curr = LinkedListNode(self.algo,value)
            temp.next = curr
            self.size += 1
        else:
            count = 1
            temp = self.head
            while index > count:
                count += 1
                temp = temp.next
            curr = LinkedListNode(self.algo,value)
            curr.next = temp.next
            temp.next = curr
            self.size += 1

    def push_front(self,value):
        """Pushes value to front.

        Args:
            value : Value to be appended to front

        Example:
            >>> fl = ARgorithmToolkit.ForwardList("fl",algo)
            >>> fl
            ForwardList([])
            >>> fl.push_front(1)
            >>> fl
            ForwardList([1])
        """
        curr = LinkedListNode(self.algo,value)
        if self.head:
            curr.next = self.head
            self.head = curr
        else:
            curr.next = None
            self.head = curr
        self.size+=1

    def pop_front(self):
        """Pops first element of forwardlist.

        Raises:
            ARgorithmError: Raised if list is empty

        Returns:
            element: The first element of list

        Example:

            >>> fl
            ForwardList([2, 1])
            >>> fl.pop_front()
            2
        """
        if self.head is None:
            raise ARgorithmError("Empty list")
        data = self.head.value
        temp = self.head
        self.head = self.head.next
        del temp
        self.size -= 1
        return data

    def front(self):
        """Returns the first element of list.

        Raises:
            ARgorithmError: Raised when list is empty

        Returns:
            element: The first element of list

        Example:

            >>> fl
            ForwardList([2, 1])
            >>> fl.front()
            2
        """
        if self.head is None:
            raise ARgorithmError("Empty list")
        return self.head.value

    def __iter__(self):
        """Returns the generator object to iterate through elements of
        ForwardList.

        Returns:
            ForwardListIterator: Generator class for ForwardList

        Example:

            >>> [x for x in fl]
            [2, 2, 1]
        """
        return ForwardListIterator(self)

    def remove(self,value):
        """Remove elements with given value from list.

        Args:
            value : The value which has to be removed

        Raises:
            ARgorithmError: Raised if list is empty

        Example:

            >>> fl
            ForwardList([2, 2, 1])
            >>> fl.remove(2)
            >>> fl
            ForwardList([1])
        """
        if self.head is None:
            raise ARgorithmError("Empty list")
        while value == self.head.value:
            temp = self.head
            self.head = self.head.next
            del temp
            self.size -= 1
            if self.head is None:
                return
        curr = self.head
        while curr:
            if curr.next:
                if curr.next.value == value:
                    temp = curr.next
                    curr.next = curr.next.next
                    del temp
                    self.size -= 1
                    continue
            curr = curr.next

    def tolist(self):
        """Converts the ForwardList to python list.

        Returns:
            list: list of ForwardList items

        Example:

            >>> fl
            ForwardList([3, 1])
            >>> fl.tolist()
            [3, 1]
        """
        curr = self.head
        data = []
        while curr:
            data.append(curr.value)
            curr = curr.next
        return data

    def __repr__(self):
        return f"ForwardList({self.tolist()})"

    def __str__(self):
        return f"ForwardList({self.tolist()})"
