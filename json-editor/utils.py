from PyQt5 import uic, QtCore, QtGui, QtWidgets
import re
from constants import CONSTANTS
ct = CONSTANTS
class UTILS:
    @staticmethod
    def get_sub_widgets(tree_widget_item):
        return [tree_widget_item.child(i) for i in range(tree_widget_item.childCount())]

    @staticmethod
    def get_data_type(tree_widget_item):
        return tree_widget_item.text(ct.TYPE_FIELD)


    @staticmethod
    def majority_element(num_list):
        """
        Find the element which shows up the most in a list

        :param num_list:
        :return:
        """
        index, control = 0, 1

        for i in range(1, len(num_list)):
            if num_list[index] == num_list[i]:
                control += 1
            else:
                control -= 1
                if control == 0:
                    index = i
                    control = 1

        return num_list[index]

    @staticmethod
    def convert_data_type(data, data_type):
        """
        Converts the input string or whatever to appropriate format for saving

        :param data:
        :param data_type:
        :return:
        """
        if data_type in [ct.DT_INT, ct.DT_FLOAT]:
            try:  # This is kinda dumb
                if data_type == ct.DT_INT:  # check if the values in the fields are valid
                    int(data)
                if data_type == ct.DT_FLOAT:
                    float(data)

            except ValueError:
                data = "".join([s for s in str(data) if not s.isalpha()])  # remove letters

        eval_statement = "{}('{}')".format(data_type, data)
        data = eval(eval_statement)

        return data

    @staticmethod
    def create_new_item(key="", data="", data_type="dict", parent_item=None):
        print('create_new_item')
        """
        Creates a new item in the tree widget

        :param key:
        :param data:
        :param data_type:
        :param parent_item:
        :return:
        """
        widget_item = QtWidgets.QTreeWidgetItem(parent_item, [key, str(data)])
        widget_item.setFlags(parent_item.flags() | QtCore.Qt.ItemIsEditable)
        widget_item.setData(ct.TYPE_FIELD, QtCore.Qt.DisplayRole, data_type)
        if parent_item:
            parent_type = UTILS.get_data_type(parent_item)
            UTILS.fix_list_indices(parent_item)

            if parent_type == "dict" and not key:
                widget_item.setData(ct.KEY_FIELD, QtCore.Qt.DisplayRole, UTILS.get_unique_dict_key(parent_item))

        if not data:
            if data_type in ["float"]:
                widget_item.setData(ct.VALUE_FIELD, QtCore.Qt.DisplayRole, 0.0)

            if data_type in ["int"]:
                widget_item.setData(ct.VALUE_FIELD, QtCore.Qt.DisplayRole, 0)

            if data_type in ["unicode"]:
                widget_item.setData(ct.VALUE_FIELD, QtCore.Qt.DisplayRole, "STRING")

        return widget_item

    @staticmethod
    def get_unique_dict_key(parent_item, key_name="KEY_0"):
        """
        Creates a unique key to use in a dictionary
        +1 to end of name if key already exists

        :param parent_item:
        :param key_name:
        :return:
        """
        existing_keys = [i.text(ct.KEY_FIELD) for i in UTILS.get_sub_widgets(parent_item)]
        if key_name and key_name not in existing_keys:
            return key_name

        if not key_name[-1].isdigit():
            key_name += "_0"

        while key_name in existing_keys:
            old_index = re.findall(r'\d+', key_name)[-1]
            key_name_without_last_number = key_name[:-len(str(old_index))]
            key_name = key_name_without_last_number + str(int(old_index) + 1)

        return key_name

    @staticmethod
    def fix_list_indices(parent_item):
        print('fix_list_indices')
        """
        Sets the list indices on a list tree widget item

        :param parent_item:
        :return:
        """
        if not isinstance(parent_item, list):
            parent_item = [parent_item]

        # print(parent_item)
        # resolve_list_indices = list(set(parent_item))  # Fix indices of list items
        # for item in resolve_list_indices:
        for item in parent_item:
            if UTILS.get_data_type(item) not in ["list", "tuple"]:
                continue

            children = UTILS.get_sub_widgets(item)
            for i, child_item in enumerate(children):
                child_item.setData(ct.KEY_FIELD, QtCore.Qt.DisplayRole, "[{}]".format(i))
