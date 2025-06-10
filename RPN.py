def convertToRPN(expression):
    n = []
    for item in expression:
        n.append(item)

    precedence = {"+": 1,
                  "-": 1,
                  "*": 2,
                  "/": 2,
                  "^": 3}

    queue = []
    stack = []

    for value in n:
        if value == '(':
            stack.insert(0, value)

        elif value == ')':
            found = False
            while not found:
                if stack[0] == '(':
                    found = True
                else:
                    queue.append(stack[0])
                    stack.pop(0)

            stack.pop(0)

        elif value not in precedence:
            queue.append(value)

        elif value in precedence:
            if len(stack) > 0:
                if precedence[stack[0]] >= precedence[value]:
                    queue.append(stack[0])
                    stack.pop(0)
                    stack.insert(0, value)
                else:
                    stack.insert(0, value)
            else:
                stack.append(value)

    while len(stack) > 0:
        queue.append(stack[0])
        stack.pop(0)

    return " ".join(queue)


infix = input("Enter an expression: ")
print(convertToRPN(infix))
