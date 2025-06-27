class Operation:
    INSERT=1
    DELETE=2
    def __init__(self, tp, params):
        #tp: type of operation, INSERT or DELETE
        # params: tuple of operation params, (index, string) or (index, count)
        self.tp = tp
        self.params = params
        self.next:Operation|None = None # For stack

class OperationStack:
    # Class representing a stack of operations for undo and redo
    def __init__(self):
        self.head = None
    def push(self, tp:int, params):
        op = Operation(tp, params)
        self.push_op(op)
    def push_op(self, op: Operation):
        op.next = self.head
        self.head = op
    def peek(self):
        return self.head
    def pop(self):
        tmp = self.head
        if self.head != None:
            self.head = self.head.next
            return tmp
        else:
            return None
    def is_empty(self):
        return self.head == None
    def clear(self):
        self.head = None

def fibonacci(n):
    if n < 3:
        return 1
    i = 3
    prev = 1
    cur = 1
    while i <= n:
        next = prev + cur
        prev = cur
        cur = next
        i += 1
    return cur

class Rope:
    counter = 0
    def __init__(self, maxlen=5):
        # maxlen: maximum length of each fixed len str in the rope
        self.left:None|Rope = None
        self.right:None|Rope = None
        # If str is None, internal node, else leaf node
        self.str:None|str = None
        self.strlen:int = 0
        self.maxlen:int = maxlen
        # Ignore this, for debugging only
        self.id = Rope.counter
        Rope.counter += 1
    @staticmethod
    def from_string(st: str, start:int=0, end:int=None, maxlen=5):
        # Returns a balanced head node for rope with the string st
        # maxlen: maximum length of each fixed len str in the rope
        # start and end: bounds of the string to be included in the rope
        if end == None:
            end = len(st)
        length = end-start
        if length <= maxlen:
            # Base case, return a single leaf node with the given string
            if length <= 0:
                return None
            rp = Rope(maxlen)
            rp.str = st[start:end]
            rp.strlen = length
            return rp
        else:
            # Recursive case
            # Split the string in two and generate a rope from each subrope
            rp = Rope(maxlen)
            strlen = length
            idx = strlen//2
            # Create a rope with left subrope as the first substring
            # and right subrope as second substring
            rp.left = Rope.from_string(st, start, start+length//2, maxlen)
            rp.right = Rope.from_string(st, start+length//2, end, maxlen)
            rp.strlen = idx
            return rp
    def get_length(self):
        # Return the length of this rope
        if self.str != None:
            # Leaf node, base case
            return self.strlen
        else:
            # Recursive case, return the length of left side
            # plus length of right side
            l = self.strlen
            if self.right != None:
                l += self.right.get_length()
            return l
    def insert_string(self, idx, st):
        # Insert string st at index idx
        rp = Rope.from_string(st, maxlen = self.maxlen)
        # Split current rope at idx
        rs = self.split(idx)
        # Concatenate the string
        self.concat(rp)
        # Concatenate the string that was removed
        self.concat(rs)
        self.rebalance()
    def delete_chars(self, idx, n):
        # Delete n chars from index idx
        # idx: index to remove from
        # n: number of chars to remove

        # Split rope at idx and remove all chars starting at idx
        tail = self.split(idx)
        if tail == None:
            self.rebalance
            return
        # Separate all chars after index idx+n
        tail_of_tail = tail.split(n)
        # Concatenate chars after idx+n back to original rope
        if tail_of_tail != None:
            self.concat(tail_of_tail)
        self.rebalance()
    def get_substring(self, idx, n):
        # Get n characters starting from index idx
        if self.str == None:
            # Recursive case, either idx is in the left side, right side or splits
            # left and right side perfectly

            # li is None if idx is on the right side
            li = idx if idx < self.strlen else None
            ln = min(n, self.strlen-idx)
            if idx >= self.strlen:
                # Completely in right side
                ri = idx - self.strlen
            elif idx + n-1 >= self.strlen:
                # Partially in right side
                ri = 0
            else:
                # Left side only
                ri = None
            rn = n if idx >= self.strlen else n - (self.strlen - idx)

            if li != None and self.left == None:
                raise IndexError("Invalid index in get_substring()")
            elif ri != None and self.right == None:
                raise IndexError("Invalid index in get_substring()")

            # Retrieve the part of substring from left and right side if they exist
            # Concatenate and return
            left_str = "" if li == None else self.left.get_substring(li, ln)
            right_str = "" if ri == None else self.right.get_substring(ri, rn)
            return left_str + right_str
        else:
            # Base case, leaf node
            if idx > self.strlen or idx + n > self.strlen: # Corrected condition
                raise IndexError("Invalid index used with get_substring()")
            else:
                return self.str[idx:idx+n]
    def get_string(self):
        # Return the entire string
        strb = []
        if self.str == None:
            # Recursive case
            # Concatenate left and right substrings and return
            if self.left != None:
                strb.append(self.left.get_string())
            if self.right != None:
                strb.append(self.right.get_string())
        else:
            # Base case, return string stored in leaf node
            strb.append(self.str)
        return "".join(strb)
    def get_depth(self):
        if self.str == None:
            return 0
        else:
            ld = -1 if self.left == None else self.left.get_depth()
            rd = -1 if self.right == None else self.right.get_depth()
            return max(ld, rd) + 1
    def is_balanced(self):
        depth = self.get_depth()
        len = self.get_length()
        # Rope is balanced if length of string >= fib(depth + 2)
        return len >= fibonacci(depth + 2)

    @staticmethod
    def from_leaflist(leaflist: list[any], start: int, end: int, maxlen:int=5) -> any:
        # Create a rope from the list of leaves given, similar to from_string
        count = end-start
        if count == 0:
            return
        elif count == 1:
            # Single leaf, return as a rope
            return leaflist[start]
        elif count == 2:
            # Two leaves, combine into a rope with an internal node
            rp = Rope(maxlen)
            rp.left = leaflist[start]
            rp.right = leaflist[start+1]
            rp.strlen = rp.left.strlen
            return rp
        else:
            # Any number of leaves, create left and right subropes, combine and return
            rp = Rope(maxlen)
            rp.left = Rope.from_leaflist(leaflist, start, start + count//2, maxlen)
            rp.right = Rope.from_leaflist(leaflist, start + count//2, end, maxlen)
            rp.strlen = rp.left.get_length()
            return rp

    def rebalance(self):
        leaflist = []
        self.collect_leaves(leaflist)
        # Construct the rope from the ground-up
        rp = Rope.from_leaflist(leaflist, 0, len(leaflist), self.maxlen)
        # Copy the newly created rope to the current one
        Rope.copy(rp, self)

    def collect_leaves(self, leaflist):
        # Add all leaves in this rope to the list leaflist, in 
        # order from left to right
        if self.str != None and self.strlen > 0:
            # Base case, current node is a leaf node, append the current
            # node to the list
            leaflist.append(self)
            return
        # Recursive case, append all leaves in left sub-rope and then
        # right sub-rope
        if self.left != None:
            self.left.collect_leaves(leaflist)
        if self.right != None:
            self.right.collect_leaves(leaflist)

    @staticmethod
    def copy(fr, to):
        if fr == None:
            to.left = None
            to.right = None
            to.str = None
            to.strlen = 0
            return
        to.left = fr.left
        to.right = fr.right
        to.str = fr.str
        to.strlen = fr.strlen

    def concat(self, other):
        if self.get_length() == 0:
            # If current rope is empty, just make current rope
            # the same as the other rope
            Rope.copy(other, self)
            return
        # Create a new rope with left subrope as this rope and
        # right subrope as the other rope
        rp = Rope()
        Rope.copy(self, rp)
        self.left = rp
        self.right = other
        self.str = None
        self.strlen = self.left.get_length()

    def split(self, idx):
        # Split at idx, stores indices 0 to idx-1 in this Rope itself
        # Return a Rope with indices idx to the end
        if self.str != None:
            # Base case, leaf node
            # If split is within the node, remove excess portion, create a new Rope
            # with what was removed and return the new Rope
            if idx > self.strlen:
                raise IndexError('Invalid index in split')
            self.strlen = idx
            ret = self.str[idx:]
            self.str = self.str[0:idx]
            return Rope.from_string(ret, maxlen=self.maxlen)
        else:
            if idx == self.strlen:
                # If split is exactly between left and right child,
                # return right child
                other = self.right
                self.right = None
                return other
            elif idx < self.strlen:
                # if split starts in left subrope,
                # Recursively call on left subrope, and concatenate
                # right subrope
                if self.left == None:
                    raise IndexError('Invalid index in split')
                other = Rope(maxlen=self.maxlen)
                other.left = self.left.split(idx)
                other.strlen = self.strlen - idx
                other.right = self.right
                self.right = None
                return other
            else:
                # If split starts completely in the right, 
                # decrement index and call recursively on the right
                # subrope
                if self.right == None:
                    raise IndexError('Invalid index in split')
                other = self.right.split(idx - self.strlen)
                return other

    def print_debug(self):
        if self.str == None:
            print(f'Internal node {self.id}')
            print(f'strlen: {self.strlen}')
            if self.left != None:
                print(f'Left: {self.left.id}')
            if self.right != None:
                print(f'Right: {self.right.id}')
            print('')

            if self.left != None:
                self.left.print_debug()
            if self.right != None:
                self.right.print_debug()
        else:
            print(f'External node {self.id}')
            print(f'str: {self.str} strlen: {self.strlen}')
            print('')

class TextEditor:
    def __init__(self, rope=None):
        if rope == None:
            rope = Rope(maxlen=5)
        self.rope = rope
        self.undo_stack = OperationStack()
        self.redo_stack = OperationStack()
    def insert_string(self, idx, st):
        # Push the type of operation (INSERT) and params, idx and st into the undo stack)
        self.undo_stack.push(Operation.INSERT, (idx, st))
        # Insert the string st into index idx
        self.rope.insert_string(idx, st)
        # Clear the redo stack, since redo is possible only immediately after a sequence of undos
        self.redo_stack.clear()
        pass
    def delete_chars(self, idx, n):
        # Push the type of operation (DELETE) and params idx and the deleted substring into the undo stack
        # The substring is pushed and not n since if undone, it must be reinserted
        self.undo_stack.push(Operation.DELETE, (idx, self.rope.get_substring(idx, n)))
        # Delete n chars starting from index idx
        self.rope.delete_chars(idx, n)
        self.redo_stack.clear()
    def get_string(self):
        # Return the entire string stored in the editor
        return self.rope.get_string()
    def get_substring(self, idx, n):
        # Get the substring of n chars starting from index idx
        return self.rope.get_substring(idx, n)
    def undo(self):
        # Returns True if successfully undid the last operation
        # Returns False if no operation to undo
        # Undo the last operation
        op = self.undo_stack.pop()
        if op == None:
            # No operation to undo
            print("Popped none")
            return False
        # Push the current operation to redo stack
        # for performing redo later
        self.redo_stack.push_op(op)
        if op.tp == Operation.INSERT:
            # If last op was insert, delete the corresponding chars
            self.rope.delete_chars(op.params[0], len(op.params[1]))
            return True
        elif op.tp == Operation.DELETE:
            # If last op was delete, reinsert the corresponding chars
            self.rope.insert_string(op.params[0], op.params[1])
            return True
    def redo(self):
        # Returns True if successfully complete
        # Returns False if no operation to redo
        op = self.redo_stack.pop()
        if op == None:
            # No operations to redo
            return False
        self.undo_stack.push_op(op)
        if op.tp == Operation.INSERT:
            # Insert the string that was removed by undo
            self.rope.insert_string(op.params[0], op.params[1])
            return True
        elif op.tp == Operation.DELETE:
            # Delete the string that was reinserted by undo
            self.rope.delete_chars(op.params[0], len(op.params[1]))
            return True
        return False
    def length(self):
        return self.rope.get_length()
    def search_string(self, sub):
        # Return a list of starting indices where the string sub is present
        # in the current string stored by the TextEditor

        # prime : prime number as modulus
        # base : base that is size of English alphabet set = 26
        # sub: substring to find, use self.rope.get_string
        # st: string in which sub is to be found
        # str_hash: stores hash value of current part of string 
        # pat_hash: stores hash value of pattern
        # pat_len: store length of pattern
        # str_len: stores length of string
        st = self.rope.get_string()
        pat_len = len(sub)
        str_len = len(st)
        prime = 53
        base = 26
        str_hash = 0
        pat_hash = 0

        index_list = []

        h = pow(base, pat_len - 1, prime) # Precompute base^(pat_len-1) % prime

        if pat_len == 0:
            return []
        if pat_len > str_len:
            return []

        # Calculate hash value of pattern and first window of text
        for i in range(pat_len):
            pat_hash = (base * pat_hash + ord(sub[i])) % prime
            str_hash = (base * str_hash + ord(st[i])) % prime
    
        # Slide the pattern over text one by one
        for i in range(str_len - pat_len + 1):
            # Check the hash values of current window of text and pattern
            # If the hash values match then only check for characters one by one
            if pat_hash == str_hash:
                match = True
                for j in range(pat_len):
                    if st[i+j] != sub[j]:
                        match = False
                        break
                if match:
                    index_list.append(i)
            
            # Calculate hash value for next window of text: Remove leading digit,
            # add trailing digit
            if i < str_len - pat_len:
                # Remove leading character's hash contribution
                str_hash = (str_hash - ord(st[i]) * h) % prime
                # Add new character's hash contribution
                str_hash = (base * str_hash + ord(st[i+pat_len])) % prime
                # Ensure hash is non-negative
                if str_hash < 0:
                    str_hash += prime
        return index_list
 
if __name__ == '__main__':
    te = TextEditor()
    done = False
    while not done:
        try:
            op = input().lower().split()
            if not op: # Handle empty input
                continue
            if op[0] == 'i':
                if len(op) > 1:
                    idx = int(op[1])
                    line = input("Enter string to insert: ")
                    te.insert_string(idx, line)
                else:
                    print("Usage: i [index]")
            elif op[0] == 'p':
                if len(op) == 1:
                    print(te.get_string())
                elif len(op) == 3:
                    try:
                        print(te.get_substring(int(op[1]), int(op[2])))
                    except IndexError:
                        print("Error: Index out of bounds for substring.")
                    except ValueError:
                        print("Error: Invalid index or length for substring.")
                else:
                    print("Usage: p OR p [index] [length]")
            elif op[0] == 'd':
                if len(op) == 3:
                    try:
                        # delete_chars in TextEditor currently doesn't return the deleted string,
                        # but the sample commands imply it prints something.
                        # For now, let's assume it should print a confirmation or the operation itself.
                        # The original code had `print(te.delete_chars(int(op[1]), int(op[2])))`
                        # which would print None. Let's make it more informative.
                        deleted_substring = te.get_substring(int(op[1]), int(op[2])) # Get before deleting for undo
                        te.delete_chars(int(op[1]), int(op[2]))
                        print(f"Deleted: '{deleted_substring}'")
                    except IndexError:
                        print("Error: Index out of bounds for delete.")
                    except ValueError:
                        print("Error: Invalid index or count for delete.")
                else:
                    print("Usage: d [index] [length]")
            elif op[0] == 'f':
                if len(op) > 1:
                    print(te.search_string(op[1]))
                else:
                    print("Usage: f [substring]")
            elif op[0] == 'r':
                if te.redo():
                    print("Redo successful")
                else:
                    print("No operation to redo")
            elif op[0] == "u":
                if te.undo():
                    print("Undo successful")
                else:
                    print("No operation to undo")
            elif op[0] == "ex":
                print("Exiting...")
                done = True
            elif op[0] == "l":
                print(f'Length: {te.length()}')
            elif op[0] == "h":
                print("\nTextEditor Commands:")
                print("  i [index]          - Insert string at index (prompts for string)")
                print("  p                  - Print the entire string")
                print("  p [index] [length] - Print substring")
                print("  d [index] [length] - Delete characters")
                print("  f [substring]      - Find all occurrences of substring")
                print("  u                  - Undo last operation")
                print("  r                  - Redo last undone operation")
                print("  l                  - Print total length of the string")
                print("  h                  - Display this help message")
                print("  ex                 - Exit the editor\n")
            else:
                print(f"Unknown command: {op[0]}. Type 'h' for help.")
        except EOFError:
            print("\nExiting due to EOF (Ctrl+D).")
            done = True
        except Exception as e:
            print(f"An error occurred: {e}")
