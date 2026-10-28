from flask import Blueprint, render_template, request, redirect, url_for, flash
from stack import to_value

#                                        QUEUE IMPLEMENTATION
class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Queue:
    def __init__(self):
        self.front = None
        self.rear = None
        self.size = 0

    def is_empty(self):
        return self.front is None

    def enqueue(self, item):
        new_node = Node(item)

        if self.rear is None:
            self.front = self.rear = new_node
        else:
            self.rear.next =  new_node
            self.rear = new_node
        self.size += 1

    def dequeue(self):
        if self.is_empty():
            raise Exception("Queue is empty, cannot dequeu")

        dequeued_node = self.front
        self.front = dequeued_node.next
        
        if self. front is None:
            self.rear = None

        self.size -= 1
        return dequeued_node.data

    def peek(self):
        if self.is_empty():
            raise Exception("Peek from empty queue")
    
        return self.front.data

    def to_list(self):
        """Return the data from front to rear as a normal Python list."""
        items = []
        current = self.front
        while current:
            items.append(current.data)
            current = current.next
        return items
 
    def clear(self):
        self.front = None
        self.rear = None
        self.size = 0
 
    def __len__(self):
        return self.size
 
 
#                                        QUEUE ROUTES (blueprint)
 
queue_bp = Blueprint('queue', __name__)   # app.py registers this
qq = Queue()                              # one shared queue, kept in memory while the server runs
 
 
def back():
    return redirect(url_for('queue.queue'))
 
 
@queue_bp.route('/queue')
def queue():
    return render_template('queue.html',
                           items=qq.to_list(),
                           peeked=request.args.get('peeked'))
 
@queue_bp.route('/queue/enqueue', methods=['POST'])
def qq_enqueue():
    value = to_value(request.form.get('value', ''))
    if value == '':
        flash("Type a value first.", "error")
    else:
        qq.enqueue(value)
        flash(f'Enqueued "{value}" at the rear.', "success")
    return back()
 
@queue_bp.route('/queue/dequeue', methods=['POST'])
def qq_dequeue():
    if qq.is_empty():
        flash("The queue is empty.", "error")
    else:
        flash(f'Dequeued "{qq.dequeue()}" from the front.', "success")
    return back()
 
@queue_bp.route('/queue/peek', methods=['POST'])
def qq_peek():
    if qq.is_empty():
        flash("The queue is empty.", "error")
        return back()
    flash(f'Front value: {qq.peek()}', "success")
    return redirect(url_for('queue.queue', peeked=1))   # highlights the front node
 
@queue_bp.route('/queue/sample', methods=['POST'])
def qq_sample():
    qq.clear()
    for n in (10, 20, 30, 40):
        qq.enqueue(n)
    flash("Sample queue loaded.", "success")
    return back()
 
@queue_bp.route('/queue/clear', methods=['POST'])
def qq_clear():
    qq.clear()
    flash("Queue cleared.", "success")
    return back()
 
 
# Your own experiments go here. This block does not run when app.py imports the file.
if __name__ == "__main__":
    q = Queue()
    for value in (10, 20, 30):
        q.enqueue(value)
    print(q.to_list())      # [10, 20, 30]
    print(q.dequeue())      # 10
    print(q.peek())         # 20
 