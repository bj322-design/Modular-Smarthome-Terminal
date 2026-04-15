# widget.py
# Provides the framework for the widget class that people will implement in order to create a plugin
# A widget is an abstract class that creators will implement a subclass from in order to create their widget

from abc import ABC, abstractmethod

class Widget(ABC):
    # Widget Name - The human readable name of the widget
    @property
    @abstractmethod
    def widgetName(self):
        pass

    # Widget ID - A hard coded string that uniquely identifies the widget
    @property
    @abstractmethod
    def widgetID(self):
        pass

    # Widget HTML - HTML data that describes how to display the widget
    @property
    @abstractmethod
    def widgetHTML(self):
        pass

    # Widget Data - JSON that has any data the widget needs to store
    @property
    @abstractmethod
    def widgetData(self):
        pass

    # Widget Preferences - Any important preference variables defined for the widget
    @property
    @abstractmethod
    def widgetPreferences(self):
        pass

    # Widget Default Preferences - Loaded to the widget's preferences by default
    @property
    @abstractmethod
    def widgetDefaultPreferences(self):
        pass

    # Update Timer - Define how often (In milliseconds) this widget should update
    @property
    @abstractmethod
    def updateTimer(self):
        pass

    # Update() - Function to be run each time the widget needs to update
    @abstractmethod
    def update(self):
        pass

    # Handle Event() - Function that handles any events that the widget might need to handle for the sake of interactivity
    @abstractmethod
    def handle_event(self, event, args):
        pass