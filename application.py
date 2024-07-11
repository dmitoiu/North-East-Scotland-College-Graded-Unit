#-------------------------------------------------------------------------------
# Darie-Dragos Mitoiu
# Application v1.0.0 15/02/2019
# An application module designed for a tailoring and alterations business
#-------------------------------------------------------------------------------


# Importing Libraries
import wx
from loginwindow import LogInWindow


class Application(wx.App):
    """This class will allow the creation of the main window object."""

    def OnInit(self):
        """This method will run as soon as the object is created."""

        # Creating the main frame (window) and setting it to be on top
        self.frame = LogInWindow(None, title="pyTailor++", size=(800,350))
        self.SetTopWindow(self.frame)
        self.frame.Show()

        return True


