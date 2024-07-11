#-------------------------------------------------------------------------------
# Darie-Dragos Mitoiu
# LogInWindow v1.0.0 15/02/2019
# A log in window module designed for a tailoring and alterations business
#-------------------------------------------------------------------------------


# Importing libraries
import wx
import os
from signupwindow import SignUpWindow
from sysop import SysOp
from administrator import Administrator
from owner import Owner
from database import Database


class LogInWindow(wx.Frame):
    """This class will allow the creation of the log in window object."""

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        # Create sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)
        # Ignore warnings from wxpython
        self.logging = wx.LogNull()
        # Create main panel
        self.main_panel = LogInPanel(self)
        # Adding widgets to the sizers
        self.h_sizer.Add(self.main_panel, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer, 1, wx.EXPAND)
        # Setting sizer
        self.SetSizer(self.v_sizer)
        # Center window
        self.Center()

class LogInPanel(wx.Panel):
    """This class allows the creation of the main panel."""

    def __init__(self, master, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.build()

    def build(self):
        """This method allows the creation of widgets."""

        # Declaring sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Load and set window icon
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.master.SetIcon(self.icon)

        # Creating panels
        self.left_panel = LeftPanel(self, size=(-1,300), style=wx.SIMPLE_BORDER)
        self.right_panel = RightPanel(self, self.master, style=wx.SIMPLE_BORDER)

        # Adding widgets to the sizers
        self.h_sizer.Add(self.left_panel, 0, wx.EXPAND)
        self.h_sizer.Add(self.right_panel, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer, 1, wx.EXPAND)

        # Setting sizer
        self.SetSizer(self.v_sizer)

class LeftPanel(wx.Panel):
    """This class allows the creation of the left panel object. """

    def __init__(self, master, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.build()

    def build(self):
        """This method allows the creation of the widgets."""

        # Declaring sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Loading and setting the logo
        self.logo = wx.Bitmap("images/logo_small.png", wx.BITMAP_TYPE_PNG)
        self.app_label = wx.StaticBitmap(self, -1, self.logo)

        # Adding the widgets to sizers
        self.h_sizer.Add(self.app_label, 1, wx.ALIGN_CENTER)
        self.v_sizer.Add(self.h_sizer, 1)

        # Setting sizer
        self.SetSizer(self.v_sizer)

class RightPanel(wx.Panel):
    """This class allows the creation of the right panel object."""

    # Declaring class variables
    current_dir = os.getcwd()

    def __init__(self, master, controller, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Creating database object
        self.database = Database((RightPanel.current_dir +
                                  "/database/business.accdb"),
                                  "admin", "pyTailor++")
        self.build()

    def build(self):
        """This method allows the creation of the widgets."""

        # Declaring sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4 = wx.BoxSizer(wx.HORIZONTAL)

        # Declaring labels, entries and buttons
        self.log_in_label = wx.StaticText(self, label="LogIn")
        self.username_label = wx.StaticText(self, label="Username:",
                                            size=(60, -1))
        self.username_entry = wx.TextCtrl(self, size=(200, -1))
        self.password_label = wx.StaticText(self, label="Password:",
                                            size=(60, -1))
        self.password_entry = wx.TextCtrl(self, size=(200, -1),
                                          style=wx.TE_PASSWORD)
        self.log_in_button = wx.Button(self, label="LogIn")
        # Binding the log in method to the log in button
        self.log_in_button.Bind(wx.EVT_BUTTON, self.on_button_log_in)
        # Binding the log in method on the enter key
        self.Bind(wx.EVT_CHAR_HOOK, self.OnKey)
        self.sign_up_button = wx.Button(self, label="SignUp")
        # Binding the sing up method to the sign up button
        self.sign_up_button.Bind(wx.EVT_BUTTON, self.on_button_sign_up)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.log_in_label, 0, wx.ALL, 5)
        self.h_sizer2.Add(self.username_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer2.Add(self.username_entry, 1, wx.ALL|wx.EXPAND, 5)
        self.h_sizer3.Add(self.password_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer3.Add(self.password_entry, 1, wx.ALL|wx.EXPAND, 5)
        self.h_sizer4.Add(self.sign_up_button, 0, wx.ALL, 5)
        self.h_sizer4.Add(self.log_in_button, 0, wx.ALL, 5)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALL, 5)
        self.v_sizer.Add(self.h_sizer2, 0, wx.ALL|wx.EXPAND, 2)
        self.v_sizer.Add(self.h_sizer3, 0, wx.ALL|wx.EXPAND, 2)
        self.v_sizer.AddSpacer(25)
        self.v_sizer.Add(self.h_sizer4, 0, wx.ALL|wx.ALIGN_RIGHT, 5)

        # Setting sizer
        self.SetSizer(self.v_sizer)

    def on_button_sign_up(self, event):
        """This method will allow the creation of the sign up window object."""

        # Creating sign up window and showing it
        sign_up_window = SignUpWindow(None, title="Sign Up", size=(-1, 500))
        sign_up_window.Show()

    def on_button_log_in(self, event):
        """This method will allow the user to log in."""

        # Getting user input
        username = self.username_entry.GetValue()
        password = self.password_entry.GetValue()

        # If username and password not empty
        if username and password:
            # Search user in database
            user = self.database.get_user(username)
            if user:
                # If user found get user's password
                db_password = user[0][2]

                # If passwords match
                if password == db_password:
                    # Get user's permission level
                    db_permission_level = user[0][3]

                    # If permission level is 0 open System Operator Interface
                    if db_permission_level == 0:
                        # Close log in window
                        self.controller.Close()
                        # Create system operator interface and show it
                        system_operator = SysOp(None,
                                                username,
                                                title="pyTailor++",
                                                size=(1600, 720))
                        system_operator.Show()

                    # If permission level is 1 open Administrator Interface
                    if db_permission_level == 1:
                        # Close log in window
                        self.controller.Close()
                        # Create administrator interface and show it
                        administrator = Administrator(None,
                                                      username,
                                                      title="pyTailor++",
                                                      size=(1600, 720))
                        administrator.Show()

                    # If permission level is 2 open Owner Interface
                    if db_permission_level == 2:
                        # Close log in window
                        self.controller.Close()
                        # Create owner interface and show it
                        owner = Owner(None,
                                      username,
                                      title="pyTailor++",
                                      size=(1600, 720))
                        owner.Show()
                else:
                    # If password invalid show message
                    message = wx.MessageBox("Invalid password.",
                                            "Log In",
                                            style=wx.OK|wx.ICON_WARNING)
            else:
                # If username invalid show message
                message = wx.MessageBox("Invalid username.",
                                        "Log In",
                                        style=wx.OK|wx.ICON_WARNING)
        else:
            # If user input empty show message
            message = wx.MessageBox("All fields are required.",
                                    "Log In",
                                    style=wx.OK|wx.ICON_WARNING)

    def OnKey(self, event):
        """This method allows the user to log in using the enter key."""

        # If the key pressed is enter log in
        if event.GetKeyCode() == wx.WXK_RETURN:
            self.on_button_log_in(event)
        else:
            # Skip event
            event.Skip()


