import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
pd.set_option('display.max_columns', 8)

general = pd.read_csv('test/general.csv')
prenatal = pd.read_csv('test/prenatal.csv')
sports = pd.read_csv('test/sports.csv')

prenatal = prenatal.rename(columns={"HOSPITAL": "hospital", "Sex": "gender",
                                    })

sports = sports.rename(columns={"Hospital": "hospital", "Male/female": "gender",
                                    })
df_combined = pd.concat([general, prenatal, sports], ignore_index=True)
df_combined.drop(columns='Unnamed: 0', inplace=True)
df_combined.dropna(how='all', inplace=True)
df_combined['gender'] = df_combined['gender'].replace({
    'female': 'f', 'woman': 'f',
    'male': 'm', 'man': 'm'
})

df_combined.loc[(df_combined['hospital'] == 'prenatal') & (df_combined['gender'].isna()), 'gender'] = 'f'

columns_to_fill = ['bmi', 'diagnosis', 'blood_test', 'ecg', 'ultrasound', 'mri', 'xray', 'children', 'months']
df_combined[columns_to_fill] = df_combined[columns_to_fill].fillna(0)

# 1. Which hospital has the highest number of patients?
most_patients_hospital = df_combined['hospital'].value_counts().idxmax()

# 2. What share of the patients in the general hospital suffers from stomach-related issues?
general_stomach_issues = df_combined[(df_combined['hospital'] == 'general') & (df_combined['diagnosis'] == 'stomach')].shape[0]
general_total = df_combined[df_combined['hospital'] == 'general'].shape[0]
general_stomach_share = round(general_stomach_issues / general_total, 3)

# 3. What share of the patients in the sports hospital suffers from dislocation-related issues?
sports_dislocation_issues = df_combined[(df_combined['hospital'] == 'sports') & (df_combined['diagnosis'] == 'dislocation')].shape[0]
sports_total = df_combined[df_combined['hospital'] == 'sports'].shape[0]
sports_dislocation_share = round(sports_dislocation_issues / sports_total, 3)

# 4. What is the difference in the median ages of the patients in the general and sports hospitals?
general_median_age = df_combined[df_combined['hospital'] == 'general']['age'].median()
sports_median_age = df_combined[df_combined['hospital'] == 'sports']['age'].median()
age_difference = abs(general_median_age - sports_median_age)

# 5. In which hospital the blood test was taken the most often (biggest number of 't' in blood_test column)?
blood_test_counts = df_combined[df_combined['blood_test'] == 't'].groupby('hospital').size()
most_blood_tests_hospital = blood_test_counts.idxmax()
most_blood_tests_count = blood_test_counts.max()




# Determining the most common age range
plt.figure(figsize=(10, 6))
counts, bins, patches = plt.hist(df_combined['age'].dropna(), bins=[0, 15, 35, 55, 70, 80], edgecolor='black', alpha=0.7)
plt.title('Age Distribution Among Patients')
plt.xlabel('Age Ranges')
plt.ylabel('Number of Patients')
plt.xticks([7.5, 25, 45, 62.5, 75], ['0-15', '15-35', '35-55', '55-70', '70-80'])
plt.show()

# Determine the most common age range
age_range_labels = ['0-15', '15-35', '35-55', '55-70', '70-80']
most_common_age_range = age_range_labels[np.argmax(counts)]

# Print the most common age range
print(f"The answer to the 1st question: {most_common_age_range}")

# Plotting the pie chart for common diagnoses
plt.figure(figsize=(8, 8))
diagnosis_counts = df_combined['diagnosis'].value_counts()
plt.pie(diagnosis_counts, labels=diagnosis_counts.index, autopct='%1.1f%%', startangle=140)
plt.title('Common Diagnoses Among Patients')
plt.show()

# Most common diagnosis
most_common_diagnosis = diagnosis_counts.idxmax()

# Plotting the violin plot for height distribution by hospital
plt.figure(figsize=(10, 6))
sns.violinplot(x='hospital', y='height', data=df_combined)
plt.title('Height Distribution by Hospital')
plt.xlabel('Hospital')
plt.ylabel('Height (cm)')
plt.show()

# Print answers
print(f"The answer to the 2nd question: {most_common_diagnosis}")
print("The answer to the 3rd question: The observed differences in height distribution can be attributed to the different specializations of the hospitals. There may be two peaks because one group may represent pediatric or youth patients, and the other represents adult patients, reflecting distinct height ranges. Alternatively, the unit of measurement (cm vs inches) could cause apparent bimodality if not standardized.")