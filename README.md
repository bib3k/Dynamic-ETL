# Data Mapping ETL Tool

This Python based project implements a Data Mapping ETL (Extract, Transform, Load) tool using PyQt5 and pandas. The tool provides a graphical user interface for importing, transforming, and exporting data.
## Abstract:

The Data Mapping ETL Tool is designed to assist companies in exporting required data by selecting necessary columns from an Excel sheet (CSV or Workbook) to the company's database. It serves as a proof of concept using dummy datasets and was developed during an internship at ING Bank in Australia.
Components:
 - 'IngWindow Class':
        This class represents the main window of the application.
        It initializes the UI elements and connects them to the corresponding functions.
        Provides functions for navigating between different screens and handling user inputs.

 -  'DfModel Class':
        This class defines a custom model for displaying DataFrame objects in PyQt5 QTableView widgets.
        It extends the QAbstractTableModel class and implements methods for interacting with DataFrame data.

 - 'helpers.py':
        Contains utility functions used in the main script.
        Functions include database connection, fetching column names, and data transformation.

 -   'DataFrame.py':
        Defines a custom model for displaying DataFrame objects in PyQt5 QTableView widgets.
        This class is implemented in the provided code snippet and extends QAbstractTableModel.

 -  'DynamiCombo.py':
        Implements a dynamic combo box for selecting unknown container types.

## Functionality:

  Importing Data: Users can import data from CSV or Excel files using the "Import" button.
  Data Transformation: After importing, users can map unknown container types to standard ones and modify the dataset accordingly.
  Data Analysis: The tool provides functionalities for analyzing and summarizing the data, such as calculating counts and sums of container types based on the year of                  manufacture.
  Exporting Data: Once the data is transformed, users can export it to a MySQL database table.

## Dependencies:

  - Python 3.x
  - PyQt5
  - pandas
  - SQLAlchemy

## Additional Description:

The DfModel class provides a crucial component for displaying DataFrame data in PyQt5 QTableView widgets. It extends the QAbstractTableModel class and implements various methods for interacting with DataFrame objects. This custom model allows for seamless integration of DataFrame data into the graphical user interface, providing users with a clear and organized view of the imported datasets.

## Code Summary: 
   - Importing Necessary Libraries: The script starts by importing required libraries like sys, pandas, create_engine from SQLAlchemy, and various modules from PyQt5. Additionally, it imports custom classes Ing, DfModel, and DynamiCombo.

   - Class Definition - IngWindow: This class represents the main window of the application. It initializes the UI elements, connects buttons to their respective functions, and manages the flow between different screens of the application.

   - Initialization: Within the __init__ method of IngWindow, the main window (main_page) is created, and the UI elements are set up using the Ui_MainWindow class. Additionally, global variables like df (for storing DataFrame) and conn (for database connection) are initialized.

   - Connecting Functions: The connecting_func method is responsible for connecting the buttons on the home page to their corresponding functions based on the button clicked.

   - Functionality:
       - 'firstScreen': Displays the first page of the application, allows importing files, and navigates to the next screen.
       - 'importfile': Handles file import functionality, detects file type (CSV or Excel), reads the file using pandas, and displays it in a QTableView widget.
       - 'db_connection': Establishes a connection with the MySQL database using SQLAlchemy.
       - 'fetchColumnName': Retrieves column names from the database table.
       - 'secondScreen': Displays the second page, shows imported data, and allows selecting columns for transformation.
       - 'fetch_unknown_container': Fetches unknown container types from the selected DataFrame and counts their occurrences.
       - 'unknownContainerScreen': Displays the third page, allowing users to map unknown containers to standard ones.
       - 'export_df': Exports the modified DataFrame to the MySQL database.
       - 'selectedStandardContainers': Changes unknown container types to standard ones selected by the user.
       - 'finalTableView': Displays the final screen with summary tables and options to export or cancel.

   - Main Execution: The script creates an instance of IngWindow, shows the main page, and starts the Qt event loop.
