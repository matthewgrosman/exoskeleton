import matlab.engine


class MatlabClient:
    MATLAB_SCRIPT_PATH = "ml/scripts"

    def __init__(self):
        self.engine = matlab.engine.start_matlab()
        self.engine.cd(self.MATLAB_SCRIPT_PATH, nargout=0)
        # self.engine.getEndEffectorFunction()

    def compute_angles(self, angle1: float, angle2: float, angle3: float) -> (float, float):
        # Build the MATLAB command string with parameters
        print("hi")
        command = f"result[theta1, theta2] = getEndEffectorFunction({angle1}, {angle2}, {angle3});"
        print(command)
        # Call the MATLAB function with parameters and capture the output
        #result = self.engine.eval(command, nargout=1)  # Set nargout to 1 to indicate you expect one output

        res = self.engine.feval("getEndEffectorFunction", angle1, angle2, angle3, nargout=2)

        print("hisdfsdfsd")
        # Retrieve the result from MATLAB
        # result1 = self.engine.workspace['theta1']
        # result2 = self.engine.workspace['theta2']

        # Close the MATLAB session
        self.engine.quit()

        # Use the result in Python
        print("Result from MATLAB:", result[0], result[1])
