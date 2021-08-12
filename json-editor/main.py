import os
import sys

from PyQt5 import uic, QtCore, QtGui, QtWidgets

import time
import json
import collections
from constants import CONSTANTS
from utils import UTILS
from helpermessageOverlay import HelperMessageOverlay

DEVELOPMENT_MODE = False
TESTING_JSON = r"C:\temp\testing.json"

ct = CONSTANTS
util = UTILS

form_class = uic.loadUiType("ui/json_editor_ui.ui")[0]
class JSONEditorWindow(QtWidgets.QMainWindow, form_class):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        self.setup_connections()

        # self.ui_parent = parent
        #
        self.HelperMessageOverlay = HelperMessageOverlay(self.main_tree)
        #
        # self.show()
        #
        self.setup_extra_ui()
        self.last_font_change_time = 1

        if DEVELOPMENT_MODE:
            self.set_json_path(path=TESTING_JSON)

        self.status_message("Ready")

    #  -------------------------------------------------- UI Setup --------------------------------------------------
    def setup_connections(self):
        # Buttons and Widgets
        self.LE_json_file.textEdited.connect(self.set_json_path)
        self.BTN_browse_file.clicked.connect(self.set_json_path)
        self.BTN_clone.clicked.connect(self.clone_selected_item)
        self.BTN_rename.clicked.connect(self.rename_selected_items)

        self.main_tree.header().sectionResized.connect(self.reset_header)

        # File menu
        self.actionNew.triggered.connect(self.new_json)
        self.actionSave.triggered.connect(self.save_data)
        self.actionSave_As.triggered.connect(lambda: self.save_data(file_prompt=True))
        self.actionOpen.triggered.connect(self.set_json_path)
        self.actionReload.triggered.connect(self.reload_json_from_path)

        # Edit Menu
        self.actionCut.triggered.connect(self.cut_selected_to_clipboard)
        self.actionCopy.triggered.connect(self.copy_selected_to_clipboard)
        self.actionPaste.triggered.connect(self.paste_data_from_clipboard)
        self.actionDelete.triggered.connect(self.delete_selected_items)

        self.actionCreate_New_Item.triggered.connect(lambda: self.create_new_of_type(type_from_majority=True))
        self.actionMove_Up.triggered.connect(lambda: self.reorder_item(-1))
        self.actionMove_Down.triggered.connect(lambda: self.reorder_item(1))

        self.actionParent.triggered.connect(self.reparent_selected_items)
        self.actionUnParent.triggered.connect(lambda: self.reparent_selected_items(to_world=True))

        # UI Menu
        self.actionReset_Font_Size.triggered.connect(self.set_tree_font_size)
        self.actionIncrease_Font_Size.triggered.connect(lambda: self.increment_tree_font_size(1))
        self.actionDecrease_Font_Size.triggered.connect(lambda: self.increment_tree_font_size(-1))

    def get_standard_icon(self, icon_name):
        return self.style().standardIcon(getattr(QtWidgets.QStyle, icon_name))

    def setup_extra_ui(self):
        # Right-click menu
        self.main_tree.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
        self.main_tree.customContextMenuRequested.connect(self.context_menu)

        # icons
        self.BTN_browse_file.setIcon(self.get_standard_icon("SP_DialogOpenButton"))

        self.actionNew.setIcon(self.get_standard_icon("SP_DialogResetButton"))
        self.actionOpen.setIcon(self.get_standard_icon("SP_DialogOpenButton"))
        self.actionSave.setIcon(self.get_standard_icon("SP_DialogSaveButton"))
        self.actionReload.setIcon(self.get_standard_icon("SP_BrowserReload"))

        header = self.main_tree.header()
        header.setDefaultAlignment(QtCore.Qt.AlignCenter)
        header.setSectionResizeMode(1, QtWidgets.QHeaderView.Stretch)
        header.setStretchLastSection(False)
        header.resizeSection(0, 200)
        self.reset_header()

        self.main_tree.viewport().installEventFilter(self)

        # self.main_tree.collapseAll()
        # header.setSectionResizeMode(0, QtWidgets.QHeaderView.Stretch)
        # header.setSectionResizeMode(2, QtWidgets.QHeaderView.Stretch)
        # self.main_tree.header().ResizeMode(QtWidgets.QHeaderView.ResizeToContents)
        # self.main_tree.header().ResizeMode(QtWidgets.QHeaderView.Interactive)

    def reset_header(self):
        self.main_tree.header().resizeSection(2, 80)

    def context_menu(self):
        """
        Builds the Right-click menu for the tree widget

        :return:
        """
        menu = QtWidgets.QMenu()

        actions = [{"Cut": self.cut_selected_to_clipboard},
                   {"Copy": self.copy_selected_to_clipboard},
                   {"Paste": self.paste_data_from_clipboard},
                   {"Delete": self.delete_selected_items}
                   ]

        if self.last_selected_type() not in ct.NOT_CHILD_ALLOWED:
            actions += ["-",
                        {"+ Dict": lambda: self.create_new_of_type(data_type="dict")},
                        {"+ List": lambda: self.create_new_of_type(data_type="list")}
                        ]

            if self.json_base_exists():
                actions += [{"+ Int": lambda: self.create_new_of_type(data_type="int")},
                            {"+ Float": lambda: self.create_new_of_type(data_type="float")},
                            {"+ Unicode": lambda: self.create_new_of_type(data_type="bytes")}
                            ]

        actions += ["-",
                    {"Save JSON": self.save_data},
                    {"Clear JSON": self.clear_tree}
                    ]

        for action in actions:
            if action == "-":
                menu.addSeparator()
                continue

            for action_title, action_command in action.items():
                atn = menu.addAction(action_title)
                atn.triggered.connect(action_command)

        cursor = QtGui.QCursor()
        menu.exec_(cursor.pos())

    #  -------------------------------------------------- Events -----------------------------------------------------

    def eventFilter(self, qobject, event):
        if event.type() == QtCore.QEvent.Wheel:
            modifiers = QtWidgets.QApplication.keyboardModifiers()
            if modifiers == QtCore.Qt.ControlModifier:
                if event.delta() > 0:
                    self.increment_tree_font_size(1)
                else:
                    self.increment_tree_font_size(-1)
                return True

            return False
        return False  # standard event processing

    def dragEnterEvent(self, e):
        if e.mimeData().hasText():
            e.accept()
        else:
            e.ignore()

    def dropEvent(self, event):
        if event.mimeData().hasUrls():  # if file or link is dropped
            url = event.mimeData().urls()[0]  # get first url
            self.set_json_path(path=url.toLocalFile())
        else:
            try:
                text = event.mimeData().text()
                json_data = json.loads(text, object_pairs_hook=collections.OrderedDict)
                self.load_json_data(json_data=json_data)
            except ValueError:
                self.status_message("No JSON serializable data could be read from string")
            # except ValueError, e:
            #     self.status_message("No JSON serializable data could be read from string")

    def resizeEvent(self, event):
        self.HelperMessageOverlay.resize(event.size())
        event.accept()

    #  -------------------------------------------------- Font Size --------------------------------------------------
    def increment_tree_font_size(self, direction):
        if time.time() - self.last_font_change_time < 0.02:
            return

        current_font = self.main_tree.font()
        new_font_size = current_font.pointSize() + direction
        self.set_tree_font_size(new_font_size)

    def set_tree_font_size(self, size=7):
        current_font = self.main_tree.font()
        current_font.setPointSizeF(size)
        self.main_tree.setFont(current_font)
        self.last_font_change_time = time.time()
        self.HelperMessageOverlay.font_size = size + 6
        self.status_message("Font size set to: {}".format(size))

    #  -------------------------------------------------- ClipBoard --------------------------------------------------
    def cut_selected_to_clipboard(self):
        selected_items = self.get_selected_items()
        self.copy_selected_to_clipboard()
        self.delete_selected_items()
        self.status_message("Cut: {} item(s)".format(len(selected_items)))

    def copy_selected_to_clipboard(self):
        """
        Puts the selected data into the users clipboard for copying and pasting as they wish

        :return:
        """
        selected_items = self.get_selected_items()
        selected_data = self.get_selected_data()
        if not selected_data:
            return
        # Save to clipboard
        str_data = json.dumps(selected_data)
        cb = QtWidgets.QApplication.clipboard()
        cb.setText(str_data, mode=cb.Clipboard)

        self.status_message("Copied: {} item(s)".format(len(selected_items)))

    def get_selected_data(self):
        """
        Gets data from all selected items

        :return:
        """
        selected_items = self.get_selected_items()
        if not selected_items:
            return ""

        if len(selected_items) < 2:
            item = selected_items[0]
            copy_data = {}  # Exit early here if it's a dict
            the_data = self.get_tree_widget_item_data(item)
            copy_data[item.text(ct.KEY_FIELD)] = the_data
            return copy_data

        else:
            all_data = []
            for item in self.main_tree.selectedItems():
                # if get_data_type(item) in ["list", "tuple"]:
                copy_data = collections.OrderedDict()
                the_data = self.get_tree_widget_item_data(item)
                copy_data[item.text(ct.KEY_FIELD)] = the_data
                all_data.append(copy_data)

            return all_data

    def paste_data_from_clipboard(self):
        """
        Reads the clipboard and builds the UI from the copied data

        :return:
        """
        cb = QtWidgets.QApplication.clipboard()
        str_data = cb.text()

        """
        # If path in clipboard
        # Commenting out because you might just want to paste in a path into a value field

        path = None
        if os.path.exists(str_data):
            path = str_data

        if not path and str_data.startswith('"') and str_data.endswith('"'):
            path = str_data[1:-1] if os.path.exists(str_data[1:-1]) else ""

        if path:
            return self.set_json_path(path)
        """
        # if json data in clipboard
        try:
            clipboard_data = json.loads(str_data, object_pairs_hook=collections.OrderedDict)
        except ValueError:
            self.status_message("No JSON serializable data could be read from clipboard")
            return

        # if nothing exists in the UI, build everything at root
        if not self.json_base_exists():
            self.create_data_tree(data=clipboard_data)
            self.main_tree.expandToDepth(0)
            return

        # get items to paste under
        selected_items = self.main_tree.selectedItems()
        if not selected_items:
            selected_items = [self.main_tree.topLevelItem(0)]

        # Make sure the data can be recreated good
        if isinstance(clipboard_data, (list, tuple)):
            all_data = collections.OrderedDict()
            for copy_data in clipboard_data:
                if isinstance(copy_data, (dict, collections.OrderedDict)):
                    all_data.update(copy_data)

            if not all_data:  # Wut
                all_data = {"": clipboard_data}  # had a spot of trouble with copying lists, this seems to work
        else:
            all_data = clipboard_data

        # Paste into all selected places
        for selected_item in selected_items:
            if util.get_data_type(selected_item) not in ct.CHILD_ALLOWED:
                return

            for key, val in all_data.items():

                new_tree = self.create_data_tree(data=val, parent_item=selected_item)

                if util.get_data_type(new_tree.parent()) not in ct.LIST_TYPES:
                    unique_key = util.get_unique_dict_key(new_tree.parent(), key_name=key)
                    new_tree.setData(ct.KEY_FIELD, QtCore.Qt.DisplayRole, unique_key)

            util.fix_list_indices(selected_item)

        self.status_message("Pasted: {} item(s)".format(len(all_data.keys())))

    #  -------------------------------------------------- JSON Path ------------------------------------------------

    def set_json_path(self, path=None, read_file=True):
        print('set_json_path')
        if not path:
            path, _ = QtWidgets.QFileDialog.getOpenFileName(self, 'Open File')

        if not path:
            return

        old_path = self.LE_json_file.text()
        path = path.replace("\\", "/")
        self.LE_json_file.setText(path)

        if read_file:
            success = self.load_json_data()
            if success:
                self.status_message("Opened: {}".format(path))
            else:
                self.LE_json_file.setText(old_path)

    def get_json_path(self):
        """
        Gets the file path at the top

        :return:
        """
        path = self.LE_json_file.text()
        if not path:
            self.set_json_path(read_file=False)

        path = self.LE_json_file.text()
        return path

    def get_json_data_from_path(self):
        """
        Uses the file path and returns the json data inside

        :return:
        """
        data = {}

        json_path = self.LE_json_file.text()
        if not os.path.exists(json_path):
            self.status_message("Path does not exist: {}".format(json_path))
            return data

        if not os.path.isfile(json_path):
            self.status_message("Path does not exist: {}".format(json_path))
            return data

        with open(json_path, "r") as fp:
            try:
                data = json.load(fp, object_pairs_hook=collections.OrderedDict)
            except ValueError:
                self.status_message("No JSON serializable data could be read from file: {}".format(json_path))
        return data

    def reload_json_from_path(self):
        self.load_json_data()
        self.status_message("Reloaded: {}".format(self.get_json_path()))

    #  -------------------------------------------------- Read & Write ------------------------------------------------

    def load_json_data(self, json_data=None):
        """
        Reads the indicated json and creates the tree widget from it

        :return:
        """
        if not json_data:
            json_data = self.get_json_data_from_path()
            if not json_data:
                return

        self.main_tree.clear()

        self.create_data_tree(master_key="", data=json_data)

        self.main_tree.expandToDepth(0)
        if DEVELOPMENT_MODE:
            self.main_tree.expandAll()

        return True

    def create_data_tree(self, master_key=None, data=None, parent_item=None):
        """
        Generates the tree widget items from indicated data

        :param master_key:
        :param data:
        :param parent_item:
        :return:
        """
        if parent_item is None:
            parent_item = self.main_tree

        if isinstance(data, (dict, collections.OrderedDict)):
            parent_item = QtWidgets.QTreeWidgetItem(parent_item, [master_key])
            parent_item.setFlags(parent_item.flags() | QtCore.Qt.ItemIsEditable)
            parent_item.setData(ct.TYPE_FIELD, QtCore.Qt.DisplayRole, ct.DT_DICT)

            for key, val in data.items():
                self.create_data_tree(master_key=key, data=val, parent_item=parent_item)

        elif isinstance(data, (list, tuple)):
            parent_item = QtWidgets.QTreeWidgetItem(parent_item, [master_key])
            parent_item.setFlags(parent_item.flags() | QtCore.Qt.ItemIsEditable)
            parent_item.setData(ct.TYPE_FIELD, QtCore.Qt.DisplayRole, type(data).__name__)

            for i, sub_val in enumerate(data):
                self.create_data_tree(master_key="[{}]".format(i), data=sub_val, parent_item=parent_item)

        # elif isinstance(data, (str, unicode, float, int)):
        elif isinstance(data, (str, bytes, float, int)):
            parent_item = util.create_new_item(key=master_key, data=data, data_type=type(data).__name__, parent_item=parent_item)

        self.HelperMessageOverlay.setVisible(False)

        return parent_item

    def save_data(self, file_prompt=False):
        """
        Gathers all the data from the tree widget and saves it to the indicated JSON file

        :param file_prompt:
        :return:
        """
        tree_data = None
        for i in range(self.main_tree.topLevelItemCount()):
            top_item = self.main_tree.topLevelItem(i)
            tree_data = self.get_tree_widget_item_data(top_item)

        if tree_data:
            output_path = self.get_json_path()
            if not output_path or file_prompt:
                output_path, _ = QtWidgets.QFileDialog.getSaveFileName(self, 'Save File')

            if not output_path:
                return

            output_path = output_path.replace("\\", "/")

            if DEVELOPMENT_MODE:
                output_path = output_path.replace(".", "_TEMP.") if "_TEMP" not in output_path else output_path

            self.set_json_path(path=output_path, read_file=False)
            self.status_message("Saved: {}".format(output_path))

            with open(output_path, "w") as fp:
                # json.dump(tree_data, fp, indent=2)
                json.dump(tree_data, fp)

        else:
            self.status_message("No Data found to save")

    def new_json(self):
        """
        Resets the tree
        :return:
        """
        self.clear_tree()
        self.LE_json_file.setText("")
        self.status_message("Cleared")

    #  --------------------------------------------------- Edit Items -------------------------------------------------

    def clone_selected_item(self):
        """
        Clones the selected data and creates a unique key if in a dictionary

        :return:
        """
        new_items = []
        for item in self.get_selected_items():
            new_item = item.clone()
            item.parent().addChild(new_item)
            new_items.append(new_item)
            item.setSelected(False)

        for new_item in new_items:
            new_item.setSelected(True)

            if util.get_data_type(new_item.parent()) == ct.DT_DICT:
                unique_key = util.get_unique_dict_key(new_item.parent(), key_name=new_item.text(ct.KEY_FIELD))
                new_item.setData(ct.KEY_FIELD, QtCore.Qt.DisplayRole, unique_key)

            if util.get_data_type(new_item.parent()) in ct.LIST_TYPES:
                util.fix_list_indices(new_item.parent())

        self.rename_selected_items()
        self.status_message("Cloned: {} item(s)".format(len(new_items)))

    def rename_selected_items(self):
        """
        Renames selected items with data from prefix, suffix, search, and replace field
        :return:
        """
        modify_key = "Key" in self.CB_thing_to_modify.currentText()
        modify_value = "Value" in self.CB_thing_to_modify.currentText()

        widgets = []
        for item in self.get_selected_items():
            widgets.append(item)
            if self.CB_hierarchy_search_replace.isChecked():
                widgets += util.get_sub_widgets(item)

        for widget in widgets:
            if modify_key:
                new_key_name = self.generate_new_name(widget.text(ct.KEY_FIELD))
                widget.setData(ct.KEY_FIELD, QtCore.Qt.DisplayRole, new_key_name)

            if modify_value:
                new_value = self.generate_new_name(widget.text(ct.VALUE_FIELD))
                widget.setData(ct.VALUE_FIELD, QtCore.Qt.DisplayRole, new_value)

        self.status_message("Renamed: {} item(s)".format(len(widgets)))

    def delete_selected_items(self):
        to_delete = self.get_selected_items()
        for item in to_delete:
            try:
                item.parent().removeChild(item)
            except AttributeError:
                pass

        self.status_message("Deleted: {} item(s)".format(len(to_delete)))

    def reorder_item(self, direction=1):
        """
        This thing is such a mess

        Tries to reorder the selected items up or down

        :param direction:
        :return:
        """
        resolve_list_indices = []
        selected_items = self.get_selected_items()
        if direction == 1:
            selected_items.reverse()

        # sorted(selected_items, key=lambda student: student.parent().indexOfChild(student))

        for i, item in enumerate(selected_items):  # Find new indices for selected items
            parent_item = item.parent()
            was_expanded = item.isExpanded()

            current_index = parent_item.indexOfChild(item)
            new_index = current_index + direction

            if new_index < 0:
                new_index = 0
            if new_index > parent_item.childCount() - 1:
                new_index = parent_item.childCount() - 1

            parent_item.takeChild(current_index)
            parent_item.insertChild(new_index, item)  # ReOrder

            resolve_list_indices.append(parent_item)
            item.treeWidget().setCurrentItem(item)  # Set highlight focus
            item.setExpanded(was_expanded)
            parent_item.setExpanded(True)

        if direction == 1:
            selected_items.reverse()  # reverse back

        for item in selected_items:  # ReSelect
            item.setSelected(True)

        util.fix_list_indices(resolve_list_indices)

    def create_new_of_type(self, data_type="bytes", type_from_majority=False):
        """
        Creates a new item under selected parent

        :param data_type:
        :param type_from_majority: reads the currently existing values of parent and creates a new item of the same type
        :return:
        """
        if not self.json_base_exists():
            start_item = QtWidgets.QTreeWidgetItem(self.main_tree, ["", "", ct.DT_DICT])
            start_item.setSelected(True)
            self.HelperMessageOverlay.setVisible(False)
            return

        selected_items = self.get_selected_items()

        for parent_item in selected_items:
            if util.get_data_type(parent_item) in ct.NOT_CHILD_ALLOWED:
                continue

            if type_from_majority:
                all_data_types_in_parent = [util.get_data_type(child_item) for child_item in util.get_sub_widgets(parent_item)]
                if all_data_types_in_parent:
                    data_type = util.majority_element(all_data_types_in_parent)

            new_item = util.create_new_item(data_type=data_type, parent_item=parent_item)
            new_item.setSelected(True)

        self.status_message("Created new: {} item(s) of type: {}".format(len(selected_items), data_type))

    def reparent_selected_items(self, to_world=False):
        """
        Parents items to the last selected item

        :param to_world:
        :return:
        """
        selected_items = self.get_selected_items()
        if not to_world and len(selected_items) < 2:
            return

        if to_world:
            target_parent_item = self.main_tree.topLevelItem(0) if self.main_tree.topLevelItemCount() else None
        else:
            target_parent_item = selected_items[-1]
            selected_items = selected_items[:-1]

        if not target_parent_item or util.get_data_type(target_parent_item) in ct.NOT_CHILD_ALLOWED:
            return

        for item in selected_items:
            was_expanded = item.isExpanded()

            item.parent().takeChild(item.parent().indexOfChild(item))  # actual parenting action
            target_parent_item.addChild(item)

            item.setExpanded(was_expanded)
            item.setSelected(True)

        if util.get_data_type(target_parent_item) in ct.LIST_TYPES:
            util.fix_list_indices(target_parent_item)

        self.status_message("Parented : {} item(s)".format(len(selected_items)))

    #  --------------------------------------------------- Utilities --------------------------------------------------

    def get_tree_widget_item_data(self, tree_widget_item):
        """
        Returns all the data from the item hierarchy

        :param tree_widget_item:
        :return:
        """
        data_type = util.get_data_type(tree_widget_item)

        if data_type in ct.DT_DICT:
            all_sub_data = collections.OrderedDict()
            for sub_widget in util.get_sub_widgets(tree_widget_item):
                all_sub_data[sub_widget.text(ct.KEY_FIELD)] = self.get_tree_widget_item_data(sub_widget)

            data = all_sub_data

        elif data_type in ct.LIST_TYPES:
            all_sub_data = []
            for sub_widget in util.get_sub_widgets(tree_widget_item):
                all_sub_data.append(self.get_tree_widget_item_data(sub_widget))

            data = all_sub_data

        else:
            data = tree_widget_item.text(ct.VALUE_FIELD)
            if data_type in ["str", ct.DT_BYTES, ct.DT_INT, ct.DT_FLOAT]:
                data = util.convert_data_type(data, data_type)  # Jesus there's a lot of "data" here

        return data

    def json_base_exists(self):
        return self.main_tree.topLevelItemCount()

    def clear_tree(self):
        self.main_tree.clear()
        self.HelperMessageOverlay.setVisible(True)

    def get_selected_items(self):
        return self.main_tree.selectedItems()

    def last_selected_type(self):
        """
        Returns the type of the last selected item

        :return:
        """
        selected_items = self.get_selected_items()
        if not selected_items:
            return ""

        indicated_item = selected_items[-1]
        return util.get_data_type(indicated_item)

    def generate_new_name(self, current_name):
        """
        Uses the prefix, suffix, search and replaces to generate a new name from the input

        :param current_name:
        :return:
        """
        prefix = self.LE_prefix.text()
        suffix = self.LE_suffix.text()
        searches = self.LE_search.text().split(",")
        replaces = self.LE_replace.text().split(",")
        for search, replace in zip(searches, replaces):
            current_name = current_name.replace(search, replace)

        return "{}{}{}".format(prefix, current_name, suffix)

    def status_message(self, text=""):
        current_time = time.strftime("%H:%M:%S", time.gmtime())
        full_message = "{} - {}".format(current_time, text)
        self.statusbar.showMessage(full_message)

    #  ------------------------------------------------ Standalone Utils --------------------------------------------------



if __name__ == "__main__":
    app = QtWidgets.QApplication(sys.argv)
    main = JSONEditorWindow()
    main.show()
    sys.exit(app.exec_())
