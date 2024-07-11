#-------------------------------------------------------------------------------
# Darie-Dragos Mitoiu
# SysOp v1.0.0 15/02/2019
# A system operator UI module designed for a tailoring and alterations business
#-------------------------------------------------------------------------------


# Importing libraries
import os
import wx
import wx.adv
import wx.lib.agw.customtreectrl as CT
import wx.lib.scrolledpanel as scrolled
import matplotlib as mpl
import loginwindow
import numpy.core._methods
import numpy.lib.format
from matplotlib.backends.backend_wxagg import FigureCanvasWxAgg as FigureCanvas
from matplotlib.backends.backend_wxagg import NavigationToolbar2WxAgg as ToolBar
from datetime import datetime
from datetime import timedelta
from database import Database
from controller import Controller


class SysOp(wx.Frame):
    """This class allow the creation of the system operator interface object,
       this class will act as a container for the other essential objects."""

    def __init__(self, master, user, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.user = user
        # Ignore warnings from wxpython
        self.logging = wx.LogNull()
        # Loading the window icon and converting the png image to icon format
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        # Creating the menu bar
        self.menu_bar = MenuBar(self)
        # Creating sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        # Creating splitter object
        self.splitter = wx.SplitterWindow(self)
        # Creating horizontal splitter object
        self.h_splitter = wx.SplitterWindow(self.splitter)
        # Creating left panel
        self.left_panel = LeftPanel(self.splitter,
                                    self,
                                    style=wx.SIMPLE_BORDER)
        # Creating top panel
        self.top_panel = RightTopPanel(self.h_splitter,
                                       self,
                                       self.user,
                                       self.left_panel,
                                       style=wx.SIMPLE_BORDER)
        # Getting the top panel tool bar
        self.top_panel_tool_bar = self.top_panel.tool_bar
        # Creating bottom panel
        self.bottom_panel = RightBottomPanel(self.h_splitter,
                                             self.top_panel)
        # Creating the logger attribute in the top panel
        self.top_panel.logger = self.bottom_panel.notebook.logger_panel.list_box
        # Splitting the window vertically
        # Placing the left panel on the left side of window,
        # placing the right panel on the right side of the window
        self.splitter.SplitVertically(self.left_panel, self.h_splitter)
        # Splitting the right panel in two horrizontal panels
        self.h_splitter.SplitHorizontally(self.top_panel, self.bottom_panel)
        # Setting the sash for the vertical splitter object
        self.splitter.SetSashPosition(220)
        self.splitter.SetMinimumPaneSize(20)
        # Setting the sash for the horizontal splitter object
        self.h_splitter.SetSashPosition(250)
        self.h_splitter.SetMinimumPaneSize(20)
        # Setting the window icon
        self.SetIcon(self.icon)
        # Setting the menu bar
        self.SetMenuBar(self.menu_bar)
        # Creating status bar object
        self.status_bar = StatusBar(self)
        # Setting status bar
        self.SetStatusBar(self.status_bar)
        # Adding the vertical splitter to the vertical sizer
        self.v_sizer.Add(self.splitter, 1, wx.EXPAND)
        # Setting window sizer
        self.SetSizer(self.v_sizer)
        # Center window
        self.Center()

    def set_customers_tree(self):
        """This method will set the behaviour for the customers item situated
           in the left panel under the database root of the tree ctrl."""

        # Loading the tool bar in top panel for the customers item
        self.top_panel_tool_bar.customers_tree()
        # Counting the records in the customer's list ctrl
        self.customers_count = self.top_panel.list_ctrl.GetItemCount()

        # Freezing the content in the top panel
        # This is done in order to reduce the "flickering" of the window
        # when objects are hidden and shown
        self.top_panel.Freeze()
        # Hidding others list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Loading the content from the customers table
        self.top_panel.view_customers()
        # Show customer list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer2)
        # Update panel content
        self.top_panel.Layout()
        # Resume panel after freeze
        self.top_panel.Thaw()

        # Update status bar
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.customers_count)),
                                       5)

    def set_tailors_tree(self):
        """This method will set the behaviour for the tailors item situated
           in the left panel under the database root of the tree ctrl."""

        # Loading the tool bar for the tailors item
        self.top_panel_tool_bar.tailors_tree()
        # Count records in the tailors list ctrl
        self.tailors_count = self.top_panel.list_ctrl_tailors.GetItemCount()

        # Freeze the top panel
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Show tailors list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer3)
        # Update panel content
        self.top_panel.Layout()
        # Resume panel
        self.top_panel.Thaw()

        # Update status bar
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.tailors_count)),
                                       5)

    def set_projects_tree(self):
        """This method will set the behaviour for the projects item situated
           in the left panel under the database root of the tree ctrl."""

        # Setting the tool bar for the projects item
        self.top_panel_tool_bar.projects_tree()
        # Count the records in the projects list ctrl
        self.projects_count = self.top_panel.list_ctrl_projects.GetItemCount()

        # Freeze the top panel
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Show projects list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer4)
        # Update top panel content
        self.top_panel.Layout()
        # Resume panel
        self.top_panel.Thaw()

        # Update status bar
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.projects_count)),
                                       5)

    def set_alterations_tree(self):
        """This method will set the behaviour for the alterations item situated
           in the left panel under the database root of the tree ctrl."""

        # Load the tool bar for the alterations item
        self.top_panel_tool_bar.alterations_tree()
        # Count the records in the alterations list ctrl
        self.a_table_count = self.top_panel.list_ctrl_alterations.GetItemCount()

        # Freeze the top panel
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
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
        """This method will set the behaviour for the active item situated
           in the left panel under the database root of the tree ctrl."""

        # Load the tool bar for the active item
        self.top_panel_tool_bar.active_tree()
        # Count the records in the active list ctrl
        self.active_count = self.top_panel.list_ctrl_active.GetItemCount()

        # Freeze the top panel
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer8)

        # Load records in the list ctrl
        self.top_panel.view_active()
        # Resize the columns based on the largest item in the list ctrl
        self.top_panel.list_ctrl_active.SetColumnWidth(0, 0)
        self.top_panel.list_ctrl_active.SetColumnWidth(1, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(2, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(3, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(4, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(5, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(6, -2)
        self.top_panel.list_ctrl_active.SetColumnWidth(7, -2)

        # Show the active list ctrl
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
        """This method will set the behaviour for the completed item situated
           in the left panel under the database root of the tree ctrl."""

        # Load the tool bar for the completed item in the tree ctrl
        self.top_panel_tool_bar.completed_tree()
        # Count the records in the list ctrl
        self.completed_count = self.top_panel.list_ctrl_completed.GetItemCount()

        # Freeze the top panel
        self.top_panel.Freeze()
        # Hide list ctrls
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer2)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer3)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer4)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer5)
        self.top_panel.v_sizer.Hide(self.top_panel.h_sizer7)

        # Load records in the list ctrl
        self.top_panel.view_completed()
        # Resize the columns based on the largest item in the list ctrl
        self.top_panel.list_ctrl_completed.SetColumnWidth(0, 0)
        self.top_panel.list_ctrl_completed.SetColumnWidth(1, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(2, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(3, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(4, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(5, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(6, -2)
        self.top_panel.list_ctrl_completed.SetColumnWidth(7, -2)

        # Show list ctrl
        self.top_panel.v_sizer.Show(self.top_panel.h_sizer8)
        # Update top panel content
        self.top_panel.Layout()
        # Resume top panel
        self.top_panel.Thaw()

        # Update status bar
        self.status_bar.SetStatusText(("Records Count: " +
                                       str(self.completed_count)),
                                       5)

class MenuBar(wx.MenuBar):
    """This class will allow the creation of the menu bar object."""

    def __init__(self, controller, *args, **kwargs):
        wx.MenuBar.__init__(self, *args, **kwargs)
        self.controller = controller
        self.build()

    def build(self):
        """This class will allow the creation of widgets."""

        # Creating menu bar options
        # Create file object
        self.file_menu = FileMenu()
        # Create edit object
        self.edit_menu = EditMenu()
        # Create options object
        self.options_menu = OptionsMenu()
        # Creating help object
        self.help_menu = HelpMenu(self, self.controller)

        # Appending objects to the menu bar
        self.Append(self.file_menu, "File")
        self.Append(self.edit_menu, "Edit")
        self.Append(self.options_menu, "Options")
        self.Append(self.help_menu, "Help")

class FileMenu(wx.Menu):
    """This class will allow the creation of a menu bar item."""

    def __init__(self):
        wx.Menu.__init__(self)
        self.build()

    def build(self):
        """This method will allow the creation of widgets for the file item."""

        # Appending options to the file item
        self.Append(wx.ID_OPEN, "Open\tCTRL+O")
        self.Append(wx.ID_EXIT, "Exit\tCTRL+Q")

class EditMenu(wx.Menu):
    """This class will allow the creation of a menu bar item."""

    def __init__(self):
        wx.Menu.__init__(self)
        self.build()

    def build(self):
        """This method will allow the creation of widgets for the edit item."""

        # Appending options to the edit item
        self.Append(wx.ID_COPY, "Copy\tCTRL+C")
        self.Append(wx.ID_CUT, "Cut\tCTRL+X")

class OptionsMenu(wx.Menu):
    """This class will allow the creation of a menu bar item."""

    def __init__(self):
        wx.Menu.__init__(self)
        self.build()

    def build(self):
        """This method will allow the creation of widgets for the options item.
        """

        # Appending options
        self.Append(wx.ID_PREFERENCES, "Preferences\tCTRL+P",
                    "Show preferences dialog")
        self.Append(wx.ID_SETUP, "Setup Guide\tCTRL+G",
                    "Show setup guide dialog")

class HelpMenu(wx.Menu):
    """This class will allow the creation of a menu bar item."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Menu.__init__(self, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.build()

    def build(self):
        """This method will allow the creation of widgets for the help item."""

        # Appending options
        self.help = self.Append(wx.ID_HELP,
                                "pyTailor++ Help",
                                "Show help dialog")
        self.about = self.Append(wx.ID_ABOUT,
                                 "pyTailor++ About")

        # Binding methods to the options
        self.controller.Bind(wx.EVT_MENU, self.about_dialog, self.about)

    def about_dialog(self, event):
        """This method will open the about dialog."""

        # Create about dialog object
        self.about_window = AboutDialog()

class HelpDocumentation(wx.Frame):
    """This class will allow the creation of a help window object,
       this feature is not available yet and also this feature is not part of
       the functional requirements."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Creating the main panel
        self.main_panel = HelpPanel(self)
        # Center the window
        self.Center()

class HelpPanel(wx.Panel):
    """This class allows the creation of the help panel object."""

    def __init__(self, master, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.build()

    def build(self):
        """This method allows the creation of the panel's widgets."""

        # Creating vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)

        # Loading the setting the window icon
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.master.SetIcon(self.icon)

        # Adding widgets to the sizers
        self.v_sizer.Add(self.h_sizer1, 1, wx.EXPAND)

        # Setting sizer
        self.SetSizer(self.v_sizer)

class AboutDialog(wx.adv.AboutDialogInfo):
    """This class allow the creation of about dialog object."""

    def __init__(self, *args, **kwargs):
        wx.adv.AboutDialogInfo.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method allows the creation of the about dialog's widgets."""

        # Loading and setting the dialog logo
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/about_logo.png",
                                           wx.BITMAP_TYPE_PNG))
        self.SetIcon(self.icon)
        # Setting program's details
        self.SetName("pyTailor++")
        self.SetVersion("1.0.0")
        self.SetDescription("Tailoring and Alterations Software")
        self.SetCopyright("(C) Darie-Dragos Mitoiu")
        self.SetWebSite("https://nescol.ac.uk")

        # Show dialog
        wx.adv.AboutBox(self)

class StatusBar(wx.StatusBar):
    """This class will allow the creation of the status bar object."""

    def __init__(self, *args, **kwargs):
        wx.StatusBar.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will allow the creation of the status bar's widgets."""

        # Getting the current date
        self.current_month = datetime.now()
        # Setting the date in the format Month-Year
        self.month = self.current_month.strftime("%B-%Y")

        # Adding 6 status bar fields
        self.SetFieldsCount(6)
        # Set dimensions for status bar fields
        # The size increases when the number in the list increases too
        self.SetStatusWidths([-2, -1, -2, -1, -1, -1])
        # Adding status bar text
        self.SetStatusText(("Permission Level: System Operator"), 2)
        self.SetStatusText(("Session: " + str(self.month)), 3)
        self.SetStatusText(("Position: 0"), 4)
        self.SetStatusText(("Records Count: 0"), 5)

        # Create font object
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        # Setting status bar font
        self.SetFont(self.font)

class LeftPanel(wx.Panel):
    """This class will allow the creation of the left panel object."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.build()

    def build(self):
        """This method will allow the creation of the left panel's widgets."""

        # Creating vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)

        # Creating tree ctrl object
        self.tree = LeftTreeCtrl(self, style=wx.NO_BORDER|
                                             wx.TR_DEFAULT_STYLE|
                                             wx.TR_TWIST_BUTTONS|
                                             wx.TR_NO_LINES|
                                             wx.TR_FULL_ROW_HIGHLIGHT)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.tree, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer1, 1, wx.EXPAND)

        # Binding a method on the tree ctrl object for the item changed event
        self.tree.Bind(wx.EVT_TREE_SEL_CHANGED, self.on_select_tree)

        # Focus the left panel when the window is created
        self.SetFocus()

        # Set panel sizer
        self.SetSizer(self.v_sizer)

    def on_select_tree(self, event):
        """This method will run whenever an item is selected in
           the tree ctrl object."""

        # If the tree is selected
        if self.tree:
            # Get selection
            self.selection = event.GetItem()
            # Get the selection's string
            self.selection_string = self.tree.GetItemText(self.selection)

            # Assign the system operator object to a new variable,
            # this assigning is done in order to simplify things and
            # in order to access the methods of the system operator object.
            self.sys_op = self.controller

            # If database item is selected, do nothing
            if self.selection_string == "Database":
                pass
            if self.selection_string == "Customers":
                # If customers item is selected set the customers tree
                self.sys_op.set_customers_tree()
            if self.selection_string == "Tailors":
                # If the tailors item is selected set the tailors tree
                self.sys_op.set_tailors_tree()
            if self.selection_string == "Projects":
                # If the projects item is selected set the project tree
                self.sys_op.set_projects_tree()
            if self.selection_string == "Alterations":
                # If the alterations item is selected set the alterations tree
                self.sys_op.set_alterations_tree()
            if self.selection_string == "Active":
                # If the active item is selected set the active tree
                self.sys_op.set_active_tree()
            if self.selection_string == "Completed":
                # If the completed item is selected set the completed tree
                self.sys_op.set_completed_tree()

            print self.selection_string

class RightTopPanel(wx.Panel):
    """This class will allow the creation of the top panel object."""

    # Declaring class variables
    current_dir = os.getcwd()

    def __init__(self, master, controller, user, left_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.user = user
        self.left_panel = left_panel
        # Creating database object
        self.database = Database((RightTopPanel.current_dir +
                                  "/database/business.accdb"),
                                  "admin", "pyTailor++")
        self.selected_customer = None
        self.selected_tailor = None
        self.selected_project = None
        self.selected_alteration = None
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Creating vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer8 = wx.BoxSizer(wx.HORIZONTAL)

        # Creating tool bar object
        self.tool_bar = RightToolBar(self,
                                     self,
                                     style=wx.TB_FLAT|wx.TB_NODIVIDER)
        # Show tool bar
        self.tool_bar.Realize()

        # Create customers list ctrl
        self.list_ctrl = CustomersListCtrl(self,
                                           style=wx.LC_REPORT)
        # Binding methods to select record event,
        # deselect record event and on column drag event
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.get_customer)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.deselect_customer)
        self.list_ctrl.Bind(wx.EVT_LIST_COL_BEGIN_DRAG, self.on_column_drag)

        # Creating tailors list ctrl
        self.list_ctrl_tailors = TailorsListCtrl(self,
                                                 style=wx.LC_REPORT)
        # Binding methods to select record event,
        # deselect record event and on column drag event
        self.list_ctrl_tailors.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                    self.get_tailor)
        self.list_ctrl_tailors.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                                    self.deselect_tailor)
        self.list_ctrl_tailors.Bind(wx.EVT_LIST_COL_BEGIN_DRAG,
                                    self.on_column_drag)

        # Create projects list ctrl
        self.list_ctrl_projects = ProjectsListCtrl(self,
                                                   style=wx.LC_REPORT)
        # Binding methods to select record event,
        # deselect record event and on column drag event
        self.list_ctrl_projects.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                     self.get_project)
        self.list_ctrl_projects.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                                     self.deselect_project)
        self.list_ctrl_projects.Bind(wx.EVT_LIST_COL_BEGIN_DRAG,
                                     self.on_column_drag)

        # Create alterations list ctrl
        self.list_ctrl_alterations = AlterationsListCtrl(self,
                                                         style=wx.LC_REPORT)
        # Binding methods to select record event,
        # deselect record event and on column drag event
        self.list_ctrl_alterations.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                        self.get_alteration)
        self.list_ctrl_alterations.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                                        self.deselect_alteration)
        self.list_ctrl_alterations.Bind(wx.EVT_LIST_COL_BEGIN_DRAG,
                                        self.on_column_drag)

        # Creating active list ctrl
        self.list_ctrl_active = ProjectsListCtrl(self,
                                                 style=wx.LC_REPORT)
        # Binding method to on column drag event
        self.list_ctrl_active.Bind(wx.EVT_LIST_COL_BEGIN_DRAG,
                                   self.on_column_drag)

        # Create completed list ctrl
        self.list_ctrl_completed = ProjectsListCtrl(self,
                                                    style=wx.LC_REPORT)
        # Binding method to on column drag event
        self.list_ctrl_completed.Bind(wx.EVT_LIST_COL_BEGIN_DRAG,
                                      self.on_column_drag)

        # Bind method to the left panel's tree ctrl
        self.left_panel.tree.Bind(wx.EVT_TREE_SEL_CHANGING,
                                  self.clear_tree_selection)

        # Creating label objects and setting a font to them
        self.welcome_label = wx.StaticText(self, label="HELLO, ")
        self.username_label = wx.StaticText(self, label=(self.user.upper()))
        self.font = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.welcome_label.SetFont(self.font)
        self.username_label.SetFont(self.font)

        # Loading the log out image and creating the log out button
        self.log_out_bitmap = wx.Bitmap("images/log_out_red.png")
        self.log_out_button = wx.BitmapButton(self, wx.ID_ANY,
                                              bitmap = self.log_out_bitmap)

        # Setting text on hover event for the log out button
        self.log_out_button.SetToolTip("Logout")
        # Binding the log out method to the log out button
        self.log_out_button.Bind(wx.EVT_BUTTON, self.on_button_log_out)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.tool_bar, 1, wx.EXPAND)
        self.h_sizer1.Add(self.welcome_label, 0, wx.ALIGN_BOTTOM)
        self.h_sizer1.Add(self.username_label, 0, wx.ALIGN_BOTTOM)
        self.h_sizer1.Add(self.log_out_button, 0, wx.LEFT|wx.ALIGN_BOTTOM, 10)
        self.h_sizer2.Add(self.list_ctrl, 1, wx.EXPAND)
        self.h_sizer3.Add(self.list_ctrl_tailors, 1, wx.EXPAND)
        self.h_sizer4.Add(self.list_ctrl_projects, 1, wx.EXPAND)
        self.h_sizer5.Add(self.list_ctrl_alterations, 1, wx.EXPAND)
        self.h_sizer7.Add(self.list_ctrl_active, 1, wx.EXPAND)
        self.h_sizer8.Add(self.list_ctrl_completed, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer1, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer2, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer3, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer4, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer5, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer7, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer8, 1, wx.EXPAND)

        # Hiding list ctrls
        self.v_sizer.Hide(self.h_sizer3)
        self.v_sizer.Hide(self.h_sizer4)
        self.v_sizer.Hide(self.h_sizer5)
        self.v_sizer.Hide(self.h_sizer7)
        self.v_sizer.Hide(self.h_sizer8)

        # Loading data from database and inserting it in the list ctrls
        self.view_customers()
        self.view_tailors()
        self.view_projects()
        self.view_alterations()
        self.view_active()
        self.view_completed()

        # Setting sizer
        self.SetSizer(self.v_sizer)

    def view_customers(self):
        """This method will load the data from customers table and
           insert it in the customer listr ctrl."""

        # Getting data from database
        customers_data = self.database.view_customers()

        # Delete list ctrl content before adding the new data
        self.list_ctrl.DeleteAllItems()
        # Adding data in the list ctrl
        for row in customers_data:
            self.list_ctrl.Append((row[0], row[1],
                                   row[2], row[3],
                                   row[4], row[5],
                                   row[6]))

        # Resizing the columns to fit the largest item in the list ctrl
        self.list_ctrl.SetColumnWidth(0, 0)
        self.list_ctrl.SetColumnWidth(1, -2)
        self.list_ctrl.SetColumnWidth(2, -2)
        self.list_ctrl.SetColumnWidth(3, -2)
        self.list_ctrl.SetColumnWidth(4, -2)
        self.list_ctrl.SetColumnWidth(5, -2)
        self.list_ctrl.SetColumnWidth(6, -2)

    def on_column_drag(self, event):
        """This method will prevent the resizing of the column 0, this column
           contains the ID of each record in the database, this is done
           for better esthetics of the program, when a record will be deleted
           the ID order will stop making sense."""

        # If column 0 selected and dragged veto the event
        if event.Column == 0:
            event.Veto()

    def view_tailors(self):
        """This method will load the data from tailors table and insert it
           in the tailors list ctrl."""

        # Getting the tailors data from database
        tailors_data = self.database.view_tailors()

        # Clearing the tailors list ctrl
        self.list_ctrl_tailors.DeleteAllItems()
        # Adding data to list ctrl
        for row in tailors_data:
            self.list_ctrl_tailors.Append((row[0], row[1],
                                           row[2], row[3],
                                           row[4], row[5],
                                           row[6]))

        # Resizing the columns to fit the largest item in the list ctrl
        self.list_ctrl_tailors.SetColumnWidth(0, 0)
        self.list_ctrl_tailors.SetColumnWidth(1, -2)
        self.list_ctrl_tailors.SetColumnWidth(2, -2)
        self.list_ctrl_tailors.SetColumnWidth(3, -2)
        self.list_ctrl_tailors.SetColumnWidth(4, -2)
        self.list_ctrl_tailors.SetColumnWidth(5, -2)
        self.list_ctrl_tailors.SetColumnWidth(6, -2)

    def view_projects(self):
        """This method will load the data from the projects table and insert it
           in the projects list ctrl."""

        # Getting the projects data from database
        projects_data = self.database.view_projects()

        # Clearing the projects list ctrl
        self.list_ctrl_projects.DeleteAllItems()
        # Adding data to the list ctrl
        for row in projects_data:
            # Converting the date/time object returned from database to string
            self.s_d_format = row[5].strftime("%d/%m/%Y")
            self.d_d_format = row[6].strftime("%d/%m/%Y")
            self.list_ctrl_projects.Append((row[0], row[1],
                                            row[2], row[3],
                                            row[4], self.s_d_format,
                                            self.d_d_format, row[7]))

        # Resizing the list ctrl to fit the largest item in the list ctrl
        self.list_ctrl_projects.SetColumnWidth(0, 0)
        self.list_ctrl_projects.SetColumnWidth(1, -2)
        self.list_ctrl_projects.SetColumnWidth(2, -2)
        self.list_ctrl_projects.SetColumnWidth(3, -2)
        self.list_ctrl_projects.SetColumnWidth(4, -2)
        self.list_ctrl_projects.SetColumnWidth(5, -2)
        self.list_ctrl_projects.SetColumnWidth(6, -2)
        self.list_ctrl_projects.SetColumnWidth(7, -2)

    def view_alterations(self):
        """This method will load the data from the alterations table and
           insert it in the alterations list ctrl."""

        # Getting the alterations data from database
        alterations_data = self.database.view_alterations()

        # Clearing the alterations list ctrl
        self.list_ctrl_alterations.DeleteAllItems()
        # Adding data to the list ctrl
        for row in alterations_data:
            # Converting the date/time object returned from database to string
            self.s_d_format = row[5].strftime("%d/%m/%Y")
            self.d_d_format = row[6].strftime("%d/%m/%Y")
            self.list_ctrl_alterations.Append((row[0], row[1],
                                               row[2], row[3],
                                               row[4], self.s_d_format,
                                               self.d_d_format, row[7]))

        # Resizing the columns to fit the largest item in the list ctrl
        self.list_ctrl_alterations.SetColumnWidth(0, 0)
        self.list_ctrl_alterations.SetColumnWidth(1, -2)
        self.list_ctrl_alterations.SetColumnWidth(2, -2)
        self.list_ctrl_alterations.SetColumnWidth(3, -2)
        self.list_ctrl_alterations.SetColumnWidth(4, -2)
        self.list_ctrl_alterations.SetColumnWidth(5, -2)
        self.list_ctrl_alterations.SetColumnWidth(6, -2)
        self.list_ctrl_alterations.SetColumnWidth(7, -2)

    def view_active(self):
        """This method will read both projects and alterations tables from
           database in order to find what projects and alterations are active,
           once that is known the method will display them in the active
           list ctrl."""

        # Getting the projects and alterations from database
        self.a_p_data = self.database.get_all_projects()
        self.a_a_data = self.database.get_all_alterations()

        # Clear list ctrl
        self.list_ctrl_active.DeleteAllItems()
        for row in self.a_p_data:
            # Split the start date and the delivery date objects.
            self.start_date_split = row[5].strftime("%d/%m/%Y").split("/")
            self.delivery_date_split = row[6].strftime("%d/%m/%Y").split("/")

            # Getting the year of the dates
            self.start_date_year_format = (str(self.start_date_split[2]))
            self.delivery_date_year_format = (str(self.delivery_date_split[2]))

            # Creating date objects
            self.start_date = datetime(int(self.start_date_year_format),
                                       int(self.start_date_split[1]),
                                       int(self.start_date_split[0]))

            self.delivery_date = datetime(int(self.delivery_date_year_format),
                                          int(self.delivery_date_split[1]),
                                          int(self.delivery_date_split[0]))

            # Changing the date objects format to yyyy-mm-dd
            self.start_date_str = self.start_date.strftime("%Y-%m-%d")
            self.start_date_strp = self.start_date.strptime(self.start_date_str,
                                                            "%Y-%m-%d")

            self.del_date_str = self.delivery_date.strftime("%Y-%m-%d")
            self.del_date_strp = self.delivery_date.strptime(self.del_date_str,
                                                            "%Y-%m-%d")

            # Getting the current date as a string and as an object
            self.current_date_str = datetime.now().strftime("%Y-%m-%d")
            self.current_date_strp = datetime.strptime(self.current_date_str,
                                                       "%Y-%m-%d")

            # The following comparisons are done in order to verify
            # if the current project in the loop is active or not.

            # Comparing if the start date is smaller or equal
            # than the current date of the project
            # If the start date is greater than the current date
            # the record is not active so it cannot be added to the list
            self.s_c_compare = self.start_date_strp <= self.current_date_strp

            # Comparing if the current date is smaller or equal
            # than the delivery date
            # If the current date is greater than the delivery date
            # the record is not active so it cannot be added to the list
            self.c_d_compare = self.current_date_strp <= self.del_date_strp

            # If the start date is smaller or equal than the current date
            # Continue...
            if self.s_c_compare:
                # If current date smaller or equal than the delivery date
                # Continue...
                if self.c_d_compare:
                    # Converting the date objects to the format dd/mm/yyyy
                    self.s_d_format = row[5].strftime("%d/%m/%Y")
                    self.d_d_format = row[6].strftime("%d/%m/%Y")
                    # Adding data to the list ctrl
                    self.list_ctrl_active.Append((row[0], row[1],
                                                  row[2], row[3],
                                                  row[4], self.s_d_format,
                                                  self.d_d_format, row[7]))

        for row in self.a_a_data:
            # Split the date objects
            self.a_start_date_split = row[5].strftime("%d/%m/%Y").split("/")
            self.a_delivery_date_split = row[6].strftime("%d/%m/%Y").split("/")

            # Getting the years of the dates
            self.a_start_date_year_format = str(self.a_start_date_split[2])
            self.a_del_date_year_format = str(self.a_delivery_date_split[2])

            # Creating date objects
            self.a_start_date = datetime(int(self.a_start_date_year_format),
                                         int(self.a_start_date_split[1]),
                                         int(self.a_start_date_split[0]))

            self.a_delivery_date = datetime(int(self.a_del_date_year_format),
                                            int(self.a_delivery_date_split[1]),
                                            int(self.a_delivery_date_split[0]))

            # Changing the dates format
            self.a_start_str = self.a_start_date.strftime("%Y-%m-%d")
            self.a_start_strp = self.a_start_date.strptime(self.a_start_str,
                                                           "%Y-%m-%d")

            self.a_del_str = self.a_delivery_date.strftime("%Y-%m-%d")
            self.a_del_strp = self.a_delivery_date.strptime(self.a_del_str,
                                                            "%Y-%m-%d")

            # Getting the current date as a string and as an object
            self.a_current_date_str = datetime.now().strftime("%Y-%m-%d")
            self.a_current_strp = datetime.strptime(self.a_current_date_str,
                                                    "%Y-%m-%d")

            # The following comparisons are done in order to verify
            # if the current alteration in the loop is active or not.

            # Comparing if the start date is smaller or equal
            # than the current date of the alteration
            # If the start date is greater than the current date
            # the record is not active so it cannot be added to the list
            self.a_s_c_compare = self.a_start_strp <= self.a_current_strp

            # Comparing if the current date is smaller or equal
            # than the delivery date
            # If the current date is greater than the delivery date
            # the record is not active so it cannot be added to the list
            self.a_c_d_compare = self.a_current_strp <= self.a_del_strp

            # If the start date is smaller or equal than the current date
            # Continue...
            if self.a_s_c_compare:
                # If current date is smaller or equal than delivery date
                # Continue...
                if self.a_c_d_compare:
                    # Convert date objects to format dd/mm/yyyy
                    self.s_d_format = row[5].strftime("%d/%m/%Y")
                    self.d_d_format = row[6].strftime("%d/%m/%Y")
                    # Adding data to list ctrl
                    self.list_ctrl_active.Append((row[0], row[1],
                                                  row[2], row[3],
                                                  row[4], self.s_d_format,
                                                  self.d_d_format, row[7]))

        # Resizing columns to fit the largest item in the list ctrl
        self.list_ctrl_active.SetColumnWidth(0, 0)
        self.list_ctrl_active.SetColumnWidth(1, -2)
        self.list_ctrl_active.SetColumnWidth(2, -2)
        self.list_ctrl_active.SetColumnWidth(3, -2)
        self.list_ctrl_active.SetColumnWidth(4, -2)
        self.list_ctrl_active.SetColumnWidth(5, -2)
        self.list_ctrl_active.SetColumnWidth(6, -2)
        self.list_ctrl_active.SetColumnWidth(7, -2)

    def view_completed(self):
        """This method will read both projects and alterations tables from
           database in order to find what projects and alterations are complete,
           once that is known the method will display them in the completed
           list ctrl."""

        # Getting projects and alterations
        self.a_p_data = self.database.get_all_projects()
        self.a_a_data = self.database.get_all_alterations()

        # Clearing completed list ctrl
        self.list_ctrl_completed.DeleteAllItems()
        for row in self.a_p_data:
            # Splitting date objects
            self.start_date_split = row[5].strftime("%d/%m/%Y").split("/")
            self.delivery_date_split = row[6].strftime("%d/%m/%Y").split("/")

            # Getting the dates years
            self.start_date_year_format = str(self.start_date_split[2])
            self.delivery_date_year_format = str(self.delivery_date_split[2])

            # Converting the dates into objects
            self.start_date = datetime(int(self.start_date_year_format),
                                       int(self.start_date_split[1]),
                                       int(self.start_date_split[0]))

            self.delivery_date = datetime(int(self.delivery_date_year_format),
                                          int(self.delivery_date_split[1]),
                                          int(self.delivery_date_split[0]))

            self.start_date_str = self.start_date.strftime("%Y-%m-%d")
            self.start_date_strp = self.start_date.strptime(self.start_date_str,
                                                            "%Y-%m-%d")

            self.del_date_str = self.delivery_date.strftime("%Y-%m-%d")
            self.del_date_strp = self.delivery_date.strptime(self.del_date_str,
                                                            "%Y-%m-%d")

            # Getting the current date as a string and as an object
            self.current_date_str = datetime.now().strftime("%Y-%m-%d")
            self.current_date_strp = datetime.strptime(self.current_date_str,
                                                       "%Y-%m-%d")

            # The following comparisons are done in order to verify
            # if the current project in the loop is active or not.

            # Comparing if the start date is smaller or equal
            # than the current date of the project
            # If the start date is greater than the current date
            # the record is not active so it cannot be added to the list
            self.s_c_compare = self.start_date_strp <= self.current_date_strp

            # Comparing if the current date is smaller or equal
            # than the delivery date
            # If the current date is greater than the delivery date
            # the record is not active so it cannot be added to the list
            self.c_d_compare = self.current_date_strp >= self.del_date_strp

            # If the start date is smaller or equal than the current date
            # Continue...
            if self.s_c_compare:
                # If current date is greater or equal than the delivery date
                # Continue...
                if self.c_d_compare:
                    # Converting the dates object in the format dd/mm/yyyy
                    self.s_d_format = row[5].strftime("%d/%m/%Y")
                    self.d_d_format = row[6].strftime("%d/%m/%Y")
                    # Adding data to the list ctrl
                    self.list_ctrl_completed.Append((row[0], row[1],
                                                     row[2], row[3],
                                                     row[4], self.s_d_format,
                                                     self.d_d_format, row[7]))

        for row in self.a_a_data:
            # Split the date objects
            self.a_start_date_split = row[5].strftime("%d/%m/%Y").split("/")
            self.a_delivery_date_split = row[6].strftime("%d/%m/%Y").split("/")

            # Get the dates years
            self.a_start_date_year_format = str(self.a_start_date_split[2])
            self.a_del_date_year_format = str(self.a_delivery_date_split[2])

            # Create date objects
            self.a_start_date = datetime(int(self.a_start_date_year_format),
                                         int(self.a_start_date_split[1]),
                                         int(self.a_start_date_split[0]))

            self.a_delivery_date = datetime(int(self.a_del_date_year_format),
                                            int(self.a_delivery_date_split[1]),
                                            int(self.a_delivery_date_split[0]))

            self.a_start_str = self.a_start_date.strftime("%Y-%m-%d")
            self.a_start_strp = self.a_start_date.strptime(self.a_start_str,
                                                           "%Y-%m-%d")

            self.a_del_str = self.a_delivery_date.strftime("%Y-%m-%d")
            self.a_del_strp = self.a_delivery_date.strptime(self.a_del_str,
                                                            "%Y-%m-%d")

            # Getting the current date as a string and as an object
            self.a_current_date_str = datetime.now().strftime("%Y-%m-%d")
            self.a_current_strp = datetime.strptime(self.a_current_date_str,
                                                    "%Y-%m-%d")

            # The following comparisons are done in order to verify
            # if the current alteration in the loop is active or not.

            # Comparing if the start date is smaller or equal
            # than the current date of the alteration
            # If the start date is greater than the current date
            # the record is not active so it cannot be added to the list
            self.a_s_c_compare = self.a_start_strp <= self.a_current_strp

            # Comparing if the current date is smaller or equal
            # than the delivery date
            # If the current date is greater than the delivery date
            # the record is not active so it cannot be added to the list
            self.a_c_d_compare = self.a_current_strp >= self.a_del_strp

            # If the start date is smaller or equal than the current date
            # Continue...
            if self.a_s_c_compare:
                # If current date is greater or equal than the delivery date
                # Continue...
                if self.a_c_d_compare:
                    # Convert date object format to dd/mm/yyyy
                    self.s_d_format = row[5].strftime("%d/%m/%Y")
                    self.d_d_format = row[6].strftime("%d/%m/%Y")
                    # Adding data to the list ctrl
                    self.list_ctrl_completed.Append((row[0], row[1],
                                                     row[2], row[3],
                                                     row[4], self.s_d_format,
                                                     self.d_d_format, row[7]))

        # Resizing the columns to fit the largest item in the list ctrl
        self.list_ctrl_completed.SetColumnWidth(0, 0)
        self.list_ctrl_completed.SetColumnWidth(1, -2)
        self.list_ctrl_completed.SetColumnWidth(2, -2)
        self.list_ctrl_completed.SetColumnWidth(3, -2)
        self.list_ctrl_completed.SetColumnWidth(4, -2)
        self.list_ctrl_completed.SetColumnWidth(5, -2)
        self.list_ctrl_completed.SetColumnWidth(6, -2)
        self.list_ctrl_completed.SetColumnWidth(7, -2)

    def get_customer(self, event):
        """This method will get run whenever a customer is selected,
           the objective of this method is to get the customer's ID
           from column 0."""

        try:
            # Get selected record
            self.selected_customer = self.list_ctrl.GetFocusedItem()
            # Get customer's ID
            self.customer = self.list_ctrl.GetItemText(self.selected_customer,
                                                       col=0)
            # Get record's position in the list ctrl
            self.position_customer = int(self.selected_customer) + 1

            # Update status bar
            self.controller.SetStatusText(("Position: " +
                                           str(self.position_customer)), 4)
        except:
            pass

    def get_tailor(self, event):
        """This method will get run whenever a tailor is selected,
           the objective of this method is to get the customer's ID
           from column 0."""

        try:
            # Assign the tailors list ctrl to a new variable
            self.list_tailors = self.list_ctrl_tailors
            # Get the selected record
            self.selected_tailor = self.list_ctrl_tailors.GetFocusedItem()
            # Get the tailor's ID
            self.tailor = self.list_tailors.GetItemText(self.selected_tailor,
                                                        col=0)
            # Increasing position by 1
            self.position_tailor = int(self.selected_tailor) + 1

            # Update status bar
            self.controller.SetStatusText(("Position: " +
                                           str(self.position_tailor)), 4)
        except:
            pass

    def get_project(self, event):
        """This method will get run whenever a project is selected,
           the objective of this method is to get the customer's ID
           from column 0."""

        try:
            # Assign the projects list ctrl to a new variable
            self.list_projects = self.list_ctrl_projects
            # Get selected record
            self.selected_project = self.list_ctrl_projects.GetFocusedItem()
            # Get project ID
            self.project = self.list_projects.GetItemText(self.selected_project,
                                                          col=0)
            # Increase record's position by 1,
            # this is done because the first position is 0
            self.position_project = int(self.selected_project) + 1

            # Update status bar
            self.controller.SetStatusText(("Position: " +
                                           str(self.position_project)), 4)
        except:
            pass

    def get_alteration(self, event):
        """This method will get run whenever an alteration is selected,
           the objective of this method is to get the customer's ID
           from column 0."""

        try:
            # Assign the alterations list ctrl to a new variable
            self.list_a = self.list_ctrl_alterations
            # Get the selected record
            self.selected_alteration = self.list_a.GetFocusedItem()
            # Get alteration ID
            self.alteration = self.list_a.GetItemText(self.selected_alteration,
                                                      col=0)
            # Increase record's position by 1
            self.position_alteration = int(self.selected_alteration) + 1

            # Update status bar
            self.controller.SetStatusText(("Position: " +
                                           str(self.position_alteration)), 4)
        except:
            pass

    def deselect_customer(self, event):
        """This method will run whenever a customer is deselected,
           the objective of this method is to reset the data
           in the bottom panel."""

        # Set the selected customer to None
        self.selected_customer = None

    def deselect_tailor(self, event):
        """This method will run whenever a tailor is deselected,
           the objective of this method is to reset the data
           in the bottom panel."""

        # Set the selected tailor to None
        self.selected_tailor = None

    def deselect_project(self, event):
        """This method will run whenever a project is deselected,
           the objective of this method is to reset the data
           in the bottom panel."""

        # Set the selected project to None
        self.selected_project = None

    def deselect_alteration(self, event):
        """This method will run whenever an alteration is deselected,
           the objective of this method is to reset the data
           in the bottom panel."""

        # Set the selected alteration to None
        self.selected_alteration = None

    def clear_tree_selection(self, event):
        """This method will run whenever the tree ctrl is deselected,
           the objective of this method is to reset the data in the
           bottom panel."""

        # Loop over all list ctrls and deselect all items.
        for x in range(0, self.list_ctrl.GetItemCount()):
            self.list_ctrl.Select(x, on=0)

        for x in range(0, self.list_ctrl_tailors.GetItemCount()):
            self.list_ctrl_tailors.Select(x, on=0)

        for x in range(0, self.list_ctrl_projects.GetItemCount()):
            self.list_ctrl_projects.Select(x, on=0)

        for x in range(0, self.list_ctrl_alterations.GetItemCount()):
            self.list_ctrl_alterations.Select(x, on=0)

        for x in range(0, self.list_ctrl_active.GetItemCount()):
            self.list_ctrl_active.Select(x, on=0)

        for x in range(0, self.list_ctrl_completed.GetItemCount()):
            self.list_ctrl_completed.Select(x, on=0)

    def on_button_log_out(self, event):
        """This method will run whenever the log out button is pressed,
           the objective of this method is to close the main window and
           open the log in window."""

        # Closing the main window
        self.controller.Close()
        # Creating the log in window object and showing it.
        self.log_in_frame = loginwindow.LogInWindow(None,
                                                    title="pyTailor++",
                                                    size=(800,350))
        self.log_in_frame.Show()

