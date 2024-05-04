"""
Troy Husted
May 29, 2024
----------------
Description:
    A simple example to demonstrate how to create threads

    Example use:
        python3 MultiThreadExample.py
"""

import threading


# -------------------------------------------------------------
#  Define a simple add function
# -------------------------------------------------------------
def add(num1, num2):
    print("Add function: ", num1 + num2)


# -------------------------------------------------------------
#  Define a simple multiply function
# -------------------------------------------------------------
def multiply(num1, num2):
    print("Multiply function: ", num1 * num2)


if __name__ == "__main__":
    # -------------------------------------------------------------
    # Initialize add and mulyiply threads (note how the arguments are passed)
    # -------------------------------------------------------------
    thread_1 = threading.Thread(target=add, args=(10, 5))
    thread_2 = threading.Thread(target=multiply, args=(10, 5))

    # -------------------------------------------------------------
    # Start Threads
    # -------------------------------------------------------------
    thread_1.start()
    thread_2.start()

    # -------------------------------------------------------------
    # Join threads - this ensures all threads are given time to finish
    # -------------------------------------------------------------
    thread_1.join()
    thread_2.join()

    print("All threads finished.\n")
