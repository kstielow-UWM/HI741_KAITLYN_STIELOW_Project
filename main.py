import tkinter as tk
from tkinter import messagebox, simpledialog
import csv
from patients import HospitalRecord, Patient
from datetime import datetime

class App:
    def __init__(self, root):
        self.root = root
        self.root.title("Clinical Data Warehouse")
        
        self.login_frame = tk.Frame(self.root)
        self.login_frame.pack()

        self.username_label = tk.Label(self.login_frame, text="Username:")
        self.username_label.grid(row=0, column=0)
        self.username_entry = tk.Entry(self.login_frame)
        self.username_entry.grid(row=0, column=1)

        self.password_label = tk.Label(self.login_frame, text="Password:")
        self.password_label.grid(row=1, column=0)
        self.password_entry = tk.Entry(self.login_frame, show="*")
        self.password_entry.grid(row=1, column=1)

        self.login_button = tk.Button(self.login_frame, text="Login", command=self.login)
        self.login_button.grid(row=2, columnspan=2)

        self.patients_frame = tk.Frame(self.root)

    def login(self):
        username = self.username_entry.get()
        password = self.password_entry.get()

        if self.validate_credentials(username, password):
            self.login_frame.pack_forget()
            self.show_main_menu()
            
            user_role = self.get_user_role(username)  
            self.log_usage(username, user_role, "Login", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))  
        else:
            messagebox.showerror("Error", "Invalid username or password")
            
            self.log_usage(username, "", "Failed Login Attempt", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def validate_credentials(self, username, password):
        try:
            with open("Project_credentials.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username and row['password'] == password:
                        self.hospital = self.load_patients("Project_patient_information.csv")
                        return True
        except FileNotFoundError:
            messagebox.showerror("Error", "Credential file not found")
        return False

    def get_user_role(self, username):
        try:
            with open("Project_credentials.csv", "r") as file:
                reader = csv.DictReader(file)
                for row in reader:
                    if row['username'] == username:
                        return row['role']  
        except FileNotFoundError:
            pass  

        return ""  

    def show_main_menu(self):
        self.patients_frame.pack()

        retrieve_button = tk.Button(self.patients_frame, text="Retrieve Patient", command=self.retrieve_patient)
        retrieve_button.pack()

        add_button = tk.Button(self.patients_frame, text="Add Patient", command=self.add_patient)
        add_button.pack()

        remove_button = tk.Button(self.patients_frame, text="Remove Patient", command=self.remove_patient)
        remove_button.pack()

        count_button = tk.Button(self.patients_frame, text="Count Visits", command=self.count_visits)
        count_button.pack()

        stats_button = tk.Button(self.patients_frame, text="Generate Statistics", command=self.generate_statistics)
        stats_button.pack()

        exit_button = tk.Button(self.patients_frame, text="Exit", command=self.root.destroy)
        exit_button.pack()

    def retrieve_patient(self):
        patient_id = simpledialog.askstring("Retrieve Patient", "Enter Patient ID:")

        if patient_id:
            patient_info = self.hospital.retrieve_patient(patient_id)
            
            if patient_info:
                messagebox.showinfo("Patient Information", self.format_patient_info(patient_info))
                self.log_usage(self.username_entry.get(), "", "Retrieve Patient", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))
            else:
                messagebox.showerror("Error", "Patient ID not found")

    def format_patient_info(self, patient_info):
        info_str = f"Patient ID: {patient_info['Patient_ID']}\n"
        info_str += f"Gender: {patient_info['Gender']}\n"
        info_str += f"Race: {patient_info['Race']}\n"
        info_str += f"Age: {patient_info['Age']}\n"
        info_str += f"Ethnicity: {patient_info['Ethnicity']}\n"
        info_str += f"Insurance: {patient_info['Insurance']}\n"
        info_str += f"Zip code: {patient_info['Zip_code']}\n"
        info_str += "Visits:\n"
        for visit in patient_info['Visits']:
            info_str += f"  Visit ID: {visit['Visit_ID']}, Visit Time: {visit['Visit_time']}, Chief Complaint: {visit['Chief_complaint']}\n"
        return info_str

    def add_patient(self):
        patient_data = {}
        patient_data['Patient_ID'] = simpledialog.askstring("Add Patient", "Enter Patient ID:")
        if patient_data['Patient_ID']:
            patient_data['Gender'] = simpledialog.askstring("Add Patient", "Enter Gender:")
            patient_data['Race'] = simpledialog.askstring("Add Patient", "Enter Race:")
            patient_data['Age'] = simpledialog.askinteger("Add Patient", "Enter Age:")
            patient_data['Ethnicity'] = simpledialog.askstring("Add Patient", "Enter Ethnicity:")
            patient_data['Insurance'] = simpledialog.askstring("Add Patient", "Enter Insurance:")
            patient_data['Zip_code'] = simpledialog.askstring("Add Patient", "Enter Zip code:")
            patient_data['Visit_time'] = simpledialog.askstring("Add Patient", "Enter Visit time (yyyy-mm-dd):")
            patient_data['Chief_complaint'] = simpledialog.askstring("Add Patient", "Enter Chief Complaint:")
            patient_data['Note_ID'] = simpledialog.askstring("Add Patient", "Enter Note ID:")
            patient_data['Note_type'] = simpledialog.askstring("Add Patient", "Enter Note Type:")

            self.hospital.add_patient_record(patient_data)
            self.save_patient_info("Project_patient_information.csv")
            messagebox.showinfo("Success", "Patient added successfully")
            self.log_usage(self.username_entry.get(), "", "Add Patient", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def remove_patient(self):
        patient_id = simpledialog.askstring("Remove Patient", "Enter Patient ID to remove:")

        if patient_id:
            self.hospital.delete_patient_record(patient_id)
            self.save_patient_info("Project_patient_information.csv")
            messagebox.showinfo("Success", "Patient removed successfully")
            self.log_usage(self.username_entry.get(), "", "Remove Patient", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def count_visits(self):
        date = simpledialog.askstring("Count Visits", "Enter date to count visits (yyyy-mm-dd):")

        if date:
            total_visits = 0
            for patient in self.hospital.patients.values():
                for visit in patient.visits:
                    try:
                        visit_time = datetime.strptime(visit["Visit_time"], '%m/%d/%Y').strftime('%Y-%m-%d')
                    except ValueError:
                        visit_time = datetime.strptime(visit["Visit_time"], '%Y-%m-%d').strftime('%Y-%m-%d')
                    if visit_time == date:
                        total_visits += 1
            messagebox.showinfo("Total Visits", f"Total visits on {date}: {total_visits}")
            self.log_usage(self.username_entry.get(), "", "Count Visits", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def generate_statistics(self):
        statistics = self.hospital.generate_statistics()
        messagebox.showinfo("Statistics", statistics)
        self.log_usage(self.username_entry.get(), "", "Generate Statistics", datetime.now().strftime('%Y-%m-%d %H:%M:%S'))

    def log_usage(self, username, user_role, action, timestamp):
        with open("usage_statistics.csv", "a") as log_file:
            writer = csv.writer(log_file)
            writer.writerow([username, user_role, action, timestamp])

    def load_patients(self, filename):
        hospital = HospitalRecord()
        with open(filename, 'r') as file:
            reader = csv.DictReader(file)
            for row in reader:
                patient_data = {
                    "Patient_ID": row["Patient_ID"],
                    "Gender": row["Gender"],
                    "Race": row["Race"],
                    "Age": int(row["Age"]),
                    "Ethnicity": row["Ethnicity"],
                    "Insurance": row["Insurance"],
                    "Zip_code": row["Zip_code"],
                    "Visit_time": row["Visit_time"],
                    "Chief_complaint": row["Chief_complaint"],
                    "Note_ID": row["Note_ID"],
                    "Note_type": row["Note_type"]
                }
                hospital.add_patient_record(patient_data)
        return hospital

    def save_patient_info(self, filename):
        with open(filename, 'w', newline='') as file:
            writer = csv.writer(file)
            writer.writerow(["Patient_ID", "Gender", "Race", "Age", "Ethnicity", "Insurance", "Zip_code", "Visit_time", "Chief_complaint", "Note_ID", "Note_type"])
            for patient in self.hospital.patients.values():
                for visit in patient.visits:
                    writer.writerow([patient.patient_id, patient.gender, patient.race, patient.age, patient.ethnicity, patient.insurance, patient.zip_code, visit['Visit_time'], visit['Chief_complaint'], visit['Note_ID'], visit['Note_type']])

if __name__ == "__main__":
    root = tk.Tk()
    app = App(root)
    root.mainloop()