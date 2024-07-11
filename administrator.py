#-------------------------------------------------------------------------------
# Darie-Dragos Mitoiu
# Administrator v1.0.0 15/02/2019
# An administrator UI module designed for a tailoring and alterations business
#-------------------------------------------------------------------------------


# Importing libraries
import wx
from datetime import datetime
from sysop import SysOp
from controller import Controller


class Administrator(SysOp):
    """This class allow the creation of the administrator interface object,
       this class will act as a container for the other essential objects."""

    def __init__(self, master, user, *args, **kwargs):
        SysOp.__init__(self, master, user, *args, **kwargs)
        # Assigning the tool bar to a new variable
        self.tool_bar = self.top_panel_tool_bar
        # Setting the new top panel object
        self.set_right_top_panel()
        # Setting the new status bar object
        self.status_bar.SetStatusText(("Permission Level: Administrator"), 2)

    def set_customers_tree(self):
        """This method will set the administrator user top panel object."""

        # Load customers tree
        self.customers_tree()
        # Count records
        self.customers_count = self.top_panel.list_ctrl.GetItemCount()

        # Freeze top panel and hide list ctrls
        self.top_panel.Freeze()
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Show customers list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer2)
        # Update top panel content
        self.top_panel.Layout()
        # Resume panel
        self.top_panel.Thaw()

        # Update status bar object
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.customers_count)),
                                       5)

    def set_tailors_tree(self):
        """This method will set the administrator user top panel object."""

        # Load tailors tree
        self.tailors_tree()
        # Count records
        self.tailors_count = self.top_panel.list_ctrl_tailors.GetItemCount()

        # Freeze top panel and hide list ctrls
        self.top_panel.Freeze()
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Show tailors list ctrl
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
        """This method will set the administrator user top panel object."""

        # Load projects tree
        self.projects_tree()
        # Count records
        self.projects_count = self.top_panel.list_ctrl_projects.GetItemCount()

        # Freeze top panel and hide list ctrl
        self.top_panel.Freeze()
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Show projects list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer4)
        # Update top panel content
        self.top_panel.Layout()
        # Resume top panel
        self.top_panel.Thaw()

        # Update status bar object
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.projects_count)),
                                       5)

    def set_alterations_tree(self):
        """This method will set the administrator user top panel object."""

        # Laod alterations tree
        self.alterations_tree()
        # Count records
        self.a_table_count = self.top_panel.list_ctrl_alterations.GetItemCount()

        # Freeze top panel and hide list ctrl
        self.top_panel.Freeze()
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Show alterations list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer5)
        # Update top panel content
        self.top_panel.Layout()
        # Resume top panel content
        self.top_panel.Thaw()

        # Update status bar object
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.a_table_count)),
                                       5)

    def set_active_tree(self):
        """This method will set the administrator user top panel object."""

        # Load active tree
        self.active_tree()
        # Count records
        self.active_count = self.top_panel.list_ctrl_active.GetItemCount()

        # Freeze top panel and hide list ctrls
        self.top_panel.Freeze()
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Load active data and set list ctrl column width
        self.top_panel.view_active()
        self.top_panel.list_ctrl_active.SetColumnWidth(0, 0)
        self.top_panel.list_ctrl_active.SetColumnWidth(1, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(2, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(3, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(4, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(5, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(6, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(7, -2)

        # Show active list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer7)
        # Update top panel content
        self.top_panel.Layout()
        # Resume top panel
        self.top_panel.Thaw()

        # Update status bar object
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.active_count)),
                                       5)

    def set_completed_tree(self):
        """This method will set the administrator user top panel object."""

        # Load completed tree
        self.completed_tree()
        # Count records
        self.completed_count = self.top_panel.list_ctrl_completed.GetItemCount()

        # Freeze top panel and hide list ctrls
        self.top_panel.Freeze()
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)

        # Load completed data and set list ctrl column width
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

        # Update status bar object
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.completed_count)),
                                       5)

    def customers_tree(self):
        """This method will run whenever the customers tree item will be
           selected, the objective of this method is to update the tool bar
           object."""

        # Update tool bar object
        self.tool_bar.EnableTool(wx.ID_ADD, True)
        self.tool_bar.EnableTool(wx.ID_EDIT, True)
        self.tool_bar.EnableTool(wx.ID_DELETE, True)
        self.tool_bar.EnableTool(wx.ID_FIND, True)

        # Bind new methods to the tools
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.tool_bar.on_button_add_customer,
                           self.tool_bar.add_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.tool_bar.on_button_update_customer,
                           self.tool_bar.edit_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.tool_bar.on_button_delete_customer,
                           self.tool_bar.delete_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.tool_bar.on_button_search_customer,
                           self.tool_bar.search_tool)

    def tailors_tree(self):
        """This method will run whenever the tailors tree item will be
           selected, the objective of this method is to update the tool bar
           object."""

        # Update tool bar object
        self.tool_bar.EnableTool(wx.ID_ADD, True)
        self.tool_bar.EnableTool(wx.ID_EDIT, True)
        self.tool_bar.EnableTool(wx.ID_DELETE, True)
        self.tool_bar.EnableTool(wx.ID_FIND, True)

        # Bind new methods to the tools
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.on_button_add_tailor,
                           self.tool_bar.add_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.on_button_update_tailor,
                           self.tool_bar.edit_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.on_button_delete_tailor,
                           self.tool_bar.delete_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.tool_bar.on_button_search_tailor,
                           self.tool_bar.search_tool)

    def projects_tree(self):
        """This method will run whenever the projects tree item will be
           selected, the objective of this method is to update the tool bar
           object."""

        # Update tool bar object
        self.top_panel_tool_bar.EnableTool(wx.ID_ADD, True)
        self.top_panel_tool_bar.EnableTool(wx.ID_EDIT, True)
        self.top_panel_tool_bar.EnableTool(wx.ID_DELETE, True)
        self.top_panel.tool_bar.EnableTool(wx.ID_FIND, True)

        # Bind new methods to the tools
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.tool_bar.on_button_add_project,
                           self.tool_bar.add_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.tool_bar.on_button_update_project,
                           self.tool_bar.edit_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.on_button_delete_project,
                           self.tool_bar.delete_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.tool_bar.on_button_search_project,
                           self.tool_bar.search_tool)

    def alterations_tree(self):
        """This method will run whenever the alterations tree item will be
           selected, the objective of this method is to update the tool bar
           object."""

        # Update tool bar object
        self.tool_bar.EnableTool(wx.ID_ADD, True)
        self.tool_bar.EnableTool(wx.ID_EDIT, True)
        self.tool_bar.EnableTool(wx.ID_DELETE, True)
        self.tool_bar.EnableTool(wx.ID_FIND, True)

        # Bind new methods to the tools
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.tool_bar.on_button_add_alteration,
                           self.tool_bar.add_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.top_panel_tool_bar.on_button_update_alteration,
                           self.top_panel_tool_bar.edit_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.on_button_delete_alteration,
                           self.tool_bar.delete_tool)
        self.tool_bar.Bind(wx.EVT_TOOL,
                           self.top_panel_tool_bar.on_button_search_alteration,
                           self.top_panel_tool_bar.search_tool)

    def active_tree(self):
        """This method will run whenever the active tree item will be
           selected, the objective of this method is to update the tool bar
           object."""

        # Update tool bar object
        self.tool_bar.EnableTool(wx.ID_ADD, False)
        self.tool_bar.EnableTool(wx.ID_EDIT, False)
        self.tool_bar.EnableTool(wx.ID_DELETE, False)
        self.tool_bar.EnableTool(wx.ID_FIND, False)

    def completed_tree(self):
        """This method will run whenever the completed tree item will be
           selected, the objective of this method is to update the tool bar
           object."""

        # Update tool bar object
        self.tool_bar.EnableTool(wx.ID_ADD, False)
        self.tool_bar.EnableTool(wx.ID_EDIT, False)
        self.tool_bar.EnableTool(wx.ID_DELETE, False)
        self.tool_bar.EnableTool(wx.ID_FIND, False)

    def on_button_add_tailor(self, event):
        """This method will run whenever the add tailor buttons is pressed,
           the objective of this method is to create the add tailor window
           object."""

        # Create add tailor window object and show it
        self.add_tailor_window = AddTailor(None,
                                           self.top_panel,
                                           title="Add Tailor",
                                           size=(500, 500))
        self.add_tailor_window.Show()

    def on_button_update_tailor(self, event):
        """This method will run whenever the update tailor buttons is pressed,
           the objective of this method is to create the update tailor window
           object."""

        if self.top_panel.selected_tailor is not None:
            # If there is a tailor selected open update tailor window object
            self.update_tailor_window = UpdateTailor(None,
                                                     self.top_panel,
                                                     title="Update Tailor",
                                                     size=(500, 500))
            self.update_tailor_window.Show()
        else:
            # If no tailor selected show message
            message = wx.MessageBox("No record selected.", "Update Tailor",
                                    style=wx.OK|wx.ICON_WARNING)

    def on_button_delete_tailor(self, event):
        """This method will run whenever the delete tailor buttons is pressed,
           the objective of this method is to create the delete tailor window
           object."""

        if self.top_panel.selected_tailor is not None:

            # Show delete dialog
            message = wx.MessageDialog(None,
                                       ("Are you sure you want to delete "
                                        "the selected record?"),
                                        "Delete Record",
                                        wx.YES_NO|wx.ICON_QUESTION)
            result = message.ShowModal()

            if result == wx.ID_YES:
                # If response is yes, delete tailor from database
                self.database = self.top_panel.database
                self.database.delete_tailor(self.top_panel.tailor)
                self.top_panel.view_tailors()
                self.top_panel.selected_tailor = None
            else:
                pass
        else:
            # If no tailor is selected show message
            message = wx.MessageBox("No record selected.",
                                    "Delete Tailor",
                                    style=wx.OK|wx.ICON_WARNING)

    def on_button_delete_project(self, event):
        """This method will run whenever the delete project buttons is pressed,
           the objective of this method is to create the delete project window
           object."""

        if self.top_panel.selected_project is not None:

            # Show delete project dialog
            message = wx.MessageDialog(None,
                                       ("Are you sure you want to delete "
                                        "the selected record?"),
                                        "Delete Record",
                                        wx.YES_NO|wx.ICON_QUESTION)
            result = message.ShowModal()

            if result == wx.ID_YES:
                # If response is yes delete project
                self.database = self.top_panel.database
                self.database.delete_project(self.top_panel.project)
                self.top_panel.view_projects()
                self.top_panel.selected_project = None
            else:
                pass
        else:
            # If no proeject is selected show message
            message = wx.MessageBox("No record selected.",
                                    "Delete Project",
                                    style=wx.OK|wx.ICON_WARNING)

    def on_button_delete_alteration(self, event):
        """This method will run whenever the delete alteration buttons is
           pressed, the objective of this method is to create the
           delete alteration window object."""

        if self.top_panel.selected_alteration is not None:

            # Show delete alteration dialog
            message = wx.MessageDialog(None,
                                       ("Are you sure you want to delete "
                                        "the selected record?"),
                                        "Delete Record",
                                        wx.YES_NO|wx.ICON_QUESTION)
            result = message.ShowModal()

            if result == wx.ID_YES:
                # if response is yes delete alteration from database
                self.database = self.top_panel.database
                self.database.delete_alteration(self.top_panel.alteration)
                self.top_panel.view_alterations()
                self.top_panel.selected_alteration = None
            else:
                pass
        else:
            # If no alteration is selected show message
            message = wx.MessageBox("No record selected.",
                                    "Delete Alteration",
                                    style=wx.OK|wx.ICON_WARNING)

    def set_right_top_panel(self):
        """This method will update the top panel object."""

        # Update username label
        self.administrator_username_label = (self.user.upper())
        # Set label and update top panel content
        self.top_panel.username_label.SetLabel(self.administrator_username_label)
        self.top_panel.Layout()

