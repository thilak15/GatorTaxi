import sys
# Ride class to represent a single ride request
class Ride:
    def __init__(self, rideNumber, rideCost, tripDuration):
        self.rideNumber = rideNumber
        self.rideCost = rideCost
        self.tripDuration = tripDuration
    

    # Comparison function to compare two rides based on rideCost and tripDuration
    def less_than(self, other_ride):
        if self.rideCost != other_ride.rideCost:
            return self.rideCost < other_ride.rideCost
        return self.tripDuration <= other_ride.tripDuration

# MinHeap class to represent a min heap data structure
class MinHeap:
    def __init__(self):
        self.heap_list = [0]
        self.curr_size = 0

    # Function to insert an element into the min heap
    def insert(self, ele):
        self.heap_list.append(ele)
        self.curr_size += 1
        self.heapify_up(self.curr_size)
    
    # Function to swap two elements in the heap
    def swap(self, ind1, ind2):
        self.heap_list[ind1], self.heap_list[ind2] = self.heap_list[ind2], self.heap_list[ind1]
        self.heap_list[ind1].min_heap_index = ind1
        self.heap_list[ind2].min_heap_index = ind2
    # Function to move an element up in the heap to maintain the heap property
    def heapify_up(self, p):
        while (p // 2) > 0:
            if self.heap_list[p].ride.less_than(self.heap_list[p // 2].ride):
                self.swap(p, (p // 2))
            else:
                break
            p = p // 2
    # Function to move an element down in the heap to maintain the heap property
    def heapify_down(self, p):
        while (p * 2) <= self.curr_size:
            ind = self.get_min_child_index(p)
            if not self.heap_list[p].ride.less_than(self.heap_list[ind].ride):
                self.swap(p, ind)
            p = ind
    
    # Function to get the index of the minimum child of a given element
    def get_min_child_index(self, p):
        left_child = p * 2
        right_child = (p * 2) + 1

        if right_child > self.curr_size:
            return left_child
        elif self.heap_list[left_child].ride.less_than(self.heap_list[right_child].ride):
            return left_child
        else:
            return right_child

    # Function to update an element in the heap and maintain the heap property
    def update(self, p, new_key):
        node = self.heap_list[p]
        node.ride.tripDuration = new_key

        parent = p // 2
        if p == 1 or self.heap_list[parent].ride.less_than(node.ride):
            self.heapify_down(p)
        else:
            self.heapify_up(p)

    # Function to delete an element from the heap and maintain the heap property
    def delete(self, p):
        self.swap(p, self.curr_size)
        self.curr_size -= 1
        self.heap_list.pop()
        self.heapify_down(p)

    # Function to remove and return the root element from the heap
    def pop(self):
        if len(self.heap_list) == 1:
            return 'No Rides Available'

        root = self.heap_list[1]
        self.delete(1)

        return root



class MinHeapNode:
    def __init__(self, ride, rbt, min_heap_index):
        # Initialize the MinHeapNode with the given ride, RBT, and min_heap_index attributes
        self.ride = ride
        self.rbTree = rbt
        self.min_heap_index = min_heap_index
class RBTNode:
    def __init__(self, ride, min_heap_node):
        # Initialize the RBTNode with the given ride and min_heap_node attributes
        self.ride = ride
        self.parent = None  # parent node
        self.left = None  # left node
        self.right = None  # right node
        self.color = 1  # 1=red , 0 = black
        self.min_heap_node = min_heap_node # MinHeapNode associated with the node


class RedBlackTree:
    def __init__(self):
        # Initialize the red-black tree with a null node and set it as the root node
        self.null_node = RBTNode(None, None)
        self.null_node.left = None
        self.null_node.right = None
        self.null_node.color = 0
        self.root = self.null_node

    # To retrieve the ride with the rideNumber equal to the key
    def get_ride(self, key):
        # Start at the root node
        temp = self.root

        # Iterating through the tree to find the node with rideNumber equal to the key
        while temp != self.null_node:
            # If the rideNumber of the current node is equal to the key, return the node
            if temp.ride.rideNumber == key:
                return temp
            # If the rideNumber of the current node is less than the key, go to the right child node
            temp = temp.right if temp.ride.rideNumber < key else temp.left


        # If the key is not found in the tree, return None

        return None

    # Balancing the tree after deletion
    def balance_tree_after_delete(self, node):
        while node != self.root and node.color == 0:
            # Check if the node is a right child or a left child
            is_right_child = node == node.parent.right
            # Find the sibling node of the parent
            if is_right_child:
                parent_sibling = node.parent.left
            else:
                parent_sibling = node.parent.right
            # Case 1: If the sibling is red, recolor the parent and sibling, and perform a rotation to make the sibling black
            if parent_sibling.color != 0:
                node.parent.color = 1
                parent_sibling.color = 0
                if is_right_child:
                    self.r_rotation(node.parent)
                else:
                    self.l_rotation(node.parent)
                if is_right_child:
                    parent_sibling = node.parent.left
                else:
                    parent_sibling = node.parent.right
            # Case 2: If both children of the sibling are black, recolor the sibling and move up the tree
            if parent_sibling.right.color == 0 and parent_sibling.left.color == 0:
                parent_sibling.color = 1
                node = node.parent
            # Case 3: If the sibling is black and has a red child, recolor the sibling's red child and perform a rotation
            else:
                if (is_right_child and parent_sibling.left.color != 1) or (not is_right_child and parent_sibling.right.color != 1):
                    if is_right_child:
                        parent_sibling.right.color = 0
                    else:
                        parent_sibling.left.color = 0
                    parent_sibling.color = 1
                    if is_right_child:
                        self.l_rotation(parent_sibling)
                    else:
                        self.r_rotation(parent_sibling)
                    if is_right_child:
                        parent_sibling = node.parent.left
                    else:
                        parent_sibling = node.parent.right
            # Case 4: Recolor the parent and sibling, and perform a rotation to make the parent the new root
                parent_sibling.color = node.parent.color
                node.parent.color = 0
                if is_right_child:
                    parent_sibling.left.color = 0
                    self.r_rotation(node.parent)
                else:
                    parent_sibling.right.color = 0
                    self.l_rotation(node.parent)
                node = self.root

        node.color = 0


    def __rb_trans(self, node, child_node):
        # Replace the node with the child node in the tree
        if node.parent is None:
            self.root = child_node
        elif node == node.parent.right:
            node.parent.right = child_node
        else:
            node.parent.left = child_node

        child_node.parent = node.parent



    def delete_helper(self, node, key):
        # Find the node to delete and its corresponding MinHeapNode
        delete_node = self.null_node

        while node != self.null_node:
            if node.ride.rideNumber == key:
                delete_node = node

            node = node.left if node.ride.rideNumber >= key else node.right

        if delete_node == self.null_node:
            return

        heap_node = delete_node.min_heap_node

        # Perform the deletion
        y = delete_node
        y_original_color = y.color
        x = None

        if delete_node.left == self.null_node:
            x = delete_node.right
            self.__rb_trans(delete_node, delete_node.right)
        elif delete_node.right == self.null_node:
            x = delete_node.left
            self.__rb_trans(delete_node, delete_node.left)
        else:
            y = self.minimum(delete_node.right)
            y_original_color = y.color
            x = y.right

            if y.parent == delete_node:
                x.parent = y
            else:
                self.__rb_trans(y, y.right)
                y.right = delete_node.right
                y.right.parent = y

            self.__rb_trans(delete_node, y)
            y.left = delete_node.left
            y.left.parent = y
            y.color = delete_node.color
        # Balance the tree after the deletion
        if y_original_color == 0:
            self.balance_tree_after_delete(x)

        return heap_node


    def balance_post_insert(self, curr_node):
        while curr_node.parent.color == 1:
            # Check if the parent node is a left child or a right child
            is_left_child = curr_node.parent == curr_node.parent.parent.left

            # Find the sibling node of the parent
            if is_left_child:
                parent_sibling = curr_node.parent.parent.right
            else:
                parent_sibling = curr_node.parent.parent.left

            if parent_sibling.color == 0:
                if (is_left_child and curr_node == curr_node.parent.right) or (not is_left_child and curr_node == curr_node.parent.left):
                    curr_node = curr_node.parent
                    if is_left_child:
                        self.l_rotation(curr_node)
                    else:
                        self.r_rotation(curr_node)

                curr_node.parent.color = 0
                curr_node.parent.parent.color = 1
                if is_left_child:
                    self.r_rotation(curr_node.parent.parent)
                else:
                    self.l_rotation(curr_node.parent.parent)
            else:
                parent_sibling.color = 0
                curr_node.parent.color = 0
                curr_node.parent.parent.color = 1
                curr_node = curr_node.parent.parent

            if curr_node == self.root:
                break

        self.root.color = 0


    def __rides_in_range(self, node, low, high, res):
        # Recursive helper method to find all rides with rideNumbers between low and high
        if node != self.null_node:
            if low < node.ride.rideNumber:
                self.__rides_in_range(node.left, low, high, res)

            if low <= node.ride.rideNumber <= high:
                res.append(node.ride)

            self.__rides_in_range(node.right, low, high, res)

    def get_rides_in_range(self, low, high):
        # Method to get all rides with rideNumbers between low and high

        res = []
        self.__rides_in_range(self.root, low, high, res)
        return res

    def minimum(self, node):
        # Method to find the node with the minimum rideNumber in the subtree rooted at node

        while node.left != self.null_node:
            node = node.left
        return node


    def l_rotation(self, x):
        # Left rotation method
        y = x.right # Set y to be the right child of x
        x.right = y.left    # Set the right child of x to be the left child of y

        if y.left != self.null_node:
            y.left.parent = x

        y.parent = x.parent

        if x.parent is None:
            self.root = y
        else:
            if x == x.parent.left:
                x.parent.left = y
            else:
                x.parent.right = y

        y.left, x.parent = x, y


    def r_rotation(self, x):
        # Right rotation method
        y = x.left # Set y to be the left child of x
        x.left = y.right # Set the left child of x to be the right child of y
        if y.right != self.null_node:
            y.right.parent = x

        y.parent = x.parent
        if x.parent is None:
            self.root = y
        elif x == x.parent.right:
            x.parent.right = y
        else:
            x.parent.left = y
        y.right,x.parent = x,y

    def insert(self, ride, min_heap):
        # Create new RBTNode with the given ride and min heap node
        node = RBTNode(ride, min_heap)
        node.parent = None
        node.left = self.null_node
        node.right = self.null_node
        node.color = 1

        insertion_node = None
        temp_node = self.root

        # Traverse the tree to find the insertion point for the new node
        while temp_node != self.null_node:
            insertion_node = temp_node
            temp_node = temp_node.left if node.ride.rideNumber < temp_node.ride.rideNumber else temp_node.right

        node.parent = insertion_node
         # If the insertion node is None, set the root to be the new node
        if insertion_node is None:
            self.root = node
        else:
            # Otherwise, insert the new node as a child of the insertion node

            if node.ride.rideNumber > insertion_node.ride.rideNumber:
                insertion_node.right = node
            else:
                insertion_node.left = node
        # If the parent of the new node is None, color it black and return
        if node.parent is None:
            node.color = 0
            return
        # Otherwise, balance the tree to maintain the Red-Black Tree properties
        if node.parent.parent is None:
            return

        self.balance_post_insert(node)


    def delete_node(self, rideNumber):
        return self.delete_helper(self.root, rideNumber)
class DuplicateRideNumberError(Exception):
    pass


def insert_ride(ride, heap, rbt):
    # checking if the given ride already exists in the Red_black Tree
    if rbt.get_ride(ride.rideNumber) is not None:
        # if the ride already exists exception is raised
        raise DuplicateRideNumberError("Duplicate RideNumber")
    rbt_node = RBTNode(None, None)
    min_heap_node = MinHeapNode(ride, rbt_node, heap.curr_size + 1)
    heap.insert(min_heap_node)
    rbt.insert(ride, min_heap_node)


def add_to_output(ride, message, list):
    # Append data to the file
    with open("output_file.txt", "a") as file:
        if ride is None:
            file.write(message)
        else:
            message = ""
            if not list:
                message += f"({ride.rideNumber},{ride.rideCost},{ride.tripDuration})"
            else:
                if len(ride) == 0:
                    message += "(0,0,0)"
                else:
                    rides_str = ",".join([f"({r.rideNumber},{r.rideCost},{r.tripDuration})" for r in ride])
                    message += rides_str

            file.write(message)

        # Write a newline character if it's not the last line in the output
        if not (ride is None and message == "Duplicate RideNumber"):
            file.write("\n")




def print_ride(rideNumber, rbt):
    # Get the ride with the given rideNumber from the Red-Black Tree
    res = rbt.get_ride(rideNumber)
    # If the ride is not found, add a placeholder ride to the output with a flag indicating that it is not a real ride
    if res is None:
        add_to_output(Ride(0, 0, 0), "", False)
    # If the ride is found, add it to the output

    else:
        add_to_output(res.ride, "", False)


def print_rides(l, h, rbt):
    # Get a list of rides with ride numbers in the range [l, h] from the Red-Black Tree
    list = rbt.get_rides_in_range(l, h)
    # Add the list of rides to the output, with a flag indicating that it is a list of real rides
    add_to_output(list, "", True)


def get_next_ride(heap, rbt):
    # If there are rides in the heap, pop the ride with the smallest trip duration
    if heap.curr_size != 0:
        popped_node = heap.pop()
        # Remove the corresponding ride from the Red-Black Tree
        rbt.delete_node(popped_node.ride.rideNumber)
        # Add the popped ride to the output

        add_to_output(popped_node.ride, "", False)
    
    # If there are no rides in the heap, add a message to the output indicating that there are no active ride requests
    else:
        add_to_output(None, "No active ride requests", False)


def cancel_ride(ride_number, heap, rbt):
    # Delete the ride with the given rideNumber from the Red-Black Tree
    heap_node = rbt.delete_node(ride_number)
    # If the ride was found in the Red-Black Tree, delete its corresponding MinHeapNode from the MinHeap
    if heap_node is not None:
        heap.delete(heap_node.min_heap_index)


def update_ride(rideNumber, new_duration, heap, rbt):
     # Get the RBTNode corresponding to the ride with the given rideNumber
    rbt_node = rbt.get_ride(rideNumber)
    # If the ride does not exist, print a newline and return
    if rbt_node is None:
        print("")
        return
    
    # Get the old duration of the ride
    old_duration = rbt_node.ride.tripDuration
    # If the new duration is less than or equal to the old duration, update the MinHeap with the new duration

    if new_duration <= old_duration:
        heap.update(rbt_node.min_heap_node.min_heap_index, new_duration)
    # If the new duration is greater than the old duration, cancel the ride and create a new ride with the updated duration and cost

    else:
        cancel_ride(rideNumber, heap, rbt)
        # If the new duration is less than or equal to twice the old duration, increase the cost of the new ride by 10 and insert it into the heap and Red-Black Tree
        if new_duration <= 2 * old_duration:
            new_cost = rbt_node.ride.rideCost + 10
            insert_ride(Ride(rideNumber, new_cost, new_duration), heap, rbt)



if __name__ == "__main__":
    # Get the input file path from the command line arguments
    input_file = sys.argv[1]
    # Create an empty MinHeap and Red-Black Tree

    heap = MinHeap()
    rbt = RedBlackTree()
    # Create an empty output file

    with open("output_file.txt", "w") as output_file:
        pass
    # Open the input file and read its lines one by one
    with open(input_file, "r") as input_file:
        for line in input_file.readlines():
            try:
                # Extract the action and its parameters from the current line
                numbers = [int(num) for num in line[line.index("(") + 1:line.index(")")].split(",") if num != '']
                action = line.split("(")[0].strip()

                if action == "Insert":
                    insert_ride(Ride(numbers[0], numbers[1], numbers[2]), heap, rbt)
                elif action == "Print":
                    if len(numbers) == 1:
                        print_ride(numbers[0], rbt)
                    elif len(numbers) == 2:
                        print_rides(numbers[0], numbers[1], rbt)
                elif action == "UpdateTrip":
                    update_ride(numbers[0], numbers[1], heap, rbt)
                elif action == "GetNextRide":
                    get_next_ride(heap, rbt)
                elif action == "CancelRide":
                    cancel_ride(numbers[0], heap, rbt)
            # If a DuplicateRideNumberError is raised during an insertion, add an error message to the output and break out of the loop
            except DuplicateRideNumberError as e:
                add_to_output(None, str(e), False)
                break

    
    

