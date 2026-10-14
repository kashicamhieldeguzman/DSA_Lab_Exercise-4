from flask import Flask, render_template, request, redirect, url_for, flash

app = Flask(__name__)
app.secret_key = 'your_secret_key'


@app.route('/')
def index():
    return render_template('index.html')
@app.route('/home')
def home():
    return render_template('home.html')

@app.route('/profile')
def profile():
    return render_template('profile.html')

@app.route('/works')
def works():
    return render_template('works.html')

@app.route('/works/convert/touppercase', methods=['GET', 'POST'])
def touppercase():
    result = None
    if request.method == 'POST':
        input_string = request.form.get('inputString', '')
        result = input_string.upper()
    return render_template('touppercase.html', result=result)

@app.route('/works/area/circle', methods=['GET', 'POST'])
def circle():
    result = None
    if request.method == 'POST':
        radius = request.form.get('radius', '')
        result = int(radius)*3.14*int(radius)
    return render_template('circle.html', result=result)

@app.route('/works/area/triangle', methods=['GET', 'POST'])
def triangle():
    result = None
    if request.method == 'POST':
        base = request.form.get('base', '')
        height = request.form.get('height', '')
        result = 0.5 * int(base) * int(height)
    return render_template('triangle.html', result=result)

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
    
ll = LinkedList()

def to_value(text):
    text= text.strip() 
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text

def list_items():
    items, cur = [], ll.head
    while cur:
        items.append(cur.data)
        cur = cur.next
    return items

def back():
    return redirect(url_for('linkedlist'))

@app.route('/linkedlist')
def linkedlist():
    found = request.args.get("found")
    return render_template('linkedlist.html', items=list_items(), found=found)


@app.route("/ll/insert_beginning", methods=["POST"])
def ll_insert_beginning():
    value = to_value(request.form["value"])
    if value == "":
        flash("Type a value first.", "error")
    else:
        ll.insert_at_beginning(value)
        flash(f'Added "{value}" to the start.', "success")
    return back()


@app.route("/ll/insert_end", methods=["POST"])
def ll_insert_end():
    value = to_value(request.form["value"])
    if value == "":
        flash("Type a value first.", "error")
    else:
        ll.insert_at_end(value)
        flash(f'Added "{value}" to the end.', "success")
    return back()


@app.route("/ll/insert_after", methods=["POST"])
def ll_insert_after():
    value = to_value(request.form["value"])
    after = to_value(request.form["after"])
    if value == "" or after == "":
        flash("Type both values first.", "error")
    elif ll.insert_after(after, value) is None:
        flash(f'"{after}" is not in the list.', "error")
    else:
        flash(f'Inserted "{value}" after "{after}".', "success")
    return back()


@app.route("/ll/search", methods=["POST"])
def ll_search():
    value = to_value(request.form["value"])
    if value == "":
        flash("Type a value first.", "error")
    elif ll.search(value):
        flash(f'Found "{value}"!', "success")
        return redirect(url_for("linkedlist", found=value))
    else:
        flash(f'"{value}" is not in the list.', "error")
    return back()


@app.route("/ll/delete_first", methods=["POST"])
def ll_delete_first():
    removed = ll.remove_beginning()
    if removed is None:
        flash("The list is empty.", "error")
    else:
        flash(f'Deleted "{removed}" from the start.', "success")
    return back()


@app.route("/ll/delete_last", methods=["POST"])
def ll_delete_last():
    removed = ll.remove_at_end()
    if removed is None:
        flash("The list is empty.", "error")
    else:
        flash(f'Deleted "{removed}" from the end.', "success")
    return back()


@app.route("/ll/delete_value", methods=["POST"])
def ll_delete_value():
    value = to_value(request.form["value"])
    if value == "":
        flash("Type a value first.", "error")
    elif ll.remove_at(value) is None:
        flash(f'"{value}" is not in the list.', "error")
    else:
        flash(f'Deleted "{value}".', "success")
    return back()


@app.route("/ll/sample", methods=["POST"])
def ll_sample():
    ll.head = ll.tail = None
    for n in [10, 20, 30, 40, 50]:
        ll.insert_at_end(n)
    flash("Loaded sample list.", "success")
    return back()


@app.route("/ll/clear", methods=["POST"])
def ll_clear():
    ll.head = ll.tail = None
    flash("List cleared.", "success")
    return back()

