# Painter API Import
from itertools import dropwhile
from logging import INFO
from re import sub
import sys
from tkinter.tix import ComboBox, Tree

from math import log2
# from os import startfile

import os


# for path in sys.path:
#     print(f"Path: {path}")
# sys.path.append('/Applications/Adobe Substance 3D Painter.app/Contents/Resources/python/modules', '/Users/aranazadahmed/Documents/Adobe/Adobe Substance 3D Painter/python/modules')


#print (f"System Path is: {sys.path}")
# import substance_painter


# 3rd Party UI Library Import
# from PySide2.QtWidgets import QtWidget

# Custom Exporter Module import
import modules_export
import module_validation_name
import module_validation_resolution


# Default utils imports
import importlib

# Remove for production
is_user_dev = True

if is_user_dev:
    importlib.reload(modules_export)
    importlib.reload(module_validation_name)
    importlib.reload(module_validation_resolution)

# test_widget.py
import substance_painter
import substance_painter_plugins
import substance_painter.event
import substance_painter.textureset

from PySide2 import QtCore, QtGui
from PySide2.QtWidgets import QApplication, QListWidget, QWidget, QAction, QLineEdit , QVBoxLayout, QHBoxLayout, QCheckBox, QComboBox, QMenu, QLabel, QPushButton, QGridLayout, QTableWidget, QTableWidgetItem, QDialog, QDialogButtonBox
from PySide2.QtCore import QEvent, Qt

# Global variable
custom_exporter = None
personal_checkbox = None
custom_exporter_obj_name = "custom_exporter"

# Lists to populate the Texset Rename editor : Extension Task - Make these lists be populated from a JSON / Spreadsheet thing
asset_types_acronyms = ['PROP', 'WPN', 'CHAR']

asset_detail_01_props = ['CHR','TBL', 'LMP', 'WIN']
asset_detail_01_wpns = ['SWD','BOW', 'RFL', 'EXP']
asset_detail_01_chars = ['PLR', 'ENM', 'CIV']

asset_detail_02_props = ['S','M', 'L']
asset_detail_02_wpns = ['COM','RAR', 'EPC']
asset_detail_02_chars = ['ML','FL', 'NB']