class RightBottomPanel(wx.Panel):
    """This class will allow the creation of the bottom panel object,
       this object will act as a container for the other objects
       that will be placed inside."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Creating vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Creating notebook
        self.notebook = RightNotebook(self,
                                      self.controller)

        # Adding widgets to the sizers
        self.h_sizer.Add(self.notebook, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer, 1, wx.EXPAND)

        # Setting sizer
        self.SetSizer(self.v_sizer)

class LeftTreeCtrl(wx.TreeCtrl):
    """This class allows the creation of a tree ctrl object situated in the
       left panel, this class has the objective to allow the user to visualize
       the data inside the database."""

    def __init__(self, *args, **kwargs):
        wx.TreeCtrl.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method allows the creation of the tree ctrl items."""

        # Creating font object
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        # Adding the root
        self.root = self.AddRoot("Database")

        # Adding items to the root
        self.customers = self.AppendItem(self.root, "Customers")
        self.tailors = self.AppendItem(self.root, "Tailors")
        self.projects = self.AppendItem(self.root, "Projects")
        self.alterations = self.AppendItem(self.root, "Alterations")
        self.active = self.AppendItem(self.root, "Active")
        self.completed = self.AppendItem(self.root, "Completed")

        # Creating a image list with dimensions 20x20
        self.image_list = wx.ImageList(20, 20)

        # loading images
        self.database_bitmap = wx.Bitmap("images/database.png",
                                        wx.BITMAP_TYPE_PNG)
        self.customers_bitmap = wx.Bitmap("images/customer.png",
                                          wx.BITMAP_TYPE_PNG)
        self.tailors_bitmap = wx.Bitmap("images/tailor.png",
                                        wx.BITMAP_TYPE_PNG)
        self.projects_bitmap = wx.Bitmap("images/projects.png",
                                         wx.BITMAP_TYPE_PNG)
        self.alterations_bitmap = wx.Bitmap("images/alterations.png",
                                         wx.BITMAP_TYPE_PNG)
        self.active_bitmap = wx.Bitmap("images/active.png",
                                          wx.BITMAP_TYPE_PNG)
        self.completed_bitmap = wx.Bitmap("images/completed.png",
                                          wx.BITMAP_TYPE_PNG)

        # Adding images to the list
        self.database_image = self.image_list.Add(self.database_bitmap)
        self.customers_image = self.image_list.Add(self.customers_bitmap)
        self.tailors_image = self.image_list.Add(self.tailors_bitmap)
        self.projects_image = self.image_list.Add(self.projects_bitmap)
        self.alterations_image = self.image_list.Add(self.alterations_bitmap)
        self.completed_image = self.image_list.Add(self.completed_bitmap)
        self.active_image = self.image_list.Add(self.active_bitmap)

        # Assigning image list
        self.AssignImageList(self.image_list)

        # Setting the root's image and the items images
        self.SetItemImage(self.root, self.database_image)
        self.SetItemImage(self.customers, self.customers_image)
        self.SetItemImage(self.tailors, self.tailors_image)
        self.SetItemImage(self.projects, self.projects_image)
        self.SetItemImage(self.alterations, self.alterations_image)
        self.SetItemImage(self.completed, self.completed_image)
        self.SetItemImage(self.active, self.active_image)

        # Expanding the root
        self.Expand(self.root)
        # Setting the cursor icon to be a hand
        self.SetCursor(wx.Cursor(wx.CURSOR_HAND))
        # Setting tree ctrl font
        self.SetFont(self.font)

class CustomersListCtrl(wx.ListCtrl):
    """This class will allow the creation of the customers list ctrl."""

    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will allow the creation of the list ctrl columns."""

        # Creating font object and setting it.
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.SetFont(self.font)

        # Inserting columns
        self.InsertColumn(0, "ID")
        self.InsertColumn(1, "First Name")
        self.InsertColumn(2, "Last Name")
        self.InsertColumn(3, "Address")
        self.InsertColumn(4, "Postcode")
        self.InsertColumn(5, "Phone")
        self.InsertColumn(6, "Email")

        # Setting columns width to fit the largest item in the list,
        # This will also resize the headers to fit the text inside.
        self.SetColumnWidth(0, -2)
        self.SetColumnWidth(1, -2)
        self.SetColumnWidth(2, -2)
        self.SetColumnWidth(3, -2)
        self.SetColumnWidth(4, -2)
        self.SetColumnWidth(5, -2)
        self.SetColumnWidth(6, -2)

class TailorsListCtrl(wx.ListCtrl):
    """This class will allow the creation of the tailors list ctrl object."""

    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will allow the creation of the list ctrl columns."""

        # Creating the font object and setting it
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.SetFont(self.font)

        # Inserting columns and setting width
        self.InsertColumn(0, "ID")
        self.InsertColumn(1, "First Name")
        self.InsertColumn(2, "Last Name")
        self.InsertColumn(3, "Address")
        self.InsertColumn(4, "Postcode")
        self.InsertColumn(5, "Phone")
        self.InsertColumn(6, "Email")
        self.SetColumnWidth(0, -2)
        self.SetColumnWidth(1, -2)
        self.SetColumnWidth(2, -2)
        self.SetColumnWidth(3, -2)
        self.SetColumnWidth(4, -2)
        self.SetColumnWidth(5, -2)
        self.SetColumnWidth(6, -2)

class ProjectsListCtrl(wx.ListCtrl):
    """This class will allow the creation of the projects list ctrl object."""

    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will allow the creation of the list ctrl columns."""

        # Creating the font object and setting it
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.SetFont(self.font)

        # Inserting columns and setting the width
        self.InsertColumn(0, "ID")
        self.InsertColumn(1, "Name")
        self.InsertColumn(2, "Product")
        self.InsertColumn(3, "Material")
        self.InsertColumn(4, "Colour")
        self.InsertColumn(5, "Start Date")
        self.InsertColumn(6, "Delivery Date")
        self.InsertColumn(7, "Price")
        self.SetColumnWidth(0, -2)
        self.SetColumnWidth(1, -2)
        self.SetColumnWidth(2, -2)
        self.SetColumnWidth(3, -2)
        self.SetColumnWidth(4, -2)
        self.SetColumnWidth(5, -2)
        self.SetColumnWidth(6, -2)
        self.SetColumnWidth(7, -2)

class AlterationsListCtrl(wx.ListCtrl):
    """This class allows the creation of the alterations list ctrl object."""

    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method allows the creation of the columns of the list ctrl."""

        # Creating the font object and setting it
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.SetFont(self.font)

        # Inserting the columns and setting the width
        self.InsertColumn(0, "ID")
        self.InsertColumn(1, "Name")
        self.InsertColumn(2, "Product")
        self.InsertColumn(3, "Material")
        self.InsertColumn(4, "Colour")
        self.InsertColumn(5, "Start Date")
        self.InsertColumn(6, "Delivery Date")
        self.InsertColumn(7, "Price")
        self.SetColumnWidth(0, -2)
        self.SetColumnWidth(1, -2)
        self.SetColumnWidth(2, -2)
        self.SetColumnWidth(3, -2)
        self.SetColumnWidth(4, -2)
        self.SetColumnWidth(5, -2)
        self.SetColumnWidth(6, -2)
        self.SetColumnWidth(7, -2)

