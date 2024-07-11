#-------------------------------------------------------------------------------
# Darie-Dragos Mitoiu
# Owner v1.0.0 15/02/2019
# An owner UI module designed for a tailoring and alterations business
#-------------------------------------------------------------------------------


import wx
from datetime import datetime
from administrator import Administrator


class Owner(Administrator):
    """This class allow the creation of the owner interface object, this class
       will act as a container for the other essential objects."""

    def __init__(self, master, user, *args, **kwargs):
        Administrator.__init__(self, master, user, *args, **kwargs)
        # Create new attribute for top panel object,
        # Create horizontal sizer object
        self.top_panel.h_sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        # Declare attributes
        self.selected_user = None

        # Create users list ctrl object and bind methods
        self.users_list_ctrl = UsersListCtrl(self.top_panel, style=wx.LC_REPORT)
        self.users_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                  self.get_user)
        self.users_list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                                  self.deselect_user)
        self.users_list_ctrl.Bind(wx.EVT_LIST_COL_BEGIN_DRAG,
                                  self.on_column_drag)

        # Add widgets to the sizers
        self.top_panel.h_sizer6.Add(self.users_list_ctrl, 1, wx.EXPAND)
        self.top_panel.v_sizer.Add(self.top_panel.h_sizer6, 1, wx.EXPAND)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer6)

        # Setting owner left panel and top panel objects (update objects)
        self.set_left_panel()
        self.set_right_top_panel()

        # Load users data from database and set list ctrl column width
        self.view_users()
        self.users_list_ctrl.SetColumnWidth(0, 0)
        self.users_list_ctrl.SetColumnWidth(1, -2)
        self.users_list_ctrl.SetColumnWidth(2, 0)
        self.users_list_ctrl.SetColumnWidth(3, -2)
        self.users_list_ctrl.SetColumnWidth(4, -2)
        self.users_list_ctrl.SetColumnWidth(5, -2)

        # Update status bar object
        self.status_bar.SetStatusText(("Permission Level: Owner"), 2)

    def set_left_panel(self):
        """This method will update the left panel object."""

        # Assigning the left panel tree object to a new variable
        self.tree = self.left_panel.tree
        self.tree_root = self.left_panel.tree.root

        # Inserting new tree item
        self.users = self.left_panel.tree.InsertItem(self.tree_root, 0, "Users")

        # Setting item image
        self.users_bitmap = wx.Bitmap("images/users.png",
                                      wx.BITMAP_TYPE_PNG)
        self.users_image = self.tree.image_list.Add(self.users_bitmap)

        self.tree.SetItemImage(self.users, self.users_image)

        # Binding tree method
        self.left_panel.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_select_tree)

    def on_select_tree(self, event):
        """This method will run whenever the tree ctrl is selected,
           the objective of this method is to update the top panel
           object."""

        if self.left_panel.tree:
            # If there is a selection get item
            self.selection = event.GetItem()
            # Get item string
            self.selection_string = self.left_panel.tree.GetItemText(self.selection)

            if self.selection_string == "Database":
                pass
            if self.selection_string == "Users":
                # If item selected is users set users tree
                self.set_users_tree()
            if self.selection_string == "Customers":
                # If customers item is selected set customers tree
                self.set_customers_tree()
            if self.selection_string == "Tailors":
                # If tailors item is selected set tailors tree
                self.set_tailors_tree()
            if self.selection_string == "Projects":
                # If projects item is selected set projects tree
                self.set_projects_tree()
            if self.selection_string == "Alterations":
                # If alterations item is selected set alterations tree
                self.set_alterations_tree()
            if self.selection_string == "Active":
                # If active item is selected set active tree
                self.set_active_tree()
            if self.selection_string == "Completed":
                # If completed item is selected set completed tree
                self.set_completed_tree()

    def set_users_tree(self):
        """This method will run whenever the users item from the tree ctrl
           is selected, the objective of this method is to handle
           the content of the top panel object."""

        # Load users tree
        self.users_tree()
        # Count records
        self.users_count = self.users_list_ctrl.GetItemCount()

        # Freeze top panel object
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Show users list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer6)
        # Update top panel object content
        self.top_panel.Layout()
        # Resume top panel
        self.top_panel.Thaw()

        # Update status bar
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.users_count)),
                                       5)

    def set_customers_tree(self):
        """This method will run whenever the customers item from the tree ctrl
           is selected, the objective of this method is to handle
           the content of the top panel object."""

        # Load customers tree
        self.customers_tree()
        # Count records
        self.customers_count = self.top_panel.list_ctrl.GetItemCount()

        # Freeze top panel object
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer6)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Show customers list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer2)
        # Update top panel object content
        self.top_panel.Layout()
        # Resume top panek object
        self.top_panel.Thaw()

        # Update status bar
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.customers_count)),
                                       5)

    def set_tailors_tree(self):
        """This method will run whenever the tailors item from the tree ctrl
           is selected, the objective of this method is to handle
           the content of the top panel object."""

        # Load tailors tree
        self.tailors_tree()
        # Count records
        self.tailors_count = self.top_panel.list_ctrl_tailors.GetItemCount()

        # Freeze top panel object
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer6)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Show tailors list ctrls
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer3)
        # Update top panel content
        self.top_panel.Layout()
        # Resume top panel
        self.top_panel.Thaw()

        # Update status bar
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.tailors_count)),
                                       5)

    def set_projects_tree(self):
        """This method will run whenever the projects item from the tree ctrl
           is selected, the objective of this method is to handle
           the content of the top panel object."""

        # Load projects tree
        self.projects_tree()
        # Count records
        self.projects_count = self.top_panel.list_ctrl_projects.GetItemCount()

        # Freeze top panel
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer6)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Show projects list ctrls
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer4)
        # Update top panel content
        self.top_panel.Layout()
        # Resume top panel
        self.top_panel.Thaw()

        # Update status bar
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.projects_count)),
                                       5)

    def set_alterations_tree(self):
        """This method will run whenever the alterations item from the tree ctrl
           is selected, the objective of this method is to handle
           the content of the top panel object."""

        # Load alterations tree
        self.alterations_tree()
        # Count records
        self.a_table_count = self.top_panel.list_ctrl_alterations.GetItemCount()

        # Freeze top panel
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer6)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Show alterations list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer5)
        # Update top panel content
        self.top_panel.Layout()
        # Resume top panel
        self.top_panel.Thaw()

        # Update status bar
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.a_table_count)),
                                       5)

    def set_active_tree(self):
        """This method will run whenever the active item from the tree ctrl
           is selected, the objective of this method is to handle
           the content of the top panel object."""

        # Load active tool bar and count records
        self.top_panel_tool_bar.active_tree()
        self.active_count = self.top_panel.list_ctrl_active.GetItemCount()

        # Freeze top panel
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer6)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Load data
        self.top_panel.view_active()
        self.top_panel.list_ctrl_active.SetColumnWidth(0, 0)
        self.top_panel.list_ctrl_active.SetColumnWidth(1, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(2, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(3, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(4, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(5, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(6, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(7, -2)

        # Show list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer7)
        # Update top panel content
        self.top_panel.Layout()
        # Resume top panel
        self.top_panel.Thaw()

        # Update status bar
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.active_count)),
                                       5)

    def set_completed_tree(self):
        """This method will run whenever the completed item from the tree ctrl
           is selected, the objective of this method is to handle
           the content of the top panel object."""

        # Load completed tool bar
        self.top_panel_tool_bar.completed_tree()
        # Count records
        self.completed_count = self.top_panel.list_ctrl_completed.GetItemCount()

        # Freeze top panel
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer6)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)

        # Load completed data
        self.top_panel.view_completed()
        self.top_panel.list_ctrl_completed.SetColumnWidth(0, 0)
        self.top_panel.list_ctrl_completed.SetColumnWidth(1, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(2, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(3, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(4, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(5, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(6, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(7, -2)

        # Show completed list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer8)
        # Update top panel content
        self.top_panel.Layout()
        # Resume top panel
        self.top_panel.Thaw()

        # Update status bar
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.completed_count)),
                                       5)

    def view_users(self):
        """This method will allow the users data to be loaded and inserted
           into the users list ctrl."""

        # Getting users data
        users_data = self.top_panel.database.view_users()

        # Clear list ctrl
        self.users_list_ctrl.DeleteAllItems()
        for row in users_data:
            # Appending data
            self.users_list_ctrl.Append((row[0], row[1],
                                         row[2], row[3],
                                         row[4]))

    def get_user(self, event):
        """This method will run whenever an user is selected in the users
           list ctrl, the objective of this method is to get the user's ID."""

        try:
            # Assign users list ctrl to a new variable
            self.list_users = self.users_list_ctrl
            # Get selected record
            self.selected_user = self.list_users.GetFocusedItem()
            # Get user's ID
            self.user = self.list_users.GetItemText(self.selected_user,
                                                    col=0)
            # Get record's position
            self.position_user = int(self.selected_user) + 1

            # Update status bar
            self.SetStatusText(("Position: " +
                                str(self.position_user)), 4)
        except:
            pass

    def deselect_user(self, event):
        """This method will run whenever the user is deselected."""

        # Deselect user
        self.selected_user = None

    def on_column_drag(self, event):
        """This method will run whenever the first column or the third one is
           dragged, the objective of this method is to hide the user ID and
           password."""

        if event.Column == 0 or event.Column == 2:
            # If column dragged is 0 or 2 veto the event
            event.Veto()

    def users_tree(self):
        """This method will handle the tool bar object."""

        # Update tool bar
        self.tool_bar.EnableTool(wx.ID_ADD, False)
        self.tool_bar.EnableTool(wx.ID_EDIT, True)
        self.tool_bar.EnableTool(wx.ID_DELETE, True)
        self.tool_bar.EnableTool(wx.ID_FIND, True)

        # Bind new methods
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.on_button_update_user,
                           self.tool_bar.edit_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.on_button_delete_user,
                           self.tool_bar.delete_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.on_button_search_user,
                           self.tool_bar.search_tool)

    def on_button_update_user(self, event):
        """This method will allow the creation of the update user window object,
           the objective of this method is to update an user in database."""

        if self.selected_user is not None:
            # If an user is selected open window object
            self.update_user_window = UpdateUser(None,
                                                 self,
                                                 self.top_panel,
                                                 title="Update User",
                                                 size=(500, 500))
            self.update_user_window.Show()
        else:
            # If no user is selected show message
            message = wx.MessageBox("No record selected.", "Update User",
                                    style=wx.OK|wx.ICON_WARNING)

    def on_button_delete_user(self, event):
        """This method will allow the creation of the delete user window object,
           the objective of this method is to update an user in database."""

        if self.selected_user is not None:

            # If an user is selected show delete user dialog
            message = wx.MessageDialog(None,
                                       ("Are you sure you want to delete "
                                        "the selected record?"),
                                        "Delete Record",
                                        wx.YES_NO|wx.ICON_QUESTION)
            result = message.ShowModal()

            if result == wx.ID_YES:
                # If response is yes delete user and deselect user
                self.database = self.top_panel.database
                self.database.delete_user(self.user)
                self.view_users()
                self.selected_user = None
            else:
                pass
        else:
            # If no user is selected show message
            message = wx.MessageBox("No record selected.",
                                    "Delete User",
                                    style=wx.OK|wx.ICON_WARNING)

    def on_button_search_user(self, event):
        """This method will allow the creation of the search user window object,
           the objective of this method is to update an user in database."""

        # Open search user window
        self.search_user_window = SearchUser(None,
                                             self.top_panel,
                                             title="Search User",
                                             size=(1200, 500))
        self.search_user_window.Show()

    def set_right_top_panel(self):
        """This method will update the top panel object."""

        # Update top panel object
        self.administrator_username_label = (self.user.upper())
        self.top_panel.username_label.SetLabel(self.administrator_username_label)
        self.top_panel.Layout()

class UsersListCtrl(wx.ListCtrl):
    """This method will allow the creation of the users list ctrl object."""

    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will insert the columns of the list ctrl."""

        # Create font and set it to the list ctrl
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.SetFont(self.font)

        # Insert columns
        self.InsertColumn(0, "ID")
        self.InsertColumn(1, "Username")
        self.InsertColumn(2, "Password")
        self.InsertColumn(3, "Permission Level")
        self.InsertColumn(4, "Email")
        self.SetColumnWidth(0, -2)
        self.SetColumnWidth(1, -2)
        self.SetColumnWidth(2, -2)
        self.SetColumnWidth(3, -2)
        self.SetColumnWidth(4, -2)

class UpdateUser(wx.Frame):
    """This class will allow the creation of the update users window object."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Create main panel object
        self.main_panel = UpdateUserPanel(self,
                                          self,
                                          self.controller,
                                          self.top_panel)
        # Center window
        self.Center()

class UpdateUserPanel(wx.Panel):
    """This class will allow the creation of the update users panel object."""

    def __init__(self, master, controller, owner, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.owner = owner
        self.top_panel = top_panel
        # Accessing top panel objects
        self.database = self.top_panel.database
        self.logger = self.top_panel.logger
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal sizers objects
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)

        # Create static box object and static box sizer object
        self.static_box1 = wx.StaticBox(self)
        self.static_sizer1 = wx.StaticBoxSizer(self.static_box1, wx.VERTICAL)

        # Horizontal sizers for the general interface elements
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer6 = wx.BoxSizer(wx.HORIZONTAL)

        # Create icon object and set it to the master window
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.master.SetIcon(self.icon)

        # Getting user details
        self.get_user()

        # Create label object and font objects
        self.title_label = wx.StaticText(self, label="Update User")
        self.font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create label objects
        self.username_label = wx.StaticText(self,
                                              label="Username:",
                                              size=(150, -1))

        self.password_label = wx.StaticText(self,
                                             label="Password:",
                                             size=(150, -1))

        self.verify_password_label = wx.StaticText(self,
                                             label="Repeat Password:",
                                             size=(150, -1))

        self.permission_level_label = wx.StaticText(self,
                                           label="Permission Level:",
                                           size=(150, -1))

        self.email_label = wx.StaticText(self,
                                           label="Email:",
                                           size=(150, -1))

        # Create entry objects
        self.username_entry = wx.TextCtrl(self)
        self.password_entry = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.verify_password_entry = wx.TextCtrl(self, style=wx.TE_PASSWORD)
        self.permission_level_choices = wx.Choice(self,
                                                  choices=["1-System Operator",
                                                           "2-Administrator",
                                                           "3-Owner"])
        self.email_entry = wx.TextCtrl(self)

        # Setting label fonts
        self.username_label.SetFont(self.font_normal)
        self.password_label.SetFont(self.font_normal)
        self.verify_password_label.SetFont(self.font_normal)
        self.permission_level_label.SetFont(self.font_normal)
        self.email_label.SetFont(self.font_normal)

        # Create button objects
        self.cancel_button = wx.Button(self, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_button_close_update_user)
        self.update_user_button = wx.Button(self, label="Update")
        self.update_user_button.Bind(wx.EVT_BUTTON, self.on_button_update_user)

        # Setting button fonts
        self.cancel_button.SetFont(self.font_normal)
        self.update_user_button.SetFont(self.font_normal)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
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
        self.h_sizer6.Add(self.email_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer6.Add(self.email_entry, 1, wx.ALL, 5)
        self.static_sizer1.Add(self.h_sizer2, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer3, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer4, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer5, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer6, 0, wx.ALL|wx.EXPAND, 2)

        self.h_sizer_buttons.Add(self.cancel_button, 0, wx.ALL, 5)
        self.h_sizer_buttons.Add(self.update_user_button, 0, wx.ALL, 5)

        self.h_sizer0.Add(self.static_sizer1, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.Add(self.h_sizer0, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer_buttons, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Inserting data into the fields
        self.insert_data()

        # Setting panel's sizer
        self.SetSizer(self.v_sizer)

    def get_user(self):
        """This method will get the user's data."""

        # Acessing top panel objects
        self.u_list_ctrl = self.owner.users_list_ctrl
        self.database = self.top_panel.database
        self.user = self.owner.selected_user
        self.user_id = self.u_list_ctrl.GetItemText(self.user, col=0)
        self.user_data = self.database.get_user_id(self.user_id)

        # Getting user's data
        self.username_value = self.user_data[0][1]
        self.password_value = self.user_data[0][2]
        self.permission_level_value = self.user_data[0][3]
        self.email_value = self.user_data[0][4]

    def insert_data(self):
        """This method will insert the user's data into the fields."""

        # Setting entries values
        self.username_entry.SetValue(self.username_value)
        self.password_entry.SetValue(self.password_value)
        self.verify_password_entry.SetValue(self.password_value)
        self.permission_level_choices.SetSelection(self.permission_level_value)
        self.email_entry.SetValue(self.email_value)

    def on_button_close_update_user(self, event):
        """This method will run whenever the cancel button is pressed."""

        # Close update user window object
        self.controller.Close()

    def on_button_update_user(self, event):
        """This method will run whenever the update button is pressed,
           the objective of this method is to update an user in
           database."""

        # Getting user input
        self.permission = self.permission_level_choices
        self.username_value = self.username_entry.GetValue()
        self.password_value = self.password_entry.GetValue()
        self.password_repeat_value = self.verify_password_entry.GetValue()
        self.permission_level_value = self.permission.GetSelection()
        self.email_value = self.email_entry.GetValue()

        # Create array
        data = []

        # Append data to the array
        data.append(self.username_value)
        data.append(self.password_value)
        data.append(self.password_repeat_value)
        data.append(self.permission_level_value)
        data.append(self.email_value)

        # Validation of data
        empty_elements = [x == "" for x in data]

        if any(empty_elements) or data[3] == -1:
            # If there are any empty elements in the list or no permission level
            # show message
            message = wx.MessageBox("All fields are required.", "Update User",
                                    style=wx.OK|wx.ICON_WARNING)
        elif len(data[0]) < 8:
            # If the username is shorter than 8 characters long
            message = wx.MessageBox(("The username must be longer "
                                     "than 8 characters."), "Update User",
                                     style=wx.OK|wx.ICON_WARNING)
        elif len(data[1]) < 8:
            # If the password is shorter than 8 characters long show message
            message = wx.MessageBox(("The password must be longer "
                                     "than 8 characters."), "Update User",
                                     style=wx.OK|wx.ICON_WARNING)
        elif data[1] != data[2]:
            # If passwords do not match show message
            message = wx.MessageBox("The passwords do not match.",
                                    "Update User",
                                    style=wx.OK|wx.ICON_WARNING)
        else:
            # If user input is valid update user in database
            self.database.update_user(self.username_value,
                                      self.password_value,
                                      self.permission_level_value,
                                      self.email_value,
                                      self.user_id)

            # Show notification
            message = wx.MessageBox(("The user has been updated successfully."),
                                     "Update User",
                                     style=wx.OK|wx.ICON_INFORMATION)

            # Update users list ctrl
            self.owner.view_users()

            # Update logger
            self.current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.message = ("[" + str(self.current_date_time) + "]" +
                            " - User: " +
                            str(self.username_value) + " " +
                            "has been updated successfully.")
            self.logger.Append((self.message))

class SearchUser(wx.Frame):
    """This class will allow the creation of the search user window object."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel object
        self.main_panel = SearchUserPanel(self,
                                          self,
                                          self.controller)
        # Center window
        self.Center()

class SearchUserPanel(wx.Panel):
    """This class will allow the creation of the search user panel object."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        self.database = self.top_panel.database
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal sizers objects
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        # Create icon object and set it to the master window
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.master.SetIcon(self.icon)

        # Create label object
        self.title_label = wx.StaticText(self, label="Search User")
        self.font_title = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.title_label.SetFont(self.font_title)

        self.search_label = wx.StaticText(self, label="Search:")
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.search_label.SetFont(self.font)

        self.by_label = wx.StaticText(self, label="by")
        self.by_label.SetFont(self.font)

        self.choices = wx.Choice(self,
                                 choices=["1-Username",
                                          "2-Permission Level",
                                          "3-Email"])

        # Create entry object
        self.search_entry = wx.TextCtrl(self, size=(250, -1))

        # Create button object and bind method
        self.search_button = wx.Button(self, label="Search")
        self.search_button.Bind(wx.EVT_BUTTON, self.search_user)

        # Create users list ctrl
        self.list_ctrl = UsersListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.SetColumnWidth(0, 0)
        self.list_ctrl.SetColumnWidth(2, 0)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
        self.h_sizer2.Add(self.search_label, 0, wx.ALL, 5)
        self.h_sizer2.Add(self.search_entry, 0, wx.ALL, 5)
        self.h_sizer2.Add(self.by_label, 0, wx.ALL, 5)
        self.h_sizer2.Add(self.choices, 0, wx.ALL, 5)
        self.h_sizer2.Add(self.search_button, 0, wx.ALL, 5)
        self.h_sizer3.Add(self.list_ctrl, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.AddSpacer(50)
        self.v_sizer.Add(self.h_sizer2)
        self.v_sizer.AddSpacer(50)
        self.v_sizer.Add(self.h_sizer3, 1, wx.EXPAND)

        # Setting panel's sizer
        self.SetSizer(self.v_sizer)

    def search_user(self, event):
        """This method will allow the user to search an user in database."""

        # Getting user selection
        self.choices_value = self.choices.GetSelection()
        if self.choices_value == 0:
            # If user selection is the first element in the list,
            # search for the username in database
            self.username = self.search_entry.GetValue()
            self.data = self.database.search_user_username(self.username)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, 0)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
            except:
                pass

        if self.choices_value == 1:
            # If user selection is the second item in the list,
            # search for permission level in database
            self.permission = self.search_entry.GetValue()
            self.data = self.database.search_user_permission(self.permission)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, 0)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
            except:
                pass

        if self.choices_value == 2:
            # If user selection is the third element in the list,
            # search for email in database
            self.email = self.search_entry.GetValue()
            self.data = self.database.search_user_email(self.email)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, 0)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
            except:
                pass
