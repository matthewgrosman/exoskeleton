# Exoskeleton Software

## Original Research
This project builds off of an existing research project, below are the relevant links to the original material:
* [Research paper](https://cctomm.ca/2023/CCToMM_M3_Symposium_paper_13.pdf)
* [Original MATLAB code](https://drive.google.com/drive/folders/18XZ3T8iQ1MzVMngPpcYfKfxNLCJTCkb_)


## Overview
This project is the software component for a variation of the exoskeleton designed in [this research paper](https://cctomm.ca/2023/CCToMM_M3_Symposium_paper_13.pdf). A friend of mine who worked on the research paper was working on some designs for a variation of the exoskeleton here, and asked me if I wanted to help out with writing some of the software components. 

In short, this exoskeleton attaches to someones shoulder to get some data about their arm movement. The way this exoskeleton picks up data is though a few sensors on the frame that are connected to an Arduino device. The goal of this project is to create a way to get this sensor data from the Arduino, run some calculations on it to find relevent metrics for doctors to view, and then display these metrics in a simple way.


## How does it work?
First we need some data. There's some script running on the Arduino device that tells it to send us it's sensor data over serial port. We use a Python serial library to read this data on our local computer. The Arduino is actually getting a ton of data from the sensors, much more than our program can handle without crashing. To get around this, we sample data at a constant rate at an interval we can safely process. Currently, we have our sampling rate at 0.25 to refresh the metric displayed four times each second- a level that is easy to handle for our program and is not an overwhelming amount of data for the user to interpret.

Once we get sensor data, we run a series of calculations on it to calculate relevant metrics for users of the program to see. These calculations are translated into Python from [the MATLAB code used in the orignal research project]((https://drive.google.com/drive/folders/18XZ3T8iQ1MzVMngPpcYfKfxNLCJTCkb_)). I decided to re-write this in Python using Numpy as it made the project easier to package as an executable application. MATLAB requires licensing for use, and trying to configure it to be packaged was really annoying when I tried to do it. Just having the logic in Python and cutting the depepdency was much easier to run and distribute.

Lastly, after we have finished our metric calculations, we update a simple Tkinter GUI application to display the new metric valuse (for reference, we are just displaying two values currently). This GUI runs when the user opens the program, and refreshes every 0.25 seconds with new metrics.

## What's next?
I passed this along to another researcher who worked on the project to check out/use if it ended up being helpful.