class RightToolBar(wx.ToolBar):
    """This class allows the creation of the tool bar object situated in the
       top panel, this class has the objective to allow the user to access
       the main features of the program like: add, update, delete, search and
       preferences (the preferences feature is not part of the functional
       requirements)."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.ToolBar.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.build()

    def build(self):
        """This class allows the creation of the tool bar objects."""

        # Ignoring warnings from wxpython
        self.logging = wx.LogNull()

        # Adding tools to the tool bar
        self.add_tool = self.AddTool(wx.ID_ADD, "Add",
                                     wx.Bitmap("images/add_file.png"))
        self.edit_tool = self.AddTool(wx.ID_EDIT, "Update",
                                      wx.Bitmap("images/update_file.png"))
        self.delete_tool = self.AddTool(wx.ID_DELETE, "Delete",
                                        wx.Bitmap("images/delete_file.png"))
        self.search_tool = self.AddTool(wx.ID_FIND, "Search",
                                        wx.Bitmap("images/search_file.png"))
        self.AddSeparator()
        self.preferences_tool = self.AddTool(wx.ID_PREFERENCES, "Preferences",
                                             wx.Bitmap("images/wheel.png"))

        # Setting text on hover for tool bar tools
        self.SetToolShortHelp(wx.ID_ADD, "Add Record")
        self.SetToolShortHelp(wx.ID_EDIT, "Update Record")
        self.SetToolShortHelp(wx.ID_DELETE, "Delete Record")
        self.SetToolShortHelp(wx.ID_FIND, "Search Record")
        self.SetToolShortHelp(wx.ID_PREFERENCES, "Preferences")

        # Binding methods to the tools
        self.Bind(wx.EVT_TOOL, self.on_button_add_customer, self.add_tool)
        self.Bind(wx.EVT_TOOL, self.on_button_update_customer, self.edit_tool)
        self.Bind(wx.EVT_TOOL, self.on_button_delete_customer, self.delete_tool)
        self.Bind(wx.EVT_TOOL, self.on_button_search_customer, self.search_tool)
        self.Bind(wx.EVT_TOOL, self.on_button_preferences, self.preferences_tool)

    def customers_tree(self):
        """This method will set the tool bar for the customers tree ctrl item,
           this method has the objective to change the access to the tool bar
           features."""

        # Setting tools
        self.EnableTool(wx.ID_ADD, True)
        self.EnableTool(wx.ID_EDIT, True)
        self.EnableTool(wx.ID_DELETE, True)
        self.EnableTool(wx.ID_FIND, True)

        # Binding the methods which will allow the manipulation of the
        # customers table in the database.
        self.Bind(wx.EVT_TOOL, self.on_button_add_customer, self.add_tool)
        self.Bind(wx.EVT_TOOL, self.on_button_update_customer, self.edit_tool)
        self.Bind(wx.EVT_TOOL, self.on_button_delete_customer, self.delete_tool)
        self.Bind(wx.EVT_TOOL, self.on_button_search_customer, self.search_tool)

    def tailors_tree(self):
        """This method will set the tool bar for the tailors tree ctrl item,
           this method has the objective to change the access to the tool bar
           features."""

        # Setting tools
        self.EnableTool(wx.ID_ADD, False)
        self.EnableTool(wx.ID_EDIT, False)
        self.EnableTool(wx.ID_DELETE, False)
        self.EnableTool(wx.ID_FIND, True)

        # Binding the methods which will allow the manipulation of the
        # tailors table in the database.
        self.Bind(wx.EVT_TOOL, self.on_button_search_tailor, self.search_tool)

    def projects_tree(self):
        """This method will set the tool bar for the projects tree ctrl item,
           this method has the objective to change the access to the tool bar
           features."""

        # Setting tools
        self.EnableTool(wx.ID_ADD, True)
        self.EnableTool(wx.ID_EDIT, True)
        self.EnableTool(wx.ID_DELETE, False)
        self.EnableTool(wx.ID_FIND, True)

        # Binding the methods which will allow the manipulation of the
        # projects table in the database.
        self.Bind(wx.EVT_TOOL, self.on_button_add_project, self.add_tool)
        self.Bind(wx.EVT_TOOL, self.on_button_update_project, self.edit_tool)
        self.Bind(wx.EVT_TOOL, self.on_button_search_project, self.search_tool)

    def alterations_tree(self):
        """This method will set the tool bar for the alterations tree ctrl item,
           this method has the objective to change the access to the tool bar
           features."""

        # Setting tools
        self.EnableTool(wx.ID_ADD, True)
        self.EnableTool(wx.ID_EDIT, True)
        self.EnableTool(wx.ID_DELETE, False)
        self.EnableTool(wx.ID_FIND, True)

        # Binding the methods which will allow the manipulation of the
        # alterations table in the database.
        self.Bind(wx.EVT_TOOL, self.on_button_add_alteration, self.add_tool)
        self.Bind(wx.EVT_TOOL, self.on_button_update_alteration, self.edit_tool)
        self.Bind(wx.EVT_TOOL, self.on_button_search_alteration, self.search_tool)

    def active_tree(self):
        """This method will set the tool bar for the active tree ctrl item,
           this method has the objective to change the access to the tool bar
           features."""

        # Setting tools
        self.EnableTool(wx.ID_ADD, False)
        self.EnableTool(wx.ID_EDIT, False)
        self.EnableTool(wx.ID_DELETE, False)
        self.EnableTool(wx.ID_FIND, False)

    def completed_tree(self):
        """This method will set the tool bar for the alterations tree ctrl item,
           this method has the objective to change the access to the tool bar
           features."""

        # Setting tools
        self.EnableTool(wx.ID_ADD, False)
        self.EnableTool(wx.ID_EDIT, False)
        self.EnableTool(wx.ID_DELETE, False)
        self.EnableTool(wx.ID_FIND, False)

    def on_button_add_customer(self, event):
        """This method will allow the creation of the add customer window
           object, this class has the objective to add a new customer
           to database."""

        # Creating add customer window object and showing it
        self.add_customer_window = AddCustomer(None,
                                               self.controller,
                                               title="Add Customer",
                                               size=(1200, 500))
        self.add_customer_window.Show()

    def on_button_update_customer(self, event):
        """This method will allow the creation of the update customer window
           object, this class has the objective to update a customer
           in database."""

        # If a customer is selected open the update customer window object.
        if self.controller.selected_customer is not None:
            self.update_customer_window = UpdateCustomer(None,
                                                         self.controller,
                                                         title="Update Customer",
                                                         size=(1200, 500))
            self.update_customer_window.Show()
        else:
            # Show no record selected message
            message = wx.MessageBox("No record selected.", "Update Customer",
                                    style=wx.OK|wx.ICON_WARNING)

    def on_button_delete_customer(self, event):
        """This method will allow the creation of the delete customer window
           object, this class has the objective to delete a customer
           from database."""

        # If a customer is selected open delete customer dialog
        if self.controller.selected_customer is not None:

            message = wx.MessageDialog(None,
                                       ("Are you sure you want to delete "
                                        "the selected record?"),
                                        "Delete Record",
                                        wx.YES_NO|wx.ICON_QUESTION)
            result = message.ShowModal()

            # If result is yes delete customer and deselect customer
            if result == wx.ID_YES:
                self.database = self.controller.database
                self.database.delete_customer(self.controller.customer)
                self.controller.view_customers()
                self.controller.selected_customer = None
            else:
                pass
        else:
            # Else show no record selected message
            message = wx.MessageBox("No record selected.",
                                    "Delete Customer",
                                    style=wx.OK|wx.ICON_WARNING)

    def on_button_search_customer(self, event):
        """This method will allow the creation of the search customer window
           object, this class has the objective to search a customer
           in database."""

        # Create search customer window object and show it
        self.search_customer_window = SearchCustomer(None,
                                                     self.controller,
                                                     title="Search Customer",
                                                     size=(1200, 500))
        self.search_customer_window.Show()

    def on_button_search_tailor(self, event):
        """This method will allow the creation of the search tailor window
           object, this class has the objective to search a tailor
           in database."""

        # Create the search tailor window object and show it
        self.search_tailor_window = SearchTailor(None,
                                                 self.controller,
                                                 title="Search Tailor",
                                                 size=(1200, 500))
        self.search_tailor_window.Show()

    def on_button_add_project(self, event):
        """This method will allow the creation of the add new project window
           object, this class has the objective to add a new project
           in database."""

        # Create add project window object and show it
        self.add_project_window = AddProject(None,
                                             self.controller,
                                             title="Add Project",
                                             size=(1550, 500))
        self.add_project_window.Show()

    def on_button_update_project(self, event):
        """This method will allow the creation of the update project window
           object, this class has the objective to update a project
           in database."""

        # If a project is selected open the update project window object
        if self.controller.selected_project is not None:
            self.update_project_window = UpdateProject(None,
                                                       self.controller,
                                                       title="Update Project",
                                                       size=(1550, 500))
            self.update_project_window.Show()
        else:
            # Else show no record selected message
            message = wx.MessageBox("No record selected.", "Update Project",
                                    style=wx.OK|wx.ICON_WARNING)

    def on_button_search_project(self, event):
        """This method will allow the creation of the search project window
           object, this class has the objective to search a project
           in database."""

        # Create the search project window object and show it
        self.search_project_window = SearchProject(None,
                                                   self.controller,
                                                   title="Search Project",
                                                   size=(1200, 500))
        self.search_project_window.Show()

    def on_button_add_alteration(self, event):
        """This method will allow the creation of the add a new alteration
           window object, this class has the objective to add a new alteration
           in database."""

        # Create the add a new alteration window object and show it
        self.add_alteration_window = AddAlteration(None,
                                                   self.controller,
                                                   title="Add Alteration",
                                                   size=(1550, 500))
        self.add_alteration_window.Show()

    def on_button_update_alteration(self, event):
        """This method will allow the creation of the update an alteration
           window object, this class has the objective to update an alteration
           in database."""

        # If an alteration is selected open the update alteration window object
        if self.controller.selected_alteration is not None:
            self.update_alteration_window = UpdateAlteration(None,
                                                             self.controller,
                                                             title=
                                                             "Update Alteration",
                                                             size=(1550, 500))
            self.update_alteration_window.Show()
        else:
            # Else show no record selected message
            message = wx.MessageBox("No record selected.", "Update Alteration",
                                    style=wx.OK|wx.ICON_WARNING)

    def on_button_search_alteration(self, event):
        """This method will allow the creation of the search alteration window
           object, this class has the objective to search an alteration
           in database."""

        # Create the search alteration window object and show it
        self.search_alteration_window = SearchAlteration(None,
                                                         self.controller,
                                                         title=
                                                         "Search Alteration",
                                                         size=(1200, 500))
        self.search_alteration_window.Show()

    def on_button_preferences(self, event):
        """This method will allow the creation of the preferences window
           object, this class has the objective to allow the user to select
           his/her own preferences for the program, this feature is not part
           of the functional requirements."""

        # Create the preferences window object and show it
        self.preferences_window = Preferences(None,
                                              self.controller,
                                              title="Preferences",
                                              size=(500, 500))
        self.preferences_window.Show()

class RightNotebook(wx.Notebook):
    """This class allows the creation of the notebook object situated in the
       bottom panel, this class has the objective to allow the user to access
       tabs like: general tab (contains customers data),
       requests tab (contains the customer's requests),
       statistics tab (contains information about the business progress),
       logger tab (contains information about the operations made)."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Notebook.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.build()

    def build(self):
        """This method allow the creation of the notebook's tabs."""

        # Creating panels, which will be placed inside tabs
        self.general_panel = GeneralPanel(self, self.controller)
        self.requests_panel = CustomersRequestsPanel(self,
                                                     self,
                                                     self.controller)
        self.graph_panel = GraphPanel(self,
                                      self,
                                      self.controller)
        self.logger_panel = LoggerPanel(self)

        # Adding tabs
        self.AddPage(self.general_panel, "General")
        self.AddPage(self.requests_panel, "Requests")
        self.AddPage(self.graph_panel, "Statistics")
        self.AddPage(self.logger_panel, "Logger")

        # Creating font object
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        # Creating image list with dimensions 32x32
        self.image_list = wx.ImageList(32, 32)
        # Adding images to the list
        self.page_one_image = self.image_list.Add(wx.Bitmap("images/info.png",
                                                            wx.BITMAP_TYPE_PNG))
        self.page_two_image = self.image_list.Add(wx.Bitmap("images/request.png",
                                                            wx.BITMAP_TYPE_PNG))
        self.page_three_image = self.image_list.Add(wx.Bitmap("images/graph.png",
                                                            wx.BITMAP_TYPE_PNG))
        self.page_four_image = self.image_list.Add(wx.Bitmap("images/logger.png",
                                                            wx.BITMAP_TYPE_PNG))

        # Setting notebook's image list
        self.AssignImageList(self.image_list)

        # Setting tabs images
        self.SetPageImage(0, self.page_one_image)
        self.SetPageImage(1, self.page_two_image)
        self.SetPageImage(2, self.page_three_image)
        self.SetPageImage(3, self.page_four_image)

        # Setting notebook's font
        self.SetFont(self.font)

class GeneralPanel(wx.Panel):
    """This class allows the creation of the general panel object."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.build()

    def build(self):
        """This class allows the creation of the widgets of the panel object."""

        # Creating vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)

        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        # Creting label objects and the progress bar
        self.customer_label = wx.StaticText(self, label=" Customer: ")
        self.progress_label = wx.StaticText(self, label=" Progress: ")
        self.progress_bar = ProgressBar(self,
                                        style=wx.GA_HORIZONTAL|wx.GA_SMOOTH)
        self.progress_p = wx.StaticText(self,
                                        label="  ",
                                        size=(90, -1))

        # Creating the measurements panel, where the customer data will be shown
        self.measurements_panel = MeasurementsGeneralPanel(self,
                                                           self,
                                                           self.controller)

        # Creating the font objects
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.normal_font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        # Setting the labels font
        self.customer_label.SetFont(self.normal_font)
        self.progress_label.SetFont(self.normal_font)
        self.progress_p.SetFont(self.normal_font)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.customer_label, 0, wx.EXPAND)
        self.h_sizer2.Add(self.progress_label, 0, wx.EXPAND)
        self.h_sizer2.Add(self.progress_bar, 1, wx.EXPAND)
        self.h_sizer2.Add(self.progress_p, 0, wx.EXPAND)
        self.h_sizer3.Add(self.measurements_panel, 1, wx.EXPAND)

        self.v_sizer.Add(self.h_sizer1, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer2, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer3, 1, wx.EXPAND)

        # Setting the panel's sizer
        self.SetSizer(self.v_sizer)

        # Hidding the progress bar
        self.h_sizer2.Hide(self.progress_bar)
        # Update panel's content
        self.Layout()

class MeasurementsGeneralPanel(scrolled.ScrolledPanel):
    """This class will allow the creation of the customer's measurements panel
      object, this class has the objective to display the customer's data."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        scrolled.ScrolledPanel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Assigning the list ctrls from the top panel to new variables
        self.list_ctrl = self.top_panel.list_ctrl
        self.p_list_ctrl = self.top_panel.list_ctrl_projects
        self.a_list_ctrl = self.top_panel.list_ctrl_alterations
        self.active_list = self.top_panel.list_ctrl_active
        self.complete_list = self.top_panel.list_ctrl_completed
        self.database = self.top_panel.database
        self.project_name = None
        self.alteration_name = None
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Creating vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)

        # Creating the static box and the static box's sizer
        self.static_box = wx.StaticBox(self)
        self.static_sizer = wx.StaticBoxSizer(self.static_box, wx.VERTICAL)

        # Creating horizontal sizers
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer7 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer8 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer9 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer10 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer11 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer12 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer13 = wx.BoxSizer(wx.HORIZONTAL)

        # Binding new methods to the customer list ctrl,
        # also keeping the old ones
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
                            self.get_customer_data)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                            self.deselect_customer)

        # Binding new methods to the projects list ctrl,
        # also keeping the old ones
        self.p_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
                              self.get_project_customer_data)
        self.p_list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                              self.deselect_customer)

        # Binding new methods to the alterations list ctrl,
        # also keeping the old ones
        self.a_list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
                              self.get_alteration_customer_data)
        self.a_list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                              self.deselect_customer)

        # Binding new methods to the active list ctrl,
        # also keeping the old ones
        self.active_list.Bind(wx.EVT_LIST_ITEM_SELECTED,
                              self.get_active_customer_data)
        self.active_list.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                              self.deselect_customer)

        # Binding new methods to the completed list ctrl,
        # also keeping the old ones
        self.complete_list.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                self.get_complete_customer_data)
        self.complete_list.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                                self.deselect_customer)

        # Declaring the panel's labels
        self.upper_body_label = wx.StaticText(self, label="Upper Body")
        self.neck_label = wx.StaticText(self, label="Neck: ")
        self.chest_label = wx.StaticText(self, label="Chest: ")
        self.shoulders_label = wx.StaticText(self, label="Shoulders: ")
        self.sleeve_label = wx.StaticText(self, label="Sleeve: ")
        self.biceps_label = wx.StaticText(self, label="Biceps: ")
        self.wrist_label = wx.StaticText(self, label="Wrist: ")
        self.waist_label = wx.StaticText(self, label="Waist: ")
        self.hips_label = wx.StaticText(self, label="Hips: ")
        self.shirt_length_label = wx.StaticText(self, label="Shirt Length: ")

        self.lower_body_label = wx.StaticText(self, label="Lower Body")
        self.trouser_waist_label = wx.StaticText(self, label="Trouser Waist: ")
        self.trouser_outseam_label = wx.StaticText(self, label="Trouser Outseam: ")
        self.trouser_inseam_label = wx.StaticText(self, label="Trouser Inseam: ")
        self.crotch_label = wx.StaticText(self, label="Crotch: ")
        self.thigh_label = wx.StaticText(self, label="Thigh: ")
        self.knee_label = wx.StaticText(self, label="Knee: ")

        self.general_label = wx.StaticText(self, label="General")
        self.project_label = wx.StaticText(self, label="Project: ")
        self.alteration_label = wx.StaticText(self, label="Alteration: ")

        # Setting the background for headers
        self.upper_body_label.SetBackgroundColour((247,247,247))
        self.lower_body_label.SetBackgroundColour((247,247,247))
        self.general_label.SetBackgroundColour((247,247,247))

        # Creating the font objects
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.normal_font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        # Setting the labels fonts
        self.upper_body_label.SetFont(self.font)
        self.neck_label.SetFont(self.normal_font)
        self.chest_label.SetFont(self.normal_font)
        self.shoulders_label.SetFont(self.normal_font)
        self.sleeve_label.SetFont(self.normal_font)
        self.biceps_label.SetFont(self.normal_font)
        self.wrist_label.SetFont(self.normal_font)
        self.waist_label.SetFont(self.normal_font)
        self.hips_label.SetFont(self.normal_font)
        self.shirt_length_label.SetFont(self.normal_font)

        self.lower_body_label.SetFont(self.font)
        self.trouser_waist_label.SetFont(self.normal_font)
        self.trouser_outseam_label.SetFont(self.normal_font)
        self.trouser_inseam_label.SetFont(self.normal_font)
        self.crotch_label.SetFont(self.normal_font)
        self.thigh_label.SetFont(self.normal_font)
        self.knee_label.SetFont(self.normal_font)

        self.general_label.SetFont(self.font)
        self.project_label.SetFont(self.normal_font)
        self.alteration_label.SetFont(self.normal_font)

        # Adding widgets to the sizers
        self.h_sizer3.Add(self.upper_body_label, 1, wx.EXPAND)
        self.h_sizer4.Add(self.neck_label, 1, wx.EXPAND)
        self.h_sizer4.Add(self.chest_label, 1, wx.EXPAND)
        self.h_sizer4.Add(self.shoulders_label, 1, wx.EXPAND)
        self.h_sizer5.Add(self.sleeve_label, 1, wx.EXPAND)
        self.h_sizer5.Add(self.biceps_label, 1, wx.EXPAND)
        self.h_sizer5.Add(self.wrist_label, 1, wx.EXPAND)
        self.h_sizer6.Add(self.waist_label, 1, wx.EXPAND)
        self.h_sizer6.Add(self.hips_label, 1, wx.EXPAND)
        self.h_sizer6.Add(self.shirt_length_label, 1, wx.EXPAND)

        self.h_sizer7.Add(self.lower_body_label, 1, wx.EXPAND)
        self.h_sizer8.Add(self.trouser_waist_label, 1, wx.EXPAND)
        self.h_sizer8.Add(self.trouser_outseam_label, 1, wx.EXPAND)
        self.h_sizer8.Add(self.trouser_inseam_label, 1, wx.EXPAND)
        self.h_sizer9.Add(self.crotch_label, 1, wx.EXPAND)
        self.h_sizer9.Add(self.thigh_label, 1, wx.EXPAND)
        self.h_sizer9.Add(self.knee_label, 1, wx.EXPAND)
        self.h_sizer10.Add(self.general_label, 1, wx.EXPAND)
        self.h_sizer11.Add(self.project_label, 1, wx.EXPAND)
        self.h_sizer12.Add(self.alteration_label, 1, wx.EXPAND)

        # Adding horizontal sizers to the static sizer
        self.static_sizer.Add(self.h_sizer3, 0, wx.EXPAND)
        self.static_sizer.Add(self.h_sizer4, 0, wx.EXPAND)
        self.static_sizer.Add(self.h_sizer5, 0, wx.EXPAND)
        self.static_sizer.Add(self.h_sizer6, 0, wx.EXPAND)
        self.static_sizer.Add(self.h_sizer7, 0, wx.EXPAND)
        self.static_sizer.Add(self.h_sizer8, 0, wx.EXPAND)
        self.static_sizer.Add(self.h_sizer9, 0, wx.EXPAND)
        self.static_sizer.Add(self.h_sizer10, 0, wx.EXPAND)
        self.static_sizer.Add(self.h_sizer11, 0, wx.EXPAND)
        self.static_sizer.Add(self.h_sizer12, 0, wx.EXPAND)

        # Adding static sizer to the vertical sizer
        self.v_sizer.Add(self.static_sizer, 1, wx.EXPAND)

        # Setting the panel's sizer
        self.SetSizer(self.v_sizer)
        # Allow the panel to be scrollable
        self.SetupScrolling()

    def get_customer_data(self, event):
        """This method will run whenever a customer is selected in the customers
           list ctrl, the objective of this class is to get the customer's data
           from database and show it in the measurements panel, also this method
           has the role of calculating the progress made so far on the
           customer's project/alteration, the method will use the first
           project or alteration that is found in order to show the progress,
           for the progress made on a specific project or alteration, the
           projects and alterations items from tree ctrl should be used."""

        try:
            # Get selected record
            self.selected_customer = self.list_ctrl.GetFocusedItem()
            # Get customer's ID
            self.customer = self.list_ctrl.GetItemText(self.selected_customer,
                                                       col=0)

            # Get customer's data
            self.data = self.database.get_customer(self.customer)
            # Getting the project's data
            self.p_data = self.database.get_project_customer(self.customer)
            # Getting the alteration's data
            self.a_data = self.database.get_alteration_customer(self.customer)

            # If data is found for the project
            if self.p_data:
                # Get the project's data
                self.project_name = self.p_data[0][1]
                # Convert the date to the format dd/mm/yyyy
                self.p_start_date = self.p_data[0][5].strftime("%d/%m/%Y")
                self.p_delivery_date = self.p_data[0][6].strftime("%d/%m/%Y")
                # Split the dates
                self.start_date = self.p_start_date.split("/")
                self.delivery_date = self.p_delivery_date.split("/")
                # Change the dates format to dd-mm-yyyy
                self.start_date_format = (self.start_date[0] + "-" +
                                          self.start_date[1] + "-" +
                                          self.start_date[2])

                self.delivery_date_format = (self.delivery_date[0] + "-" +
                                             self.delivery_date[1] + "-" +
                                             self.delivery_date[2])

                # Create date objects
                self.d1 = datetime.strptime(self.start_date_format,
                                            "%d-%m-%Y")
                self.d2 = datetime.strptime(self.delivery_date_format,
                                            "%d-%m-%Y")

                # Get the current date as string and as an object
                self.current_date = datetime.now().strftime("%d-%m-%Y")
                self.current_date_strp = datetime.strptime(self.current_date,
                                                           "%d-%m-%Y")

                # Calculate the difference between start date and delivery date
                # This will result in a negative number which will be change
                # into a positive one, this number is the number of days
                self.difference = abs((self.d1 - self.d2).days)

                # Calculate how many days have been completed so far
                # (the number of days passed so far)
                self.complete = abs((self.d1 - self.current_date_strp).days)
                # Divide the completed number of days to the
                # total number of days between start date and delivery date
                self.percent_complete = (float(self.complete) /
                                         float(self.difference))
                # Multiply the result with 100 in order to show the progress
                self.adjust_percent = float(self.percent_complete) * 100.0

                # Set the result to 100 if the result is bigger than 100
                # No reason to show the percent over 100%
                if self.adjust_percent > 100:
                    self.adjust_percent = 100

                # Format the result
                self.progress_p_value = (" " +
                                         format(self.adjust_percent, ".2f") +
                                         " %")

                # Set the progress bar value (between 0-100)
                # Set the result after the progress bar
                self.controller.progress_bar.SetValue(int(self.adjust_percent))
                self.controller.progress_p.SetLabel(self.progress_p_value)

            # If alteration data found
            if self.a_data:
                # Get alteration's data
                self.alteration_name = self.a_data[0][1]
                # Get the alteration's dates in the format dd/mm/yyyy
                self.a_s_date_str = self.a_data[0][5].strftime("%d/%m/%Y")
                self.a_d_date_str = self.a_data[0][6].strftime("%d/%m/%Y")
                # Split the dates
                self.a_start_date = self.a_s_date_str.split("/")
                self.a_delivery_date = self.a_d_date_str.split("/")

                # Format the dates in the format dd-mm-yyyy
                self.a_start_date_format = (self.a_start_date[0] + "-" +
                                            self.a_start_date[1] + "-" +
                                            self.a_start_date[2])

                self.a_delivery_date_format = (self.a_delivery_date[0] + "-" +
                                               self.a_delivery_date[1] + "-" +
                                               self.a_delivery_date[2])

                # Create date objects
                self.a_d1 = datetime.strptime(self.a_start_date_format,
                                              "%d-%m-%Y")
                self.a_d2 = datetime.strptime(self.a_delivery_date_format,
                                              "%d-%m-%Y")

                # Getting the current date as a string and as an object
                self.a_current_date = datetime.now().strftime("%d-%m-%Y")
                self.a_curr_date_strp = datetime.strptime(self.a_current_date,
                                                          "%d-%m-%Y")

                # Calculate the difference between start date and delivery date
                self.a_difference = abs((self.a_d1 - self.a_d2).days)
                # Calculate the difference between start date and current date
                self.a_complete = abs((self.a_d1 - self.a_curr_date_strp).days)
                # Divide the completed number of days to the total number of
                # days in order to find the days passed so far
                self.a_percent_complete = (float(self.a_complete) /
                                           float(self.a_difference))
                # Multiply the result with 100
                self.a_adjust_percent = float(self.a_percent_complete) * 100.0

                # If result bigger than 100% set it to 100
                if self.a_adjust_percent > 100:
                    self.a_adjust_percent = 100

                # Format result
                self.a_progress_p_value = (" " +
                                          format(self.a_adjust_percent, ".2f") +
                                          " %")

                # Set progress bar value and label
                self.controller.progress_bar.SetValue(int(self.a_adjust_percent))
                self.controller.progress_p.SetLabel(self.a_progress_p_value)


            # Getting the customer's data from database
            # The customer's name and the customer's measurements
            self.customer_name = (str(self.data[0][1]) + " " +
                                  str(self.data[0][2]))
            self.neck_value = self.data[0][7]
            self.chest_value = self.data[0][8]
            self.shoulders_value = self.data[0][9]
            self.sleeve_value = self.data[0][10]
            self.biceps_value = self.data[0][11]
            self.wrist_value = self.data[0][12]
            self.waist_value = self.data[0][13]
            self.hips_value = self.data[0][14]
            self.shirt_length_value = self.data[0][15]

            self.trouser_waist_value = self.data[0][16]
            self.trouser_outseam_value = self.data[0][17]
            self.trouser_inseam_value = self.data[0][18]
            self.crotch_value = self.data[0][19]
            self.thigh_value = self.data[0][20]
            self.knee_value = self.data[0][21]

            # Updating the labels inside the measurements panel
            self.controller.customer_label.SetLabel((" Customer: ") +
                                                     str(self.customer_name))

            self.controller.h_sizer2.Show(self.controller.progress_bar)

            self.neck_label.SetLabel(("Neck:\t\t" +
                                      str(self.neck_value)))
            self.chest_label.SetLabel(("Chest:\t\t\t" +
                                       str(self.chest_value)))
            self.shoulders_label.SetLabel(("Shoulders:\t\t" +
                                          str(self.shoulders_value)))
            self.sleeve_label.SetLabel(("Sleeve:\t\t" +
                                        str(self.sleeve_value)))
            self.biceps_label.SetLabel(("Biceps:\t\t\t" +
                                        str(self.biceps_value)))
            self.wrist_label.SetLabel(("Wrist:\t\t\t" +
                                       str(self.wrist_value)))
            self.waist_label.SetLabel(("Waist:\t\t" +
                                       str(self.waist_value)))
            self.hips_label.SetLabel(("Hips:\t\t\t" +
                                      str(self.hips_value)))
            self.shirt_length_label.SetLabel(("Shirt Length:\t\t" +
                                              str(self.shirt_length_value)))

            self.trouser_waist_label.SetLabel(("Trouser Waist:\t" +
                                               str(self.trouser_waist_value)))
            self.trouser_outseam_label.SetLabel(("Trouser Outseam:\t" +
                                                str(self.trouser_outseam_value)))
            self.trouser_inseam_label.SetLabel(("Trouser Inseam:\t\t" +
                                                str(self.trouser_inseam_value)))
            self.crotch_label.SetLabel(("Crotch:\t\t" +
                                        str(self.crotch_value)))
            self.thigh_label.SetLabel(("Thigh:\t\t\t" +
                                       str(self.thigh_value)))
            self.knee_label.SetLabel(("Knee:\t\t\t" +
                                      str(self.knee_value)))
            self.project_label.SetLabel(("Project: " +
                                         str(self.project_name)))
            self.alteration_label.SetLabel(("Alteration: " +
                                            str(self.alteration_name)))

            # Update the panel's content
            self.Layout()
            # Update the controller panel content
            self.controller.Layout()

            # Look for futher binded events
            event.Skip()
        except:
            pass

    def get_project_customer_data(self, event):
        """This method will run whenever a project is selected in the list ctrl,
           the objective of this method is to show the customer's data in the
           measurements panel."""

        try:
            # Deselect customer
            self.deselect_customer(event)
            # Get the selected record
            self.selected_project = self.p_list_ctrl.GetFocusedItem()
            # Get the project's ID
            self.project = self.p_list_ctrl.GetItemText(self.selected_project,
                                                        col=0)

            # Getting the project's data and the customer's data
            self.p_data = self.database.get_project(self.project)
            self.data = self.database.get_customer(self.p_data[0][8])

            # If project data found continue...
            if self.p_data:
                # Getting the project's data
                self.project_name = self.p_data[0][1]
                # Converting the date objects to the format dd/mm/yyyy
                self.p_s_date_str = self.p_data[0][5].strftime("%d/%m/%Y")
                self.p_d_date_str = self.p_data[0][6].strftime("%d/%m/%Y")
                # Split the dates
                self.start_date = self.p_s_date_str.split("/")
                self.delivery_date = self.p_d_date_str.split("/")
                # Converting the dates to the foramt dd-mm-yyyy
                self.start_date_format = (self.start_date[0] + "-" +
                                          self.start_date[1] + "-" +
                                          self.start_date[2])

                self.delivery_date_format = (self.delivery_date[0] + "-" +
                                             self.delivery_date[1] + "-" +
                                             self.delivery_date[2])

                # Creating date objects
                self.d1 = datetime.strptime(self.start_date_format,
                                            "%d-%m-%Y")
                self.d2 = datetime.strptime(self.delivery_date_format,
                                            "%d-%m-%Y")

                # Getting the current date as a string and as an object
                self.current_date = datetime.now().strftime("%d-%m-%Y")
                self.current_date_strp = datetime.strptime(self.current_date,
                                                           "%d-%m-%Y")

                # Calculating difference between start date and delivery date
                self.difference = abs((self.d1 - self.d2).days)
                # Calculating the number of days passed so far
                self.complete = abs((self.d1 - self.current_date_strp).days)
                # Divide the number of days passed to the total number of days
                self.percent_complete = (float(self.complete) /
                                         float(self.difference))
                # Multiply the result with 100, in order to get a percent
                self.adjust_percent = float(self.percent_complete) * 100.0

                # If result is bigger than 100%, set it to 100
                if self.adjust_percent > 100:
                    self.adjust_percent = 100

                # Format the result
                self.progress_p_value = (" " +
                                         format(self.adjust_percent, ".2f") +
                                         " %")

                # Set the progress bar value and label
                self.controller.progress_bar.SetValue(int(self.adjust_percent))
                self.controller.progress_p.SetLabel(self.progress_p_value)

            # Getting the customer's data, the customer's name and measurements
            self.customer_name = (str(self.data[0][1]) + " " +
                                  str(self.data[0][2]))
            self.neck_value = self.data[0][7]
            self.chest_value = self.data[0][8]
            self.shoulders_value = self.data[0][9]
            self.sleeve_value = self.data[0][10]
            self.biceps_value = self.data[0][11]
            self.wrist_value = self.data[0][12]
            self.waist_value = self.data[0][13]
            self.hips_value = self.data[0][14]
            self.shirt_length_value = self.data[0][15]

            self.trouser_waist_value = self.data[0][16]
            self.trouser_outseam_value = self.data[0][17]
            self.trouser_inseam_value = self.data[0][18]
            self.crotch_value = self.data[0][19]
            self.thigh_value = self.data[0][20]
            self.knee_value = self.data[0][21]

            # Updating the labels in the measurements panel
            self.controller.customer_label.SetLabel((" Customer: ") +
                                                     str(self.customer_name))

            self.controller.h_sizer2.Show(self.controller.progress_bar)

            self.neck_label.SetLabel(("Neck:\t\t" +
                                      str(self.neck_value)))
            self.chest_label.SetLabel(("Chest:\t\t\t" +
                                       str(self.chest_value)))
            self.shoulders_label.SetLabel(("Shoulders:\t\t" +
                                          str(self.shoulders_value)))
            self.sleeve_label.SetLabel(("Sleeve:\t\t" +
                                        str(self.sleeve_value)))
            self.biceps_label.SetLabel(("Biceps:\t\t\t" +
                                        str(self.biceps_value)))
            self.wrist_label.SetLabel(("Wrist:\t\t\t" +
                                       str(self.wrist_value)))
            self.waist_label.SetLabel(("Waist:\t\t" +
                                       str(self.waist_value)))
            self.hips_label.SetLabel(("Hips:\t\t\t" +
                                      str(self.hips_value)))
            self.shirt_length_label.SetLabel(("Shirt Length:\t\t" +
                                              str(self.shirt_length_value)))

            self.trouser_waist_label.SetLabel(("Trouser Waist:\t" +
                                               str(self.trouser_waist_value)))
            self.trouser_outseam_label.SetLabel(("Trouser Outseam:\t" +
                                                str(self.trouser_outseam_value)))
            self.trouser_inseam_label.SetLabel(("Trouser Inseam:\t\t" +
                                                str(self.trouser_inseam_value)))
            self.crotch_label.SetLabel(("Crotch:\t\t" +
                                        str(self.crotch_value)))
            self.thigh_label.SetLabel(("Thigh:\t\t\t" +
                                       str(self.thigh_value)))
            self.knee_label.SetLabel(("Knee:\t\t\t" +
                                      str(self.knee_value)))
            self.project_label.SetLabel(("Project: " +
                                         str(self.project_name)))
            self.alteration_label.SetLabel(("Alteration: " +
                                            str(self.alteration_name)))

            # Update the panel's content
            self.Layout()
            # Update the controller's panel content
            self.controller.Layout()

            # look for further binded events
            event.Skip()
        except:
            pass

    def get_alteration_customer_data(self, event):
        """This method will run whenever an alteration is selected in the
           list ctrl, the objective of this method is to show the
           customer's data in the measurements panel."""

        try:
            # Deselect customer
            self.deselect_customer(event)
            # Get selected record
            self.selected_alteration = self.a_list_ctrl.GetFocusedItem()
            # Get alteration's ID
            self.alt = self.a_list_ctrl.GetItemText(self.selected_alteration,
                                                    col=0)

            # Get alteration's data and customer's data
            self.a_data = self.database.get_alteration(self.alt)
            self.data = self.database.get_customer(self.a_data[0][8])

            # If alteration data found continue...
            if self.a_data:
                # Get alteration's data
                self.alteration_name = self.a_data[0][1]
                # Convert the date to the format dd/mm/yyyy
                self.a_s_date_str = self.a_data[0][5].strftime("%d/%m/%Y")
                self.a_d_date_str = self.a_data[0][6].strftime("%d/%m/%Y")
                # Split the dates
                self.a_start_date = self.a_s_date_str.split("/")
                self.a_delivery_date = self.a_d_date_str.split("/")
                # Convert the dates in the format dd-mm-yyyy
                self.a_start_date_format = (self.a_start_date[0] + "-" +
                                            self.a_start_date[1] + "-" +
                                            self.a_start_date[2])

                self.a_delivery_date_format = (self.a_delivery_date[0] + "-" +
                                               self.a_delivery_date[1] + "-" +
                                               self.a_delivery_date[2])

                # Create date objects
                self.a_d1 = datetime.strptime(self.a_start_date_format,
                                              "%d-%m-%Y")
                self.a_d2 = datetime.strptime(self.a_delivery_date_format,
                                              "%d-%m-%Y")

                # Getting the current date as a string and as an object
                self.a_current_date = datetime.now().strftime("%d-%m-%Y")
                self.a_curr_date_strp = datetime.strptime(self.a_current_date,
                                                          "%d-%m-%Y")

                # Calculate difference between start date and delivery date
                self.a_difference = abs((self.a_d1 - self.a_d2).days)
                # Calculate the number of days completed so far
                self.a_complete = abs((self.a_d1 - self.a_curr_date_strp).days)
                # Divide the number of days passed to the total number of days
                self.a_percent_complete = (float(self.a_complete) /
                                           float(self.a_difference))
                # Multiply the result with 100, in order to get the percent
                self.a_adjust_percent = float(self.a_percent_complete) * 100.0

                # If the result is bigger than 100%, set it to 100%
                if self.a_adjust_percent > 100:
                    self.a_adjust_percent = 100

                # Format the result
                self.a_progress_p_value = (" " +
                                          format(self.a_adjust_percent, ".2f") +
                                          " %")

                # Set the progress bar value and label
                self.controller.progress_bar.SetValue(int(self.a_adjust_percent))
                self.controller.progress_p.SetLabel(self.a_progress_p_value)

            # Get the customer's data and the customer's measurements
            self.customer_name = (str(self.data[0][1]) + " " +
                                  str(self.data[0][2]))
            self.neck_value = self.data[0][7]
            self.chest_value = self.data[0][8]
            self.shoulders_value = self.data[0][9]
            self.sleeve_value = self.data[0][10]
            self.biceps_value = self.data[0][11]
            self.wrist_value = self.data[0][12]
            self.waist_value = self.data[0][13]
            self.hips_value = self.data[0][14]
            self.shirt_length_value = self.data[0][15]

            self.trouser_waist_value = self.data[0][16]
            self.trouser_outseam_value = self.data[0][17]
            self.trouser_inseam_value = self.data[0][18]
            self.crotch_value = self.data[0][19]
            self.thigh_value = self.data[0][20]
            self.knee_value = self.data[0][21]

            # Updating the measurements panel's labels
            self.controller.customer_label.SetLabel((" Customer: ") +
                                                     str(self.customer_name))

            self.controller.h_sizer2.Show(self.controller.progress_bar)

            self.neck_label.SetLabel(("Neck:\t\t" +
                                      str(self.neck_value)))
            self.chest_label.SetLabel(("Chest:\t\t\t" +
                                       str(self.chest_value)))
            self.shoulders_label.SetLabel(("Shoulders:\t\t" +
                                          str(self.shoulders_value)))
            self.sleeve_label.SetLabel(("Sleeve:\t\t" +
                                        str(self.sleeve_value)))
            self.biceps_label.SetLabel(("Biceps:\t\t\t" +
                                        str(self.biceps_value)))
            self.wrist_label.SetLabel(("Wrist:\t\t\t" +
                                       str(self.wrist_value)))
            self.waist_label.SetLabel(("Waist:\t\t" +
                                       str(self.waist_value)))
            self.hips_label.SetLabel(("Hips:\t\t\t" +
                                      str(self.hips_value)))
            self.shirt_length_label.SetLabel(("Shirt Length:\t\t" +
                                              str(self.shirt_length_value)))

            self.trouser_waist_label.SetLabel(("Trouser Waist:\t" +
                                               str(self.trouser_waist_value)))
            self.trouser_outseam_label.SetLabel(("Trouser Outseam:\t" +
                                                str(self.trouser_outseam_value)))
            self.trouser_inseam_label.SetLabel(("Trouser Inseam:\t\t" +
                                                str(self.trouser_inseam_value)))
            self.crotch_label.SetLabel(("Crotch:\t\t" +
                                        str(self.crotch_value)))
            self.thigh_label.SetLabel(("Thigh:\t\t\t" +
                                       str(self.thigh_value)))
            self.knee_label.SetLabel(("Knee:\t\t\t" +
                                      str(self.knee_value)))
            self.project_label.SetLabel(("Project: " +
                                         str(self.project_name)))
            self.alteration_label.SetLabel(("Alteration: " +
                                            str(self.alteration_name)))

            # Update the measurements panel content
            self.Layout()
            # Update the controller panel content
            self.controller.Layout()

            # Look for further binded events
            event.Skip()
        except:
            pass

    def get_active_customer_data(self, event):
        """This method will run whenever a project/alteration is selected
           in the active list ctrl, the objective of this method is to show
           the customer's data in the measurements panel."""

        try:
            # Deselect customer
            self.deselect_customer(event)
            # Get selected record
            self.selected_active = self.active_list.GetFocusedItem()
            # Get project/alteration ID
            self.active = self.active_list.GetItemText(self.selected_active,
                                                       col=0)
            # Get the project/alteration name
            self.name = self.active_list.GetItemText(self.selected_active,
                                                     col=1)

            # Search for an unique record
            self.act_data = self.database.get_projects_alterations(self.active,
                                                                   self.name,
                                                                   self.active,
                                                                   self.name)

            # Get the customer's data
            self.data = self.database.get_customer(self.act_data[0][8])

            # If project/alteration data is found continue...
            if self.act_data:
                # Get project/alteration data
                self.active_name = self.act_data[0][1]
                # Getting the dates in format dd/mm/yyyy
                self.active_s_date_str = self.act_data[0][5].strftime("%d/%m/%Y")
                self.active_d_date_str = self.act_data[0][6].strftime("%d/%m/%Y")
                # Split the dates
                self.active_start = self.active_s_date_str.split("/")
                self.active_delivery = self.active_d_date_str.split("/")
                # Convert the dates in format dd-mm-yyyy
                self.active_start_format = (self.active_start[0] + "-" +
                                            self.active_start[1] + "-" +
                                            self.active_start[2])

                self.active_delivery_format = (self.active_delivery[0] + "-" +
                                               self.active_delivery[1] + "-" +
                                               self.active_delivery[2])

                # Create date objects
                self.active_d1 = datetime.strptime(self.active_start_format,
                                                   "%d-%m-%Y")
                self.active_d2 = datetime.strptime(self.active_delivery_format,
                                                   "%d-%m-%Y")

                # Get current date
                self.active_current = datetime.now().strftime("%d-%m-%Y")
                self.active_curr_strp = datetime.strptime(self.active_current,
                                                          "%d-%m-%Y")

                # Calculate difference between start date and delivery date
                self.active_difference = abs((self.active_d1 -
                                              self.active_d2).days)

                # Calculate the days passed so far
                self.active_complete = abs((self.active_d1 -
                                            self.active_curr_strp).days)

                # Divide the days passed to the total number of days
                self.active_percent = (float(self.active_complete) /
                                       float(self.active_difference))

                # Multiply the result with 100
                self.active_adjust = float(self.active_percent) * 100.0

                # If result greater than 100, set result to 100%
                if self.active_adjust > 100:
                    self.active_adjust = 100

                # Format the result
                self.active_progress_p = (" " +
                                          format(self.active_adjust,
                                                 ".2f") +
                                          " %")

                # Setting the progress bar value and label
                self.controller.progress_bar.SetValue(int(self.active_adjust))
                self.controller.progress_p.SetLabel(self.active_progress_p)

            # Getting the customer's data
            self.customer_name = (str(self.data[0][1]) + " " +
                                  str(self.data[0][2]))
            self.neck_value = self.data[0][7]
            self.chest_value = self.data[0][8]
            self.shoulders_value = self.data[0][9]
            self.sleeve_value = self.data[0][10]
            self.biceps_value = self.data[0][11]
            self.wrist_value = self.data[0][12]
            self.waist_value = self.data[0][13]
            self.hips_value = self.data[0][14]
            self.shirt_length_value = self.data[0][15]

            self.trouser_waist_value = self.data[0][16]
            self.trouser_outseam_value = self.data[0][17]
            self.trouser_inseam_value = self.data[0][18]
            self.crotch_value = self.data[0][19]
            self.thigh_value = self.data[0][20]
            self.knee_value = self.data[0][21]

            # Updating the measurements panel labels
            self.controller.customer_label.SetLabel((" Customer: ") +
                                                     str(self.customer_name))

            self.controller.h_sizer2.Show(self.controller.progress_bar)

            self.neck_label.SetLabel(("Neck:\t\t" +
                                      str(self.neck_value)))
            self.chest_label.SetLabel(("Chest:\t\t\t" +
                                       str(self.chest_value)))
            self.shoulders_label.SetLabel(("Shoulders:\t\t" +
                                          str(self.shoulders_value)))
            self.sleeve_label.SetLabel(("Sleeve:\t\t" +
                                        str(self.sleeve_value)))
            self.biceps_label.SetLabel(("Biceps:\t\t\t" +
                                        str(self.biceps_value)))
            self.wrist_label.SetLabel(("Wrist:\t\t\t" +
                                       str(self.wrist_value)))
            self.waist_label.SetLabel(("Waist:\t\t" +
                                       str(self.waist_value)))
            self.hips_label.SetLabel(("Hips:\t\t\t" +
                                      str(self.hips_value)))
            self.shirt_length_label.SetLabel(("Shirt Length:\t\t" +
                                              str(self.shirt_length_value)))

            self.trouser_waist_label.SetLabel(("Trouser Waist:\t" +
                                               str(self.trouser_waist_value)))
            self.trouser_outseam_label.SetLabel(("Trouser Outseam:\t" +
                                                str(self.trouser_outseam_value)))
            self.trouser_inseam_label.SetLabel(("Trouser Inseam:\t\t" +
                                                str(self.trouser_inseam_value)))
            self.crotch_label.SetLabel(("Crotch:\t\t" +
                                        str(self.crotch_value)))
            self.thigh_label.SetLabel(("Thigh:\t\t\t" +
                                       str(self.thigh_value)))
            self.knee_label.SetLabel(("Knee:\t\t\t" +
                                      str(self.knee_value)))
            self.project_label.SetLabel(("Project: " +
                                         str(self.project_name)))
            self.alteration_label.SetLabel(("Alteration: " +
                                            str(self.alteration_name)))

            # Updating the measurements panel content
            self.Layout()
            # Update the controller panel's content
            self.controller.Layout()

            # Look for further binded events
            event.Skip()
        except:
            pass

    def get_complete_customer_data(self, event):
        """This method will run whenever a project/alteration is selected
           in the completed list ctrl, the objective of this method is to show
           the customer's data in the measurements panel."""

        try:
            # Deselect customer
            self.deselect_customer(event)
            # Get selected record
            self.selected_com = self.complete_list.GetFocusedItem()
            # Get project/alteration ID
            self.com = self.complete_list.GetItemText(self.selected_com,
                                                      col=0)

            # Get project/alteration name
            self.name = self.complete_list.GetItemText(self.selected_com,
                                                       col=1)

            # Search for an unique record
            self.com_data = self.database.get_projects_alterations(self.com,
                                                                   self.name,
                                                                   self.com,
                                                                   self.name)

            # Getting the customer's data
            self.data = self.database.get_customer(self.com_data[0][8])

            # If project/alteration data found continue...
            if self.com_data:
                # Getting the project/alteration data
                self.com_name = self.com_data[0][1]
                # Converting the date to the format dd/mm/yyyy
                self.com_s_date_str = self.com_data[0][5].strftime("%d/%m/%Y")
                self.com_d_date_str = self.com_data[0][6].strftime("%d/%m/%Y")
                # Split the dates
                self.com_start = self.com_s_date_str.split("/")
                self.com_delivery = self.com_d_date_str.split("/")
                # Convert the dates to the format dd-mm-yyyy
                self.com_start_format = (self.com_start[0] + "-" +
                                         self.com_start[1] + "-" +
                                         self.com_start[2])

                self.com_delivery_format = (self.com_delivery[0] + "-" +
                                            self.com_delivery[1] + "-" +
                                            self.com_delivery[2])

                # Create date objects
                self.com_d1 = datetime.strptime(self.com_start_format,
                                                "%d-%m-%Y")
                self.com_d2 = datetime.strptime(self.com_delivery_format,
                                                "%d-%m-%Y")

                # Getting the current date as a string and as an object
                self.com_current = datetime.now().strftime("%d-%m-%Y")
                self.com_curr_strp = datetime.strptime(self.com_current,
                                                       "%d-%m-%Y")

                # Calculate difference between start date and delivery date
                self.com_difference = abs((self.com_d1 -
                                           self.com_d2).days)

                # Calculate the number of days passed
                self.com_complete = abs((self.com_d1 -
                                         self.com_curr_strp).days)

                # Divide the number of days passed to the total number of days
                self.com_percent = (float(self.com_complete) /
                                    float(self.com_difference))

                # Multiply the result with 100
                self.com_adjust = float(self.com_percent) * 100.0

                # If result bigger than 100%, set it to 100
                if self.com_adjust > 100:
                    self.com_adjust = 100

                # Format the result
                self.com_progress_p = (" " +
                                       format(self.com_adjust, ".2f") +
                                       " %")

                # Setting the progress bar value and label
                self.controller.progress_bar.SetValue(int(self.com_adjust))
                self.controller.progress_p.SetLabel(self.com_progress_p)

            # Getting the customer's data
            self.customer_name = (str(self.data[0][1]) + " " +
                                  str(self.data[0][2]))
            self.neck_value = self.data[0][7]
            self.chest_value = self.data[0][8]
            self.shoulders_value = self.data[0][9]
            self.sleeve_value = self.data[0][10]
            self.biceps_value = self.data[0][11]
            self.wrist_value = self.data[0][12]
            self.waist_value = self.data[0][13]
            self.hips_value = self.data[0][14]
            self.shirt_length_value = self.data[0][15]

            self.trouser_waist_value = self.data[0][16]
            self.trouser_outseam_value = self.data[0][17]
            self.trouser_inseam_value = self.data[0][18]
            self.crotch_value = self.data[0][19]
            self.thigh_value = self.data[0][20]
            self.knee_value = self.data[0][21]

            # Updating the measurements panel labels
            self.controller.customer_label.SetLabel((" Customer: ") +
                                                     str(self.customer_name))

            self.controller.h_sizer2.Show(self.controller.progress_bar)

            self.neck_label.SetLabel(("Neck:\t\t" +
                                      str(self.neck_value)))
            self.chest_label.SetLabel(("Chest:\t\t\t" +
                                       str(self.chest_value)))
            self.shoulders_label.SetLabel(("Shoulders:\t\t" +
                                          str(self.shoulders_value)))
            self.sleeve_label.SetLabel(("Sleeve:\t\t" +
                                        str(self.sleeve_value)))
            self.biceps_label.SetLabel(("Biceps:\t\t\t" +
                                        str(self.biceps_value)))
            self.wrist_label.SetLabel(("Wrist:\t\t\t" +
                                       str(self.wrist_value)))
            self.waist_label.SetLabel(("Waist:\t\t" +
                                       str(self.waist_value)))
            self.hips_label.SetLabel(("Hips:\t\t\t" +
                                      str(self.hips_value)))
            self.shirt_length_label.SetLabel(("Shirt Length:\t\t" +
                                              str(self.shirt_length_value)))

            self.trouser_waist_label.SetLabel(("Trouser Waist:\t" +
                                               str(self.trouser_waist_value)))
            self.trouser_outseam_label.SetLabel(("Trouser Outseam:\t" +
                                                str(self.trouser_outseam_value)))
            self.trouser_inseam_label.SetLabel(("Trouser Inseam:\t\t" +
                                                str(self.trouser_inseam_value)))
            self.crotch_label.SetLabel(("Crotch:\t\t" +
                                        str(self.crotch_value)))
            self.thigh_label.SetLabel(("Thigh:\t\t\t" +
                                       str(self.thigh_value)))
            self.knee_label.SetLabel(("Knee:\t\t\t" +
                                      str(self.knee_value)))
            self.project_label.SetLabel(("Project: " +
                                         str(self.project_name)))
            self.alteration_label.SetLabel(("Alteration: " +
                                            str(self.alteration_name)))

            # Update the measurements panel content
            self.Layout()
            # Update the controller panel content
            self.controller.Layout()

            # Look for further binded events
            event.Skip()
        except:
            pass

    def deselect_customer(self, event):
        """This method will run whenever a customer, project or alteration
           is deselected, the objective of this method is to reset the labels
           inside the measurements panel."""

        # Reset the labels
        self.controller.customer_label.SetLabel((" Customer:"))
        self.controller.h_sizer2.Hide(self.controller.progress_bar)

        self.neck_label.SetLabel(("Neck:"))
        self.chest_label.SetLabel(("Chest:" ))
        self.shoulders_label.SetLabel(("Shoulders:"))
        self.sleeve_label.SetLabel(("Sleeve:"))
        self.biceps_label.SetLabel(("Biceps:"))
        self.wrist_label.SetLabel(("Wrist:"))
        self.waist_label.SetLabel(("Waist:"))
        self.hips_label.SetLabel(("Hips:"))
        self.shirt_length_label.SetLabel(("Shirt Length:"))

        self.trouser_waist_label.SetLabel(("Trouser Waist:"))
        self.trouser_outseam_label.SetLabel(("Trouser Outseam:"))
        self.trouser_inseam_label.SetLabel(("Trouser Inseam:"))
        self.crotch_label.SetLabel(("Crotch:"))
        self.thigh_label.SetLabel(("Thigh:"))
        self.knee_label.SetLabel(("Knee:"))

        self.project_label.SetLabel(("Project:"))
        self.alteration_label.SetLabel(("Alteration:"))
        self.project_name = None
        self.alteration_name = None

        self.controller.progress_bar.SetValue(0)
        self.controller.progress_p.SetLabel("  ")

        event.Skip()

