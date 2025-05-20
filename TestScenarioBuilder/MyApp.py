from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QFileDialog, QSplitter, QTreeWidget, QTreeWidgetItem, QLabel, QLineEdit, QFormLayout
)
import sys
import json
from collection import Collection, TestGroup, TestScenario

def main():
    app = QApplication(sys.argv)
    window = QMainWindow()
    window.setWindowTitle("APITestBuilder")
    window.setGeometry(100, 100, 800, 600)

    # Central widget and main layout
    central_widget = QWidget(window)
    main_layout = QVBoxLayout(central_widget)

    # Top section: Buttons
    top_widget = QWidget()
    top_layout = QHBoxLayout(top_widget)

    create_collection_button = QPushButton("Create Test Collection")
    create_collection_button.clicked.connect(lambda: print("Create Test Collection clicked"))
    top_layout.addWidget(create_collection_button)

    import_collection_button = QPushButton("Import Test Collection (JSON)")
    top_layout.addWidget(import_collection_button)

    create_environment_button = QPushButton("Create Environment File")
    create_environment_button.clicked.connect(lambda: print("Create Environment File clicked"))
    top_layout.addWidget(create_environment_button)

    import_environment_button = QPushButton("Import Environment File (JSON)")
    import_environment_button.clicked.connect(lambda: QFileDialog.getOpenFileName(window, "Import Environment File", "", "JSON Files (*.json)"))
    top_layout.addWidget(import_environment_button)

    main_layout.addWidget(top_widget)

    # Splitter for left and right sections
    splitter = QSplitter()

    # Left section: Collection tree
    left_widget = QWidget()
    left_layout = QVBoxLayout(left_widget)

    collection_tree = QTreeWidget()
    collection_tree.setHeaderLabel("Collections")
    left_layout.addWidget(collection_tree)

    splitter.addWidget(left_widget)

    # Right section: Collection properties editor
    right_widget = QWidget()
    right_layout = QVBoxLayout(right_widget)

    # Form for editing collection properties
    form_widget = QWidget()
    form_layout = QFormLayout(form_widget)
    collection_name_edit = QLineEdit()
    collection_description_edit = QLineEdit()
    form_layout.addRow(QLabel("Collection Name:"), collection_name_edit)
    form_layout.addRow(QLabel("Collection Description:"), collection_description_edit)
    right_layout.addWidget(form_widget)

    # Save button
    save_button = QPushButton("Save")
    right_layout.addWidget(save_button)

    splitter.addWidget(right_widget)

    main_layout.addWidget(splitter)
    window.setCentralWidget(central_widget)

    # Function to load collection file
    def load_collection():
        file_path, _ = QFileDialog.getOpenFileName(window, "Import Test Collection", "", "JSON Files (*.json)")
        if file_path:
            with open(file_path, 'r') as file:
                data = json.load(file)
                collection_data = data.get("Collection", {})
                collection = Collection(collection_data.get("name", ""), collection_data.get("description", ""))
                
                for group_data in collection_data.get("TestGroup", []):
                    test_group = TestGroup(group_data.get("name", ""), group_data.get("description", ""))
                    
                    for scenario_data in group_data.get("TestScenario", []):
                        test_scenario = TestScenario(
                            scenario_data.get("name", ""),
                            scenario_data.get("tag", ""),
                            scenario_data.get("DataGenerationSteps", []),
                            scenario_data.get("Execution", {}),
                            scenario_data.get("Assertions", [])
                        )
                        test_group.add_test_scenario(test_scenario)
                    
                    collection.add_test_group(test_group)
                
                # Populate the collection tree
                collection_tree.clear()
                root = QTreeWidgetItem(collection_tree, [collection.name])
                root.setData(0, 1, collection.description)  # Save description as custom data
                for group in collection.test_groups:
                    group_item = QTreeWidgetItem(root, [group.name])
                    for scenario in group.test_scenarios:
                        QTreeWidgetItem(group_item, [scenario.name])

    # Function to handle collection item click
    def on_collection_item_clicked(item):
        if item.parent() is None:  # Only handle root items (collections)
            collection_name_edit.setText(item.text(0))
            collection_description_edit.setText(item.data(0, 1) or "")  # Use custom data for description

    # Function to save updated collection properties
    def save_collection_properties():
        selected_item = collection_tree.currentItem()
        if selected_item and selected_item.parent() is None:  # Only update root items (collections)
            selected_item.setText(0, collection_name_edit.text())
            selected_item.setData(0, 1, collection_description_edit.text())  # Save description as custom data

    # Connect signals
    collection_tree.itemClicked.connect(on_collection_item_clicked)
    save_button.clicked.connect(save_collection_properties)

    # Update import collection button to load and display the collection
    import_collection_button.clicked.connect(load_collection)

    window.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()