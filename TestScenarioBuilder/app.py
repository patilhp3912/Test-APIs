import sys
import json
import os

from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QTabWidget, 
    QTextEdit, QTableWidget, QTableWidgetItem, QHeaderView
)
from PyQt5.QtCore import Qt

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.settings = self.load_settings()
        self.setWindowTitle('Test Scenario Builder')
        self.setGeometry(100, 100, 800, 600)
        self.showMaximized()

        # Create tab widget
        tabs = QTabWidget(self)
        self.tab1 = QWidget()
        self.tab2 = QWidget()
        tabs.addTab(self.tab1, 'Collection')
        tabs.addTab(self.tab2, 'Environment')

        # Tab 1: Collection
        self.setup_collection_tab()
        
        # Tab 2: Environment
        self.setup_environment_tab()

        self.setCentralWidget(tabs)

        # Load initial files from settings
        self.load_initial_files()

    def load_settings(self):
        try:
            settings_path = os.path.join(os.path.dirname(__file__), 'appSettings.json')
            with open(settings_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            print(f"Error loading settings: {e}")
            return {
                "collectionFilePath": "",
                "environmentFilePath": "",
                "lastUsedPaths": {"collection": "", "environment": ""}
            }

    def setup_collection_tab(self):
        layout = QVBoxLayout(self.tab1)
        self.collection_text = QTextEdit(None)
        self.collection_text.setReadOnly(True)
        layout.addWidget(self.collection_text)
        self.tab1.setLayout(layout)

    def setup_environment_tab(self):
        # Set up layout with no margins for maximum space
        layout = QVBoxLayout(self.tab2)
        layout.setContentsMargins(0, 0, 0, 0)
        layout.setSpacing(0)
        
        self.env_table = QTableWidget()
        # Make table fill the available space
        #self.env_table.setSizeAdjustPolicy(QTableWidget.adjustToContents)
        
        # Set up columns
        self.env_table.setColumnCount(3)
        self.env_table.setHorizontalHeaderLabels(['Name', 'Value', 'Description'])
        
        # Set column widths to distribute available space
        total_width = self.tab2.width()
        self.env_table.setColumnWidth(0, int(total_width * 0.25))  # 25% for Name
        self.env_table.setColumnWidth(1, int(total_width * 0.35))  # 35% for Value
        self.env_table.setColumnWidth(2, int(total_width * 0.40))  # 40% for Description
        
        # Enable editing
        self.env_table.setEditTriggers(QTableWidget.DoubleClicked | QTableWidget.EditKeyPressed)
        
        # Connect cell change signal
        self.env_table.itemChanged.connect(self.on_env_table_changed)
        
        layout.addWidget(self.env_table)
        self.tab2.setLayout(layout)

    def on_env_table_changed(self, item):
        if not hasattr(self, 'is_loading') or not self.is_loading:
            row = item.row()
            if row == self.env_table.rowCount() - 1:  # If editing the last row
                # Add a new empty row
                self.env_table.setRowCount(self.env_table.rowCount() + 1)
            self.save_environment_changes()

    def save_environment_changes(self):
        try:
            # Get the environment file path
            env_path = self.settings["lastUsedPaths"]["environment"] or self.settings["environmentFilePath"]
            if not env_path:
                return

            # Collect all variables from the table
            variables = []
            for row in range(self.env_table.rowCount() - 1):  # Exclude the last empty row
                name = self.env_table.item(row, 0)
                value = self.env_table.item(row, 1)
                description = self.env_table.item(row, 2)
                
                # Only add if name is not empty
                if name and name.text().strip():
                    variables.append({
                        "name": name.text().strip(),
                        "value": value.text().strip() if value else "",
                        "description": description.text().strip() if description else ""
                    })

            # Save to file
            with open(env_path, 'r+') as f:
                data = json.load(f)
                data['variables'] = variables
                f.seek(0)
                json.dump(data, f, indent=4)
                f.truncate()

        except Exception as e:
            print(f"Error saving environment changes: {e}")

    def load_initial_files(self):
        collection_path = self.settings["lastUsedPaths"]["collection"] or self.settings["collectionFilePath"]
        environment_path = self.settings["lastUsedPaths"]["environment"] or self.settings["environmentFilePath"]
        
        if collection_path:
            self.load_collection_file(collection_path)
        if environment_path:
            self.load_environment_file(environment_path)

    def load_collection_file(self, file_path):
        try:
            with open(file_path, 'r') as f:
                data = json.load(f)
            self.collection_text.setText(json.dumps(data, indent=4))
        except Exception as e:
            self.collection_text.setText(f"Error loading file: {str(e)}")

    def load_environment_file(self, file_path):
        try:
            self.is_loading = True  # Prevent triggering save while loading
            with open(file_path, 'r') as f:
                data = json.load(f)
            
            variables = data.get('variables', [])
            # Set row count to variables length plus one for new row
            self.env_table.setRowCount(len(variables) + 1)
            self.env_table.setColumnCount(3)
            self.env_table.setHorizontalHeaderLabels(['Name', 'Value', 'Description'])
            
            # Set default column widths
            self.env_table.setColumnWidth(0, 200)  # Name column
            self.env_table.setColumnWidth(1, 300)  # Value column
            self.env_table.setColumnWidth(2, 300)  # Description column
            
            for i, var in enumerate(variables):
                self.env_table.setItem(i, 0, QTableWidgetItem(var.get('name', '')))
                self.env_table.setItem(i, 1, QTableWidgetItem(var.get('value', '')))
                self.env_table.setItem(i, 2, QTableWidgetItem(var.get('description', '')))
            
        except Exception as e:
            self.env_table.setRowCount(1)
            self.env_table.setColumnCount(1)
            self.env_table.setHorizontalHeaderLabels(['Error'])
            self.env_table.setItem(0, 0, QTableWidgetItem(f"Error loading file: {str(e)}"))
        finally:
            self.is_loading = False

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec_())
