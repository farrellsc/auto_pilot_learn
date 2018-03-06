# zAutoPilot
A toy project for udacity robotics course https://classroom.udacity.com/courses/cs373  
Includes a basic set of tools for robotics on localization, route finding, control, and map building.

# Installation
`python setup.py install`

# How to run
To run a module use `python -m zautopilot <command>`
For detailed usage introduction see `zautopilot.example (TO BE ADDED)`

# Contents
Module|Functionality|Class
:--:|:--:|:--:
zautopilot.commands|functionality for command line interface|-
zautopilot.robot|robot instances|vehicle
zautopilot.data|data processing module and gardgets|-
zautopilot.localization|a collection of localization algorithms|Kalman Filter, Particle Filter, Histogram Filter
zautopilot.search|a collection of route searching/optimizing algorithms|A*, Dynamic Programming, Smoothing
zautopilot.control|a collection of control algorithms|PID
zautopilot.mapping|a collection of map building algorithms|SLAM
