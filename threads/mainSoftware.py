import threading
from motorPIDSoftware import MotorSimulation
from tensioningSoftware import TensionValueGrabSoftware


if __name__ == "__main__":
    try:
        # -------------------------------------------------------------
        # Initialize Motor Simulation Thread
        # -------------------------------------------------------------
        thread_1 = threading.Thread(
            target=MotorSimulation, args=(2, 3, 30, 0.6, 0.0, 0.0)
        )

        # -------------------------------------------------------------
        # Initialize Magnetic Brake Simulation Thread
        # -------------------------------------------------------------
        thread_2 = threading.Thread(target=TensionValueGrabSoftware, args=(3, 9.5, 10))

        thread_1.daemon = True
        thread_2.daemon = True

        # -------------------------------------------------------------
        # Start Threads
        # -------------------------------------------------------------

        thread_1.start()
        thread_2.start()

        # -------------------------------------------------------------
        # Join threads (good practice even though these are infinite loops)
        # -------------------------------------------------------------

        thread_1.join()
        thread_2.join()

    except KeyboardInterrupt:
        print("Stopped")
        thread_1._stop()
        thread_2._stop()
