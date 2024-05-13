# Clinical Data Warehouse ReadMe
## How to Run

To run the Clinical Data Warehouse program, you need to execute the Python script **`main.py`**. Ensure you have Python installed on your system. You can run the script using the following command:

**python main.py**

Make sure you have the necessary packages installed. The program relies on the following Python packages:
- `tkinter` for the GUI interface.
- `csv` for reading and writing CSV files.
- `patients` module for handling patient data.

## Description
The Clinical Data Warehouse is a Python application designed to manage patient information in a hospital setting. It provides functionalities such as retrieving patient information, adding new patients, removing patients, counting visits, and generating statistics based on the stored data.

## Features
- **Login System**: Users can log in using their credentials stored in a CSV file.
- **Main Menu**: After logging in, users are presented with a main menu to access various functionalities.
- **Patient Management**: Users can retrieve, add, and remove patient records.
- **Visit Counting**: Users can count the visits on a specific date.
- **Statistics Generation**: Users can generate statistics based on the stored patient data.
- **Logging Usage**: Usage statistics including user actions and timestamps are logged to a CSV file.

## Additional Information
- **Credentials File**: User credentials are stored in a CSV file named `Project_credentials.csv`.
- **Patient Information File**: Patient data is stored in a CSV file named `Project_patient_information.csv`.
- **Usage Statistics Logging**: User actions and timestamps are logged to a CSV file named `usage_statistics.csv`.
- **Module Dependencies**: The program depends on a `patients` module for handling patient data.
- **User Roles**: User roles (e.g., clinician, management, admin) are retrieved from the credentials file and logged during login for tracking usage statistics.