#                                               STACK IMPLEMENTATION

class Node:
    def __init__(self, data):
        self.data = data
        self.next = None


class Stack:
    def __init__(self):
        self.top = None

    def push(self, data):
        new_node = Node(data)
        if self.top:
            new_node.next = self.top
        self.top = new_node


    def pop(self):
        if self.top is None:
            return None
        else:
            popped_node = self.top
            self.top = self.top.next
            popped_node.next = None
            return popped_node.data

    def peek(self):
        if self.top:
            return self.top.data
        else:
            return None

    def print_stack(self):
        if self.top is None:
            print("Stack is empty")
        else:
            current = self.top
            print("Stack elements (top → bottom):")
            while current:
                print(current.data)
                current = current.next

    def to_list(self):
        items = []
        current = self.top
        while current:
            items.append(current.data)
            current = current.next
        return items
    
    def clear_stack(self):
        self.top = []

    @staticmethod
    def precedence(op):
        if op == '^':
            return 3
        elif op == '*' or op == '/':
            return 2
        elif op == '+' or op == '-':
            return 1
        else:
            return -1

    @ staticmethod
    def infix_to_postfix(expression):
        ops = Stack()
        postfix = []
        for char in expression:
            if char.isspace():
                continue
            if char.isalnum():
                postfix.append(char)
            elif char == '(':
                ops.push(char)
            elif char == ')':
                while ops.peek() is not None and ops.peek() != '(':
                    postfix.append(ops.pop())
                if ops.peek() is None:
                    return None
                ops.pop  # Remove '(' from stack
            else:  # Operator
                if Stack.precedence(char) == -1:
                    return None
                while (ops.peek() is not None and
                       (Stack.precedence(ops.peek()) >= Stack.precedence(char) and char != '^')):
                    postfix.append(ops.pop())
                ops.push(char)

        while ops.peek() is not None:
            op = ops.pop()
            if op == '(':
                return None
            postfix.append(op)

        return ''.join(postfix)
st = Stack()

@app.route('/stack')
def stack():
    return render_template('stack.html', items=st.to_list()[::-1])

@app.route('/stack/push', methods=['POST'])
def st_push():
    value = to_value(request.form.get('value', ''))
    if value == '':
        flash("Type a value first.", "error")
    else:
        st.push(value)
        flash(f"Pushed {value} onto the stack", "success")
    return redirect(url_for('stack'))

@app.route('/stack/pop', methods=['POST'])
def st_pop():
    popped_value = st.pop()
    if popped_value is not None:
        flash(f"Popped value: {popped_value}", "success")
    else:
        flash("Stack is empty.", "error")
    return redirect(url_for('stack'))

@app.route('/stack/peek', methods=['POST'])
def st_peek():
    top_value = st.peek()
    if top_value is not None:
        flash(f"Top value: {top_value}", "success")
    else:
        flash("Stack is empty.", "error")
    return redirect(url_for('stack'))

@app.route('/stack/sample', methods=['POST'])
def st_sample():
    st.clear_stack()
    for v in (10, 20, 30, 40):
        st.push(v)
    flash("Sample stack loaded.", "success")
    return redirect(url_for('stack'))
    
@app.route('/stack/clear', methods=['POST'])
def st_clear():
    st.clear_stack()
    flash("Stack cleared.", "success")
    return redirect(url_for('stack'))

@app.route('/stack/infix_to_postfix', methods=['POST'])
def st_infix_to_postfix():
    expression = request.form.get('expression', '').strip()
    if not expression:
        flash("Please enter an infix expression.", "error")
    else:
        postfix = Stack.infix_to_postfix(expression)
        if postfix is None:
            flash("Invalid expression. Check your parentheses and symbols.", "error")
        else:
            flash(f"Postfix: {postfix}", "success")
    return redirect(url_for('stack'))

# @app.route('/areaOfcirle', methods=['GET', 'POST'])
# def areaOfcirle():
#     result = None
#     name=request.get('name','')
#     print(name)
#     if request.method == 'POST':
#         input_string = request.form.get('inputradius', '')
#         result = int(input_string) * int(input_string) * 3.14
#     return render_template('areaCircle.html', result=result)

@app.route('/contact')
def contact():
    return render_template('contact.html')

if __name__ == "__main__":
    app.run(debug=True)
