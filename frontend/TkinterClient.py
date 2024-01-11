import tkinter as tk
import time
import tkinter.font

from frontend.constants import FONT, WINDOW_TITLE, WINDOW_SIZE, JOINT_A_NAME, JOINT_B_NAME

# FONT = "Arial"


class TkinterClient:
    def __init__(self, root):
        self.root = root
        self.root.title(WINDOW_TITLE)
        self.root.geometry(WINDOW_SIZE)

        self.theta1 = tk.DoubleVar()
        self.theta2 = tk.DoubleVar()
        self.theta1.set(0)
        self.theta2.set(0)

        self.left_frame = self._create_frame(JOINT_A_NAME, self.theta1)
        self.right_frame = self._create_frame(JOINT_B_NAME, self.theta2)

    def update_display(self, theta_1: float, theta_2: float) -> None:
        """
        Function that takes in two floats to display for theta angle 1 and 2, respectively, updates the
        tkinter window with the new values.

        :param theta_1: Float representing the value to display for theta angle 1.
        :param theta_2: Float representing the value to display for theta angle 2.
        :return:        None.
        """
        self.theta1.set(round(theta_1, 2))
        self.theta2.set(round(theta_2, 2))
        self.root.update()

    def _create_frame(self, frame_text: str, theta: tk.DoubleVar) -> tk.Frame:
        """
        Crates a tk.Frame object that holds one of the joint angles.
        :param frame_text:  The text to display above the joint angle.
        :param theta:       The tk.DoubleVar that holds the joint angle we want for this frame.
        :return:
        """
        frame = tk.Frame(self.root)
        frame.pack(padx=1, pady=40, anchor=tk.CENTER)
        label = tk.Label(frame, text=frame_text, font=(FONT, 20))
        label.pack()
        label = tk.Label(frame, textvariable=theta, font=(FONT, 22))
        label.pack()
        return frame


if __name__ == '__main__':
    root = tk.Tk()
    app = TkinterClient(root)
    print(tkinter.font.families())
    t1 = 1.34728934792
    t2 = 2.8723489294237

    while True:
        time.sleep(0.5)
        app.update_display(t1, t2)
        t1 += 1.1231234
        t2 += 1.12839
