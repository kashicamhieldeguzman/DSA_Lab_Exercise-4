from flask import Blueprint, render_template, request, redirect, url_for, flash


def to_value(text):
    """Turn '10' into the number 10 and '2.5' into 2.5. Anything else stays text."""
    text = text.strip()
    try:
        return int(text)
    except ValueError:
        try:
            return float(text)
        except ValueError:
            return text

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
        """Return the data from top to bottom as a normal Python list."""
        items = []
        current = self.top
        while current:
            items.append(current.data)
            current = current.next
        return items

    def clear_stack(self):
        self.top = None

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

    @staticmethod
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
                ops.pop()
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

    @staticmethod
    def decimal_to_base(number, base):
        """Convert a whole decimal number to base 2 to 16 using a stack.
        Each remainder is pushed, then popped in reverse order to build the answer."""
        if number == 0:
            return "0"

        digits = "0123456789ABCDEF"
        sign = "-" if number < 0 else ""
        number = abs(number)

        remainders = Stack()
        while number > 0:
            remainders.push(digits[number % base])
            number //= base

        result = sign
        while remainders.peek() is not None:
            result += remainders.pop()
        return result

    @staticmethod
    def reverse_string(text):
        """Reverse a string using a stack: push every character, then pop them all."""
        letters = Stack()
        for char in text:
            letters.push(char)

        reversed_text = ""
        while letters.peek() is not None:
            reversed_text += letters.pop()
        return reversed_text


#                                               STACK ROUTES (blueprint)

stack_bp = Blueprint('stack', __name__)   # app.py registers this
st = Stack()                              # one shared stack, kept in memory while the server runs


@stack_bp.route('/stack')
def stack():
    return render_template('stack.html',
                           items=st.to_list()[::-1],
                           peeked=request.args.get('peeked'))

@stack_bp.route('/stack/push', methods=['POST'])
def st_push():
    value = to_value(request.form.get('value', ''))
    if value == '':
        flash("Type a value first.", "error")
    else:
        st.push(value)
        flash(f"Pushed {value} onto the stack", "success")
    return redirect(url_for('stack.stack'))

@stack_bp.route('/stack/pop', methods=['POST'])
def st_pop():
    popped_value = st.pop()
    if popped_value is not None:
        flash(f"Popped value: {popped_value}", "success")
    else:
        flash("Stack is empty.", "error")
    return redirect(url_for('stack.stack'))

@stack_bp.route('/stack/peek', methods=['POST'])
def st_peek():
    top_value = st.peek()
    if top_value is not None:
        flash(f"Top value: {top_value}", "success")
        return redirect(url_for('stack.stack', peeked=1))   
    flash("Stack is empty.", "error")
    return redirect(url_for('stack.stack'))

@stack_bp.route('/stack/sample', methods=['POST'])
def st_sample():
    st.clear_stack()
    for v in (10, 20, 30, 40):
        st.push(v)
    flash("Sample stack loaded.", "success")
    return redirect(url_for('stack.stack'))

@stack_bp.route('/stack/clear', methods=['POST'])
def st_clear():
    st.clear_stack()
    flash("Stack cleared.", "success")
    return redirect(url_for('stack.stack'))

@stack_bp.route('/stack/infix_to_postfix', methods=['POST'])
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
    return redirect(url_for('stack.stack'))

@stack_bp.route('/stack/convert', methods=['POST'])
def st_convert():
    text = request.form.get('number', '').strip()
    base = request.form.get('base', '')
    names = {'2': 'binary', '8': 'octal', '16': 'hexadecimal'}

    if text == '':
        flash("Type a whole number first.", "error")
    elif base not in names:
        flash("Pick a number system.", "error")
    elif len(text) > 18:
        flash("That number is too long. Use 18 digits or fewer.", "error")
    else:
        try:
            number = int(text)
        except ValueError:
            flash("Enter a whole number, like 25.", "error")
        else:
            result = Stack.decimal_to_base(number, int(base))
            flash(f"{number} in {names[base]} is {result}", "success")
    return redirect(url_for('stack.stack'))

@stack_bp.route('/stack/reverse', methods=['POST'])
def st_reverse():
    text = request.form.get('text', '').strip()
    if not text:
        flash("Type a string first.", "error")
    elif len(text) > 100:
        flash("That is too long. Use 100 characters or fewer.", "error")
    else:
        flash(f"Reversed: {Stack.reverse_string(text)}", "success")
    return redirect(url_for('stack.stack'))


if __name__ == "__main__":
    s = Stack()
    for value in (10, 20, 30):
        s.push(value)
    s.print_stack()
    print(Stack.infix_to_postfix("(A+B)*C"))  
    print(Stack.decimal_to_base(25, 2))        
    print(Stack.reverse_string("hello"))     