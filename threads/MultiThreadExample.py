import threading


def add(num1, num2):
    print("Add function: ", num1 + num2)


def multiply(num1, num2):
    print("Multiply function: ", num1 * num2)


if __name__ == "__main__":
    thread_1 = threading.Thread(target=add, args=(10, 5))
    thread_2 = threading.Thread(target=multiply, args=(10, 5))

    thread_1.start()
    thread_2.start()

    thread_1.join()
    thread_2.join()

    print("All threads finished.\n")
