import tkinter as tk


class GUIClient:
    def __init__(self, root):
        self.root = root
        self.root.title("Exoskeleton")

        self.theta1 = tk.IntVar()
        self.theta1.set(0)
        self.theta2 = tk.IntVar()
        self.theta2.set(0)

        # Create left column
        self.left_frame = tk.Frame(self.root)
        self.left_frame.pack(side=tk.LEFT, padx=10)
        self.label_theta1 = tk.Label(self.left_frame, text="new theta 1", font=("Helvetica", 12))
        self.label_theta1.pack()
        self.label_number1 = tk.Label(self.left_frame, textvariable=self.theta1, font=("Helvetica", 18))
        self.label_number1.pack()

        # Create right column
        self.right_frame = tk.Frame(self.root)
        self.right_frame.pack(side=tk.RIGHT, padx=10)
        self.label_theta2 = tk.Label(self.right_frame, text="new theta 2", font=("Helvetica", 12))
        self.label_theta2.pack()
        self.label_number2 = tk.Label(self.right_frame, textvariable=self.theta2, font=("Helvetica", 18))
        self.label_number2.pack()

    def update_display(self, theta_1, theta_2):
        self.theta1.set(theta_1)
        self.theta2.set(theta_2)