class CustomExporter:
    def __init__(self):
        self.initialization()
        
    def initialization(self):
        # Refactored methods
        self.init_widget_window()
        self.connect_widget_events()
        self.connect_painter_events()
        self.show_ui_widgets()
        
        # self.fill_texset_table()
        
        
        # Debugging setup : Dev use only
        is_debugging = False
        if is_debugging:
            import ptvsd
            port = 3000
            ptvsd.enable_attach(address=("localhost", port))
            substance_painter.logging.log(substance_painter.logging.WARNING, "custom_exporter", f"Waiting for the debugger to attach from VS Code in port {port}")

    def init_widget_window(self):
        # Variables
        self.asset_types = ['Props','Weapons','Characters']
        self.shader_types = ['Basic','Armament','Morph']
        self.texset_with_overbudget_res = []
        self.widget = QWidget()
        self.widget.setObjectName(custom_exporter_obj_name)
        self.widget.setWindowTitle("Custom Exporter") 

        # File directory
        self.file_dir = os.path.dirname(__file__)
        # Icon path directory addons
        self.icons_path = os.path.join(self.file_dir, "Icons")
        self.pixmap_help_path = os.path.join(self.icons_path, "help.png")
        # Icon paths application
        self.icon_main_window = QtGui.QIcon(os.path.join(self.icons_path, "main_window_icon.png"))
        self.icon_validation_ok = QtGui.QIcon(os.path.join(self.icons_path, "validation_ok.png"))
        self.icon_validation_fail = QtGui.QIcon(os.path.join(self.icons_path, "validation_fail.png"))
        self.pixmap_help = QtGui.QPixmap(self.pixmap_help_path)
        
        self.widget.setWindowIcon(self.icon_main_window)

        # Add a widget
        self.main_layout = QVBoxLayout(self.widget)

        help_layout = QHBoxLayout()
        help_layout.setAlignment(QtCore.Qt.AlignRight)

        help_label = QLabel() 
        scaled_pixmap = self.pixmap_help.scaled(32,32)
        help_label.setPixmap(scaled_pixmap)
        help_label.setFixedSize(scaled_pixmap.size())
        help_label.mousePressEvent = self.on_open_help_document
        help_label.setToolTip("Click Here show the help documentation. \
                              \nHotkey: Alt + F1")
        help_layout.addWidget(help_label)

        # Creating QAction to handle the Documentation shortcut as the QLabel doesn't contain setShortcut method
        self.help_action = QAction("Show Help", self.widget)
        self.help_action.setShortcut(QtCore.Qt.ALT + QtCore.Qt.Key_F1)
        self.widget.addAction(self.help_action)

        # Adds help_layout to main_layout : align right
        self.main_layout.addLayout(help_layout)
        
        # Personal export checkbox
        # Implement Checkbox
        self.personal_export_cb = QCheckBox("Personal Export")
        self.personal_export_cb.setToolTip("Specify desired project root export path: Personal or Official")
        
        # Add cb to mainlayout
        self.main_layout.addWidget(self.personal_export_cb)
        self.personal_export_cb.setChecked(False)

        #Add text
        self.label_01 = QLabel()

        self.main_layout.addWidget(self.label_01)

        #QCombo Box - combines button with a dropdown list
        self.asset_type_cbbx = QComboBox()
        # for i in self.asset_types:
        #     self.asset_type_cbbx.addItem(i) 
        
        self.asset_type_cbbx.addItems(self.asset_types)
        self.asset_type_cbbx.setToolTip("Set the desired Asset type. \nIt will affect Export path generation and Texture Set validation.")

        self.main_layout.addWidget(self.asset_type_cbbx)
        current_index_dropdown = self.asset_type_cbbx.currentText()

        # This sets the text of the Asset type : to equal the dropdown input but is only called at start
        # Fix to update when setting changes
        self.label_01.setText(f"Asset Type: {current_index_dropdown}")

        # Button for Refreshing the list
        self.refresh_button = QPushButton("Refresh")
        self.refresh_button.setToolTip("This button will refresh the results of the tool. \nHotkey: Alt + R")
        self.refresh_button.setShortcut(QtCore.Qt.ALT + QtCore.Qt.Key_R)
        self.main_layout.addWidget(self.refresh_button)

        # QTableWidget, include : coloumn 1 : Export checkbox, coloumn2 : Texture set name, coloumn 3 : Shader Type dropdown, Rows, coloumns
        self.texset_table = QTableWidget()
        self.texset_table.setMinimumSize(730, 250)
        # Initialize tex set table IMPORTANT
        self.init_texset_table()
        self.main_layout.addWidget(self.texset_table)

        # List Widget Init
        # layout = QVBoxLayout()
        # self.menu_widget = QWidget()
        # self.menu_widget.setLayout(layout)

        self.list_widget = QListWidget()
        # self.list_widget.addItems(('Rename'), ('Close'))
        # layout.addWidget(self.list_widget)
        
        # self.widget.installEventFilter(self.main_layout)

        # Right click menu
        self.rename_action  = QAction('Rename', self.list_widget)
        self.context_menu = QMenu(self.list_widget)
        self.context_menu.addAction(self.rename_action)
        
        #self.context_menu.show()

        self.context_menu.popup(QtGui.QCursor.pos())
        self.texset_table.addAction(self.rename_action)

        #self.main_layout.addWidget(self.context_menu)

        
        # column_count=5
        # self.table_widget.columnCount()

         # Adds a button
        self.export_button = QPushButton("Export")
        self.export_button.setToolTip("This button will attempt to Export the validated textures. \nHotkey: Alt + E")
        self.export_button.setShortcut(QtCore.Qt.ALT + QtCore.Qt.Key_E)
        
        self.main_layout.addWidget(self.export_button)


        

        
        #if self.textset_uv_tiles is not None:

        if substance_painter.project.is_open():
            self.fill_texset_table()
            settings = QtCore.QSettings()
            settings.setValue("dialogue_window_checkbox_state", QtCore.Qt.Unchecked) 

    # def event_filter(self, source, event):
    #     if event.type() == QEvent.ContextMenu and source is self.widget:
    #         print(event)
    #         print(source)
    #         return True
        
    #     return super().event_filter(source, event)
    
    def contextMenuEvent(self, event):
        self.context_menu.exec_(QtGui.QCursor.pos())

    def on_open_help_document(self, event):
        help_doc_path = os.path.join(self.file_dir, "Custom_Exporter_Help/Custom_Exporter_Help.pdf")
        help_url = QtCore.QUrl.fromLocalFile(help_doc_path)
        QtGui.QDesktopServices.openUrl(help_url)
    
    def connect_widget_events(self):

        # Refresh Button Interaction
        self.refresh_button.clicked.connect(self.on_refresh_texset_table)


        # When CB state changed
        self.personal_export_cb.stateChanged.connect(self.on_refresh_texset_table)

        # When asset type changed..
        self.asset_type_cbbx.currentIndexChanged.connect(self.on_refresh_texset_table)

         # Interaction signal emitter for button
        self.export_button.clicked.connect(self.on_export_requested)

        # Help icon action trigger
        self.help_action.triggered.connect(self.on_open_help_document)

        # Right click menu Action triggger
        #self.rename_action.triggered.connect(self.rename_slot)

        # When dropdown item changed
        #self.asset_type_cbbx.currentIndexChanged.connect(self.on_dropdown_state_changed)

        
        # self.asset_type_cbbx.stateChanged.connect(self.grey_out_unchecked_row)

    def init_texset_table(self):
        # Attributes of the QtTableWidget()
        column_headers = ('Export', 'Texture Set Name', 'Shader Type', 'Resolution', 'Export Path', 'Validation')
        num_columns = len(column_headers)
        num_rows = 0
        
        self.texset_table.setRowCount(num_rows)
        self.texset_table.setColumnCount(num_columns)

        self.texset_table.setHorizontalHeaderLabels(column_headers)

        # Hiding the row header
        self.texset_table.verticalHeader().setVisible(False)

        self.texset_table.setColumnWidth(0, 40) # Export check box width
        self.texset_table.setColumnWidth(3, 85) # Texture Res width
        self.texset_table.setColumnWidth(4, 350) # Export path width
        self.texset_table.setColumnWidth(5, 65) # Validation Icon width

        self.texset_table.setContextMenuPolicy(Qt.CustomContextMenu)
        self.texset_table.customContextMenuRequested.connect(self.show_context_menu)

    # def contextMenuEvent(self, event):
    #     self.menu = QMenu(self)
    #     self.rename_action  = QAction('Rename', self)
    #     self.rename_action.triggered.connect(lambda: self.rename_slot(event))
    #     self.menu.addAction(self.rename_action)
    #     self.menu.popup(QtGui.QCursor.pos())
       
    def rename_slot(self, row, column):
        # print(f"Rename clicked on row:{row}, column: {column}")
        texset_rename_window = TexsetRenameWindow(self.textset_name)
        if texset_rename_window.exec_():
            print("Execute stuff for Popup Window")
            new_asset_type, new_asset_detail_01, new_asset_detail_02, new_asset_id  = texset_rename_window.getData()
            self.update_texture_set_name(row, new_asset_type,new_asset_detail_01, new_asset_detail_02, new_asset_id)
        
    
        #self.context_menu.popup(QtGui.QCursor.pos())

    def update_texture_set_name(self, row, asset_type, asset_detail_01, asset_detail_02, asset_id):
        texset_name = self.textset_name

        parts = texset_name.split('_')

        # Sets the texture table item correctly but not on sub painter side...
        self.texset_table.setItem(row,1, QTableWidgetItem(f"{asset_type}_{asset_detail_01}_{asset_detail_02}_{asset_id}"))
        print(texset_name)


    def fill_texset_table(self):
        # Note : here we are creating an attribute, NOT a local variable
        # The self infront of our variable name means we can access across the script
        self.all_texture_sets = substance_painter.textureset.all_texture_sets()
        self.texset_table.setRowCount(len(self.all_texture_sets))

        """
        Checking whether texture sets is using the UV_Tiles Workflow
        Plans: 
            Extend this to then check if it can then add an additional suffix to the naming convention,
              to specify which part of the UDIM tile this texture belongs to...
        Goals: 
            Understand difference between uv tiles and UDIMs
        """
        # if self.all_texture_sets[0].has_uv_tiles:
        #     print("Has UV Tiles")

    
        # self.has_uv_tiles =  substance_painter.textureset.TextureSet.has_uv_tiles(material_id)
        # print(self.has_uv_tiles)

        for i, texture_set in enumerate(self.all_texture_sets):
            # Use QCheckBox for the "Export" column    
            check_box = QCheckBox()
            check_box.setChecked(True)
            check_box.stateChanged.connect(self.grey_out_unchecked_row)
            self.texset_table.setCellWidget(i, 0, check_box)

            # Text set name column
            self.textset_name = texture_set.name()
            self.texset_widget_item = QTableWidgetItem(self.textset_name)
            self.texset_table.setItem(i, 1, self.texset_widget_item)

            # Use QComboBox for ShaderType column
            combo_box = QComboBox()
            combo_box.addItems(self.shader_types)
            combo_box.currentIndexChanged.connect(self.on_refresh_texset_table)

            combo_box.setToolTip("Specify the export preset that will be used during export")
            self.texset_table.setCellWidget(i, 2, combo_box)
            
            # Resolution Column using getresoltion()
            resolution = texture_set.get_resolution()
            width = resolution.width
            height = resolution.height

            resolution_text = QTableWidgetItem(f"{width} x {height}")

            self.texset_table.setItem(i, 3,resolution_text)


        self.on_refresh_texset_table()

    def show_context_menu(self, pos):
        # Get Item at clicked pos
        item = self.texset_table.itemAt(pos)

        if item:
            row = item.row()
            column = item.column()

            if column == 1:
                menu = QMenu(self.texset_table)

                # Actions
                rename_action = QAction('Rename', self.texset_table)

                # Connect Action to slots
                rename_action.triggered.connect(lambda: self.rename_slot(row, column))
                rename_action.triggered.connect(self.get_info_from_selection(column))

                # Add actions to menu
                menu.addAction(rename_action)

                # Show menu
                menu.exec_(self.texset_table.viewport().mapToGlobal(pos))

    def get_info_from_selection(self, column):
        self.all_texture_sets = substance_painter.textureset.all_texture_sets()
        # for i, texture_set_name in enumerate()


        pass

    def validate_texture_sets(self):
        self.texset_with_overbudget_res = [] 
        asset_type = self.asset_type_cbbx.currentText()

        # Check name of each texture set
        for i, texture_set in enumerate(self.all_texture_sets):

            # Intializing variables for readibility
            # texture_set_resolution = texture_set.get_resolution()
            # texture_set_name = texture_set.name()

            res_is_valid, res_validation_details = module_validation_resolution.validate_res(asset_type, texture_set.get_resolution())
            
            validation_item = QTableWidgetItem(QtCore.Qt.AlignRight)
            
            export_checkbox = self.texset_table.cellWidget(i, 0)

            if res_is_valid:
                # self.texset_with_overbudget_res.clear()

                name_is_valid, name_validation_details = module_validation_name.validate_name(asset_type, texture_set.name())
                
                if name_is_valid:
                    validation_item.setIcon(self.icon_validation_ok)
                    #validation_item.setTextAlignment(QtCore.Qt.AlignCenter)
                    validation_item.setToolTip(f"Texture Set validations are OK for texture set #{i + 1} \
                                            \n{texture_set.name()} \
                                            \nGood Job!")
                    export_checkbox.setToolTip(f"Specify if texture set #{i + 1}: {texture_set.name()} \
                                               should be exported or skipped.")
                else:
                    validation_item.setIcon(self.icon_validation_fail)
                    validation_item.setToolTip(f"Texture Set Name validation has FAILED for texture set #{i + 1} \
                                            \n{texture_set.name()} \
                                            \nReason: {name_validation_details}\
                                            \nExport of this texture set is forcibly disabled until validation is OK.")
                    export_checkbox.setToolTip(f"Texture Set name validation has FAILED for texture set #{i + 1} \
                                            \n{texture_set.name()} \
                                            \nReason: {name_validation_details}\
                                            \nExport of this texture set is forcibly disabled until validation is OK.")
            else:
                validation_item.setIcon(self.icon_validation_fail)
                validation_item.setToolTip(f"Texture Set Resolution validation has FAILED for texture set #{i + 1} \
                                        \n{texture_set.get_resolution()} \
                                        \nReason: {res_validation_details}\
                                        \nExport of this texture set is forcibly disabled until validation is OK.")
                export_checkbox.setToolTip(f"Texture Set Resolution validation has FAILED for texture set #{i + 1} \
                                        \n{texture_set.get_resolution()} \
                                        \nReason: {res_validation_details}\
                                        \nExport of this texture set is forcibly disabled until validation is OK.")
                # self.texset_with_overbudget_res.clear()
                
                self.texset_with_overbudget_res.append(texture_set)
                
            export_checkbox.setEnabled(res_is_valid and name_is_valid)
            export_checkbox.setChecked(res_is_valid and name_is_valid)
            self.texset_table.setItem(i, 5, validation_item)

        if len(self.texset_with_overbudget_res) > 0:
            self.open_dialogue_res_confirmation()

    def open_dialogue_res_confirmation(self):
        settings = QtCore.QSettings()
        if settings.value("dialogue_window_checkbox_state", QtCore.Qt.Unchecked) == QtCore.Qt.Unchecked:
            dialogue = DialogueWindow(self.icon_main_window)
            if dialogue.exec_() == QDialog.Accepted:
                self.apply_required_res()
                self.on_refresh_texset_table()
            else:
                substance_painter.logging.log(
                                                severity=substance_painter.logging.WARNING,
                                                channel="custom_exporter", 
                                                message="Please remember to fix resolution manually in the texture set settings. \
                                                \nOtherwise validation error would be present")
        else:
            substance_painter.logging.log(
                                                severity=substance_painter.logging.INFO,
                                                channel="custom_exporter", 
                                                message="Dialogue for Resolution validation was not triggered as per user settings")

    def apply_required_res(self):
        required_width, required_height = module_validation_resolution.get_required_res_from_asset_type(self.asset_type_cbbx.currentText())
        required_res = substance_painter.textureset.Resolution(required_width, required_height)
        for texture_set in self.texset_with_overbudget_res:
            # substance_painter.logging.log(severity=substance_painter.logging.WARNING,
            #                                 channel="custom_exporter",
            #                               message=f"List of overbudget: {texture_set}") 
            original_res = texture_set.get_resolution()
            texture_set.set_resolution(required_res) 
            substance_painter.logging.log(severity=substance_painter.logging.INFO,
                                          channel="custom_exporter",
                                          message=f"Applied minimum required resolution for: {texture_set.name()}\
                                                    \nWas: {original_res}. Now Set to: {required_res}")
            
    def grey_out_unchecked_row(self):
        for i in range(self.texset_table.rowCount()):
            check_box_item = self.texset_table.cellWidget(i, 0)
            if check_box_item.isChecked():
                for j in range(1, self.texset_table.columnCount() - 1):
                    # Each item
                    item = self.texset_table.item(i, j)
                    if item is not None:
                        item.setFlags(item.flags()| QtCore.Qt.ItemIsEnabled)
                    else:
                        cell_widget = self.texset_table.cellWidget(i, j)
                        if cell_widget is not None:
                            cell_widget.setEnabled(True)
            # if check_box not checked: 
            else:
                for j in range(1, self.texset_table.columnCount() - 1):
                    item = self.texset_table.item(i, j)
                    if item is not None:
                        item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEnabled)
                    else:
                        cell_widget = self.texset_table.cellWidget(i, j)
                        if cell_widget is not None:
                            cell_widget.setDisabled(True)

    def on_refresh_texset_table(self):
        if substance_painter.project.is_open():
            
            export_path_root = self.build_root_export_path()
            if self.all_texture_sets is not None:
                for i, texture_set in enumerate(self.all_texture_sets):
                    # Set Texture Set Name
                    self.texset_table.setItem(i, 1, QTableWidgetItem(texture_set.name()))

                    # Resolution Column using getresoltion()
                    resolution = texture_set.get_resolution()   
                    width = resolution.width
                    height = resolution.height
                    self.texset_table.setItem(i, 3, QTableWidgetItem(f"{width} x {height}"))
                    
                    # Export Path Column
                    self.texset_table.setItem(i, 4, QTableWidgetItem(f"{export_path_root}/{self.asset_type_cbbx.currentText()}/{texture_set.name()}_{self.texset_table.cellWidget(i, 2).currentText()}/"))
                
                self.validate_texture_sets()
                self.grey_out_unchecked_row()

                #self.set_column_read_only(1) # Texture Set name Column
                self.set_column_read_only(3) # Resolution name Column
                self.set_column_read_only(4) # Export Path Column
                self.set_column_read_only(5) # Validation Column


    def set_column_read_only(self, column_index):
        for row in range(self.texset_table.rowCount()):
            item = self.texset_table.item(row, column_index)
            if item is not None:
                item.setFlags(item.flags() & ~QtCore.Qt.ItemIsEditable)


    def build_root_export_path(self):
        if self.personal_export_cb.isChecked():
            root = f"/Users/aranazadahmed/Documents/SubstancePainter/{custom_exporter_obj_name}/Personal"
        else:
            root = f"/Users/aranazadahmed/Documents/SubstancePainter/{custom_exporter_obj_name}/Assets/Textures"
        return root

    def connect_painter_events(self):
    #   substance_painter.event.DISPATCHER.connect(event, callback=)
        # Dictionary to connect events with a value
        painter_connections = {
            substance_painter.event.ProjectOpened : self.on_project_opened,
            substance_painter.event.ProjectCreated : self.on_project_created,
            substance_painter.event.ProjectAboutToClose : self.on_project_about_to_close
            }

        for event, callback in painter_connections.items():
            substance_painter.event.DISPATCHER.connect(event, callback)

    

    def show_ui_widgets(self):
        plugin = substance_painter_plugins.plugins.get("custom_exporter", None)
        if plugin is not None:
            # Refresh of widget
            self.delete_widget()
            self.init_widget_window()


        substance_painter.ui.add_dock_widget(self.widget)
        self.widget.show()

    # Functions for signal emitters in UI
    def on_export_requested(self):
        if self.all_texture_sets != None:
            for i in range(len(self.all_texture_sets)):
                should_export = self.texset_table.cellWidget(i, 0).isChecked()
                
                if not should_export:
                    continue
                
                texset_name = self.texset_table.item(i, 1).text()
                shader_type = self.texset_table.cellWidget(i, 2).currentText()
                export_path = self.texset_table.item(i, 4).text()

                modules_export.export_textures(texset_name, shader_type, export_path)
      
    def on_dropdown_state_changed(self):
        self.label_01.setText(f"Asset Type: {self.asset_type_cbbx.currentText()}")


    # prevents multiple instances of widget
    def delete_widget(self):
        if self.widget is not None:
            substance_painter.ui.delete_ui_element(self.widget)

    def on_project_opened(self, e):
        substance_painter.logging.log(substance_painter.logging.INFO, "custom_exporter", f"Project {substance_painter.project.name()} openend")
        self.fill_texset_table()

    def on_project_created(self, e):
        substance_painter.logging.log(substance_painter.logging.INFO, "custom_exporter", f"Project {substance_painter.project.name()} created")    
        self.fill_texset_table()

    def on_project_about_to_close(self, e):
        substance_painter.logging.log(substance_painter.logging.INFO, "custom_exporter", f"Project {substance_painter.project.name()} about to close..")    
        self.init_texset_table()

