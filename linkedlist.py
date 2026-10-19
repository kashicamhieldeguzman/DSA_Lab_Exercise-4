from flask import Blueprint, render_template, request, redirect, url_for, flash
from stack import to_value

#                                       LINKED LIST IMPLEMENTATION

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None

    def insert_at_beginning(self, data):
        new_node = Node(data)
        if self.head:
            new_node.next = self.head
            self.head = new_node
        else:
            self.head = new_node
            self.tail = new_node

    def insert_at_end(self, data):
        new_node = Node(data)
        if self.head:
            self.tail.next = new_node
            self.tail = new_node
        else:
            self.tail = new_node
            self.head = new_node

    def search(self, data):
        current_node = self.head
        while current_node:
            if current_node.data == data:
                return True
            current_node = current_node.next
        return False

    def printLinkedList(self):
        current_node = self.head
        while current_node:
            print(current_node.data)
            current_node = current_node.next

    def remove_beginning(self):
        if not self.head:
            return None

        removed_data = self.head.data
        self.head = self.head.next
        if self.head is None:
            self.tail = None

        return removed_data

    def remove_at_end(self):
        if not self.head:
            return None

        if self.head == self.tail:
            removed_data = self.head.data
            self.head = None
            self.tail = None
            return removed_data

        current = self.head
        while current.next != self.tail:
            current = current.next

        removed_data = self.tail.data
        self.tail = current
        self.tail.next = None

        return removed_data

    def remove_at(self, data):
        if not self.head:
            return None

        if self.head.data == data:
            removed_data = self.head.data
            self.head = self.head.next

            if self.head is None:
                self.tail = None
            return removed_data

        current_node = self.head
        while current_node.next:
            if current_node.next.data == data:
                removed_data = current_node.next.data
                current_node.next = current_node.next.next
                if current_node.next is None:
                    self.tail = current_node
                return removed_data
            current_node = current_node.next
        return None

    def insert_after(self, nodedata, data):
        if not self.head:
            return None

        current_node = self.head
        while current_node:
            if current_node.data == nodedata:
                new_node = Node(data)
                new_node.next = current_node.next
                current_node.next = new_node

                if current_node == self.tail:
                    self.tail = new_node
                return data
            current_node = current_node.next
        return None

    def to_list(self):
        """Return the data from head to tail as a normal Python list."""
        items = []
        current = self.head
        while current:
            items.append(current.data)
            current = current.next
        return items

    def clear_list(self):
        self.head = None
        self.tail = None
#                                       LINKED LIST ROUTES (blueprint)
 
linkedlist_bp = Blueprint('linkedlist', __name__)   # app.py registers this
ll = LinkedList()                                   # one shared list, kept in memory while the server runs
 
 
def back():
    return redirect(url_for('linkedlist.linkedlist'))
 
 
@linkedlist_bp.route('/linkedlist')
def linkedlist():
    found = request.args.get("found")
    return render_template('linkedlist.html', items=ll.to_list(), found=found)
 
@linkedlist_bp.route("/ll/insert_beginning", methods=["POST"])
def ll_insert_beginning():
    value = to_value(request.form.get("value", ""))
    if value == "":
        flash("Type a value first.", "error")
    else:
        ll.insert_at_beginning(value)
        flash(f'Added "{value}" to the start.', "success")
    return back()
 
@linkedlist_bp.route("/ll/insert_end", methods=["POST"])
def ll_insert_end():
    value = to_value(request.form.get("value", ""))
    if value == "":
        flash("Type a value first.", "error")
    else:
        ll.insert_at_end(value)
        flash(f'Added "{value}" to the end.', "success")
    return back()
 
@linkedlist_bp.route("/ll/insert_after", methods=["POST"])
def ll_insert_after():
    value = to_value(request.form.get("value", ""))
    after = to_value(request.form.get("after", ""))
    if value == "" or after == "":
        flash("Type both values first.", "error")
    elif ll.insert_after(after, value) is None:
        flash(f'"{after}" is not in the list.', "error")
    else:
        flash(f'Inserted "{value}" after "{after}".', "success")
    return back()
 
@linkedlist_bp.route("/ll/search", methods=["POST"])
def ll_search():
    value = to_value(request.form.get("value", ""))
    if value == "":
        flash("Type a value first.", "error")
    elif ll.search(value):
        flash(f'Found "{value}"!', "success")
        return redirect(url_for("linkedlist.linkedlist", found=value))
    else:
        flash(f'"{value}" is not in the list.', "error")
    return back()
 
@linkedlist_bp.route("/ll/delete_first", methods=["POST"])
def ll_delete_first():
    removed = ll.remove_beginning()
    if removed is None:
        flash("The list is empty.", "error")
    else:
        flash(f'Deleted "{removed}" from the start.', "success")
    return back()
 
@linkedlist_bp.route("/ll/delete_last", methods=["POST"])
def ll_delete_last():
    removed = ll.remove_at_end()
    if removed is None:
        flash("The list is empty.", "error")
    else:
        flash(f'Deleted "{removed}" from the end.', "success")
    return back()
 
@linkedlist_bp.route("/ll/delete_value", methods=["POST"])
def ll_delete_value():
    value = to_value(request.form.get("value", ""))
    if value == "":
        flash("Type a value first.", "error")
    elif ll.remove_at(value) is None:
        flash(f'"{value}" is not in the list.', "error")
    else:
        flash(f'Deleted "{value}".', "success")
    return back()
 
@linkedlist_bp.route("/ll/sample", methods=["POST"])
def ll_sample():
    ll.clear_list()
    for n in [10, 20, 30, 40, 50]:
        ll.insert_at_end(n)
    flash("Loaded sample list.", "success")
    return back()
 
@linkedlist_bp.route("/ll/clear", methods=["POST"])
def ll_clear():
    ll.clear_list()
    flash("List cleared.", "success")
    return back()
 
 

if __name__ == "__main__":
    test = LinkedList()
    for value in [10, 20, 30]:
        test.insert_at_end(value)
    test.printLinkedList()                                        
