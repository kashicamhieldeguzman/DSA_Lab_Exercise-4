from flask import Blueprint, render_template, request, redirect, url_for, flash
from stack import to_value

#                                        DEQUE IMPLEMENTATION

class Node:
    def __init__(self, data):
        self.data = data
        self.prev = None
        self.next = None


class Deque:
    def __init__(self):
        self.head = None
        self.tail = None
        self.size = 0

    def is_empty(self):
        return self.head is None

    def add_front(self, item):
        new_node = Node(item)

        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.next = self.head
            self.head.prev = new_node
            self.head = new_node

        self.size += 1

    def add_rear(self, item):
        new_node = Node(item)

        if self.is_empty():
            self.head = self.tail = new_node
        else:
            new_node.prev = self.tail
            self.tail.next = new_node
            self.tail = new_node

        self.size += 1

    def remove_front(self):
        if self.is_empty():
            raise Exception ("DeQue is empty, cannot remove")

        removed_data = self.head.data
        self.head = self.head.next

        if self.head is None:
            self.tail = None
        else:
            self.head.prev = None

        self.size -= 1
        
        
        return removed_data

    def remove_rear(self):
        if self.is_empty():
            raise Exception("DeQue is empty, cannot remove")

        removed_data = self.tail.data
        self.tail = self.tail.prev

        if self.tail is None:
            self.head = None
        else:
            self.tail.next = None

        self.size -= 1
        return removed_data

    def peek_front(self):
        if self.is_empty():
            raise Exception("Peek from empty deque")
        return self.head.data
 
    def peek_rear(self):
        if self.is_empty():
            raise Exception("Peek from empty deque")
        return self.tail.data
 
    def to_list(self):
        """Return the data from front to rear as a normal Python list."""
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items
 
    def clear(self):
        self.head = None
        self.tail = None
        self._size = 0
 
    def __len__(self):
        return self.size
 
 
#                                        DEQUE ROUTES (blueprint)
 
deque_bp = Blueprint('deque', __name__)   # app.py registers this
dq = Deque()                              # one shared deque, kept in memory while the server runs
 
 
def back():
    return redirect(url_for('deque.deque'))
 
 
@deque_bp.route('/deque')
def deque():
    return render_template('deque.html',
                           items=dq.to_list(),
                           peeked=request.args.get('peeked'))
 
@deque_bp.route('/deque/add_front', methods=['POST'])
def dq_add_front():
    value = to_value(request.form.get('value', ''))
    if value == '':
        flash("Type a value first.", "error")
    else:
        dq.add_front(value)
        flash(f'Added "{value}" to the front.', "success")
    return back()
 
@deque_bp.route('/deque/add_rear', methods=['POST'])
def dq_add_rear():
    value = to_value(request.form.get('value', ''))
    if value == '':
        flash("Type a value first.", "error")
    else:
        dq.add_rear(value)
        flash(f'Added "{value}" to the rear.', "success")
    return back()
 
@deque_bp.route('/deque/remove_front', methods=['POST'])
def dq_remove_front():
    if dq.is_empty():
        flash("The deque is empty.", "error")
    else:
        flash(f'Removed "{dq.remove_front()}" from the front.', "success")
    return back()
 
@deque_bp.route('/deque/remove_rear', methods=['POST'])
def dq_remove_rear():
    if dq.is_empty():
        flash("The deque is empty.", "error")
    else:
        flash(f'Removed "{dq.remove_rear()}" from the rear.', "success")
    return back()
 
@deque_bp.route('/deque/peek_front', methods=['POST'])
def dq_peek_front():
    if dq.is_empty():
        flash("The deque is empty.", "error")
        return back()
    flash(f'Front value: {dq.peek_front()}', "success")
    return redirect(url_for('deque.deque', peeked='front'))   # highlights the front node
 
@deque_bp.route('/deque/peek_rear', methods=['POST'])
def dq_peek_rear():
    if dq.is_empty():
        flash("The deque is empty.", "error")
        return back()
    flash(f'Rear value: {dq.peek_rear()}', "success")
    return redirect(url_for('deque.deque', peeked='rear'))    # highlights the rear node
 
@deque_bp.route('/deque/sample', methods=['POST'])
def dq_sample():
    dq.clear()
    for n in (10, 20, 30, 40):
        dq.add_rear(n)
    flash("Sample deque loaded.", "success")
    return back()
 
@deque_bp.route('/deque/clear', methods=['POST'])
def dq_clear():
    dq.clear()
    flash("Deque cleared.", "success")
    return back()
 
 
# Your own experiments go here. This block does not run when app.py imports the file.
if __name__ == "__main__":
    d = Deque()
    d.add_rear(20)
    d.add_front(10)
    d.add_rear(30)
    print(d.to_list())          # [10, 20, 30]
    print(d.remove_rear())      # 30
    print(d.remove_front())     # 10
 