class DialogueWindow(QDialog): # QDialog is inherited from QWidget so all functions are aviable from QWidget
    def __init__(self, icon):
        super().__init__()
        self.setWindowTitle("Texture Set Resolution is over budget") # inherits from QWidget
        self.setWindowIcon(icon)
        self.setFixedSize(800, 200)

        layout = QVBoxLayout(self)

        text_label = QLabel("There is a validation error in the Resolution check step.\
                            \nThis tool can automatically set the texture resolution to the minimum required resolution. \
                            \nDo you want to set the texture resolution to the minimum requirements?")
        
        layout.addWidget(text_label)

        buttons = QDialogButtonBox(QDialogButtonBox.Yes | QDialogButtonBox.No)
        buttons.ButtonLayout(buttons.MacLayout)
        buttons.accepted.connect(self.accept)
        buttons.rejected.connect(self.reject)
        buttons.button(QDialogButtonBox.Yes).setText("Yes, apply the minimum resolution requirements to my export for me")
        buttons.button(QDialogButtonBox.No).setText("No, I will manually adjust the resolution")
        layout.addWidget(buttons)

        checkbox = QCheckBox("Do not show this window again.")
        checkbox.setChecked(False)
        checkbox.stateChanged.connect(self.save_checkbox_state)
        layout.addWidget(checkbox)

    # Function for saving checkbox state settings using QtCore.QSettings()
    def save_checkbox_state(self, state):
        settings = QtCore.QSettings()
        # state referers to result of checkbox.isChecked(T or F)
        settings.setValue("dialogue_window_checkbox_state", state) 
        # settings.value("dialogue_window_checkbox_state", QtCore.Qt.Unchecked)


