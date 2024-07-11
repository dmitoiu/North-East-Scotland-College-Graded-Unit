#-------------------------------------------------------------------------------
# Darie-Dragos Mitoiu
# SignUpWindow v1.0.0 15/02/2019
# A sign up window module designed for a tailoring and alterations business
#-------------------------------------------------------------------------------


# Importing libraries
import wx
import os
from database import Database


class SignUpWindow(wx.Frame):
    """This class allows the creation of the sign up window object."""

    # Declaring class variables
    current_dir = os.getcwd()

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        # Ignore warnings from wxpython
        self.logging = wx.LogNull()
        # Create main panel
        self.main_panel = wx.Panel(self)
        # Create database object
        self.database = Database((SignUpWindow.current_dir +
                                  "/database/business.accdb"),
                                  "admin", "pyTailor++")
        # Build widgets
        self.build()
        # Center window
        self.Center()

    def build(self):
        """This method will allow the creation of the window widgets."""

        # Declaring sizers
        # A sizer is an object that will allow the placement
        # of the other objects in a panel (container)
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer8 = wx.BoxSizer(wx.HORIZONTAL)

        # Load and set window icon
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.SetIcon(self.icon)

        # Declaring labels
        self.sign_up_label = wx.StaticText(self.main_panel, label="Sign Up")
        self.username_label = wx.StaticText(self.main_panel,
                                            size=(100, -1),
                                            label="Username:")

        self.password_label = wx.StaticText(self.main_panel,
                                            size=(100, -1),
                                            label="Password:")

        self.verify_password_label = wx.StaticText(self.main_panel,
                                                   size=(100, -1),
                                                   label="Repeat Password:")

        self.permission_level_label = wx.StaticText(self.main_panel,
                                                    size=(100, -1),
                                                    label="Permission Level:")

        self.security_code_label = wx.StaticText(self.main_panel,
                                                 size=(100, -1),
                                                 label="Security Code:")

        self.email_label = wx.StaticText(self.main_panel,
                                         size=(100, -1),
                                         label="Email:")

        # Declaring entries
        self.username_entry = wx.TextCtrl(self.main_panel)
        self.password_entry = wx.TextCtrl(self.main_panel, style=wx.TE_PASSWORD)
        self.verify_password_entry = wx.TextCtrl(self.main_panel,
                                                 style=wx.TE_PASSWORD)
        self.permission_level_choices = wx.Choice(self.main_panel,
                                                  choices=["1-System Operator",
                                                           "2-Administrator",
                                                           "3-Owner"])
        self.security_code_entry = wx.TextCtrl(self.main_panel,
                                               style=wx.TE_PASSWORD)

        self.email_entry = wx.TextCtrl(self.main_panel)

        self.cancel_button = wx.Button(self.main_panel, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_button_cancel_sign_up)
        self.sign_up_button = wx.Button(self.main_panel, label="Sign Up")
        self.sign_up_button.Bind(wx.EVT_BUTTON, self.on_button_sign_up)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.sign_up_label, 0, wx.ALL, 5)
        self.h_sizer2.Add(self.username_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer2.Add(self.username_entry, 1, wx.ALL, 5)
        self.h_sizer3.Add(self.password_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer3.Add(self.password_entry, 1, wx.ALL, 5)
        self.h_sizer4.Add(self.verify_password_label, 0,
                          wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer4.Add(self.verify_password_entry, 1, wx.ALL, 5)
        self.h_sizer5.Add(self.permission_level_label, 0,
                          wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer5.Add(self.permission_level_choices, 1, wx.ALL, 5)
        self.h_sizer6.Add(self.security_code_label, 0,
                          wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer6.Add(self.security_code_entry, 1, wx.ALL, 5)
        self.h_sizer7.Add(self.email_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer7.Add(self.email_entry, 1, wx.ALL, 5)
        self.h_sizer8.Add(self.cancel_button, 0, wx.ALL, 5)
        self.h_sizer8.Add(self.sign_up_button, 0, wx.ALL, 5)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL, 5)
        self.v_sizer.Add(self.h_sizer2, 0, wx.ALL|wx.EXPAND, 2)
        self.v_sizer.Add(self.h_sizer3, 0, wx.ALL|wx.EXPAND, 2)
        self.v_sizer.Add(self.h_sizer4, 0, wx.ALL|wx.EXPAND, 2)
        self.v_sizer.Add(self.h_sizer5, 0, wx.ALL|wx.EXPAND, 2)
        self.v_sizer.Add(self.h_sizer6, 0, wx.ALL|wx.EXPAND, 2)
        self.v_sizer.Add(self.h_sizer7, 0, wx.ALL|wx.EXPAND, 2)
        self.v_sizer.Add(self.h_sizer8, 0, wx.ALL|wx.ALIGN_RIGHT, 2)

        # Setting sizer
        self.main_panel.SetSizer(self.v_sizer)

    def on_button_sign_up(self, event):
        """This method will allow the registration of the user."""

        # Getting user input
        username = self.username_entry.GetValue()
        password = self.password_entry.GetValue()
        confirm_password = self.verify_password_entry.GetValue()
        permission_level = self.permission_level_choices.GetSelection()
        security_code = self.security_code_entry.GetValue()
        email = self.email_entry.GetValue()
        data = []

        # Appending the input to a list
        data.append(username)
        data.append(password)
        data.append(confirm_password)
        data.append(permission_level)
        data.append(security_code)
        data.append(email)

        # Verify the list for empty elements
        empty_elements = [x == "" for x in data]

        # If there are any empty elements in the list or
        # the permission level is not set show proper message
        if any(empty_elements) or data[3] == -1:
            message = wx.MessageBox("All fields are required.", "Sign Up",
                                    style=wx.OK|wx.ICON_WARNING)
        elif len(data[0]) < 8:
            # If the username is shorter than 8 characters show message
            message = wx.MessageBox(("The username must be longer "
                                     "than 8 characters."), "Sign Up",
                                     style=wx.OK|wx.ICON_WARNING)
        elif len(data[1]) < 8:
            # If the password is shorted than 8 characters show message
            message = wx.MessageBox(("The password must be longer "
                                     "than 8 characters."), "Sign Up",
                                     style=wx.OK|wx.ICON_WARNING)
        elif data[1] != data[2]:
            # If passwords do not match show message
            message = wx.MessageBox("The passwords do not match.", "Sign Up",
                                    style=wx.OK|wx.ICON_WARNING)
        elif data[4] != "30067676":
            # If the security code is invalid show message
            message = wx.MessageBox("The security code is invalid.", "Sign Up",
                                    style=wx.OK|wx.ICON_WARNING)
        else:
            # If user input is valid search the username in database
            user = self.database.get_user(username)

            # If data found
            if user:
                # If username matches show message
                if user[0][1] == username:
                    message = wx.MessageBox(("This username already exists "
                                             "in the database."), "Sign Up",
                                             style=wx.OK|wx.ICON_WARNING)
            else:
                # Else add user to database
                self.database.add_user(username, password,
                                       permission_level, email)
                message = wx.MessageBox(("The account has been added to "
                                         "the database successfully."),
                                         "Sign Up",
                                         style=wx.OK|wx.ICON_INFORMATION)

    def on_button_cancel_sign_up(self, event):
        """This method will allow the sign up to be closed."""

        # Close window
        self.Close()