class ProgressBar(wx.Gauge):
    """This class allows the creation of a progress bar object."""

    def __init__(self, *args, **kwargs):
        wx.Gauge.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        pass

class CustomersRequestsPanel(wx.Panel):
    """This class allows the creation of the requests panel situated inside
       the notebook, this class has the objective to show the requests made
       for each customer present in the database when a customer
       is selected in the customer's list ctrl."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        self.list_ctrl = self.top_panel.list_ctrl
        self.database = self.top_panel.database
        self.active_data = []
        self.status = None
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Creating the vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Binding methods to the list ctrl (customer's list ctrl, top panel)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED,
                            self.get_customer_data)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                            self.deselect_customer)

        # Create requests list ctrl
        self.c_list_ctrl = CustomersRequestsListCtrl(self, style=wx.LC_REPORT)

        # Adding widgets to the sizers
        self.h_sizer.Add(self.c_list_ctrl, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer, 1, wx.EXPAND)

        # Setting sizer
        self.SetSizer(self.v_sizer)

    def get_customer_data(self, event):
        """This method will run whenever a customer is selected in the
           customer's list ctrl, this method has the role to display
           the customer's requests."""

        try:
            # Get selected record
            self.selected_customer = self.list_ctrl.GetFocusedItem()
            # Get customer ID
            self.customer = self.list_ctrl.GetItemText(self.selected_customer,
                                                       col=0)

            # Get customer and project data
            self.c_data = self.database.get_customer(self.customer)
            self.p_data = self.database.get_project_customer(self.customer)

            # Verift if the requests are active
            # if not, set the status to completed
            self.get_active_data()
            if not self.active_data:
                self.status = "Completed"

            # Clear customer's list ctrl
            self.c_list_ctrl.DeleteAllItems()
            if self.p_data:
                # Get tailor data
                self.t_data = self.database.get_tailor(self.p_data[0][9])

                # Get customer name
                self.p_customer_name = (str(self.c_data[0][1]) + " " +
                                        str(self.c_data[0][2]))

                # Format tailor name
                self.p_tailor_name = (str(self.t_data[0][1]) + " " +
                                      str(self.t_data[0][2]))

                # Loop over the project data
                for row in self.p_data:
                    # Loop over the active data
                    for active in self.active_data:
                        # If project name in active list set status to active
                        # If project name not in active set status to completed
                        if row[1] == active:
                            self.status = "Active"
                        if row[1] not in self.active_data:
                            self.status = "Completed"

                    # Convert date to format dd/mm/yyyy
                    self.r_start_date = row[5].strftime("%d/%m/%Y")
                    self.r_del_date = row[6].strftime("%d/%m/%Y")
                    # Add project data to the requests list ctrl
                    self.c_list_ctrl.Append((row[1], row[2],
                                             row[3], row[4],
                                             self.r_start_date, self.r_del_date,
                                             row[7], self.p_customer_name,
                                             self.p_tailor_name, self.status))

            # Get alteration data
            self.a_data = self.database.get_alteration_customer(self.customer)

            # If alteration data found continue...
            if self.a_data:
                # Get tailor data
                self.t_a_data = self.database.get_tailor(self.a_data[0][9])

                # Format customer name
                self.a_customer_name = (str(self.c_data[0][1]) + " " +
                                        str(self.c_data[0][2]))

                # Format tailor name
                self.a_tailor_name = (str(self.t_a_data[0][1]) + " " +
                                      str(self.t_a_data[0][2]))

                # Loop over the alteration data
                for row in self.a_data:
                    # loop over active data
                    for active in self.active_data:
                        # If alteration name in active list set status to active
                        # If alteration name not in list set status to completed
                        if row[1] == active:
                            self.status = "Active"
                        if row[1] not in self.active_data:
                            self.status = "Completed"

                    # Format the date in the format dd/mm/yyyy
                    self.r_start_date = row[5].strftime("%d/%m/%Y")
                    self.r_del_date = row[6].strftime("%d/%m/%Y")
                    self.c_list_ctrl.Append((row[1], row[2],
                                             row[3], row[4],
                                             self.r_start_date, self.r_del_date,
                                             row[7], self.a_customer_name,
                                             self.a_tailor_name, self.status))

            # Set the columns width to fit the largest item in the list ctrl
            self.c_list_ctrl.SetColumnWidth(0, -2)
            self.c_list_ctrl.SetColumnWidth(1, -2)
            self.c_list_ctrl.SetColumnWidth(2, -2)
            self.c_list_ctrl.SetColumnWidth(3, -2)
            self.c_list_ctrl.SetColumnWidth(4, -2)
            self.c_list_ctrl.SetColumnWidth(5, -2)
            self.c_list_ctrl.SetColumnWidth(6, -2)
            self.c_list_ctrl.SetColumnWidth(7, -2)
            self.c_list_ctrl.SetColumnWidth(8, -2)
            self.c_list_ctrl.SetColumnWidth(9, -2)

            # Update panel's content
            self.Layout()

            # Look for further binded events
            event.Skip()
        except:
            pass

    def get_active_data(self):
        """This method will get active projects/alterations and
           add them in a list in order to sort them later on."""

        # Count the items in the active list ctrl
        self.active_count = self.top_panel.list_ctrl_active.GetItemCount()
        # loop that many times as items in the active list ctrl
        for row in range(self.active_count):
            # Add active project/alteration name to the active list
            self.active_item = self.top_panel.list_ctrl_active.GetItem(row,
                                                                       col=1)
            self.active_data.append(self.active_item.GetText())

    def deselect_customer(self, event):
        """This method will run whenever the customer is deselected."""

        # Clear requests list ctrl
        self.c_list_ctrl.DeleteAllItems()
        # Look for further binded events
        event.Skip()

class CustomersRequestsListCtrl(wx.ListCtrl):
    """This class will allow the creation of the customer listr ctrl object."""

    def __init__(self, *args, **kwargs):
        wx.ListCtrl.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will allow the creation of the columns."""

        # Create the font object and set it to the list ctrl
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.SetFont(self.font)

        # Insert the columns and set the width
        self.InsertColumn(0, "Name")
        self.InsertColumn(1, "Product")
        self.InsertColumn(2, "Material")
        self.InsertColumn(3, "Colour")
        self.InsertColumn(4, "Start Date")
        self.InsertColumn(5, "Delivery Date")
        self.InsertColumn(6, "Price")
        self.InsertColumn(7, "Customer")
        self.InsertColumn(8, "Tailor")
        self.InsertColumn(9, "Status")
        self.SetColumnWidth(0, -2)
        self.SetColumnWidth(1, -2)
        self.SetColumnWidth(2, -2)
        self.SetColumnWidth(3, -2)
        self.SetColumnWidth(4, -2)
        self.SetColumnWidth(5, -2)
        self.SetColumnWidth(6, -2)
        self.SetColumnWidth(7, -2)
        self.SetColumnWidth(8, -2)
        self.SetColumnWidth(9, -2)

class GraphPanel(wx.Panel):
    """This class will allow the creation of the graph panel object."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        self.database = self.top_panel.database
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Creating vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # Creating label object
        self.show_label = wx.StaticText(self, label="Show:")
        # Creating font object and setting it to the label
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.show_label.SetFont(self.font)

        # Creating label object
        self.resolution_label = wx.StaticText(self, label="Resolution:")
        self.resolution_label.SetFont(self.font)

        # Creating choices object
        self.choices = wx.Choice(self,
                                 choices=["Projects",
                                          "Alterations"])

        # Creating choices object
        self.choices_resolution = wx.Choice(self,
                                            choices=["1 Week",
                                                     "1 Month",
                                                     "3 Months"])

        # Creating button object
        self.analyse_button = wx.Button(self, label="Analyse")
        self.analyse_button.Bind(wx.EVT_BUTTON, self.on_button_analyse)

        # Creating plot object
        self.plot = Plot(self)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.show_label, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.choices, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.resolution_label, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.choices_resolution, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.analyse_button, 0, wx.ALL, 5)
        self.h_sizer2.Add(self.plot, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer1, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer2, 1, wx.EXPAND)

        # Setting sizer
        self.SetSizer(self.v_sizer)

    def draw_chart(self, x, y):
        """This method will allow the graph to be drawn."""

        try:
            # Create the chart object
            self.chart = self.plot.figure.add_subplot(111)
            # Clearing the chart,
            # this is done in order to prevend multiple line to be drawn
            self.chart.clear()
            # Plotting the graph (x and y axis must be equal)
            self.chart.plot(x, y)
            # Setting the labels
            self.chart.set_title("Statistics")
            self.chart.set_ylabel("Profit")
            # Draw the graph
            self.plot.canvas.draw()
        except:
            pass

    def on_button_analyse(self, event):
        """This method will allow the graph to be drawn, once the x and y axis
           are known, the x and y axis must be equal in order to draw the
           graph."""

        # Getting choices
        self.show_choices = self.choices.GetSelection()
        self.resolution_choices = self.choices_resolution.GetSelection()
        # Declaring x and y axis
        self.chart_dates = []
        self.chart_values = []

        if self.show_choices == 0 and self.resolution_choices == 0:

            # Getting the date of 1 week ago from the current date
            self.one_week_ago = (datetime.now() - timedelta(days=7)).date()

            # Creating date objects
            self.one_week_ago_str = self.one_week_ago.strftime("%d/%m/%Y")
            self.one_week_ago_strp = datetime.strptime(self.one_week_ago_str,
                                                       "%d/%m/%Y")
            self.current_date_str = datetime.now().strftime("%d/%m/%Y")
            self.current_date_strp = datetime.strptime(self.current_date_str,
                                                       "%d/%m/%Y")

            # Getting data
            self.data = self.database.get_projects_profit(self.one_week_ago_strp,
                                                          self.current_date_strp)

            for row in self.data:
                # Appending data to the axis
                self.chart_dates.append(row[0].strftime("%d/%m/%Y"))
                self.chart_values.append(row[1])

            # Assigning axis to new variables
            x = self.chart_dates
            y = self.chart_values
            # Draw chart
            self.draw_chart(x, y)

        if self.show_choices == 0 and self.resolution_choices == 1:

            # Getting the date of 1 month ago from the current date
            self.one_month_ago = (datetime.now() - timedelta(days=30)).date()

            # Creating date objects
            self.one_month_ago_str = self.one_month_ago.strftime("%d/%m/%Y")
            self.one_month_ago_strp = datetime.strptime(self.one_month_ago_str,
                                                        "%d/%m/%Y")
            self.current_date_str = datetime.now().strftime("%d/%m/%Y")
            self.current_date_strp = datetime.strptime(self.current_date_str,
                                                       "%d/%m/%Y")

            # Getting data
            self.data = self.database.get_projects_profit(self.one_month_ago_strp,
                                                          self.current_date_strp)

            for row in self.data:
                # Adding data to the axis lists
                self.chart_dates.append(row[0].strftime("%d/%m/%Y"))
                self.chart_values.append(row[1])

            # Assigning the axis to new variables
            x = self.chart_dates
            y = self.chart_values
            # Draw chart
            self.draw_chart(x, y)

        if self.show_choices == 0 and self.resolution_choices == 2:

            # Getting the date of 3 months ago from the current date
            self.three_m_ago = (datetime.now() - timedelta(days=90)).date()

            # Create date objects
            self.three_m_ago_str = self.three_m_ago.strftime("%d/%m/%Y")
            self.three_m_ago_strp = datetime.strptime(self.three_m_ago_str,
                                                      "%d/%m/%Y")
            self.current_date_str = datetime.now().strftime("%d/%m/%Y")
            self.current_date_strp = datetime.strptime(self.current_date_str,
                                                       "%d/%m/%Y")

            # Getting data
            self.data = self.database.get_projects_profit(self.three_m_ago_strp,
                                                          self.current_date_strp)

            for row in self.data:
                # Appending data to the axis lists
                self.chart_dates.append(row[0].strftime("%d/%m/%Y"))
                self.chart_values.append(row[1])

            # Assigning the axis to new variables
            x = self.chart_dates
            y = self.chart_values
            # Draw chart
            self.draw_chart(x, y)

        if self.show_choices == 1 and self.resolution_choices == 0:

            # Getting the date of 1 week ago from the current date
            self.one_week_ago = (datetime.now() - timedelta(days=7)).date()

            # Create date objects
            self.one_week_ago_str = self.one_week_ago.strftime("%d/%m/%Y")
            self.one_week_ago_strp = datetime.strptime(self.one_week_ago_str,
                                                       "%d/%m/%Y")
            self.current_date_str = datetime.now().strftime("%d/%m/%Y")
            self.current_date_strp = datetime.strptime(self.current_date_str,
                                                       "%d/%m/%Y")

            # Getting data
            self.data = self.database.get_a_profit(self.one_week_ago_strp,
                                                   self.current_date_strp)

            for row in self.data:
                # Appending data
                self.chart_dates.append(row[0].strftime("%d/%m/%Y"))
                self.chart_values.append(row[1])

            # Assigning axis to new variables
            x = self.chart_dates
            y = self.chart_values
            # Draw chart
            self.draw_chart(x, y)

        if self.show_choices == 1 and self.resolution_choices == 1:

            # Getting the date of 1 month ago from the current date
            self.one_month_ago = (datetime.now() - timedelta(days=30)).date()

            # Create date objects
            self.one_month_ago_str = self.one_month_ago.strftime("%d/%m/%Y")
            self.one_month_ago_strp = datetime.strptime(self.one_month_ago_str,
                                                        "%d/%m/%Y")
            self.current_date_str = datetime.now().strftime("%d/%m/%Y")
            self.current_date_strp = datetime.strptime(self.current_date_str,
                                                       "%d/%m/%Y")

            # Getting data
            self.data = self.database.get_a_profit(self.one_month_ago_strp,
                                                   self.current_date_strp)

            for row in self.data:
                # Appending data
                self.chart_dates.append(row[0].strftime("%d/%m/%Y"))
                self.chart_values.append(row[1])

            # Assigning axis to new variables
            x = self.chart_dates
            y = self.chart_values
            # Draw chart
            self.draw_chart(x, y)

        if self.show_choices == 1 and self.resolution_choices == 2:

            # Getting the date of 3 months ago from the current date
            self.three_m_ago = (datetime.now() - timedelta(days=90)).date()

            # Create date objects
            self.three_m_ago_str = self.three_m_ago.strftime("%d/%m/%Y")
            self.three_m_ago_strp = datetime.strptime(self.three_m_ago_str,
                                                      "%d/%m/%Y")
            self.current_date_str = datetime.now().strftime("%d/%m/%Y")
            self.current_date_strp = datetime.strptime(self.current_date_str,
                                                       "%d/%m/%Y")

            # Getting data
            self.data = self.database.get_a_profit(self.three_m_ago_strp,
                                                   self.current_date_strp)

            for row in self.data:
                # Appending data
                self.chart_dates.append(row[0].strftime("%d/%m/%Y"))
                self.chart_values.append(row[1])

            # Assigning axis to new variables
            x = self.chart_dates
            y = self.chart_values
            # Draw chart
            self.draw_chart(x, y)