class AddTailor(wx.Frame):
    """This class will allow the creation of the add tailor window object."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel object
        self.main_panel = AddTailorPanel(self,
                                         self,
                                         self.controller)
        # Center window
        self.Center()

class AddTailorPanel(wx.Panel):
    """This class will allow the creation of the add tailor panel object,
       the objective of this class is to add a new tailor to the database."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Accessing the objects from the top panel object
        self.database = self.top_panel.database
        self.logger = self.top_panel.logger
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal sizers objects
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)

        # Create static box and static box sizer objects
        self.static_box1 = wx.StaticBox(self)
        self.static_sizer1 = wx.StaticBoxSizer(self.static_box1, wx.VERTICAL)

        # Horizontal sizers for the general interface elements
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer7 = wx.BoxSizer(wx.HORIZONTAL)

        # Create icon object and set it to the master window
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.master.SetIcon(self.icon)

        # Create label object and font object
        self.title_label = wx.StaticText(self, label="Add Tailor")
        self.font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create label objects
        self.first_name_label = wx.StaticText(self,
                                              label="First Name:",
                                              size=(100, -1))

        self.last_name_label = wx.StaticText(self,
                                             label="Last Name:",
                                             size=(100, -1))

        self.address_label = wx.StaticText(self,
                                           label="Address:",
                                           size=(100, -1))

        self.postcode_label = wx.StaticText(self,
                                           label="Postcode:",
                                           size=(100, -1))

        self.phone_label = wx.StaticText(self,
                                         label="Phone:",
                                         size=(100, -1))

        self.email_label = wx.StaticText(self,
                                         label="Email:",
                                         size=(100, -1))

        # Create entry objects
        self.first_name_entry = wx.TextCtrl(self)
        self.last_name_entry = wx.TextCtrl(self)
        self.address_entry = wx.TextCtrl(self)
        self.postcode_entry = wx.TextCtrl(self)
        self.phone_entry = wx.TextCtrl(self)
        self.email_entry = wx.TextCtrl(self)

        # Setting label fonts
        self.first_name_label.SetFont(self.font_normal)
        self.last_name_label.SetFont(self.font_normal)
        self.address_label.SetFont(self.font_normal)
        self.postcode_label.SetFont(self.font_normal)
        self.phone_label.SetFont(self.font_normal)
        self.email_label.SetFont(self.font_normal)

        # Create button objects
        self.cancel_button = wx.Button(self, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_button_close)
        self.add_customer_button = wx.Button(self, label="Add")
        self.add_customer_button.Bind(wx.EVT_BUTTON, self.on_button_add_tailor)

        # Setting buttons font
        self.cancel_button.SetFont(self.font_normal)
        self.add_customer_button.SetFont(self.font_normal)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
        self.h_sizer2.Add(self.first_name_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer2.Add(self.first_name_entry, 1, wx.ALL, 5)
        self.h_sizer3.Add(self.last_name_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer3.Add(self.last_name_entry, 1, wx.ALL, 5)
        self.h_sizer4.Add(self.address_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer4.Add(self.address_entry, 1, wx.ALL, 5)
        self.h_sizer5.Add(self.postcode_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer5.Add(self.postcode_entry, 1, wx.ALL, 5)
        self.h_sizer6.Add(self.phone_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer6.Add(self.phone_entry, 1, wx.ALL, 5)
        self.h_sizer7.Add(self.email_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer7.Add(self.email_entry, 1, wx.ALL, 5)
        self.static_sizer1.Add(self.h_sizer2, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer3, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer4, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer5, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer6, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer7, 0, wx.ALL|wx.EXPAND, 2)

        self.h_sizer_buttons.Add(self.cancel_button, 0, wx.ALL, 5)
        self.h_sizer_buttons.Add(self.add_customer_button, 0, wx.ALL, 5)

        self.h_sizer0.Add(self.static_sizer1, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.Add(self.h_sizer0, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer_buttons, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Setting panel's sizer
        self.SetSizer(self.v_sizer)

    def on_button_add_tailor(self, event):
        """This method will run whenever the add button is pressed,
           the objective of this method is to add a new tailor to the
           database."""

        # Getting user input
        self.first_name_value = self.first_name_entry.GetValue()
        self.last_name_value = self.last_name_entry.GetValue()
        self.address_value = self.address_entry.GetValue()
        self.postcode_value = self.postcode_entry.GetValue()
        self.phone_value = self.phone_entry.GetValue()
        self.email_value = self.email_entry.GetValue()

        # Create array and data controller object
        data_general = []
        data_controller = Controller("Data Controller")

        # Appending data to the array
        data_general.append(self.first_name_value)
        data_general.append(self.last_name_value)
        data_general.append(self.address_value)
        data_general.append(self.postcode_value)
        data_general.append(self.phone_value)
        data_general.append(self.email_value)

        # Validation of data
        empty_elements_general = [x == "" for x in data_general]

        v_first_name = data_controller.validate_alpha(self.first_name_value)
        v_last_name = data_controller.validate_alpha(self.last_name_value)
        v_address = data_controller.validate_integer_alpha(self.address_value)
        v_postcode = data_controller.validate_integer_alpha(self.postcode_value)
        v_phone = data_controller.validate_integer(self.phone_value)
        v_email = data_controller.validate_email(self.email_value)
        v_tailor = self.database.get_tailor_name(self.first_name_value,
                                                 self.last_name_value,
                                                 self.address_value)

        if any(empty_elements_general):
            # If any element in the list is empty show message
            message = wx.MessageBox("All fields are required.", "Add Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_first_name:
            # If first name is invalid show message
            message = wx.MessageBox("Invalid first name.",
                                    "Add Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_last_name:
            # If last name is invalid show message
            message = wx.MessageBox("Invalid last name.",
                                    "Add Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_address:
            # If address is invalid show message
            message = wx.MessageBox("Invalid address.",
                                    "Add Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_postcode:
            # If postcode is invalid show message
            message = wx.MessageBox("Invalid postcode.",
                                    "Add Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_phone:
            # If phone number is invalid show message
            message = wx.MessageBox("Invalid phone number.",
                                    "Add Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_email:
            # If email is invalid show message
            message = wx.MessageBox("Invalid email.",
                                    "Add Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif v_tailor:
            # If tailor already in database show message
            message = wx.MessageBox("Tailor already in database.",
                                    "Add Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        else:
            # If user input is valid add tailor to database
            self.database.add_tailor(self.first_name_value,
                                     self.last_name_value,
                                     self.address_value,
                                     self.postcode_value,
                                     self.phone_value,
                                     self.email_value)

            # Show notification
            message = wx.MessageBox(("The tailor has been added to "
                                     "the database successfully."),
                                     "Add Tailor",
                                     style=wx.OK|wx.ICON_INFORMATION)

            # Clear fields
            self.first_name_entry.Clear()
            self.last_name_entry.Clear()
            self.address_entry.Clear()
            self.postcode_entry.Clear()
            self.phone_entry.Clear()
            self.email_entry.Clear()

            # Update tailors list ctrl object and logger object
            self.top_panel.view_tailors()

            self.current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.message = ("[" + str(self.current_date_time) + "]" +
                            " - Tailor: " +
                            str(self.first_name_value) + " " +
                            str(self.last_name_value) + " " +
                            "has been added successfully to the database.")
            self.logger.Append((self.message))

    def on_button_close(self, event):
        """This method will run whenever the cancel button is pressed."""

        # Close controller window
        self.controller.Close()

class UpdateTailor(wx.Frame):
    """This class will allow the creation of the update tailor window object."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel object
        self.main_panel = UpdateTailorPanel(self,
                                            self,
                                            self.controller)
        # Center window
        self.Center()

class UpdateTailorPanel(wx.Panel):
    """This class will allow the creation of the update tailor panel object,
       the objective of this class is to update a current tailor in database."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Accessing logger object from top panel object
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
        self.h_sizer7 = wx.BoxSizer(wx.HORIZONTAL)

        # Create icon object and set it to the master window
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.master.SetIcon(self.icon)

        # Get tailor's data
        self.get_tailor()

        # Create label object and font objects
        self.title_label = wx.StaticText(self, label="Update Tailor")
        self.font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create label objects
        self.first_name_label = wx.StaticText(self,
                                              label="First Name:",
                                              size=(100, -1))

        self.last_name_label = wx.StaticText(self,
                                             label="Last Name:",
                                             size=(100, -1))

        self.address_label = wx.StaticText(self,
                                           label="Address:",
                                           size=(100, -1))

        self.postcode_label = wx.StaticText(self,
                                           label="Postcode:",
                                           size=(100, -1))

        self.phone_label = wx.StaticText(self,
                                         label="Phone:",
                                         size=(100, -1))

        self.email_label = wx.StaticText(self,
                                         label="Email:",
                                         size=(100, -1))

        # Create entry objects
        self.first_name_entry = wx.TextCtrl(self)
        self.last_name_entry = wx.TextCtrl(self)
        self.address_entry = wx.TextCtrl(self)
        self.postcode_entry = wx.TextCtrl(self)
        self.phone_entry = wx.TextCtrl(self)
        self.email_entry = wx.TextCtrl(self)

        # Set labels fonts
        self.first_name_label.SetFont(self.font_normal)
        self.last_name_label.SetFont(self.font_normal)
        self.address_label.SetFont(self.font_normal)
        self.postcode_label.SetFont(self.font_normal)
        self.phone_label.SetFont(self.font_normal)
        self.email_label.SetFont(self.font_normal)

        # Create button objects
        self.cancel_button = wx.Button(self, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON,
                                self.on_button_close_update_tailor)
        self.update_tailor_button = wx.Button(self, label="Update")
        self.update_tailor_button.Bind(wx.EVT_BUTTON,
                                       self.on_button_update_tailor)

        # Setting buttons fonts
        self.cancel_button.SetFont(self.font_normal)
        self.update_tailor_button.SetFont(self.font_normal)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
        self.h_sizer2.Add(self.first_name_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer2.Add(self.first_name_entry, 1, wx.ALL, 5)
        self.h_sizer3.Add(self.last_name_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer3.Add(self.last_name_entry, 1, wx.ALL, 5)
        self.h_sizer4.Add(self.address_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer4.Add(self.address_entry, 1, wx.ALL, 5)
        self.h_sizer5.Add(self.postcode_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer5.Add(self.postcode_entry, 1, wx.ALL, 5)
        self.h_sizer6.Add(self.phone_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer6.Add(self.phone_entry, 1, wx.ALL, 5)
        self.h_sizer7.Add(self.email_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer7.Add(self.email_entry, 1, wx.ALL, 5)
        self.static_sizer1.Add(self.h_sizer2, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer3, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer4, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer5, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer6, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer7, 0, wx.ALL|wx.EXPAND, 2)

        self.h_sizer_buttons.Add(self.cancel_button, 0, wx.ALL, 5)
        self.h_sizer_buttons.Add(self.update_tailor_button, 0, wx.ALL, 5)

        self.h_sizer0.Add(self.static_sizer1, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.Add(self.h_sizer0, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer_buttons, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Setting panel's sizer
        self.SetSizer(self.v_sizer)

        # Inserting tailor's data into the fields
        self.insert_data()

    def get_tailor(self):
        """This method will access the tailor's data from database."""

        # Assigning the tailors list ctrl object to a new variable
        self.t_list_ctrl = self.top_panel.list_ctrl_tailors
        # Assigning database object to a new variable
        self.database = self.top_panel.database
        # Getting tailor's ID and later on tailor's data
        self.tailor = self.top_panel.selected_tailor
        self.tailor_id = self.t_list_ctrl.GetItemText(self.tailor, col=0)
        self.tailor_data = self.database.get_tailor(self.tailor_id)

        # Assigning the tailor's data to new variables
        self.first_name_value = self.tailor_data[0][1]
        self.last_name_value = self.tailor_data[0][2]
        self.address_value = self.tailor_data[0][3]
        self.postcode_value = self.tailor_data[0][4]
        self.phone_value = self.tailor_data[0][5]
        self.email_value = self.tailor_data[0][6]

    def insert_data(self):
        """This method will insert the tailor's data into the fields."""

        # Setting entries values
        self.first_name_entry.SetValue(self.first_name_value)
        self.last_name_entry.SetValue(self.last_name_value)
        self.address_entry.SetValue(self.address_value)
        self.postcode_entry.SetValue(self.postcode_value)
        self.phone_entry.SetValue(self.phone_value)
        self.email_entry.SetValue(self.email_value)

    def on_button_close_update_tailor(self, event):
        """This method will run whenever the cancel button will be pressed."""

        # Close controller window
        self.controller.Close()

    def on_button_update_tailor(self, event):
        """This method will run whenever the update tailor button is pressed,
           the objective of this method is to update a tailor in database."""

        # Getting entry values
        self.first_name_value = self.first_name_entry.GetValue()
        self.last_name_value = self.last_name_entry.GetValue()
        self.address_value = self.address_entry.GetValue()
        self.postcode_value = self.postcode_entry.GetValue()
        self.phone_value = self.phone_entry.GetValue()
        self.email_value = self.email_entry.GetValue()

        # Declaring array and data controller object
        data_general = []
        data_controller = Controller("Data Controller")

        # Appending data to array
        data_general.append(self.first_name_value)
        data_general.append(self.last_name_value)
        data_general.append(self.address_value)
        data_general.append(self.postcode_value)
        data_general.append(self.phone_value)
        data_general.append(self.email_value)

        # Validation of data
        empty_elements_general = [x == "" for x in data_general]

        v_first_name = data_controller.validate_alpha(self.first_name_value)
        v_last_name = data_controller.validate_alpha(self.last_name_value)
        v_address = data_controller.validate_integer_alpha(self.address_value)
        v_postcode = data_controller.validate_integer_alpha(self.postcode_value)
        v_phone = data_controller.validate_integer(self.phone_value)
        v_email = data_controller.validate_email(self.email_value)

        if any(empty_elements_general):
            # If any element is empty in the list show message
            message = wx.MessageBox("All fields are required.", "Update Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_first_name:
            # If first name is invalid show message
            message = wx.MessageBox("Invalid first name.",
                                    "Update Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_last_name:
            # If last name is invalid show message
            message = wx.MessageBox("Invalid last name.",
                                    "Update Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_address:
            # If address is invalid show message
            message = wx.MessageBox("Invalid address.",
                                    "Update Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_postcode:
            # If postcode is invalid show message
            message = wx.MessageBox("Invalid postcode.",
                                    "Update Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_phone:
            # If phone number is invalid show message
            message = wx.MessageBox("Invalid phone number.",
                                    "Update Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_email:
            # If email is invalid show message
            message = wx.MessageBox("Invalid email.",
                                    "Update Tailor",
                                    style=wx.OK|wx.ICON_WARNING)
        else:
            # If user input is valid update tailor in database
            self.database.update_tailor(self.first_name_value,
                                        self.last_name_value,
                                        self.address_value,
                                        self.postcode_value,
                                        self.phone_value,
                                        self.email_value,
                                        self.tailor_id)

            # Show notification
            message = wx.MessageBox(("The tailor has been updated "
                                     "successfully."),
                                     "Update Tailor",
                                     style=wx.OK|wx.ICON_INFORMATION)

            # Update tailors list ctrl object and logger object
            self.top_panel.view_tailors()

            self.current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.message = ("[" + str(self.current_date_time) + "]" +
                            " - Tailor: " +
                            str(self.first_name_value) + " " +
                            str(self.last_name_value) + " " +
                            "has been updated successfully.")
            self.logger.Append((self.message))
