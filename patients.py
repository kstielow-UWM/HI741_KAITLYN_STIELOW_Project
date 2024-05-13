from datetime import datetime
from collections import defaultdict

class Patient:
    def __init__(self, patient_id, gender, race, age, ethnicity, insurance, zip_code):
        self.patient_id = patient_id
        self.gender = gender
        self.race = race
        self.age = age
        self.ethnicity = ethnicity
        self.insurance = insurance
        self.zip_code = zip_code
        self.visits = []

    def add_visit(self, visit):
        self.visits.append(visit)

    def remove_visit(self, visit_id):
        for visit in self.visits:
            if visit["Visit_ID"] == visit_id:
                self.visits.remove(visit)
                print(f"Visit ID '{visit_id}' removed for patient ID '{self.patient_id}'")
                return
        print(f"No visit found with ID '{visit_id}' for patient ID '{self.patient_id}'")

    def get_patient_info(self):
        return {
            "Patient_ID": self.patient_id,
            "Gender": self.gender,
            "Race": self.race,
            "Age": self.age,
            "Ethnicity": self.ethnicity,
            "Insurance": self.insurance,
            "Zip_code": self.zip_code,
            "Visits": self.visits
        }

class HospitalRecord:
    def __init__(self):
        self.patients = {}

    def add_patient_record(self, patient_data):
        patient_id = patient_data.pop("Patient_ID")
        if patient_id in self.patients:
            self.patients[patient_id].add_visit(patient_data)
        else:
            patient = Patient(patient_id, patient_data["Gender"], patient_data["Race"], patient_data["Age"], patient_data["Ethnicity"], patient_data["Insurance"], patient_data["Zip_code"])
            visit_data = {
                "Visit_time": patient_data["Visit_time"],
                "Visit_ID": patient_data.get("Visit_ID", self.generate_visit_id()),
                "Chief_complaint": patient_data["Chief_complaint"],
                "Note_ID": patient_data["Note_ID"],
                "Note_type": patient_data["Note_type"]
            }
            patient.add_visit(visit_data)
            self.patients[patient_id] = patient

    def generate_visit_id(self):
        pass

    def delete_patient_record(self, patient_id):
        if patient_id in self.patients:
            del self.patients[patient_id]
            print(f"Deleted patient record for Patient ID '{patient_id}'")
        else:
            print(f"Patient ID '{patient_id}' not found.")

    def retrieve_patient(self, patient_id):
        if patient_id in self.patients:
            return self.patients[patient_id].get_patient_info()
        else:
            print("Patient ID not found.")
            return None

    def count_visits(self, date):
        total_visits = 0
        for patient in self.patients.values():
            for visit in patient.visits:
                try:
                    visit_time = datetime.strptime(visit["Visit_time"], '%m/%d/%Y').strftime('%Y-%m-%d')
                except ValueError:
                    visit_time = datetime.strptime(visit["Visit_time"], '%Y-%m-%d').strftime('%Y-%m-%d')
                if visit_time == date:
                    total_visits += 1
        print(f"Total visits on {date}: {total_visits}")

    def generate_statistics(self):
        total_patients = len(self.patients)
        if total_patients == 0:
            return "No patients found."

        age_distribution = defaultdict(int)
        insurance_distribution = defaultdict(int)
        gender_distribution = defaultdict(int)
        race_distribution = defaultdict(int)
        total_age = 0
        oldest_patient = {"Age": 0}
        youngest_patient = {"Age": float('inf')}

        for patient in self.patients.values():
            age_distribution[patient.age] += 1
            insurance_distribution[patient.insurance] += 1
            gender_distribution[patient.gender] += 1
            race_distribution[patient.race] += 1
            total_age += patient.age
            if patient.age > oldest_patient["Age"]:
                oldest_patient = {"Patient_ID": patient.patient_id, "Age": patient.age}
            if patient.age < youngest_patient["Age"]:
                youngest_patient = {"Patient_ID": patient.patient_id, "Age": patient.age}

        statistics = ""
        statistics += "Age Distribution:\n"
        for age, count in age_distribution.items():
            percentage = (count / total_patients) * 100
            statistics += f"Age {age}: {count} ({percentage:.2f}%)\n"

        statistics += "\nInsurance Distribution:\n"
        for insurance, count in insurance_distribution.items():
            percentage = (count / total_patients) * 100
            statistics += f"{insurance}: {count} ({percentage:.2f}%)\n"

        statistics += "\nGender Distribution:\n"
        for gender, count in gender_distribution.items():
            statistics += f"{gender}: {count}\n"

        statistics += "\nRace Distribution:\n"
        for race, count in race_distribution.items():
            statistics += f"{race}: {count}\n"

        average_age = total_age / total_patients
        statistics += f"\nAverage Age: {average_age:.2f}\n"

        statistics += f"\nOldest Patient: Patient ID - {oldest_patient['Patient_ID']}, Age - {oldest_patient['Age']}\n"
        statistics += f"Youngest Patient: Patient ID - {youngest_patient['Patient_ID']}, Age - {youngest_patient['Age']}\n"

        return statistics
