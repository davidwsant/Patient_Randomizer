import pandas as pd
import copy
import random

class PatientRandomizer():
    def __init__(self, dataFrame, med1_title='Medication 1', med2_title='Medication 2', patient_title = 'patient id', number_samples=5, replacement=False):
        self.dataFrame = dataFrame
        self.med1_title = med1_title
        self.med2_title = med2_title
        self.patient_title = patient_title
        self.number_samples = number_samples
        self.replacement = replacement
        self.output_list = []
        self.med_combo_dictionary = {}
        med1_possibilities = list(self.dataFrame[self.med1_title].unique())
        med2_possibilities = list(self.dataFrame[self.med2_title].unique())
        for med1 in med1_possibilities:
            for med2 in med2_possibilities:
                if med1 == med2:
                    continue
                combined_name = med1+'_'+med2
                self.med_combo_dictionary[combined_name] = []
        for index, row in self.dataFrame.iterrows():
            med1 = row[self.med1_title]
            med2 = row[self.med2_title]
            patient_number = row[self.patient_title]
            combined_name = med1+'_'+med2
            self.med_combo_dictionary[combined_name].append(patient_number)
        
    def fit(self):
        self.selected_patients = []
        #self.combo_counts = {}
        self.med_combo_copy = copy.deepcopy(self.med_combo_dictionary)
        for combination in self.med_combo_copy:
            for i in range(self.number_samples):
                if len(self.med_combo_copy[combination]) > 0:
                    choice = random.choice(self.med_combo_copy[combination])
                    self.selected_patients.append(choice)
                    if not self.replacement:
                        self.med_combo_copy[combination].remove(choice) # remove sample from possibilities if no replacement
    def get_df(self):
        output_df = self.dataFrame[self.dataFrame[self.patient_title].isin(self.selected_patients)]
        return output_df
        