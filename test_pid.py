#!/usr/bin/python
#
# This file is part of IvPID.
# Copyright (C) 2015 Ivmech Mechatronics Ltd. <bilgi@ivmech.com>
#
# IvPID is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# IvPID is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

#title           :test_pid.py
#description     :python pid controller test
#author          :Caner Durmusoglu
#date            :20151218
#version         :0.1
#notes           :
#python_version  :2.7
#dependencies    : matplotlib, numpy, scipy
#==============================================================================

import PID
import time
import matplotlib.pyplot as plt
import numpy as np
from scipy.interpolate import spline

def test_pid(P = 0.2,  I = 0.0, D= 0.0, L=100):
    """Self-test PID class

    .. note::
        ...
        for i in range(1, END):
            pid.update(feedback)
            output = pid.output
            if pid.SetPoint > 0:
                feedback += (output - (1/i))
            if i>9:
                pid.SetPoint = 1
            time.sleep(0.02)
        ---
    """
    pid = PID.PID(P, I, D)

    pid.SetPoint=0.0
    pid.setSampleTime(0.01)

    END = L
    feedback = 0

    output_list = []
    feedback_list = []
    time_list = []
    setpoint_list = []

    for i in range(1, END):
        pid.update(feedback)
        output = pid.output
        if pid.SetPoint != 0:
            feedback += (output - (1/i))
            #feedback = output
        if 9<i<50:
            pid.SetPoint = 60
        elif 49<i<90:
            pid.SetPoint = -60
        elif 89<i<130:
            pid.SetPoint = 60
        elif 129<i<170:
            pid.SetPoint = -60
        time.sleep(0.02)

        output_list.append(output)
        feedback_list.append(feedback)
        setpoint_list.append(pid.SetPoint)
        time_list.append(i)

    time_sm = np.array(time_list)
    time_smooth = np.linspace(time_sm.min(), time_sm.max(), 300)
    feedback_smooth = spline(time_list, feedback_list, time_smooth)
    output_smooth = spline(time_list, output_list, time_smooth)

    fig = plt.figure(figsize=(5,5))
    ax = fig.add_subplot(111)
    Heading_Angle, = ax.plot(time_smooth, feedback_smooth, label='Heading Angle')
    Set_Angle, = ax.plot(time_list, setpoint_list, label='Set Angle')
    Rudder_Angle, = ax.plot(time_smooth, output_smooth, label='Rudder Angle')
    ax.legend(handles=[Heading_Angle, Set_Angle, Rudder_Angle], loc='upper right')
##    plt.plot(time_smooth, feedback_smooth)
##    plt.plot(time_list, setpoint_list)
##    plt.plot(time_smooth, output_smooth)
    plt.xlim((0, L))
    plt.ylim((min(output_smooth)-5, max(output_smooth)+5))
    plt.xlabel('time (0.1s)')
    plt.ylabel('Angle (°)')
    plt.title('Turning')

##    fig = plt.figure(figsize=(5,5))
##    ax = fig.add_subplot(111)
##    Rudder_Angle, = ax.plot(time_smooth, output_smooth, color='green', label='Rudder Angle')
##    ax.legend(handles=[Rudder_Angle], loc='lower right')

    plt.ylim((-70, 70))

    plt.grid(True)
    plt.show()

if __name__ == "__main__":
    test_pid(0.2, 0.1, 0, L=170)
#    test_pid(1.2, 1, 0.001, L=170)