class Plot(wx.Panel):
    """This class will allow the plot panel object to be created."""

    def __init__(self, master, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.build()

    def build(self):
        """This method will create the panels's widgets."""

        # Create vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)

        # Create figure and canvas objects
        self.figure = mpl.figure.Figure(dpi=100, figsize=(2, 2))
        self.canvas = FigureCanvas(self, -1, self.figure)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.canvas, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer1, 1, wx.EXPAND)

        # Setting the sizer
        self.SetSizer(self.v_sizer)

class LoggerPanel(wx.Panel):
    """This class will allow the logger's panel to be created."""

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will allow the panel's widgets to be created."""

        # Create vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer = wx.BoxSizer(wx.HORIZONTAL)

        # Create font object and setting list to the list box
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.list_box = LoggerListBox(self, style=wx.LB_MULTIPLE)
        self.list_box.SetFont(self.font)

        # Adding widgets to the sizers
        self.h_sizer.Add(self.list_box, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer, 1, wx.EXPAND)

        # Setting sizer
        self.SetSizer(self.v_sizer)

class LoggerListBox(wx.ListBox):
    """This class will allow the list box object to be created."""

    def __init__(self, *args, **kwargs):
        wx.ListBox.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will insert the initial text in the list box."""

        # Getting the current date and time and inserting it in the list box
        self.current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
        self.message = ("[" + str(self.current_date_time) + "]" +
                        " - New Session Started.")
        self.Append((self.message))

class AddCustomer(wx.Frame):
    """This class will allow the creation of the add customer window object. """

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel
        self.main_panel = AddCustomerPanel(self, self, self.controller)
        self.Center()

class AddCustomerPanel(wx.Panel):
    """This class will allow the creation of the add customer panel object."""

    # Declaring the class variables
    current_dir = os.getcwd()

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        self.logger = self.top_panel.logger
        # Create database object
        self.database = Database((AddCustomerPanel.current_dir +
                                  "/database/business.accdb"),
                                  "admin", "pyTailor++")
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets. """

        # Declaring vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)

        # Create static box objects and static box sizers objects
        self.static_box1 = wx.StaticBox(self)
        self.static_box2 = wx.StaticBox(self)
        self.static_sizer1 = wx.StaticBoxSizer(self.static_box1, wx.VERTICAL)
        self.static_sizer2 = wx.StaticBoxSizer(self.static_box2, wx.VERTICAL)

        # Horizontal sizers for the general interface elements
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer7 = wx.BoxSizer(wx.HORIZONTAL)

        # Horizontal sizers for the measurements interface elements
        self.h_sizer1_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer5_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer6_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer7_measurements = wx.BoxSizer(wx.HORIZONTAL)

        # Create icon object and set it to the master window
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.master.SetIcon(self.icon)

        # Declare label objects and create font objects
        self.title_label = wx.StaticText(self, label="Add Customer")
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
        self.first_name_entry = wx.TextCtrl(self, size=(250, -1))
        self.last_name_entry = wx.TextCtrl(self, size=(250, -1))
        self.address_entry = wx.TextCtrl(self, size=(250, -1))
        self.postcode_entry = wx.TextCtrl(self, size=(250, -1))
        self.phone_entry = wx.TextCtrl(self, size=(250, -1))
        self.email_entry = wx.TextCtrl(self, size=(250, -1))

        # Setting fonts to the labels
        self.first_name_label.SetFont(self.font_normal)
        self.last_name_label.SetFont(self.font_normal)
        self.address_label.SetFont(self.font_normal)
        self.postcode_label.SetFont(self.font_normal)
        self.phone_label.SetFont(self.font_normal)
        self.email_label.SetFont(self.font_normal)

        # Create label objects
        self.upper_body_label = wx.StaticText(self, label="Upper Body")
        self.neck_label = wx.StaticText(self,
                                        label="Neck:",
                                        size=(140, -1))
        self.chest_label = wx.StaticText(self,
                                         label="Chest:",
                                         size=(140, -1))
        self.shoulders_label = wx.StaticText(self,
                                             label="Shoulders:",
                                             size=(140, -1))
        self.sleeve_label = wx.StaticText(self,
                                          label="Sleeve:",
                                          size=(140, -1))
        self.biceps_label = wx.StaticText(self,
                                          label="Biceps:",
                                          size=(140, -1))
        self.wrist_label = wx.StaticText(self,
                                         label="Wrist:",
                                         size=(140, -1))
        self.waist_label = wx.StaticText(self,
                                         label="Waist:",
                                         size=(140, -1))
        self.hips_label = wx.StaticText(self,
                                        label="Hips:",
                                        size=(140, -1))
        self.shirt_length_label = wx.StaticText(self,
                                                label="Shirt Length:",
                                                size=(140, -1))

        self.trouser_waist_label = wx.StaticText(self,
                                                label="Trouser Waist:",
                                                size=(140, -1))

        self.trouser_outseam_label = wx.StaticText(self,
                                                label="Trouser Outseam:",
                                                size=(140, -1))

        self.trouser_inseam_label = wx.StaticText(self,
                                                label="Trouser Inseam:",
                                                size=(140, -1))

        self.crotch_label = wx.StaticText(self,
                                          label="Crotch:",
                                          size=(140, -1))

        self.thigh_label = wx.StaticText(self,
                                         label="Thigh:",
                                         size=(140, -1))

        self.knee_label = wx.StaticText(self,
                                        label="Knee:",
                                        size=(140, -1))

        # Create entry objects
        self.neck_entry = wx.TextCtrl(self, size=(50, -1))
        self.chest_entry = wx.TextCtrl(self, size=(50, -1))
        self.shoulders_entry = wx.TextCtrl(self, size=(50, -1))
        self.sleeve_entry = wx.TextCtrl(self, size=(50, -1))
        self.biceps_entry = wx.TextCtrl(self, size=(50, -1))
        self.wrist_entry = wx.TextCtrl(self, size=(50, -1))
        self.waist_entry = wx.TextCtrl(self, size=(50, -1))
        self.hips_entry = wx.TextCtrl(self, size=(50, -1))
        self.shirt_length_entry = wx.TextCtrl(self, size=(50, -1))

        self.trouser_waist_entry = wx.TextCtrl(self, size=(50, -1))
        self.trouser_outseam_entry = wx.TextCtrl(self, size=(50, -1))
        self.trouser_inseam_entry = wx.TextCtrl(self, size=(50, -1))
        self.crotch_entry = wx.TextCtrl(self, size=(50, -1))
        self.thigh_entry = wx.TextCtrl(self, size=(50, -1))
        self.knee_entry = wx.TextCtrl(self, size=(50, -1))

        # Create label object
        self.lower_body_label = wx.StaticText(self, label="Lower Body")

        # Set font to the label objects
        self.upper_body_label.SetFont(self.font_header)
        self.neck_label.SetFont(self.font_normal)
        self.chest_label.SetFont(self.font_normal)
        self.shoulders_label.SetFont(self.font_normal)
        self.sleeve_label.SetFont(self.font_normal)
        self.biceps_label.SetFont(self.font_normal)
        self.wrist_label.SetFont(self.font_normal)
        self.waist_label.SetFont(self.font_normal)
        self.hips_label.SetFont(self.font_normal)
        self.shirt_length_label.SetFont(self.font_normal)

        self.lower_body_label.SetFont(self.font_header)
        self.trouser_waist_label.SetFont(self.font_normal)
        self.trouser_outseam_label.SetFont(self.font_normal)
        self.trouser_inseam_label.SetFont(self.font_normal)
        self.crotch_label.SetFont(self.font_normal)
        self.thigh_label.SetFont(self.font_normal)
        self.knee_label.SetFont(self.font_normal)

        # Setting background colour for header labels
        self.upper_body_label.SetBackgroundColour((247,247,247))
        self.lower_body_label.SetBackgroundColour((247,247,247))

        # Create button objects and bind methods to them
        self.cancel_button = wx.Button(self, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_button_close)
        self.add_customer_button = wx.Button(self, label="Add")
        self.add_customer_button.Bind(wx.EVT_BUTTON, self.on_button_add_customer)

        # Set fonts to the button objects
        self.cancel_button.SetFont(self.font_normal)
        self.add_customer_button.SetFont(self.font_normal)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
        self.h_sizer2.Add(self.first_name_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer2.Add(self.first_name_entry, 0, wx.ALL, 5)
        self.h_sizer3.Add(self.last_name_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer3.Add(self.last_name_entry, 0, wx.ALL, 5)
        self.h_sizer4.Add(self.address_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer4.Add(self.address_entry, 0, wx.ALL, 5)
        self.h_sizer5.Add(self.postcode_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer5.Add(self.postcode_entry, 0, wx.ALL, 5)
        self.h_sizer6.Add(self.phone_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer6.Add(self.phone_entry, 0, wx.ALL, 5)
        self.h_sizer7.Add(self.email_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer7.Add(self.email_entry, 0, wx.ALL, 5)
        self.static_sizer1.Add(self.h_sizer2, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer3, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer4, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer5, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer6, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer7, 0, wx.ALL|wx.EXPAND, 2)

        self.h_sizer1_measurements.Add(self.upper_body_label, 1, wx.EXPAND)
        self.h_sizer2_measurements.Add(self.neck_label, 0, 5)
        self.h_sizer2_measurements.Add(self.neck_entry, 0, wx.ALL, 5)
        self.h_sizer2_measurements.Add(self.chest_label, 0, 5)
        self.h_sizer2_measurements.Add(self.chest_entry, 0, wx.ALL, 5)
        self.h_sizer2_measurements.Add(self.shoulders_label, 0, 5)
        self.h_sizer2_measurements.Add(self.shoulders_entry, 0, 5)
        self.h_sizer3_measurements.Add(self.sleeve_label, 0, 5)
        self.h_sizer3_measurements.Add(self.sleeve_entry, 0, wx.ALL, 5)
        self.h_sizer3_measurements.Add(self.biceps_label, 0, 5)
        self.h_sizer3_measurements.Add(self.biceps_entry, 0, wx.ALL, 5)
        self.h_sizer3_measurements.Add(self.wrist_label, 0, 5)
        self.h_sizer3_measurements.Add(self.wrist_entry, 0, 5)
        self.h_sizer4_measurements.Add(self.waist_label, 0, 5)
        self.h_sizer4_measurements.Add(self.waist_entry, 0, wx.ALL, 5)
        self.h_sizer4_measurements.Add(self.hips_label, 0, 5)
        self.h_sizer4_measurements.Add(self.hips_entry, 0, wx.ALL, 5)
        self.h_sizer4_measurements.Add(self.shirt_length_label, 0, 5)
        self.h_sizer4_measurements.Add(self.shirt_length_entry, 0, 5)

        self.h_sizer5_measurements.Add(self.lower_body_label, 1, wx.EXPAND)
        self.h_sizer6_measurements.Add(self.trouser_waist_label, 0, 5)
        self.h_sizer6_measurements.Add(self.trouser_waist_entry, 0, wx.ALL, 5)
        self.h_sizer6_measurements.Add(self.trouser_outseam_label, 0, 5)
        self.h_sizer6_measurements.Add(self.trouser_outseam_entry, 0, wx.ALL, 5)
        self.h_sizer6_measurements.Add(self.trouser_inseam_label, 0, 5)
        self.h_sizer6_measurements.Add(self.trouser_inseam_entry, 0, 5)
        self.h_sizer7_measurements.Add(self.crotch_label, 0, 5)
        self.h_sizer7_measurements.Add(self.crotch_entry, 0, wx.ALL, 5)
        self.h_sizer7_measurements.Add(self.thigh_label, 0, 5)
        self.h_sizer7_measurements.Add(self.thigh_entry, 0, wx.ALL, 5)
        self.h_sizer7_measurements.Add(self.knee_label, 0, 5)
        self.h_sizer7_measurements.Add(self.knee_entry, 0, 5)

        self.h_sizer_buttons.Add(self.cancel_button, 0, wx.ALL, 5)
        self.h_sizer_buttons.Add(self.add_customer_button, 0, wx.ALL, 5)

        self.static_sizer2.Add(self.h_sizer1_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer2_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer3_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer4_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer5_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer6_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer7_measurements, 0, wx.EXPAND)

        self.h_sizer0.Add(self.static_sizer1, 0, wx.EXPAND)
        self.h_sizer0.Add(self.static_sizer2, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.Add(self.h_sizer0, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer_buttons, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Set sizer
        self.SetSizer(self.v_sizer)

    def on_button_add_customer(self, event):
        """This method will run whenever the add button is pressed by the user,
           the objective of this method is to insert a new customer into the
           database."""

        # Getting user input
        self.first_name_value = self.first_name_entry.GetValue()
        self.last_name_value = self.last_name_entry.GetValue()
        self.address_value = self.address_entry.GetValue()
        self.postcode_value = self.postcode_entry.GetValue()
        self.phone_value = self.phone_entry.GetValue()
        self.email_value = self.email_entry.GetValue()

        self.neck_value = self.neck_entry.GetValue()
        self.chest_value = self.chest_entry.GetValue()
        self.shoulders_value = self.shoulders_entry.GetValue()
        self.sleeve_value = self.sleeve_entry.GetValue()
        self.biceps_value = self.biceps_entry.GetValue()
        self.wrist_value = self.wrist_entry.GetValue()
        self.waist_value = self.waist_entry.GetValue()
        self.hips_value = self.hips_entry.GetValue()
        self.shirt_length_value = self.shirt_length_entry.GetValue()

        self.trouser_waist_value = self.trouser_waist_entry.GetValue()
        self.trouser_outseam_value = self.trouser_outseam_entry.GetValue()
        self.trouser_inseam_value = self.trouser_inseam_entry.GetValue()
        self.crotch_value = self.crotch_entry.GetValue()
        self.thigh_value = self.thigh_entry.GetValue()
        self.knee_value = self.knee_entry.GetValue()

        # Declare local variables and the data controller object
        data_general = []
        data_measurements = []
        data_controller = Controller("Data Controller")

        # Appending data in arrays for a cleaner validation of the input
        data_general.append(self.first_name_value)
        data_general.append(self.last_name_value)
        data_general.append(self.address_value)
        data_general.append(self.postcode_value)
        data_general.append(self.phone_value)
        data_general.append(self.email_value)

        data_measurements.append(self.neck_value)
        data_measurements.append(self.chest_value)
        data_measurements.append(self.shoulders_value)
        data_measurements.append(self.sleeve_value)
        data_measurements.append(self.biceps_value)
        data_measurements.append(self.wrist_value)
        data_measurements.append(self.waist_value)
        data_measurements.append(self.hips_value)
        data_measurements.append(self.shirt_length_value)
        data_measurements.append(self.trouser_waist_value)
        data_measurements.append(self.trouser_outseam_value)
        data_measurements.append(self.trouser_inseam_value)
        data_measurements.append(self.crotch_value)
        data_measurements.append(self.thigh_value)
        data_measurements.append(self.knee_value)

        # Validation of data
        empty_elements_general = [x == "" for x in data_general]
        empty_elements_measurements = [x == "" for x in data_measurements]
        float_elements = data_controller.validate_float_list(data_measurements)

        v_first_name = data_controller.validate_alpha(self.first_name_value)
        v_last_name = data_controller.validate_alpha(self.last_name_value)
        v_address = data_controller.validate_integer_alpha(self.address_value)
        v_postcode = data_controller.validate_integer_alpha(self.postcode_value)
        v_phone = data_controller.validate_integer(self.phone_value)
        v_email = data_controller.validate_email(self.email_value)
        v_customer = self.database.get_customer_name(self.first_name_value,
                                                     self.last_name_value,
                                                     self.address_value)

        if any(empty_elements_general):
            # If any element in empty in the list show message
            message = wx.MessageBox("All fields are required.", "Add Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif any(empty_elements_measurements):
            # If any elements is empty show message
            message = wx.MessageBox("All fields are required.", "Add Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not float_elements:
            # If elements are not float format show message
            message = wx.MessageBox("Invalid measurements.",
                                    "Add Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_first_name:
            # If name not valid show message
            message = wx.MessageBox("Invalid first name.",
                                    "Add Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_last_name:
            # If name not valid show message
            message = wx.MessageBox("Invalid last name.",
                                    "Add Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_address:
            # If address not valid show message
            message = wx.MessageBox("Invalid address.",
                                    "Add Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_postcode:
            # IF postcode not valid show message
            message = wx.MessageBox("Invalid postcode.",
                                    "Add Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_phone:
            # If phone number not valid show message
            message = wx.MessageBox("Invalid phone number.",
                                    "Add Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_email:
            # If email not valid show message
            message = wx.MessageBox("Invalid email.",
                                    "Add Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif v_customer:
            # If custoemr already in database show message
            message = wx.MessageBox("Customer already in database.",
                                    "Add Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        else:
            # If data is valid insert customer into the database,
            # Show notification of successfull insertion into database
            self.database.add_customer(self.first_name_value,
                                       self.last_name_value,
                                       self.address_value,
                                       self.postcode_value,
                                       str(self.phone_value),
                                       self.email_value,
                                       float(self.neck_value),
                                       float(self.chest_value),
                                       float(self.shoulders_value),
                                       float(self.sleeve_value),
                                       float(self.biceps_value),
                                       float(self.wrist_value),
                                       float(self.waist_value),
                                       float(self.hips_value),
                                       float(self.shirt_length_value),
                                       float(self.trouser_waist_value),
                                       float(self.trouser_outseam_value),
                                       float(self.trouser_inseam_value),
                                       float(self.crotch_value),
                                       float(self.thigh_value),
                                       float(self.knee_value))
            message = wx.MessageBox(("The customer has been added to "
                                     "the database successfully."),
                                     "Add Customer",
                                     style=wx.OK|wx.ICON_INFORMATION)

            # Clear entries
            self.first_name_entry.Clear()
            self.last_name_entry.Clear()
            self.address_entry.Clear()
            self.postcode_entry.Clear()
            self.phone_entry.Clear()
            self.email_entry.Clear()

            self.neck_entry.Clear()
            self.chest_entry.Clear()
            self.shoulders_entry.Clear()
            self.sleeve_entry.Clear()
            self.biceps_entry.Clear()
            self.wrist_entry.Clear()
            self.waist_entry.Clear()
            self.hips_entry.Clear()
            self.shirt_length_entry.Clear()

            self.trouser_waist_entry.Clear()
            self.trouser_outseam_entry.Clear()
            self.trouser_inseam_entry.Clear()
            self.crotch_entry.Clear()
            self.thigh_entry.Clear()
            self.knee_entry.Clear()

            # Update the customer list ctrl and logger
            self.top_panel.view_customers()

            self.current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.message = ("[" + str(self.current_date_time) + "]" +
                            " - Customer: " +
                            str(self.first_name_value) + " " +
                            str(self.last_name_value) + " " +
                            "has been added successfully to the database.")
            self.logger.Append((self.message))

    def on_button_close(self, event):
        """This method will allow the add customer window object to close."""

        # Close add customer window object (this will destroy the object)
        self.controller.Close()

class AddProject(wx.Frame):
    """This class will allow the creation of the add project window object."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel
        self.main_panel = AddProjectPanel(self,
                                          self,
                                          self.controller)
        # Center window
        self.Center()

class AddProjectPanel(wx.Panel):
    """This class will allow the creation of the add project panel object."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Access the objects from the top panel object
        self.database = self.top_panel.database
        self.list_ctrl_projects = self.top_panel.list_ctrl_projects
        self.logger = self.top_panel.logger
        self.list_ctrl = None
        self.list_ctrl_tailors = None
        self.selected_customer = None
        self.selected_tailor = None
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        # Create icon object and set icon to the master window
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.master.SetIcon(self.icon)

        # Create label objects and font objects
        self.title_label = wx.StaticText(self, label="Add Project")
        self.font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create panel objects
        self.general_panel = AddProjectGeneralPanel(self, size=(400, -1))
        self.customers_panel = AddProjectCustomersPanel(self,
                                                        size=(400, -1),
                                                        style=wx.SIMPLE_BORDER)

        # Create customers list ctrl object
        self.list_ctrl = self.customers_panel.customers_list_ctrl
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.get_customer)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.deselect_customer)

        # Create tailors panel objects
        self.tailors_panel = AddProjectTailorsPanel(self,
                                                    size=(400, -1),
                                                    style=wx.SIMPLE_BORDER)

        # Create tailors list ctrl object
        self.list_ctrl_tailors = self.tailors_panel.tailors_list_ctrl
        self.list_ctrl_tailors.Bind(wx.EVT_LIST_ITEM_SELECTED, self.get_tailor)
        self.list_ctrl_tailors.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                                    self.deselect_tailor)

        # Create button objects
        self.cancel_button = wx.Button(self, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_button_close)
        self.add_project_button = wx.Button(self, label="Add")
        self.add_project_button.Bind(wx.EVT_BUTTON, self.on_button_add_project)

        # Set font for button objects
        self.cancel_button.SetFont(self.font_normal)
        self.add_project_button.SetFont(self.font_normal)

        # Add widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
        self.h_sizer2.Add(self.general_panel, 0, wx.EXPAND)
        self.h_sizer2.Add(self.customers_panel, 1, wx.EXPAND)
        self.h_sizer2.AddSpacer(10)
        self.h_sizer2.Add(self.tailors_panel, 1, wx.EXPAND)
        self.h_sizer2.AddSpacer(10)
        self.h_sizer3.Add(self.cancel_button, 0, wx.ALL, 5)
        self.h_sizer3.Add(self.add_project_button, 0, wx.ALL, 5)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.AddSpacer(20)
        self.v_sizer.Add(self.h_sizer2, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer3, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Set sizer
        self.SetSizer(self.v_sizer)

        # Update customers list ctrl object (load data)
        self.view_customers()
        self.list_ctrl.SetColumnWidth(0, 0)
        self.list_ctrl.SetColumnWidth(1, -2)
        self.list_ctrl.SetColumnWidth(2, -2)
        self.list_ctrl.SetColumnWidth(3, -2)
        self.list_ctrl.SetColumnWidth(4, -2)
        self.list_ctrl.SetColumnWidth(5, -2)
        self.list_ctrl.SetColumnWidth(6, -2)

        # Update tailors list ctrl object (load data)
        self.view_tailors()
        self.list_ctrl_tailors.SetColumnWidth(0, 0)
        self.list_ctrl_tailors.SetColumnWidth(1, -2)
        self.list_ctrl_tailors.SetColumnWidth(2, -2)
        self.list_ctrl_tailors.SetColumnWidth(3, -2)
        self.list_ctrl_tailors.SetColumnWidth(4, -2)
        self.list_ctrl_tailors.SetColumnWidth(5, -2)
        self.list_ctrl_tailors.SetColumnWidth(6, -2)

    def view_customers(self):
        """This method will allow the data to be loaded from database and
           inserted into the customers list ctrl from the add project panel
           object."""

        # Getting data
        customers_data = self.database.view_customers()

        # Clear list ctrl content
        self.list_ctrl.DeleteAllItems()
        for row in customers_data:
            # Append data into the customers list ctrl
            self.list_ctrl.Append((row[0], row[1],
                                   row[2], row[3],
                                   row[4], row[5],
                                   row[6]))

    def view_tailors(self):
        """This method will allow the data to be loaded from database and
           inserted into the tailors list ctrl from the add project panel
           object."""

        # Getting data
        tailors_data = self.database.view_tailors()

        # Clear list ctrl
        self.list_ctrl_tailors.DeleteAllItems()
        for row in tailors_data:
            # Appending data
            self.list_ctrl_tailors.Append((row[0], row[1],
                                           row[2], row[3],
                                           row[4], row[5],
                                           row[6]))

    def get_customer(self, event):
        """This method will run whenever a record is selected in the customers
           list ctrl object, the objective of this method is to access the
           ID column of the list ctrl (this column is hidden) and get the ID
           of the selected customer."""

        try:
            # Assign the list ctrl to a new variable
            self.list_ctrl = self.customers_panel.customers_list_ctrl
            # Get selected record
            self.selected_customer = self.list_ctrl.GetFocusedItem()
            # Get customer's ID
            self.customer = self.list_ctrl.GetItemText(self.selected_customer,
                                                       col=0)
        except:
            pass

    def get_tailor(self, event):
        """This method will run whenever a record is selected in the tailors
           list ctrl object, the objective of this method is to access the
           ID column of the list ctrl (this column is hidden) and get the ID
           of the selected tailor."""

        try:
            # Assign list ctrl to a new variable
            self.list_ctrl_tailors = self.tailors_panel.tailors_list_ctrl
            self.list_tailors = self.list_ctrl_tailors
            # Get selected record
            self.selected_tailor = self.list_ctrl_tailors.GetFocusedItem()
            # Get tailor's ID
            self.tailor = self.list_tailors.GetItemText(self.selected_tailor,
                                                        col=0)
        except:
            pass

    def deselect_customer(self, event):
        """This method will run whenever the customer is deselected."""

        # Deselect customer
        self.selected_customer = None

    def deselect_tailor(self, event):
        """This method will run whenever the tailor is deselected."""

        # Deselect tailor
        self.selected_tailor = None

    def on_button_add_project(self, event):
        """This method will run whenever the add button is pressed, the
           objective of this method is to add a new project into
           the database."""

        # Getting user input
        self.name_value = self.general_panel.name_entry.GetValue()
        self.product_value = self.general_panel.product_entry.GetValue()
        self.material_value = self.general_panel.material_entry.GetValue()
        self.colour_value = self.general_panel.colour_entry.GetValue()
        self.date_value = self.general_panel.date_entry.GetValue()
        self.delivery_value = self.general_panel.delivery_date_entry.GetValue()
        self.price_value = self.general_panel.price_entry.GetValue()

        # Converting the date from the date picker object,
        # this is done in order to send the proper dates into the database
        self.str_date = str(self.date_value)
        self.str_delivery = str(self.delivery_value)
        self.split_date = self.str_date.split(" ")
        self.split_delivery = self.str_delivery.split(" ")

        self.start_date_split = self.split_date[0].split("/")
        self.delivery_date_split = self.split_delivery[0].split("/")

        self.final_start_date = (self.start_date_split[1] + "/" +
                                 self.start_date_split[0] + "/" +
                                 self.start_date_split[2])

        self.final_delivery_date = (self.delivery_date_split[1] + "/" +
                                    self.delivery_date_split[0] + "/" +
                                    self.delivery_date_split[2])

        # Declare array and data controller object
        data_general = []
        data_controller = Controller("Data Controller")

        # Appending data to the array
        data_general.append(self.name_value)
        data_general.append(self.product_value)
        data_general.append(self.material_value)
        data_general.append(self.colour_value)
        data_general.append(self.date_value)
        data_general.append(self.delivery_value)
        data_general.append(self.price_value)

        # Validation of data
        empty_elements_general = [x == "" for x in data_general]

        v_name = data_controller.validate_alpha(self.name_value)
        v_product = data_controller.validate_alpha(self.product_value)
        v_material = data_controller.validate_alpha(self.material_value)
        v_colour = data_controller.validate_alpha(self.colour_value)
        v_price = data_controller.validate_float(self.price_value)

        if any(empty_elements_general):
            # If any element in the array is empty show message
            message = wx.MessageBox("All fields are required.", "Add Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_name:
            # If name is invalid show message
            message = wx.MessageBox("Invalid name.",
                                    "Add Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_product:
            # If product is invalid show message
            message = wx.MessageBox("Invalid product.",
                                    "Add Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_material:
            # If material is invalid show message
            message = wx.MessageBox("Invalid material.",
                                    "Add Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_colour:
            # If colour is invalid show message
            message = wx.MessageBox("Invalid colour.",
                                    "Add Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_price:
            # If price is invalid show message
            message = wx.MessageBox("Invalid price.",
                                    "Add Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif self.selected_customer is None:
            # If no customer selected show message
            message = wx.MessageBox("No customer selected.",
                                    "Add Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif self.selected_tailor is None:
            # If no tailor is selected show message
            message = wx.MessageBox("No tailor selected.",
                                    "Add Project",
                                    style=wx.OK|wx.ICON_WARNING)
        else:
            # If user input is valid insert data into the database
            self.database.add_project(str(self.name_value),
                                      str(self.product_value),
                                      str(self.material_value),
                                      str(self.colour_value),
                                      str(self.final_start_date),
                                      str(self.final_delivery_date),
                                      str(self.price_value),
                                      int(self.customer),
                                      int(self.tailor))

            # Show notification
            message = wx.MessageBox(("The project has been added to "
                                     "the database successfully."),
                                     "Add Project",
                                     style=wx.OK|wx.ICON_INFORMATION)

            # Clear entries
            self.general_panel.name_entry.Clear()
            self.general_panel.product_entry.Clear()
            self.general_panel.material_entry.Clear()
            self.general_panel.colour_entry.Clear()
            self.general_panel.price_entry.Clear()
            self.selected_customer = None
            self.selected_tailor = None

            # Update projects list ctrl
            self.top_panel.view_projects()
            self.list_ctrl_projects.SetColumnWidth(0, 0)
            self.list_ctrl_projects.SetColumnWidth(1, -2)
            self.list_ctrl_projects.SetColumnWidth(2, -2)
            self.list_ctrl_projects.SetColumnWidth(3, -2)
            self.list_ctrl_projects.SetColumnWidth(4, -2)
            self.list_ctrl_projects.SetColumnWidth(5, -2)
            self.list_ctrl_projects.SetColumnWidth(6, -2)
            self.list_ctrl_projects.SetColumnWidth(7, -2)

            # Update logger
            self.current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.message = ("[" + str(self.current_date_time) + "]" +
                            " - Project: " +
                            str(self.name_value) + " " +
                            "has been added successfully to the database.")
            self.logger.Append((self.message))

    def on_button_close(self, event):
        """This method will run whenever the close button is pressed."""

        # Close the controller window
        self.controller.Close()

class AddProjectGeneralPanel(wx.Panel):
    """This class will allow the creation of the general panel for the add
       projects, panel object, this class has the objective to create labels
       and entries objects."""

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal sizers objects
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer0 = wx.BoxSizer(wx.HORIZONTAL)

        # Create static box object and static sizer object
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

        # Create font objects
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        # Create label objects
        self.name_label = wx.StaticText(self,
                                        label="Name:",
                                        size=(120, -1))

        self.product_label = wx.StaticText(self,
                                           label="Product:",
                                           size=(120, -1))

        self.material_label = wx.StaticText(self,
                                            label="Material:",
                                            size=(120, -1))

        self.colour_label = wx.StaticText(self,
                                          label="Colour:",
                                          size=(120, -1))

        self.date_label = wx.StaticText(self,
                                         label="Start Date:",
                                         size=(120, -1))

        self.delivery_date_label = wx.StaticText(self,
                                                 label="Delivery Date:",
                                                 size=(120, -1))

        self.price_label = wx.StaticText(self,
                                         label="Price:",
                                         size=(120, -1))

        # Create entry objects
        self.name_entry = wx.TextCtrl(self)
        self.product_entry = wx.TextCtrl(self)
        self.material_entry = wx.TextCtrl(self)
        self.colour_entry = wx.TextCtrl(self)
        self.date_entry = wx.adv.DatePickerCtrl(self)
        self.delivery_date_entry = wx.adv.DatePickerCtrl(self)
        self.price_entry = wx.TextCtrl(self)

        # Set font to the labels
        self.name_label.SetFont(self.font_normal)
        self.product_label.SetFont(self.font_normal)
        self.material_label.SetFont(self.font_normal)
        self.colour_label.SetFont(self.font_normal)
        self.date_label.SetFont(self.font_normal)
        self.delivery_date_label.SetFont(self.font_normal)
        self.price_label.SetFont(self.font_normal)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.name_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer1.Add(self.name_entry, 1, wx.ALL, 5)
        self.h_sizer2.Add(self.product_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer2.Add(self.product_entry, 1, wx.ALL, 5)
        self.h_sizer3.Add(self.material_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer3.Add(self.material_entry, 1, wx.ALL, 5)
        self.h_sizer4.Add(self.colour_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer4.Add(self.colour_entry, 1, wx.ALL, 5)
        self.h_sizer5.Add(self.date_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer5.Add(self.date_entry, 1, wx.ALL, 5)
        self.h_sizer6.Add(self.delivery_date_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer6.Add(self.delivery_date_entry, 1, wx.ALL, 5)
        self.h_sizer7.Add(self.price_label, 0, wx.ALL, 5)
        self.h_sizer7.Add(self.price_entry, 1, wx.ALL, 5)
        self.static_sizer1.Add(self.h_sizer1, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer2, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer3, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer4, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer5, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer6, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer7, 0, wx.ALL|wx.EXPAND, 2)

        self.h_sizer0.Add(self.static_sizer1, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer0, 0, wx.EXPAND)

        # Set sizer
        self.SetSizer(self.v_sizer)

class AddProjectCustomersPanel(wx.Panel):
    """This class will allow the creation of the customers panel object."""

    def __init__(self, master, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        # Assign the database from the master
        self.database = self.master.database
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal sizers objects
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # Create label objects and font objects
        self.search_label = wx.StaticText(self, label="Search:")
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.search_label.SetFont(self.font)

        self.by_label = wx.StaticText(self, label="by")
        self.by_label.SetFont(self.font)

        # Create choices object
        self.choices = wx.Choice(self,
                                 choices=["1-First Name",
                                          "2-Last Name",
                                          "3-Address",
                                          "4-Postcode",
                                          "5-Phone",
                                          "6-Email"])

        # Create search entry object
        self.search_entry = wx.TextCtrl(self, size=(120, -1))

        # Create button objects
        self.search_button = wx.Button(self, label="Search")
        self.search_button.Bind(wx.EVT_BUTTON, self.search_customer)

        self.refresh_button = wx.Button(self, label="Refresh")
        self.refresh_button.Bind(wx.EVT_BUTTON, self.refresh_customers)

        # Create static line object
        self.static_line = wx.StaticLine(self)

        # Create label objects and font objects
        self.title_label = wx.StaticText(self, label="Customers")
        self.font = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create customer list ctrl object
        self.customers_list_ctrl = CustomersListCtrl(self, style=wx.LC_REPORT)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.search_label, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.search_entry, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.by_label, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.choices, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.search_button, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.refresh_button, 0, wx.ALL, 5)
        self.h_sizer2.Add(self.title_label, 0)
        self.v_sizer.Add(self.h_sizer1)
        self.v_sizer.Add(self.static_line, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer2, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.Add(self.customers_list_ctrl, 1, wx.EXPAND)

        # Set the panel's sizer
        self.SetSizer(self.v_sizer)

    def search_customer(self, event):
        """This method will allow run whenever the search button is pressed,
           the objective of this method is to search for a customer in
           the database."""

        # Get user selection
        self.choices_value = self.choices.GetSelection()
        # Assign the list ctrl to a new variable
        self.list_ctrl = self.customers_list_ctrl
        if self.choices_value == 0:
            # If the first element in the list is selected search for first name
            self.first_name = self.search_entry.GetValue()
            self.data = self.database.search_customer_first_name(self.first_name)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Append data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 1:
            # If the user selection is the second item in the list,
            # search for the last name in the database
            self.last_name = self.search_entry.GetValue()
            self.data = self.database.search_customer_last_name(self.last_name)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Append data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 2:
            # If user selection is the third item in the list,
            # Search for address in the database
            self.address = self.search_entry.GetValue()
            self.data = self.database.search_customer_address(self.address)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Append data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 3:
            # If the fouth item is selected in the list,
            # search for postcode in the database
            self.postcode = self.search_entry.GetValue()
            self.data = self.database.search_customer_postcode(self.postcode)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Append data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 4:
            # If the user selection is the fifth element in the list,
            # search for the phone number in the database
            self.phone = self.search_entry.GetValue()
            self.data = self.database.search_customer_phone(self.phone)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 5:
            # If user selection is the sixth element in the list,
            # search for the email in the database
            self.email = self.search_entry.GetValue()
            self.data = self.database.search_customer_email(self.email)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Append data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

    def refresh_customers(self, event):
        """This method will run whenever the refresh button is pressed,
           the objective of this method is to load all the data from
           database and insert it in the customer's list ctrl
           after a search have been made."""

        # Assign the list ctrl to a new variable
        self.list_ctrl = self.customers_list_ctrl

        # Load data and insert it in the list ctrl
        # Set the list ctrl column width to fit the largest item in the list
        self.master.view_customers()
        self.list_ctrl.SetColumnWidth(0, 0)
        self.list_ctrl.SetColumnWidth(1, -2)
        self.list_ctrl.SetColumnWidth(2, -2)
        self.list_ctrl.SetColumnWidth(3, -2)
        self.list_ctrl.SetColumnWidth(4, -2)
        self.list_ctrl.SetColumnWidth(5, -2)
        self.list_ctrl.SetColumnWidth(6, -2)

class AddProjectTailorsPanel(wx.Panel):
    """This class will allow the creation of the tailor panel object."""

    def __init__(self, master, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        # Assign the master database to a new variable
        self.database = self.master.database
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal sizers objects
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # Create label object and font object
        self.search_label = wx.StaticText(self, label="Search:")
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.search_label.SetFont(self.font)

        # Create label object
        self.by_label = wx.StaticText(self, label="by")
        self.by_label.SetFont(self.font)

        # Create choices object
        self.choices = wx.Choice(self,
                                 choices=["1-First Name",
                                          "2-Last Name",
                                          "3-Address",
                                          "4-Postcode",
                                          "5-Phone",
                                          "6-Email"])

        # Create search entry object
        self.search_entry = wx.TextCtrl(self, size=(120, -1))

        # Create button objects
        self.search_button = wx.Button(self, label="Search")
        self.search_button.Bind(wx.EVT_BUTTON, self.search_tailor)

        self.refresh_button = wx.Button(self, label="Refresh")
        self.refresh_button.Bind(wx.EVT_BUTTON, self.refresh_tailors)

        # Create static line object
        self.static_line = wx.StaticLine(self)

        # Create label object and font objects
        self.title_label = wx.StaticText(self, label="Tailors")
        self.font = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create tailors list ctrl object
        self.tailors_list_ctrl = TailorsListCtrl(self, style=wx.LC_REPORT)

        # Add widgets to the sizers
        self.h_sizer1.Add(self.search_label, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.search_entry, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.by_label, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.choices, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.search_button, 0, wx.ALL, 5)
        self.h_sizer1.Add(self.refresh_button, 0, wx.ALL, 5)
        self.h_sizer2.Add(self.title_label, 0)
        self.v_sizer.Add(self.h_sizer1, 0, wx.EXPAND)
        self.v_sizer.Add(self.static_line, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer2, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.Add(self.tailors_list_ctrl, 1, wx.EXPAND)

        # Set pamel's sizer
        self.SetSizer(self.v_sizer)

    def search_tailor(self, event):
        """This method will run whenever the search button from the tailors
           panel is pressed, the objective of this method is to insert in
           the list ctrl the result of the user's search."""

        # Get user selection
        self.choices_value = self.choices.GetSelection()
        # Assign list ctrl to a new variable
        self.list_ctrl = self.tailors_list_ctrl
        if self.choices_value == 0:
            # If user selection is the first elements in the list,
            # search for the first name in the database
            self.first_name = self.search_entry.GetValue()
            self.data = self.database.search_tailor_first_name(self.first_name)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Append data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 1:
            # If the user selection is the second elements in the list,
            # search for the last name in the database
            self.last_name = self.search_entry.GetValue()
            self.data = self.database.search_tailor_last_name(self.last_name)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Append data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 2:
            # If user selection is the third element in the list,
            # search for the address in the database
            self.address = self.search_entry.GetValue()
            self.data = self.database.search_tailor_address(self.address)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Append data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 3:
            # If the user selection is the fouth element in the list,
            # search for the postcode in the database
            self.postcode = self.search_entry.GetValue()
            self.data = self.database.search_tailor_postcode(self.postcode)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Append data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 4:
            # If the user selection is the fifth element in the list,
            # search for the phone number in the database
            self.phone = self.search_entry.GetValue()
            self.data = self.database.search_tailor_phone(self.phone)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Append data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 5:
            # If the user selection is the sixth element in the list,
            # search for the email in the database
            self.email = self.search_entry.GetValue()
            self.data = self.database.search_tailor_email(self.email)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Append data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

    def refresh_tailors(self, event):
        """This method will run whenever the refresh button from the tailors
           panel is pressed, the objective of this method is to load and
           insert the data from the tailors table into the tailors
           list ctrl."""

        # Assign the tailors list ctrl to a new variable
        self.list_ctrl = self.tailors_list_ctrl

        # Load and insert data into the tailors list ctrl
        # Set the list ctrl to fit the largest item in the list ctrl
        self.master.view_tailors()
        self.list_ctrl.SetColumnWidth(0, 0)
        self.list_ctrl.SetColumnWidth(1, -2)
        self.list_ctrl.SetColumnWidth(2, -2)
        self.list_ctrl.SetColumnWidth(3, -2)
        self.list_ctrl.SetColumnWidth(4, -2)
        self.list_ctrl.SetColumnWidth(5, -2)
        self.list_ctrl.SetColumnWidth(6, -2)

class AddAlteration(wx.Frame):
    """This class will allow the creation of the add alteration window
       object, the objective of this method is to insert a new alteration
       into the database."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel
        self.main_panel = AddAlterationPanel(self,
                                             self,
                                             self.controller)
        # Center window
        self.Center()

class AddAlterationPanel(wx.Panel):
    """This class will allow the creation of the add alteration panel object,
       the objective of this class is to create the widgets for
       the add alteration window object."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Assign top panel objects to new variables
        self.database = self.top_panel.database
        self.list_ctrl_alterations = self.top_panel.list_ctrl_alterations
        self.logger = self.top_panel.logger
        self.list_ctrl = None
        self.list_ctrl_tailors = None
        self.selected_customer = None
        self.selected_tailor = None
        self.build()

    def build(self):
        """This method will allow the creation of the panel's methods."""

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

        # Create label object and font objects
        self.title_label = wx.StaticText(self, label="Add Alteration")
        self.font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create panel objects
        self.general_panel = AddProjectGeneralPanel(self, size=(400, -1))
        self.customers_panel = AddProjectCustomersPanel(self,
                                                        size=(400, -1),
                                                        style=wx.SIMPLE_BORDER)

        # Create customers list ctrl
        self.list_ctrl = self.customers_panel.customers_list_ctrl
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.get_customer)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.deselect_customer)

        # Create tailors panel and list ctrl
        self.tailors_panel = AddProjectTailorsPanel(self,
                                                    size=(400, -1),
                                                    style=wx.SIMPLE_BORDER)

        self.list_ctrl_tailors = self.tailors_panel.tailors_list_ctrl
        self.list_ctrl_tailors.Bind(wx.EVT_LIST_ITEM_SELECTED, self.get_tailor)
        self.list_ctrl_tailors.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                                    self.deselect_tailor)

        # Create button objects
        self.cancel_button = wx.Button(self, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_button_close)
        self.add_alteration_button = wx.Button(self, label="Add")
        self.add_alteration_button.Bind(wx.EVT_BUTTON,
                                        self.on_button_add_alteration)

        # Set font to the button objects
        self.cancel_button.SetFont(self.font_normal)
        self.add_alteration_button.SetFont(self.font_normal)

        # Add widgets to the sizers objects
        self.h_sizer1.Add(self.title_label, 0)
        self.h_sizer2.Add(self.general_panel, 0, wx.EXPAND)
        self.h_sizer2.Add(self.customers_panel, 1, wx.EXPAND)
        self.h_sizer2.AddSpacer(10)
        self.h_sizer2.Add(self.tailors_panel, 1, wx.EXPAND)
        self.h_sizer2.AddSpacer(10)
        self.h_sizer3.Add(self.cancel_button, 0, wx.ALL, 5)
        self.h_sizer3.Add(self.add_alteration_button, 0, wx.ALL, 5)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.AddSpacer(20)
        self.v_sizer.Add(self.h_sizer2, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer3, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Load data from database and insert it into the list ctrls
        # Set list ctrls columns to fit the largest item in the list
        self.view_customers()
        self.list_ctrl.SetColumnWidth(0, 0)
        self.list_ctrl.SetColumnWidth(1, -2)
        self.list_ctrl.SetColumnWidth(2, -2)
        self.list_ctrl.SetColumnWidth(3, -2)
        self.list_ctrl.SetColumnWidth(4, -2)
        self.list_ctrl.SetColumnWidth(5, -2)
        self.list_ctrl.SetColumnWidth(6, -2)

        self.view_tailors()
        self.list_ctrl_tailors.SetColumnWidth(0, 0)
        self.list_ctrl_tailors.SetColumnWidth(1, -2)
        self.list_ctrl_tailors.SetColumnWidth(2, -2)
        self.list_ctrl_tailors.SetColumnWidth(3, -2)
        self.list_ctrl_tailors.SetColumnWidth(4, -2)
        self.list_ctrl_tailors.SetColumnWidth(5, -2)
        self.list_ctrl_tailors.SetColumnWidth(6, -2)

        # Set sizer
        self.SetSizer(self.v_sizer)

    def view_customers(self):
        """This method will load the customers data from database and insert it
           into the customers list ctrl, once the window is opened."""

        # Getting customers data
        customers_data = self.database.view_customers()

        # Clear list ctrl
        self.list_ctrl.DeleteAllItems()
        for row in customers_data:
            # Append data
            self.list_ctrl.Append((row[0], row[1],
                                   row[2], row[3],
                                   row[4], row[5],
                                   row[6]))

    def view_tailors(self):
        """This method will load the tailors data from database and insert it
           into the tailors list ctrl, once the window is opened."""

        # Getting the tailors data
        tailors_data = self.database.view_tailors()

        # Clear list ctrl
        self.list_ctrl_tailors.DeleteAllItems()
        for row in tailors_data:
            # Append data
            self.list_ctrl_tailors.Append((row[0], row[1],
                                           row[2], row[3],
                                           row[4], row[5],
                                           row[6]))

    def get_customer(self, event):
        """This method will run whenever a customer is selected in the
           customers list ctrl, the objective of this method is to
           get the ID of the selected customer."""

        try:
            # Assign customers list ctrl to a new variable
            self.list_ctrl = self.customers_panel.customers_list_ctrl
            # Get selected record
            self.selected_customer = self.list_ctrl.GetFocusedItem()
            # Get customer ID
            self.customer = self.list_ctrl.GetItemText(self.selected_customer,
                                                       col=0)
        except:
            pass

    def get_tailor(self, event):
        """This method will run whenever a tailor is selected in the
           tailors list ctrl, the objective of this method is to
           get the ID of the selected tailor."""

        try:
            # Assign the list ctrl to a new variable
            self.list_ctrl_tailors = self.tailors_panel.tailors_list_ctrl
            self.list_tailors = self.list_ctrl_tailors
            # Get selected record
            self.selected_tailor = self.list_ctrl_tailors.GetFocusedItem()
            # Get tailor's ID
            self.tailor = self.list_tailors.GetItemText(self.selected_tailor,
                                                        col=0)
        except:
            pass

    def deselect_customer(self, event):
        """This method will run whenever a customer is deselected in the
           list ctrl."""

        # Deselect customer
        self.selected_customer = None

    def deselect_tailor(self, event):
        """This method will run whenever a tailor is deselected in the
           list ctrl."""

        # Deselect tailor
        self.selected_tailor = None

    def on_button_add_alteration(self, event):
        """This method will run whenever the add button is pressed,
           the objective of this method is to add a new alteration
           to the database."""

        # Get user input
        self.name_value = self.general_panel.name_entry.GetValue()
        self.product_value = self.general_panel.product_entry.GetValue()
        self.material_value = self.general_panel.material_entry.GetValue()
        self.colour_value = self.general_panel.colour_entry.GetValue()
        self.date_value = self.general_panel.date_entry.GetValue()
        self.delivery_value = self.general_panel.delivery_date_entry.GetValue()
        self.price_value = self.general_panel.price_entry.GetValue()

        # Format the date to the proper format from the date picker object
        self.str_date = str(self.date_value)
        self.str_delivery = str(self.delivery_value)
        self.split_date = self.str_date.split(" ")
        self.split_delivery = self.str_delivery.split(" ")

        self.start_date_split = self.split_date[0].split("/")
        self.delivery_date_split = self.split_delivery[0].split("/")

        self.final_start_date = (self.start_date_split[1] + "/" +
                                 self.start_date_split[0] + "/" +
                                 self.start_date_split[2])

        self.final_delivery_date = (self.delivery_date_split[1] + "/" +
                                    self.delivery_date_split[0] + "/" +
                                    self.delivery_date_split[2])

        # Declare an array and the data controller object
        data_general = []
        data_controller = Controller("Data Controller")

        # Append data to the array
        data_general.append(self.name_value)
        data_general.append(self.product_value)
        data_general.append(self.material_value)
        data_general.append(self.colour_value)
        data_general.append(self.date_value)
        data_general.append(self.delivery_value)
        data_general.append(self.price_value)

        # Validation of data
        empty_elements_general = [x == "" for x in data_general]

        v_name = data_controller.validate_alpha(self.name_value)
        v_product = data_controller.validate_alpha(self.product_value)
        v_material = data_controller.validate_alpha(self.material_value)
        v_colour = data_controller.validate_alpha(self.colour_value)
        v_price = data_controller.validate_float(self.price_value)

        if any(empty_elements_general):
            # If there are any empty elements show message
            message = wx.MessageBox("All fields are required.", "Add Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_name:
            # If first name is invalid show message
            message = wx.MessageBox("Invalid name.",
                                    "Add Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_product:
            # If product is invalid show message
            message = wx.MessageBox("Invalid product.",
                                    "Add Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_material:
            # If material is invalid show message
            message = wx.MessageBox("Invalid material.",
                                    "Add Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_colour:
            # If colour is invalid show message
            message = wx.MessageBox("Invalid colour.",
                                    "Add Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_price:
            # If price is invalid show message
            message = wx.MessageBox("Invalid price.",
                                    "Add Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif self.selected_customer is None:
            # If no customer is selected show message
            message = wx.MessageBox("No customer selected.",
                                    "Add Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif self.selected_tailor is None:
            # If no tailor is selected show message
            message = wx.MessageBox("No tailor selected.",
                                    "Add Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        else:
            # If user input is valid insert data into the database
            self.database.add_alteration(str(self.name_value),
                                         str(self.product_value),
                                         str(self.material_value),
                                         str(self.colour_value),
                                         str(self.final_start_date),
                                         str(self.final_delivery_date),
                                         str(self.price_value),
                                         int(self.customer),
                                         int(self.tailor))

            # Show notification
            message = wx.MessageBox(("The alteration has been added to "
                                     "the database successfully."),
                                     "Add Alteration",
                                     style=wx.OK|wx.ICON_INFORMATION)

            # Clear entries
            self.general_panel.name_entry.Clear()
            self.general_panel.product_entry.Clear()
            self.general_panel.material_entry.Clear()
            self.general_panel.colour_entry.Clear()
            self.general_panel.price_entry.Clear()
            self.selected_customer = None
            self.selected_tailor = None

            # Update list ctrl and logger
            self.top_panel.view_alterations()
            self.list_ctrl_alterations.SetColumnWidth(0, 0)
            self.list_ctrl_alterations.SetColumnWidth(1, -2)
            self.list_ctrl_alterations.SetColumnWidth(2, -2)
            self.list_ctrl_alterations.SetColumnWidth(3, -2)
            self.list_ctrl_alterations.SetColumnWidth(4, -2)
            self.list_ctrl_alterations.SetColumnWidth(5, -2)
            self.list_ctrl_alterations.SetColumnWidth(6, -2)
            self.list_ctrl_alterations.SetColumnWidth(7, -2)

            self.current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.message = ("[" + str(self.current_date_time) + "]" +
                            " - Alteration: " +
                            str(self.name_value) + " " +
                            "has been added successfully to the database.")
            self.logger.Append((self.message))

    def on_button_close(self, event):
        """This method will run whenever the cancel button is pressed."""

        # Close controller window
        self.controller.Close()

class AddAlterationGeneralPanel(wx.Panel):
    """This class will allow the creation of the general panel for the
       add alteration widnow object, this class is not used in the current
       version of the program."""

    def __init__(self, *args, **kwargs):
        wx.Frame.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal sizers objects
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer0 = wx.BoxSizer(wx.HORIZONTAL)

        # Create static box object and static sizer object
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

        # Create font objects
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)

        # Create label objects
        self.name_label = wx.StaticText(self,
                                        label="Name:",
                                        size=(120, -1))

        self.product_label = wx.StaticText(self,
                                           label="Product:",
                                           size=(120, -1))

        self.material_label = wx.StaticText(self,
                                            label="Material:",
                                            size=(120, -1))

        self.colour_label = wx.StaticText(self,
                                          label="Colour:",
                                          size=(120, -1))

        self.date_label = wx.StaticText(self,
                                         label="Date:",
                                         size=(120, -1))

        self.delivery_date_label = wx.StaticText(self,
                                                 label="Delivery Date:",
                                                 size=(120, -1))

        self.price_label = wx.StaticText(self,
                                         label="Price:",
                                         size=(120, -1))

        # Create entry objects
        self.name_entry = wx.TextCtrl(self)
        self.product_entry = wx.TextCtrl(self)
        self.material_entry = wx.TextCtrl(self)
        self.colour_entry = wx.TextCtrl(self)
        self.date_entry = wx.TextCtrl(self)
        self.delivery_date_entry = wx.TextCtrl(self)
        self.price_entry = wx.TextCtrl(self)

        # Setting font to the labels
        self.name_label.SetFont(self.font_normal)
        self.product_label.SetFont(self.font_normal)
        self.material_label.SetFont(self.font_normal)
        self.colour_label.SetFont(self.font_normal)
        self.date_label.SetFont(self.font_normal)
        self.delivery_date_label.SetFont(self.font_normal)
        self.price_label.SetFont(self.font_normal)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.name_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer1.Add(self.name_entry, 1, wx.ALL, 5)
        self.h_sizer2.Add(self.product_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer2.Add(self.product_entry, 1, wx.ALL, 5)
        self.h_sizer3.Add(self.material_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer3.Add(self.material_entry, 1, wx.ALL, 5)
        self.h_sizer4.Add(self.colour_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer4.Add(self.colour_entry, 1, wx.ALL, 5)
        self.h_sizer5.Add(self.date_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer5.Add(self.date_entry, 1, wx.ALL, 5)
        self.h_sizer6.Add(self.delivery_date_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer6.Add(self.delivery_date_entry, 1, wx.ALL, 5)
        self.h_sizer7.Add(self.price_label, 0, wx.ALL, 5)
        self.h_sizer7.Add(self.price_entry, 1, wx.ALL, 5)
        self.static_sizer1.Add(self.h_sizer1, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer2, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer3, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer4, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer5, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer6, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer7, 0, wx.ALL|wx.EXPAND, 2)

        self.h_sizer0.Add(self.static_sizer1, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer0, 0, wx.EXPAND)

        # Setting the panel's sizer
        self.SetSizer(self.v_sizer)

class AddAlterationCustomersPanel(wx.Panel):
    """This class will allow the creation of the customers panel object."""

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal sizers objects
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # Create label object and font objects
        self.title_label = wx.StaticText(self, label="Customers")
        self.font = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create list ctrl object
        self.customers_list_ctrl = CustomersListCtrl(self, style=wx.LC_REPORT)

        # Add widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.Add(self.customers_list_ctrl, 1, wx.EXPAND)

        # Set panel's sizer
        self.SetSizer(self.v_sizer)

class AddAlterationTailorsPanel(wx.Panel):
    """This class will allow the creation of the tailors panel object."""

    def __init__(self, *args, **kwargs):
        wx.Panel.__init__(self, *args, **kwargs)
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal sizers objects
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)

        # Create label object and font objects
        self.title_label = wx.StaticText(self, label="Tailors")
        self.font = wx.Font(14, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create list ctrl object
        self.tailors_list_ctrl = TailorsListCtrl(self, style=wx.LC_REPORT)

        # Add widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.Add(self.tailors_list_ctrl, 1, wx.EXPAND)

        # Set panel's sizer
        self.SetSizer(self.v_sizer)

class UpdateCustomer(wx.Frame):
    """This class will allow the creation of the update customer window object,
       the objective of this class is to update a customer present in the
       database."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel object
        self.main_panel = UpdateCustomerPanel(self, self, self.controller)
        self.Center()

class UpdateCustomerPanel(wx.Panel):
    """This class will allow the creation of the update customer panel object,
       the objective of this class is to create the widgets inside the
       update customer window object."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Accessing objects from top panel object
        self.database = self.top_panel.database
        self.logger = self.top_panel.logger
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal sizers objects
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer0 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer_buttons = wx.BoxSizer(wx.HORIZONTAL)

        # Create static boxes and static box sizers objects
        self.static_box1 = wx.StaticBox(self)
        self.static_box2 = wx.StaticBox(self)
        self.static_sizer1 = wx.StaticBoxSizer(self.static_box1, wx.VERTICAL)
        self.static_sizer2 = wx.StaticBoxSizer(self.static_box2, wx.VERTICAL)

        # Horizontal sizers for the general interface elements
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer5 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer6 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer7 = wx.BoxSizer(wx.HORIZONTAL)

        # Horizontal sizers for the measurements interface elements
        self.h_sizer1_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer4_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer5_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer6_measurements = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer7_measurements = wx.BoxSizer(wx.HORIZONTAL)

        # Create icon object and setting the icon to the master window
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.master.SetIcon(self.icon)

        # Getting the customer's data
        self.get_customer()

        # Create label object and font objects
        self.title_label = wx.StaticText(self, label="Update Customer")
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
        self.first_name_entry = wx.TextCtrl(self, size=(250, -1))
        self.last_name_entry = wx.TextCtrl(self, size=(250, -1))
        self.address_entry = wx.TextCtrl(self, size=(250, -1))
        self.postcode_entry = wx.TextCtrl(self, size=(250, -1))
        self.phone_entry = wx.TextCtrl(self, size=(250, -1))
        self.email_entry = wx.TextCtrl(self, size=(250, -1))

        # Setting the font to the labels
        self.first_name_label.SetFont(self.font_normal)
        self.last_name_label.SetFont(self.font_normal)
        self.address_label.SetFont(self.font_normal)
        self.postcode_label.SetFont(self.font_normal)
        self.phone_label.SetFont(self.font_normal)
        self.email_label.SetFont(self.font_normal)

        # Creating label objects
        self.upper_body_label = wx.StaticText(self, label="Upper Body")
        self.neck_label = wx.StaticText(self,
                                        label="Neck:",
                                        size=(140, -1))
        self.chest_label = wx.StaticText(self,
                                         label="Chest:",
                                         size=(140, -1))
        self.shoulders_label = wx.StaticText(self,
                                             label="Shoulders:",
                                             size=(140, -1))
        self.sleeve_label = wx.StaticText(self,
                                          label="Sleeve:",
                                          size=(140, -1))
        self.biceps_label = wx.StaticText(self,
                                          label="Biceps:",
                                          size=(140, -1))
        self.wrist_label = wx.StaticText(self,
                                         label="Wrist:",
                                         size=(140, -1))
        self.waist_label = wx.StaticText(self,
                                         label="Waist:",
                                         size=(140, -1))
        self.hips_label = wx.StaticText(self,
                                        label="Hips:",
                                        size=(140, -1))
        self.shirt_length_label = wx.StaticText(self,
                                                label="Shirt Length:",
                                                size=(140, -1))

        self.trouser_waist_label = wx.StaticText(self,
                                                label="Trouser Waist:",
                                                size=(140, -1))

        self.trouser_outseam_label = wx.StaticText(self,
                                                label="Trouser Outseam:",
                                                size=(140, -1))

        self.trouser_inseam_label = wx.StaticText(self,
                                                label="Trouser Inseam:",
                                                size=(140, -1))

        self.crotch_label = wx.StaticText(self,
                                          label="Crotch:",
                                          size=(140, -1))

        self.thigh_label = wx.StaticText(self,
                                         label="Thigh:",
                                         size=(140, -1))

        self.knee_label = wx.StaticText(self,
                                        label="Knee:",
                                        size=(140, -1))

        # Create entry objects
        self.neck_entry = wx.TextCtrl(self, size=(50, -1))
        self.chest_entry = wx.TextCtrl(self, size=(50, -1))
        self.shoulders_entry = wx.TextCtrl(self, size=(50, -1))
        self.sleeve_entry = wx.TextCtrl(self, size=(50, -1))
        self.biceps_entry = wx.TextCtrl(self, size=(50, -1))
        self.wrist_entry = wx.TextCtrl(self, size=(50, -1))
        self.waist_entry = wx.TextCtrl(self, size=(50, -1))
        self.hips_entry = wx.TextCtrl(self, size=(50, -1))
        self.shirt_length_entry = wx.TextCtrl(self, size=(50, -1))

        self.trouser_waist_entry = wx.TextCtrl(self, size=(50, -1))
        self.trouser_outseam_entry = wx.TextCtrl(self, size=(50, -1))
        self.trouser_inseam_entry = wx.TextCtrl(self, size=(50, -1))
        self.crotch_entry = wx.TextCtrl(self, size=(50, -1))
        self.thigh_entry = wx.TextCtrl(self, size=(50, -1))
        self.knee_entry = wx.TextCtrl(self, size=(50, -1))

        # Create label object
        self.lower_body_label = wx.StaticText(self, label="Lower Body")

        # Setting font to the labels
        self.upper_body_label.SetFont(self.font_header)
        self.neck_label.SetFont(self.font_normal)
        self.chest_label.SetFont(self.font_normal)
        self.shoulders_label.SetFont(self.font_normal)
        self.sleeve_label.SetFont(self.font_normal)
        self.biceps_label.SetFont(self.font_normal)
        self.wrist_label.SetFont(self.font_normal)
        self.waist_label.SetFont(self.font_normal)
        self.hips_label.SetFont(self.font_normal)
        self.shirt_length_label.SetFont(self.font_normal)

        self.lower_body_label.SetFont(self.font_header)
        self.trouser_waist_label.SetFont(self.font_normal)
        self.trouser_outseam_label.SetFont(self.font_normal)
        self.trouser_inseam_label.SetFont(self.font_normal)
        self.crotch_label.SetFont(self.font_normal)
        self.thigh_label.SetFont(self.font_normal)
        self.knee_label.SetFont(self.font_normal)

        # Setting background colour to the header labels objects
        self.upper_body_label.SetBackgroundColour((247,247,247))
        self.lower_body_label.SetBackgroundColour((247,247,247))

        # Create button objects
        self.cancel_button = wx.Button(self, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON,
                                self.on_button_close_update_customer)
        self.add_customer_button = wx.Button(self, label="Update")
        self.add_customer_button.Bind(wx.EVT_BUTTON,
                                      self.on_button_update_customer)

        # Setting font to the buttons
        self.cancel_button.SetFont(self.font_normal)
        self.add_customer_button.SetFont(self.font_normal)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
        self.h_sizer2.Add(self.first_name_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer2.Add(self.first_name_entry, 0, wx.ALL, 5)
        self.h_sizer3.Add(self.last_name_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer3.Add(self.last_name_entry, 0, wx.ALL, 5)
        self.h_sizer4.Add(self.address_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer4.Add(self.address_entry, 0, wx.ALL, 5)
        self.h_sizer5.Add(self.postcode_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer5.Add(self.postcode_entry, 0, wx.ALL, 5)
        self.h_sizer6.Add(self.phone_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer6.Add(self.phone_entry, 0, wx.ALL, 5)
        self.h_sizer7.Add(self.email_label, 0, wx.ALL|wx.ALIGN_CENTER, 5)
        self.h_sizer7.Add(self.email_entry, 0, wx.ALL, 5)
        self.static_sizer1.Add(self.h_sizer2, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer3, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer4, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer5, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer6, 0, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.Add(self.h_sizer7, 0, wx.ALL|wx.EXPAND, 2)

        self.h_sizer1_measurements.Add(self.upper_body_label, 1, wx.EXPAND)
        self.h_sizer2_measurements.Add(self.neck_label, 0, 5)
        self.h_sizer2_measurements.Add(self.neck_entry, 0, wx.ALL, 5)
        self.h_sizer2_measurements.Add(self.chest_label, 0, 5)
        self.h_sizer2_measurements.Add(self.chest_entry, 0, wx.ALL, 5)
        self.h_sizer2_measurements.Add(self.shoulders_label, 0, 5)
        self.h_sizer2_measurements.Add(self.shoulders_entry, 0, 5)
        self.h_sizer3_measurements.Add(self.sleeve_label, 0, 5)
        self.h_sizer3_measurements.Add(self.sleeve_entry, 0, wx.ALL, 5)
        self.h_sizer3_measurements.Add(self.biceps_label, 0, 5)
        self.h_sizer3_measurements.Add(self.biceps_entry, 0, wx.ALL, 5)
        self.h_sizer3_measurements.Add(self.wrist_label, 0, 5)
        self.h_sizer3_measurements.Add(self.wrist_entry, 0, 5)
        self.h_sizer4_measurements.Add(self.waist_label, 0, 5)
        self.h_sizer4_measurements.Add(self.waist_entry, 0, wx.ALL, 5)
        self.h_sizer4_measurements.Add(self.hips_label, 0, 5)
        self.h_sizer4_measurements.Add(self.hips_entry, 0, wx.ALL, 5)
        self.h_sizer4_measurements.Add(self.shirt_length_label, 0, 5)
        self.h_sizer4_measurements.Add(self.shirt_length_entry, 0, 5)

        self.h_sizer5_measurements.Add(self.lower_body_label, 1, wx.EXPAND)
        self.h_sizer6_measurements.Add(self.trouser_waist_label, 0, 5)
        self.h_sizer6_measurements.Add(self.trouser_waist_entry, 0, wx.ALL, 5)
        self.h_sizer6_measurements.Add(self.trouser_outseam_label, 0, 5)
        self.h_sizer6_measurements.Add(self.trouser_outseam_entry, 0, wx.ALL, 5)
        self.h_sizer6_measurements.Add(self.trouser_inseam_label, 0, 5)
        self.h_sizer6_measurements.Add(self.trouser_inseam_entry, 0, 5)
        self.h_sizer7_measurements.Add(self.crotch_label, 0, 5)
        self.h_sizer7_measurements.Add(self.crotch_entry, 0, wx.ALL, 5)
        self.h_sizer7_measurements.Add(self.thigh_label, 0, 5)
        self.h_sizer7_measurements.Add(self.thigh_entry, 0, wx.ALL, 5)
        self.h_sizer7_measurements.Add(self.knee_label, 0, 5)
        self.h_sizer7_measurements.Add(self.knee_entry, 0, 5)

        self.h_sizer_buttons.Add(self.cancel_button, 0, wx.ALL, 5)
        self.h_sizer_buttons.Add(self.add_customer_button, 0, wx.ALL, 5)

        self.static_sizer2.Add(self.h_sizer1_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer2_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer3_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer4_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer5_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer6_measurements, 0, wx.EXPAND)
        self.static_sizer2.Add(self.h_sizer7_measurements, 0, wx.EXPAND)

        self.h_sizer0.Add(self.static_sizer1, 0, wx.EXPAND)
        self.h_sizer0.Add(self.static_sizer2, 1, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.Add(self.h_sizer0, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer_buttons, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Set panel's sizer
        self.SetSizer(self.v_sizer)

        # Inserting data into the fields
        self.insert_data()

    def get_customer(self):
        """This method will access the data of the selected customer."""

        # Assigning the customers list ctrl to a new variable
        self.c_list_ctrl = self.top_panel.list_ctrl
        # Accessing the database object from top panel object
        self.database = self.top_panel.database
        # Accessing the customer's ID from top panel's object
        self.customer = self.top_panel.selected_customer
        # Getting customer's ID
        self.customer_id = self.c_list_ctrl.GetItemText(self.customer, col=0)
        # Getting customer's data from database
        self.customer_data = self.database.get_customer(self.customer_id)

        # Assigning the customer's data
        self.first_name_value = self.customer_data[0][1]
        self.last_name_value = self.customer_data[0][2]
        self.address_value = self.customer_data[0][3]
        self.postcode_value = self.customer_data[0][4]
        self.phone_value = self.customer_data[0][5]
        self.email_value = self.customer_data[0][6]

        self.neck_value = self.customer_data[0][7]
        self.chest_value = self.customer_data[0][8]
        self.shoulders_value = self.customer_data[0][9]
        self.sleeve_value = self.customer_data[0][10]
        self.biceps_value = self.customer_data[0][11]
        self.wrist_value = self.customer_data[0][12]
        self.waist_value = self.customer_data[0][13]
        self.hips_value = self.customer_data[0][14]
        self.shirt_length_value = self.customer_data[0][15]

        self.trouser_waist_value = self.customer_data[0][16]
        self.trouser_outseam_value = self.customer_data[0][17]
        self.trouser_inseam_value = self.customer_data[0][18]
        self.crotch_value = self.customer_data[0][19]
        self.thigh_value = self.customer_data[0][20]
        self.knee_value = self.customer_data[0][21]

    def insert_data(self):
        """This method will insert the customer's data into the entries."""

        # Setting entries to the customer's data
        self.first_name_entry.SetValue(self.first_name_value)
        self.last_name_entry.SetValue(self.last_name_value)
        self.address_entry.SetValue(self.address_value)
        self.postcode_entry.SetValue(self.postcode_value)
        self.phone_entry.SetValue(self.phone_value)
        self.email_entry.SetValue(self.email_value)

        self.neck_entry.SetValue(str(self.neck_value))
        self.chest_entry.SetValue(str(self.chest_value))
        self.shoulders_entry.SetValue(str(self.shoulders_value))
        self.sleeve_entry.SetValue(str(self.sleeve_value))
        self.biceps_entry.SetValue(str(self.biceps_value))
        self.wrist_entry.SetValue(str(self.wrist_value))
        self.waist_entry.SetValue(str(self.waist_value))
        self.hips_entry.SetValue(str(self.hips_value))
        self.shirt_length_entry.SetValue(str(self.shirt_length_value))
        self.trouser_waist_entry.SetValue(str(self.trouser_waist_value))
        self.trouser_outseam_entry.SetValue(str(self.trouser_outseam_value))
        self.trouser_inseam_entry.SetValue(str(self.trouser_inseam_value))
        self.crotch_entry.SetValue(str(self.crotch_value))
        self.thigh_entry.SetValue(str(self.thigh_value))
        self.knee_entry.SetValue(str(self.knee_value))

    def on_button_close_update_customer(self, event):
        """This method will run whenever the cancel button is pressed."""

        # Close controller window object
        self.controller.Close()

    def on_button_update_customer(self, event):
        """This method will run whenever the update button is pressed,
           the objective of this class is to update the customer's data."""

        # Getting the values from the entry objects
        self.first_name_value = self.first_name_entry.GetValue()
        self.last_name_value = self.last_name_entry.GetValue()
        self.address_value = self.address_entry.GetValue()
        self.postcode_value = self.postcode_entry.GetValue()
        self.phone_value = self.phone_entry.GetValue()
        self.email_value = self.email_entry.GetValue()

        self.neck_value = self.neck_entry.GetValue()
        self.chest_value = self.chest_entry.GetValue()
        self.shoulders_value = self.shoulders_entry.GetValue()
        self.sleeve_value = self.sleeve_entry.GetValue()
        self.biceps_value = self.biceps_entry.GetValue()
        self.wrist_value = self.wrist_entry.GetValue()
        self.waist_value = self.waist_entry.GetValue()
        self.hips_value = self.hips_entry.GetValue()
        self.shirt_length_value = self.shirt_length_entry.GetValue()

        self.trouser_waist_value = self.trouser_waist_entry.GetValue()
        self.trouser_outseam_value = self.trouser_outseam_entry.GetValue()
        self.trouser_inseam_value = self.trouser_inseam_entry.GetValue()
        self.crotch_value = self.crotch_entry.GetValue()
        self.thigh_value = self.thigh_entry.GetValue()
        self.knee_value = self.knee_entry.GetValue()

        # Create arrays and data controller object
        data_general = []
        data_measurements = []
        data_controller = Controller("Data Controller")

        # Appending data to the arrays
        data_general.append(self.first_name_value)
        data_general.append(self.last_name_value)
        data_general.append(self.address_value)
        data_general.append(self.postcode_value)
        data_general.append(self.phone_value)
        data_general.append(self.email_value)

        data_measurements.append(self.neck_value)
        data_measurements.append(self.chest_value)
        data_measurements.append(self.shoulders_value)
        data_measurements.append(self.sleeve_value)
        data_measurements.append(self.biceps_value)
        data_measurements.append(self.wrist_value)
        data_measurements.append(self.waist_value)
        data_measurements.append(self.hips_value)
        data_measurements.append(self.shirt_length_value)
        data_measurements.append(self.trouser_waist_value)
        data_measurements.append(self.trouser_outseam_value)
        data_measurements.append(self.trouser_inseam_value)
        data_measurements.append(self.crotch_value)
        data_measurements.append(self.thigh_value)
        data_measurements.append(self.knee_value)

        # Validation of data
        empty_elements_general = [x == "" for x in data_general]
        empty_elements_measurements = [x == "" for x in data_measurements]
        float_elements = data_controller.validate_float_list(data_measurements)

        v_first_name = data_controller.validate_alpha(self.first_name_value)
        v_last_name = data_controller.validate_alpha(self.last_name_value)
        v_address = data_controller.validate_integer_alpha(self.address_value)
        v_postcode = data_controller.validate_integer_alpha(self.postcode_value)
        v_phone = data_controller.validate_integer(self.phone_value)
        v_email = data_controller.validate_email(self.email_value)

        if any(empty_elements_general):
            # If there is any empty element in the array show message
            message = wx.MessageBox("All fields are required.",
                                    "Update Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif any(empty_elements_measurements):
            # If any element is empty in the array show message
            message = wx.MessageBox("All fields are required.",
                                    "Update Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not float_elements:
            # If invalid measurements show message
            message = wx.MessageBox("Invalid measurements.",
                                    "Update Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_first_name:
            # If first name is invalid show message
            message = wx.MessageBox("Invalid first name.",
                                    "Update Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_last_name:
            # If last name is invalid show message
            message = wx.MessageBox("Invalid last name.",
                                    "Update Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_address:
            # If address is invalid show message
            message = wx.MessageBox("Invalid address.",
                                    "Update Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_postcode:
            # If postcode is invalid show message
            message = wx.MessageBox("Invalid postcode.",
                                    "Update Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_phone:
            # If phone number is invalid show message
            message = wx.MessageBox("Invalid phone number.",
                                    "Update Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_email:
            # If email is invalid show message
            message = wx.MessageBox("Invalid email.",
                                    "Update Customer",
                                    style=wx.OK|wx.ICON_WARNING)
        else:
            # If user input is valid update customer
            self.database.update_customer(self.first_name_value,
                                          self.last_name_value,
                                          self.address_value,
                                          self.postcode_value,
                                          str(self.phone_value),
                                          self.email_value,
                                          float(self.neck_value),
                                          float(self.chest_value),
                                          float(self.shoulders_value),
                                          float(self.sleeve_value),
                                          float(self.biceps_value),
                                          float(self.wrist_value),
                                          float(self.waist_value),
                                          float(self.hips_value),
                                          float(self.shirt_length_value),
                                          float(self.trouser_waist_value),
                                          float(self.trouser_outseam_value),
                                          float(self.trouser_inseam_value),
                                          float(self.crotch_value),
                                          float(self.thigh_value),
                                          float(self.knee_value),
                                          self.customer_id)

            # Show notification
            message = wx.MessageBox(("The customer has been updated "
                                     "successfully."),
                                     "Update Customer",
                                     style=wx.OK|wx.ICON_INFORMATION)

            # Update customers list ctrl and logger
            self.top_panel.view_customers()

            self.current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.message = ("[" + str(self.current_date_time) + "]" +
                            " - Customer: " +
                            str(self.first_name_value) + " " +
                            str(self.last_name_value) + " " +
                            "has been updated successfully.")
            self.logger.Append((self.message))

class UpdateProject(wx.Frame):
    """This class allows the creation of the update project window object."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel
        self.main_panel = UpdateProjectPanel(self,
                                             self,
                                             self.controller)
        # Center window
        self.Center()

class UpdateProjectPanel(wx.Panel):
    """This class allows the creation of the panel object for the
       update project window object."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Accessing objects from top panel object
        self.database = self.top_panel.database
        self.list_ctrl_projects = self.top_panel.list_ctrl_projects
        self.logger = self.top_panel.logger
        self.list_ctrl = None
        self.list_ctrl_tailors = None
        self.selected_customer = None
        self.selected_tailor = None
        self.customer = None
        self.tailor = None
        self.build()

    def build(self):
        """This method allows the creation of the panel's widgets."""

        # Create vertical and horizontal sizers
        self.v_sizer = wx.BoxSizer(wx.VERTICAL)
        self.h_sizer1 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer2 = wx.BoxSizer(wx.HORIZONTAL)
        self.h_sizer3 = wx.BoxSizer(wx.HORIZONTAL)

        # Create icon object and set it to the master window
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.master.SetIcon(self.icon)

        # Get project's data
        self.get_project()

        # Create label object and font objects
        self.title_label = wx.StaticText(self, label="Update Project")
        self.font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create panel objects
        self.general_panel = AddProjectGeneralPanel(self, size=(400, -1))
        self.customers_panel = AddProjectCustomersPanel(self,
                                                        size=(400, -1),
                                                        style=wx.SIMPLE_BORDER)

        # Create customers list ctrl object
        self.list_ctrl = self.customers_panel.customers_list_ctrl
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.get_customer)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.deselect_customer)

        # Create tailors panel object and binding methods
        self.tailors_panel = AddProjectTailorsPanel(self,
                                                    size=(400, -1),
                                                    style=wx.SIMPLE_BORDER)

        self.list_ctrl_tailors = self.tailors_panel.tailors_list_ctrl
        self.list_ctrl_tailors.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                    self.get_tailor)
        self.list_ctrl_tailors.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                                    self.deselect_tailor)

        # Create button objects and binding methods
        self.cancel_button = wx.Button(self, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON,
                                self.on_button_close_update_project)
        self.update_project_button = wx.Button(self, label="Update")
        self.update_project_button.Bind(wx.EVT_BUTTON,
                                        self.on_button_update_project)

        # Setting button fonts
        self.cancel_button.SetFont(self.font_normal)
        self.update_project_button.SetFont(self.font_normal)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
        self.h_sizer2.Add(self.general_panel, 0, wx.EXPAND)
        self.h_sizer2.Add(self.customers_panel, 1, wx.EXPAND)
        self.h_sizer2.AddSpacer(10)
        self.h_sizer2.Add(self.tailors_panel, 1, wx.EXPAND)
        self.h_sizer2.AddSpacer(10)
        self.h_sizer3.Add(self.cancel_button, 0, wx.ALL, 5)
        self.h_sizer3.Add(self.update_project_button, 0, wx.ALL, 5)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.AddSpacer(20)
        self.v_sizer.Add(self.h_sizer2, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer3, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Setting panel's sizer
        self.SetSizer(self.v_sizer)

        # Inserting data into the fields
        self.insert_data()

        # loading the data from database and inserting it into the list ctrls
        self.view_customers()
        self.list_ctrl.SetColumnWidth(0, 0)
        self.list_ctrl.SetColumnWidth(1, -2)
        self.list_ctrl.SetColumnWidth(2, -2)
        self.list_ctrl.SetColumnWidth(3, -2)
        self.list_ctrl.SetColumnWidth(4, -2)
        self.list_ctrl.SetColumnWidth(5, -2)
        self.list_ctrl.SetColumnWidth(6, -2)

        self.view_tailors()
        self.list_ctrl_tailors.SetColumnWidth(0, 0)
        self.list_ctrl_tailors.SetColumnWidth(1, -2)
        self.list_ctrl_tailors.SetColumnWidth(2, -2)
        self.list_ctrl_tailors.SetColumnWidth(3, -2)
        self.list_ctrl_tailors.SetColumnWidth(4, -2)
        self.list_ctrl_tailors.SetColumnWidth(5, -2)
        self.list_ctrl_tailors.SetColumnWidth(6, -2)

    def view_customers(self):
        """This method will load the customers data from database and it will
           insert it into the customers list ctrl."""

        # Getting customers data
        customers_data = self.database.view_customers()
        self.list_ctrl = self.customers_panel.customers_list_ctrl

        # Clearing list ctrl
        self.list_ctrl.DeleteAllItems()
        for row in customers_data:
            # Appending data
            self.list_ctrl.Append((row[0], row[1],
                                   row[2], row[3],
                                   row[4], row[5],
                                   row[6]))

    def view_tailors(self):
        """This method will load the tailors data from database and it will
           insert it into the tailors list ctrl."""

        # Getting tailors data
        tailors_data = self.database.view_tailors()
        self.list_ctrl_tailors = self.tailors_panel.tailors_list_ctrl

        # Clearing list ctrl
        self.list_ctrl_tailors.DeleteAllItems()
        for row in tailors_data:
            # Appending data
            self.list_ctrl_tailors.Append((row[0], row[1],
                                           row[2], row[3],
                                           row[4], row[5],
                                           row[6]))

    def get_customer(self, event):
        """This method will run whenever a customer is selected in the
           customers list ctrl."""

        try:
            # Assigning the customers list ctrl to a new variable
            self.list_ctrl = self.customers_panel.customers_list_ctrl
            # Get selected record
            self.selected_customer = self.list_ctrl.GetFocusedItem()
            # Get customer's ID
            self.customer = self.list_ctrl.GetItemText(self.selected_customer,
                                                       col=0)
        except:
            pass

    def get_tailor(self, event):
        """This method will run whenever a tailor is selected in the
           tailors list ctrl."""

        try:
            # Assign the tailors list ctrl to a new variable
            self.list_ctrl_tailors = self.tailors_panel.tailors_list_ctrl
            self.list_tailors = self.list_ctrl_tailors
            # Get selected record
            self.selected_tailor = self.list_ctrl_tailors.GetFocusedItem()
            # Get tailor's ID
            self.tailor = self.list_tailors.GetItemText(self.selected_tailor,
                                                        col=0)
        except:
            pass

    def deselect_customer(self, event):
        """This method will run whenever the customer is deselected in the
           customers list ctrl."""

        # Deselect customer
        self.selected_customer = None

    def deselect_tailor(self, event):
        """This method will run whenever the tailor is deselected in the
           tailors list ctrl."""

        # Deselect tailor
        self.selected_tailor = None

    def get_project(self):
        """This method will access the data of the selected project."""

        # Assigning the projects list ctrl to a new variable
        self.p_list_ctrl = self.top_panel.list_ctrl_projects
        # Assigning objects from top panel object
        self.database = self.top_panel.database
        # Getting project's data
        self.project = self.top_panel.selected_project
        self.project_id = self.p_list_ctrl.GetItemText(self.project, col=0)
        self.project_data = self.database.get_project(self.project_id)

        # Assigning the project's data to new variables
        self.name_value = self.project_data[0][1]
        self.product_value = self.project_data[0][2]
        self.material_value = self.project_data[0][3]
        self.colour_value = self.project_data[0][4]
        self.date_value = str(self.project_data[0][5].strftime("%d/%m/%Y"))
        self.delivery_value = str(self.project_data[0][6].strftime("%d/%m/%Y"))
        self.price_value = str(self.project_data[0][7])
        self.customer = int(self.project_data[0][8])
        self.tailor = int(self.project_data[0][9])

        # Formating the date (the date picker object shows wrong date)
        self.start_date = self.date_value.split("/")
        self.delivery_date = self.delivery_value.split("/")

        self.start_date_month = int(self.start_date[1]) - 1
        self.delivery_date_month = int(self.delivery_date[1]) - 1

        self.start_date_year = self.start_date[2]
        self.delivery_date_year = self.delivery_date[2]

        self.start_date_object = wx.DateTime(int(self.start_date[0]),
                                             self.start_date_month,
                                             int(self.start_date_year))

        self.delivery_date_object = wx.DateTime(int(self.delivery_date[0]),
                                                self.delivery_date_month,
                                                int(self.delivery_date_year))

    def insert_data(self):
        """This method will insert the project's data into the entries."""

        # Getting the entries
        self.name_entry = self.general_panel.name_entry
        self.product_entry = self.general_panel.product_entry
        self.material_entry = self.general_panel.material_entry
        self.colour_entry = self.general_panel.colour_entry
        self.date_entry = self.general_panel.date_entry
        self.delivery_entry = self.general_panel.delivery_date_entry
        self.price_entry = self.general_panel.price_entry

        # Setting entry values
        self.name_entry.SetValue(self.name_value)
        self.product_entry.SetValue(self.product_value)
        self.material_entry.SetValue(self.material_value)
        self.colour_entry.SetValue(self.colour_value)
        self.date_entry.SetValue(self.start_date_object)
        self.delivery_entry.SetValue(self.delivery_date_object)
        self.price_entry.SetValue(self.price_value)

    def on_button_update_project(self, event):
        """This method will run whenever the update button is pressed,
           the objective of this method is to update the project's data."""

        # Getting entry values
        self.name_value = self.general_panel.name_entry.GetValue()
        self.product_value = self.general_panel.product_entry.GetValue()
        self.material_value = self.general_panel.material_entry.GetValue()
        self.colour_value = self.general_panel.colour_entry.GetValue()
        self.date_value = self.general_panel.date_entry.GetValue()
        self.delivery_value = self.general_panel.delivery_date_entry.GetValue()
        self.price_value = self.general_panel.price_entry.GetValue()

        # Formating the dates
        self.str_date = str(self.date_value)
        self.str_delivery = str(self.delivery_value)
        self.split_date = self.str_date.split()
        self.split_delivery = self.str_delivery.split()

        self.start_date_split = self.split_date[0].split("/")
        self.delivery_date_split = self.split_delivery[0].split("/")

        self.final_start_date = (self.start_date_split[1] + "/" +
                                 self.start_date_split[0] + "/" +
                                 self.start_date_split[2])

        self.final_delivery_date = (self.delivery_date_split[1] + "/" +
                                    self.delivery_date_split[0] + "/" +
                                    self.delivery_date_split[2])

        # Declaring array and data controller object
        data_general = []
        data_controller = Controller("Data Controller")

        # Appending data to the array
        data_general.append(self.name_value)
        data_general.append(self.product_value)
        data_general.append(self.material_value)
        data_general.append(self.colour_value)
        data_general.append(self.date_value)
        data_general.append(self.delivery_value)
        data_general.append(self.price_value)

        # Validation of data
        empty_elements_general = [x == "" for x in data_general]

        v_name = data_controller.validate_alpha(self.name_value)
        v_product = data_controller.validate_alpha(self.product_value)
        v_material = data_controller.validate_alpha(self.material_value)
        v_colour = data_controller.validate_alpha(self.colour_value)
        v_price = data_controller.validate_float(self.price_value)

        if any(empty_elements_general):
            # If there is any empty element inside the array show message
            message = wx.MessageBox("All fields are required.", "Update Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_name:
            # If name is invalid show message
            message = wx.MessageBox("Invalid name.",
                                    "Update Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_product:
            # If product is invalid show message
            message = wx.MessageBox("Invalid product.",
                                    "Update Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_material:
            # If material is invalid show message
            message = wx.MessageBox("Invalid material.",
                                    "Update Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_colour:
            # If colour invalid show message
            message = wx.MessageBox("Invalid colour.",
                                    "Update Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_price:
            # If price invalid show message
            message = wx.MessageBox("Invalid price.",
                                    "Update Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif self.customer is None:
            # If no customer is selected show message
            message = wx.MessageBox("No customer selected.",
                                    "Update Project",
                                    style=wx.OK|wx.ICON_WARNING)
        elif self.tailor is None:
            # If no tailor is selected show message
            message = wx.MessageBox("No tailor selected.",
                                    "Update Project",
                                    style=wx.OK|wx.ICON_WARNING)
        else:
            # If the user input is valid update project
            self.database.update_project(self.name_value,
                                         self.product_value,
                                         self.material_value,
                                         self.colour_value,
                                         self.final_start_date,
                                         self.final_delivery_date,
                                         str(self.price_value),
                                         int(self.customer),
                                         int(self.tailor),
                                         self.project_id)

            # Show notification
            message = wx.MessageBox(("The project has been updated "
                                     "successfully."),
                                     "Update Project",
                                     style=wx.OK|wx.ICON_INFORMATION)

            # Deselect customer and tailor
            self.selected_customer = None
            self.selected_tailor = None

            # Load data from database and update projects list ctrl
            self.top_panel.view_projects()
            self.list_ctrl_projects.SetColumnWidth(0, 0)
            self.list_ctrl_projects.SetColumnWidth(1, -2)
            self.list_ctrl_projects.SetColumnWidth(2, -2)
            self.list_ctrl_projects.SetColumnWidth(3, -2)
            self.list_ctrl_projects.SetColumnWidth(4, -2)
            self.list_ctrl_projects.SetColumnWidth(5, -2)
            self.list_ctrl_projects.SetColumnWidth(6, -2)
            self.list_ctrl_projects.SetColumnWidth(7, -2)

            # Update logger
            self.current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.message = ("[" + str(self.current_date_time) + "]" +
                            " - Project: " +
                            str(self.name_value) + " " +
                            "has been updated successfully.")
            self.logger.Append((self.message))

    def on_button_close_update_project(self, event):
        """This method will run whenever the cancel button is pressed."""

        # Close the controller window object
        self.controller.Close()

class UpdateAlteration(wx.Frame):
    """This class allows the creation of the update alteration window object."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel object
        self.main_panel = UpdateAlterationPanel(self,
                                                self,
                                                self.controller)
        # Center window
        self.Center()

class UpdateAlterationPanel(wx.Panel):
    """This method will allow the creation of the update alteration panel object
       for the update alteration window object, the objective of this class is
       to update an alteration in database."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Access objects from top panel object
        self.database = self.top_panel.database
        self.list_ctrl_alterations = self.top_panel.list_ctrl_alterations
        self.logger = self.top_panel.logger
        self.list_ctrl = None
        self.list_ctrl_tailors = None
        self.selected_customer = None
        self.selected_tailor = None
        self.customer = None
        self.tailor = None
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

        # Get alteration's data
        self.get_alteration()

        # Create label object and font objects
        self.title_label = wx.StaticText(self, label="Update Alteration")
        self.font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create panel objects
        self.general_panel = AddProjectGeneralPanel(self, size=(400, -1))
        self.customers_panel = AddProjectCustomersPanel(self,
                                                        size=(400, -1),
                                                        style=wx.SIMPLE_BORDER)

        # Create customers list ctrl and bind methods
        self.list_ctrl = self.customers_panel.customers_list_ctrl
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_SELECTED, self.get_customer)
        self.list_ctrl.Bind(wx.EVT_LIST_ITEM_DESELECTED, self.deselect_customer)

        # Create tailors panel object
        self.tailors_panel = AddProjectTailorsPanel(self,
                                                    size=(400, -1),
                                                    style=wx.SIMPLE_BORDER)

        # Create tailors list ctrl object and bind methods
        self.list_ctrl_tailors = self.tailors_panel.tailors_list_ctrl
        self.list_ctrl_tailors.Bind(wx.EVT_LIST_ITEM_SELECTED,
                                    self.get_tailor)
        self.list_ctrl_tailors.Bind(wx.EVT_LIST_ITEM_DESELECTED,
                                    self.deselect_tailor)

        # Create button objects and bind methods
        self.cancel_button = wx.Button(self, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON,
                                self.on_button_close_update_alteration)
        self.update_alteration_button = wx.Button(self, label="Update")
        self.update_alteration_button.Bind(wx.EVT_BUTTON,
                                           self.on_button_update_alteration)

        # Setting button fonts
        self.cancel_button.SetFont(self.font_normal)
        self.update_alteration_button.SetFont(self.font_normal)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
        self.h_sizer2.Add(self.general_panel, 0, wx.EXPAND)
        self.h_sizer2.Add(self.customers_panel, 1, wx.EXPAND)
        self.h_sizer2.AddSpacer(10)
        self.h_sizer2.Add(self.tailors_panel, 1, wx.EXPAND)
        self.h_sizer2.AddSpacer(10)
        self.h_sizer3.Add(self.cancel_button, 0, wx.ALL, 5)
        self.h_sizer3.Add(self.update_alteration_button, 0, wx.ALL, 5)
        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.AddSpacer(20)
        self.v_sizer.Add(self.h_sizer2, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer3, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Inserting data into the fields
        self.insert_data()

        # Loading data from database and inserting it into the list ctrls
        self.view_customers()
        self.list_ctrl.SetColumnWidth(0, 0)
        self.list_ctrl.SetColumnWidth(1, -2)
        self.list_ctrl.SetColumnWidth(2, -2)
        self.list_ctrl.SetColumnWidth(3, -2)
        self.list_ctrl.SetColumnWidth(4, -2)
        self.list_ctrl.SetColumnWidth(5, -2)
        self.list_ctrl.SetColumnWidth(6, -2)

        self.view_tailors()
        self.list_ctrl_tailors.SetColumnWidth(0, 0)
        self.list_ctrl_tailors.SetColumnWidth(1, -2)
        self.list_ctrl_tailors.SetColumnWidth(2, -2)
        self.list_ctrl_tailors.SetColumnWidth(3, -2)
        self.list_ctrl_tailors.SetColumnWidth(4, -2)
        self.list_ctrl_tailors.SetColumnWidth(5, -2)
        self.list_ctrl_tailors.SetColumnWidth(6, -2)

        # Setting the panel's sizer
        self.SetSizer(self.v_sizer)

    def view_customers(self):
        """This method will load the customers data from database and it will
           insert it into the customers list ctrl."""

        # Getting the customers data
        customers_data = self.database.view_customers()
        # Assigning the customers list ctrl to a new variable
        self.list_ctrl = self.customers_panel.customers_list_ctrl

        # Clear the list ctrl
        self.list_ctrl.DeleteAllItems()
        for row in customers_data:
            # Appending data
            self.list_ctrl.Append((row[0], row[1],
                                   row[2], row[3],
                                   row[4], row[5],
                                   row[6]))

    def view_tailors(self):
        """This method will load the tailors data from database and it will
           insert it into the tailors list ctrl."""

        # Getting tailors data
        tailors_data = self.database.view_tailors()
        # Assigning the tailors list ctrl to a new variable
        self.list_ctrl_tailors = self.tailors_panel.tailors_list_ctrl

        # Clear list ctrl
        self.list_ctrl_tailors.DeleteAllItems()
        for row in tailors_data:
            # Appending data
            self.list_ctrl_tailors.Append((row[0], row[1],
                                           row[2], row[3],
                                           row[4], row[5],
                                           row[6]))

    def get_customer(self, event):
        """This method will run whenever a customer is selected in the
           customers list ctrl, this method has the objective to access
           the customer's ID."""

        try:
            # Assigning the customers list ctrl to a new variable
            self.list_ctrl = self.customers_panel.customers_list_ctrl
            # Getting the selected record
            self.selected_customer = self.list_ctrl.GetFocusedItem()
            # Getting the customer's ID
            self.customer = self.list_ctrl.GetItemText(self.selected_customer,
                                                       col=0)
        except:
            pass

    def get_tailor(self, event):
        """This method will run whenever a tailor is selected in the
           tailors list ctrl, this method has the objective to access
           the tailor's ID."""

        try:
            # Assigning the tailors list ctrl to a new variable
            self.list_ctrl_tailors = self.tailors_panel.tailors_list_ctrl
            self.list_tailors = self.list_ctrl_tailors
            # Get selected record
            self.selected_tailor = self.list_ctrl_tailors.GetFocusedItem()
            # Get tailor's ID
            self.tailor = self.list_tailors.GetItemText(self.selected_tailor,
                                                        col=0)
            print self.tailor
        except:
            pass

    def deselect_customer(self, event):
        """This method will run whenever a customer is deselected."""

        # Deselect customer
        self.selected_customer = None

    def deselect_tailor(self, event):
        """This method will run whenever a tailor is deselected."""

        # Deselect tailor
        self.selected_tailor = None

    def get_alteration(self):
        """This method has the objective to access the alteration's data."""

        # Assigning objects from top panel to new variables
        self.a_list_ctrl = self.top_panel.list_ctrl_alterations
        self.database = self.top_panel.database
        self.alteration = self.top_panel.selected_alteration
        self.alteration_id = self.a_list_ctrl.GetItemText(self.alteration, col=0)
        self.alteration_data = self.database.get_alteration(self.alteration_id)

        # Assigning alteration's data
        self.name_value = self.alteration_data[0][1]
        self.product_value = self.alteration_data[0][2]
        self.material_value = self.alteration_data[0][3]
        self.colour_value = self.alteration_data[0][4]
        self.date_value = str(self.alteration_data[0][5].strftime("%d/%m/%Y"))
        self.del_value = str(self.alteration_data[0][6].strftime("%d/%m/%Y"))
        self.price_value = str(self.alteration_data[0][7])
        self.customer = str(self.alteration_data[0][8])
        self.tailor = str(self.alteration_data[0][9])

        # Formating the dates
        self.start_date = self.date_value.split("/")
        self.delivery_date = self.del_value.split("/")

        self.start_date_month = int(self.start_date[1]) - 1
        self.delivery_date_month = int(self.delivery_date[1]) - 1

        self.start_date_year = self.start_date[2]
        self.delivery_date_year = self.delivery_date[2]

        self.start_date_object = wx.DateTime(int(self.start_date[0]),
                                             self.start_date_month,
                                             int(self.start_date_year))

        self.delivery_date_object = wx.DateTime(int(self.delivery_date[0]),
                                                self.delivery_date_month,
                                                int(self.delivery_date_year))

    def insert_data(self):
        """This method will insert the alteration's data into the fields."""

        # Accessing entries
        self.name_entry = self.general_panel.name_entry
        self.product_entry = self.general_panel.product_entry
        self.material_entry = self.general_panel.material_entry
        self.colour_entry = self.general_panel.colour_entry
        self.date_entry = self.general_panel.date_entry
        self.delivery_entry = self.general_panel.delivery_date_entry
        self.price_entry = self.general_panel.price_entry

        # Setting entries values
        self.name_entry.SetValue(self.name_value)
        self.product_entry.SetValue(self.product_value)
        self.material_entry.SetValue(self.material_value)
        self.colour_entry.SetValue(self.colour_value)
        self.date_entry.SetValue(self.start_date_object)
        self.delivery_entry.SetValue(self.delivery_date_object)
        self.price_entry.SetValue(self.price_value)

    def on_button_update_alteration(self, event):
        """This method will run whenever the update button is pressed, the
           objective of this method is to update an alteration in database."""

        # Getting entry values
        self.name_value = self.general_panel.name_entry.GetValue()
        self.product_value = self.general_panel.product_entry.GetValue()
        self.material_value = self.general_panel.material_entry.GetValue()
        self.colour_value = self.general_panel.colour_entry.GetValue()
        self.date_value = self.general_panel.date_entry.GetValue()
        self.delivery_value = self.general_panel.delivery_date_entry.GetValue()
        self.price_value = self.general_panel.price_entry.GetValue()

        # Formating dates
        self.str_date = str(self.date_value)
        self.str_delivery = str(self.delivery_value)
        self.split_date = self.str_date.split()
        self.split_delivery = self.str_delivery.split()

        self.start_date_split = self.split_date[0].split("/")
        self.delivery_date_split = self.split_delivery[0].split("/")

        self.final_start_date = (self.start_date_split[1] + "/" +
                                 self.start_date_split[0] + "/" +
                                 self.start_date_split[2])

        self.final_delivery_date = (self.delivery_date_split[1] + "/" +
                                    self.delivery_date_split[0] + "/" +
                                    self.delivery_date_split[2])

        # Creating array and data controller object
        data_general = []
        data_controller = Controller("Data Controller")

        # Appending data to the array
        data_general.append(self.name_value)
        data_general.append(self.product_value)
        data_general.append(self.material_value)
        data_general.append(self.colour_value)
        data_general.append(self.date_value)
        data_general.append(self.delivery_value)
        data_general.append(self.price_value)

        # Validation of data
        empty_elements_general = [x == "" for x in data_general]

        v_name = data_controller.validate_alpha(self.name_value)
        v_product = data_controller.validate_alpha(self.product_value)
        v_material = data_controller.validate_alpha(self.material_value)
        v_colour = data_controller.validate_alpha(self.colour_value)
        v_price = data_controller.validate_float(self.price_value)

        if any(empty_elements_general):
            # If there is any empty element in the array show message
            message = wx.MessageBox("All fields are required.",
                                    "Update Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_name:
            # If the name is invalid show message
            message = wx.MessageBox("Invalid name.",
                                    "Update Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_product:
            # If product is invalid show message
            message = wx.MessageBox("Invalid product.",
                                    "Update Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_material:
            # If material is invalid show message
            message = wx.MessageBox("Invalid material.",
                                    "Update Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_colour:
            # If colour is invalid show message
            message = wx.MessageBox("Invalid colour.",
                                    "Update Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif not v_price:
            # If price is invalid show message
            message = wx.MessageBox("Invalid price.",
                                    "Update Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif self.customer is None:
            # If no customer is selected show message
            message = wx.MessageBox("No customer selected.",
                                    "Update Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        elif self.tailor is None:
            # If no tailor is selected show message
            message = wx.MessageBox("No tailor selected.",
                                    "Update Alteration",
                                    style=wx.OK|wx.ICON_WARNING)
        else:
            # If user input is valid update alteration in database
            self.database.update_alteration(self.name_value,
                                            self.product_value,
                                            self.material_value,
                                            self.colour_value,
                                            self.final_start_date,
                                            self.final_delivery_date,
                                            str(self.price_value),
                                            int(self.customer),
                                            int(self.tailor),
                                            self.alteration_id)

            # Show notification
            message = wx.MessageBox(("The alteration has been updated "
                                     "successfully."),
                                     "Update Alteration",
                                     style=wx.OK|wx.ICON_INFORMATION)

            # Deselect records
            self.selected_customer = None
            self.selected_tailor = None

            # Update alterations list ctrl object and logger object
            self.top_panel.view_alterations()
            self.list_ctrl_alterations.SetColumnWidth(0, 0)
            self.list_ctrl_alterations.SetColumnWidth(1, -2)
            self.list_ctrl_alterations.SetColumnWidth(2, -2)
            self.list_ctrl_alterations.SetColumnWidth(3, -2)
            self.list_ctrl_alterations.SetColumnWidth(4, -2)
            self.list_ctrl_alterations.SetColumnWidth(5, -2)
            self.list_ctrl_alterations.SetColumnWidth(6, -2)
            self.list_ctrl_alterations.SetColumnWidth(7, -2)

            self.current_date_time = datetime.now().strftime("%d-%m-%Y %H:%M:%S")
            self.message = ("[" + str(self.current_date_time) + "]" +
                            " - Alteration: " +
                            str(self.name_value) + " " +
                            "has been updated successfully.")
            self.logger.Append((self.message))

    def on_button_close_update_alteration(self, event):
        """This method will run whenever the cancel button is pressed."""

        # Close controller window
        self.controller.Close()

class SearchCustomer(wx.Frame):
    """This class will allow the creation of the search customer window."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel object
        self.main_panel = SearchCustomerPanel(self, self, self.controller)
        self.Center()

class SearchCustomerPanel(wx.Panel):
    """This class will allow the creation of the search customer panel object,
       the objective of this class will allow the user to search for a customer
       based on a criteria at the user choice."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Accessing the database object from top panel object
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

        # Create label object and font objects
        self.title_label = wx.StaticText(self, label="Search Customer")
        self.font_title = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.title_label.SetFont(self.font_title)

        # Create label object
        self.search_label = wx.StaticText(self, label="Search:")
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.search_label.SetFont(self.font)

        self.by_label = wx.StaticText(self, label="by")
        self.by_label.SetFont(self.font)

        # Create choces object
        self.choices = wx.Choice(self,
                                 choices=["1-First Name",
                                          "2-Last Name",
                                          "3-Address",
                                          "4-Postcode",
                                          "5-Phone",
                                          "6-Email"])

        # Create entry object
        self.search_entry = wx.TextCtrl(self, size=(250, -1))

        # Create search button object
        self.search_button = wx.Button(self, label="Search")
        self.search_button.Bind(wx.EVT_BUTTON, self.search_customer)

        # Create customers list ctrl object
        self.list_ctrl = CustomersListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.SetColumnWidth(0, 0)

        # Add widgets to the sizers
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

    def search_customer(self, event):
        """This method will run whenever the search button is pressed,
           the objective of this method is to search for a customer."""

        # Get user selection (criteria)
        self.choices_value = self.choices.GetSelection()
        if self.choices_value == 0:
            # If user selection is the first elements in the list,
            # search for first name in database
            self.first_name = self.search_entry.GetValue()
            self.data = self.database.search_customer_first_name(self.first_name)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 1:
            # If user selection is the second item in the list,
            # search for last name in the database
            self.last_name = self.search_entry.GetValue()
            self.data = self.database.search_customer_last_name(self.last_name)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 2:
            # If user selection is the third element the list,
            # search for address in the database
            self.address = self.search_entry.GetValue()
            self.data = self.database.search_customer_address(self.address)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Clear list ctrl
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 3:
            # If user selection is the fourth element in the list,
            # search for postcode in database
            self.postcode = self.search_entry.GetValue()
            self.data = self.database.search_customer_postcode(self.postcode)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 4:
            # If user selection is the fifth elements in the list,
            # search for the phone number in database
            self.phone = self.search_entry.GetValue()
            self.data = self.database.search_customer_phone(self.phone)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 5:
            # If user selection is the sixth element in the list,
            # search for the email in the database
            self.email = self.search_entry.GetValue()
            self.data = self.database.search_customer_email(self.email)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

class SearchTailor(wx.Frame):
    """This class will allow the creation of the search tailor window object."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller= controller
        # Create main panel object
        self.main_panel = SearchTailorPanel(self,
                                            self,
                                            self.controller)
        # Center window
        self.Center()

class SearchTailorPanel(wx.Panel):
    """This class will allow the creation of the panel object for the
       search tailor window object, this class has the objective to
       search for a tailor in database."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Accessing database object from top panel object
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

        # Create label object and font object
        self.title_label = wx.StaticText(self, label="Search Tailor")
        self.font_title = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.title_label.SetFont(self.font_title)

        # Search label object
        self.search_label = wx.StaticText(self, label="Search:")
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.search_label.SetFont(self.font)

        self.by_label = wx.StaticText(self, label="by")
        self.by_label.SetFont(self.font)

        # Create choices object
        self.choices = wx.Choice(self,
                                 choices=["1-First Name",
                                          "2-Last Name",
                                          "3-Address",
                                          "4-Postcode",
                                          "5-Phone",
                                          "6-Email"])

        # Create entry object
        self.search_entry = wx.TextCtrl(self, size=(250, -1))

        # Create button object
        self.search_button = wx.Button(self, label="Search")
        self.search_button.Bind(wx.EVT_BUTTON, self.search_tailor)

        # Create tailors list ctrl object
        self.list_ctrl = TailorsListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.SetColumnWidth(0, 0)

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

    def search_tailor(self, event):
        """This method will run whenever the search button is pressed,
           the objective of this method is to search for a tailor in
           database."""

        # Get user selection
        self.choices_value = self.choices.GetSelection()
        if self.choices_value == 0:
            # If user selection is the first element in the list,
            # search for the first name in database
            self.first_name = self.search_entry.GetValue()
            self.data = self.database.search_tailor_first_name(self.first_name)

            try:
                # Clear list ctrl object
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 1:
            # If user selection is the second element in the list,
            # search for the last name in database
            self.last_name = self.search_entry.GetValue()
            self.data = self.database.search_tailor_last_name(self.last_name)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 2:
            # If user selection is the third element in the list,
            # search for the address in database
            self.address = self.search_entry.GetValue()
            self.data = self.database.search_tailor_address(self.address)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 3:
            # If user selection is the fourth element in the list,
            # search for the postcode in database
            self.postcode = self.search_entry.GetValue()
            self.data = self.database.search_tailor_postcode(self.postcode)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 4:
            # If user selection is the fifth element in the list,
            # search for the phone number in database
            self.phone = self.search_entry.GetValue()
            self.data = self.database.search_tailor_phone(self.phone)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

        if self.choices_value == 5:
            # If user selection is the sixth element in the list,
            # search for the email in database
            self.email = self.search_entry.GetValue()
            self.data = self.database.search_tailor_email(self.email)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
            except:
                pass

class SearchProject(wx.Frame):
    """This class will allow the creation of the search project window."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel object
        self.main_panel = SearchProjectPanel(self,
                                             self,
                                             self.controller)
        # Center window
        self.Center()

class SearchProjectPanel(wx.Panel):
    """This class allows the creation of the panel object for the
       search project window object, this class has the objective
       to search for a tailor in database."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Accessing database object from top panel object
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

        # Create label object and font object
        self.title_label = wx.StaticText(self, label="Search Project")
        self.font_title = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.title_label.SetFont(self.font_title)

        self.search_label = wx.StaticText(self, label="Search:")
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.search_label.SetFont(self.font)

        self.by_label = wx.StaticText(self, label="by")
        self.by_label.SetFont(self.font)

        # Create choices object
        self.choices = wx.Choice(self,
                                 choices=["1-Name",
                                          "2-Product",
                                          "3-Material",
                                          "4-Colour",
                                          "5-Start Date",
                                          "6-Delivery Date",
                                          "7-Price"])

        # Create entry object
        self.search_entry = wx.TextCtrl(self, size=(250, -1))

        # Create button object
        self.search_button = wx.Button(self, label="Search")
        self.search_button.Bind(wx.EVT_BUTTON, self.search_project)

        # Create projects list ctrl object
        self.list_ctrl = ProjectsListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.SetColumnWidth(0, 0)

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

        # Set panel's sizer
        self.SetSizer(self.v_sizer)

    def search_project(self, event):
        """This method will run whenever the search button is pressed,
           the objective of this method is to search for project in
           database."""

        # Get user selection
        self.choices_value = self.choices.GetSelection()
        if self.choices_value == 0:
            # If user selection is the first element in the list,
            # search for name in database
            self.name = self.search_entry.GetValue()
            self.data = self.database.search_project_name(self.name)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 1:
            # If user selection is the second element in the list,
            # search for product in database
            self.product = self.search_entry.GetValue()
            self.data = self.database.search_project_product(self.product)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 2:
            # If user selection is the third element in the list,
            # search for the material in database
            self.material = self.search_entry.GetValue()
            self.data = self.database.search_project_material(self.material)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 3:
            # If user selection is the fouth element in the list,
            # search for the colour in database
            self.colour = self.search_entry.GetValue()
            self.data = self.database.search_project_colour(self.colour)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 4:
            # If user selection is the fifth element in the list,
            # search for start date in database
            self.start_date = self.search_entry.GetValue()
            self.data = self.database.search_project_start_date(self.start_date)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 5:
            # If user selection is the sixth element in the list,
            # search for delivery date in database
            self.delivery = self.search_entry.GetValue()
            self.data = self.database.search_project_delivery(self.delivery)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 6:
            # If user selection is the seventh element in the list,
            # search for price in database
            self.price = self.search_entry.GetValue()
            self.data = self.database.search_project_price(self.price)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

class SearchAlteration(wx.Frame):
    """This class will allow the creation of search alteration window object."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel object
        self.main_panel = SearchAlterationPanel(self,
                                                self,
                                                self.controller)
        # Center window
        self.Center()

class SearchAlterationPanel(wx.Panel):
    """This class will allow the creation of the panel object for the
       search alteration window object, the objective of this class is
       to serach for an alteration in database."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Accessing database object from top panel object
        self.database = self.top_panel.database
        self.build()

    def build(self):
        """This method will allow the creation of the panel's widgets."""

        # Create vertical and horizontal objects
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
        self.title_label = wx.StaticText(self, label="Search Alteration")
        self.font_title = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.title_label.SetFont(self.font_title)

        self.search_label = wx.StaticText(self, label="Search:")
        self.font = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.search_label.SetFont(self.font)

        self.by_label = wx.StaticText(self, label="by")
        self.by_label.SetFont(self.font)

        # Create choices object
        self.choices = wx.Choice(self,
                                 choices=["1-Name",
                                          "2-Product",
                                          "3-Material",
                                          "4-Colour",
                                          "5-Start Date",
                                          "6-Delivery Date",
                                          "7-Price"])

        # Search entry object
        self.search_entry = wx.TextCtrl(self, size=(250, -1))

        # Create button object and bind method
        self.search_button = wx.Button(self, label="Search")
        self.search_button.Bind(wx.EVT_BUTTON, self.search_alteration)

        # Create alterations list ctrl
        self.list_ctrl = AlterationsListCtrl(self, style=wx.LC_REPORT)
        self.list_ctrl.SetColumnWidth(0, 0)

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

        # Set panel's sizer
        self.SetSizer(self.v_sizer)

    def search_alteration(self, event):
        """This method will run whenever the search button is pressed,
           the objective of this method is to search for an alteration
           in database."""

        # Get user selection
        self.choices_value = self.choices.GetSelection()
        if self.choices_value == 0:
            # If user selection is the first element in the list,
            # search for the name in database
            self.name = self.search_entry.GetValue()
            self.data = self.database.search_alteration_name(self.name)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 1:
            # If user selection is the second element in the list,
            # search for the product in database
            self.product = self.search_entry.GetValue()
            self.data = self.database.search_alteration_product(self.product)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 2:
            # If user selection is the third element in the list,
            # search for material in database
            self.material = self.search_entry.GetValue()
            self.data = self.database.search_alteration_material(self.material)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 3:
            # If user selection is the fourth element in the list,
            # search for the colour in database
            self.colour = self.search_entry.GetValue()
            self.data = self.database.search_alteration_colour(self.colour)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column wdith to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 4:
            # If user selection is the fifth element in the list,
            # search for the start date in database
            self.start_date = self.search_entry.GetValue()
            self.data = self.database.search_alteration_start_date(self.start_date)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 5:
            # If user selection is the sixth element in the list,
            # search for delivery date in database
            self.delivery = self.search_entry.GetValue()
            self.data = self.database.search_alteration_delivery(self.delivery)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

        if self.choices_value == 6:
            # If user selection is the seventh element in the list,
            # search for price in database
            self.price = self.search_entry.GetValue()
            self.data = self.database.search_alteration_price(self.price)

            try:
                # Clear list ctrl
                self.list_ctrl.DeleteAllItems()
                for row in self.data:
                    # Appending data
                    self.list_ctrl.Append((row[0],
                                           row[1],
                                           row[2],
                                           row[3],
                                           row[4],
                                           row[5],
                                           row[6],
                                           row[7]))

                # Set list ctrl column width to fit the largest item in the list
                self.list_ctrl.SetColumnWidth(0, 0)
                self.list_ctrl.SetColumnWidth(1, -2)
                self.list_ctrl.SetColumnWidth(2, -2)
                self.list_ctrl.SetColumnWidth(3, -2)
                self.list_ctrl.SetColumnWidth(4, -2)
                self.list_ctrl.SetColumnWidth(5, -2)
                self.list_ctrl.SetColumnWidth(6, -2)
                self.list_ctrl.SetColumnWidth(7, -2)
            except:
                pass

class Preferences(wx.Frame):
    """This class will allow the creation of the preferences window object."""

    def __init__(self, master, controller, *args, **kwargs):
        wx.Frame.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        # Create main panel object
        self.main_panel = PreferencesPanel(self,
                                           self,
                                           self.controller)
        # Center window
        self.Center()

class PreferencesPanel(wx.Panel):
    """This class will allow the creation of the preferences panel object."""

    def __init__(self, master, controller, top_panel, *args, **kwargs):
        wx.Panel.__init__(self, master, *args, **kwargs)
        self.master = master
        self.controller = controller
        self.top_panel = top_panel
        # Accessing objects from top panel object
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

        # Create icon object and set it to the master window
        self.icon = wx.Icon()
        self.icon.CopyFromBitmap(wx.Bitmap("images/icon_small.png",
                                           wx.BITMAP_TYPE_PNG))
        self.master.SetIcon(self.icon)

        # Create label object
        self.title_label = wx.StaticText(self, label="Preferences")
        self.font = wx.Font(18, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_header = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.BOLD)
        self.font_normal = wx.Font(12, wx.ROMAN, wx.NORMAL, wx.NORMAL)
        self.title_label.SetFont(self.font)

        # Create label object
        self.languages_label = wx.StaticText(self,
                                             label="Language:",
                                             size=(100, -1))

        # Create choice object
        self.languages_choices = wx.Choice(self,
                                           choices=["English",
                                                    "French",
                                                    "Spanish",
                                                    "Italian",
                                                    "German",
                                                    "Polish",
                                                    "Russian",
                                                    "Romanian"])

        # Setting label font
        self.languages_label.SetFont(self.font_normal)

        # Create button objects
        self.cancel_button = wx.Button(self, label="Cancel")
        self.cancel_button.Bind(wx.EVT_BUTTON, self.on_button_close_preferences)
        self.apply_button = wx.Button(self, label="Apply")
        self.apply_button.Bind(wx.EVT_BUTTON, self.on_button_apply_preferences)

        # Setting buttons font
        self.cancel_button.SetFont(self.font_normal)
        self.apply_button.SetFont(self.font_normal)

        # Adding widgets to the sizers
        self.h_sizer1.Add(self.title_label, 0)
        self.h_sizer2.Add(self.languages_label, 0)
        self.h_sizer2.Add(self.languages_choices, 1, wx.EXPAND)

        self.h_sizer_buttons.Add(self.cancel_button, 0, wx.ALL, 5)
        self.h_sizer_buttons.Add(self.apply_button, 0, wx.ALL, 5)

        self.static_sizer1.Add(self.h_sizer2, 1, wx.ALL|wx.EXPAND, 2)
        self.static_sizer1.AddSpacer(300)

        self.h_sizer0.Add(self.static_sizer1, 1, wx.EXPAND)

        self.v_sizer.Add(self.h_sizer1, 0, wx.ALIGN_CENTER_HORIZONTAL)
        self.v_sizer.Add(self.h_sizer0, 0, wx.EXPAND)
        self.v_sizer.Add(self.h_sizer_buttons, 0, wx.ALIGN_CENTER_HORIZONTAL)

        # Setting panel's sizer
        self.SetSizer(self.v_sizer)

    def on_button_apply_preferences(self, event):
        """This method will run whenever the apply button is pressed."""

        # Show notification
        message = wx.MessageBox(("Feature not available yet, "
                                 "this feature is not part of the "
                                 "functional requirements."),
                                 "Preferences",
                                 style=wx.OK|wx.ICON_INFORMATION)

    def on_button_close_preferences(self, event):
        """This method will run whenever the cancel button pressed."""

        # Close controller window
        self.controller.Close()