"""
Unfortunately I made this Class to try and have a Texture Set Name Editor within Sub Painter.
However the function to change the texture set names is not within the Substance Painter API.
I kept the code here just incase it might be useful for something else at some point.
"""
class TexsetRenameWindow(QDialog):
    def __init__(self, current_textset_name: str):
        super().__init__()

        self.current_textset_names=[] 
        self.current_textset_names = current_textset_name.split("_")


        self.setWindowTitle("Texture Set Renamer Window")
        self.setFixedSize(400, 350)

        layout = QVBoxLayout(self)

        text_label = QLabel("Here you can change the Texture Set Name \nto one that follows our validation rules:")

        horizontal_headers = ('Original Name', 'New Name') 
        vertical_headers = ('Asset Type', 'Asset Detail 1', 'Asset Detail 2', 'Asset ID') 

        asset_types = ()

        layout.addWidget(text_label)
        self.table = QTableWidget()
        layout.addWidget(self.table, alignment=Qt.AlignLeft)
        self.table.setRowCount(4)
        row_count = self.table.rowCount()
        self.table.setColumnCount(2)

        self.table.setHorizontalHeaderLabels(horizontal_headers)
        self.table.setVerticalHeaderLabels(vertical_headers)
        self.table.verticalHeader().setVisible(True)
        self.table.setFixedWidth(600)


        for i in range(row_count):
            self.table.setItem(i, 0, QTableWidgetItem(self.current_textset_names[i]))
            
            # # Set Asset type  = cbbx
            # combo_box = QTableWidgetItem()
            # table.setItem(i, 1, QTableWidgetItem("poo2"))

            if i == 0:
                self.combo_box = QComboBox()
                self.combo_box_asset_type = self.combo_box.addItems(asset_types_acronyms)
                self.combo_box.currentIndexChanged.connect(self.update_texset_name)
                self.combo_box.currentIndexChanged.connect(self.set_cbbx_data)
                self.combo_box.setToolTip("Specify the export preset that will be used during export")
                self.table.setCellWidget(i, 1, self.combo_box)

            if i == 1:
                self.combo_box_1 = QComboBox()

                self.combo_box_1.addItems(asset_detail_01_props)
                # if self.combo_box.currentText() == "PROP":
                # elif self.combo_box.currentText() == "WPN":
                #     self.combo_box_1.addItems(asset_detail_01_wpns)
                # elif self.combo_box.currentText() == "CHAR":
                #     self.combo_box_1.addItems(asset_detail_01_chars)

                self.combo_box_1.currentIndexChanged.connect(self.update_texset_name)


                self.combo_box_1.setToolTip("Specify the export preset that will be used during export")
                self.table.setCellWidget(i, 1, self.combo_box_1)

            if i == 2:
                self.combo_box_2 = QComboBox()
                
                self.combo_box_2.addItems(asset_detail_02_props)
                #combo_box.currentIndexChanged.connect(self.on_refresh_texset_table)
                self.combo_box_2.currentIndexChanged.connect(self.update_texset_name)


                self.combo_box_2.setToolTip("Specify the export preset that will be used during export")
                self.table.setCellWidget(i, 1, self.combo_box_2)

            if i == 3:
                self.combo_box_3 = QComboBox()
                self.combo_box_3.addItems([f"{i:02}" for i in range(100)])
                #combo_box.currentIndexChanged.connect(self.on_refresh_texset_table)
                self.combo_box_3.currentIndexChanged.connect(self.update_texset_name)


                self.combo_box_3.setToolTip("Specify the export preset that will be used during export")
                self.table.setCellWidget(i, 1, self.combo_box_3)

        self.descrip_label = QLabel("Copy and Paste the Following string to the desired texture set:")
        layout.addWidget(self.descrip_label, Qt.AlignCenter)

        self.data_str = (f"{self.combo_box.currentText()}_{self.combo_box_1.currentText()}_{self.combo_box_2.currentText()}_{self.combo_box_3.currentText()}")
        self.label = QLineEdit(self.data_str)
        self.label.setReadOnly(True)
        layout.addWidget(self.label)

        

        refresh_button = QPushButton("Copy To Clipboard")
        refresh_button.clicked.connect(self.copy_to_clipboard)
        refresh_button_layout = QHBoxLayout()
        refresh_button_layout.addWidget(refresh_button)

        # # Accept and Cancel buttons
        # accept_button = QPushButton("Accept")
        cancel_button = QPushButton("Close")
        # accept_button.clicked.connect(self.accept)
        cancel_button.clicked.connect(self.reject)

        button_layout = QHBoxLayout()
        # button_layout.addWidget(accept_button)
        button_layout.addWidget(cancel_button)

        layout.addLayout(refresh_button_layout)
        layout.addLayout(button_layout)
        self.setLayout(layout)

    def setData(self):
        self.combo_box.currentText()

    def copy_to_clipboard(self):
        # s_text = "Copy me to clipboard"
        qclip = QtGui.QGuiApplication.clipboard()
        qclip.clear()
        qclip.setText(self.label.text())


    def getData(self):
        return self.combo_box.currentText(),self.combo_box_1.currentText(),self.combo_box_2.currentText(), self.combo_box_3.currentText()  

    def update_texset_name(self):
        # self.combo_box.setCurrentText(self.combo_box.currentText())
        # self.current_textset_names[0] = input_text
        # print(f"Value : {input_text}")
        # self.data_str = (f"{self.combo_box.currentText()}_{self.combo_box_1.currentText()}_{self.combo_box_2.currentText()}_{self.combo_box_3.currentText()}")
        # self.table.setItem(0,0,QTableWidgetItem(self.combo_box.currentText()))
        # self.table.setItem(1,0,QTableWidgetItem(self.combo_box_1.currentText()))
        # self.table.setItem(3,0,QTableWidgetItem(self.combo_box_3.currentText()))
        # self.table.setItem(2,0,QTableWidgetItem(self.combo_box_2.currentText()))
        # self.current_textset_names[0] = input_text
        self.label.setText(f"{self.combo_box.currentText()}_{self.combo_box_1.currentText()}_{self.combo_box_2.currentText()}_{self.combo_box_3.currentText()}")

        
        
    def set_cbbx_data(self):
        self.combo_box_1.clear()
        self.combo_box_2.clear()
        if self.combo_box.currentText() == "PROP":
            #self.combo_box_1.clear()
            self.combo_box_1.addItems(asset_detail_01_props)
            #self.combo_box_2.clear()
            self.combo_box_2.addItems(asset_detail_02_props)

        elif self.combo_box.currentText() == "WPN":
            #self.combo_box_1.clear()
            self.combo_box_1.addItems(asset_detail_01_wpns)
            #self.combo_box_2.clear()
            self.combo_box_2.addItems(asset_detail_02_wpns)

        elif self.combo_box.currentText() == "CHAR":
            #self.combo_box_1.clear()
            self.combo_box_1.addItems(asset_detail_01_chars)
            #self.combo_box_2.clear()
            self.combo_box_2.addItems(asset_detail_02_chars)




def start_plugin():
    global custom_exporter
    custom_exporter = CustomExporter()


def close_plugin():
    global custom_exporter
    custom_exporter.delete_widget()

if __name__ == "__main__":
    start_plugin()


