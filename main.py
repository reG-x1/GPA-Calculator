import os
import ast

grades_eq = {
    "A+" : 10, "A": 9, "B+" : 8, "B": 7, "C+": 6, "C": 5,"D": 4,
}

class semester:
    def __init__(self,name,n_courses):
        self.n_courses = n_courses
        self.name = name
        self.Courses = self.checking_data()        

    def __str__(self):
        pass      
    
    @staticmethod
    def targeted_file():
        script_directory = os.path.dirname(__file__)
        course_data = os.path.join(script_directory, "Course_data.txt")
        return course_data
    
    @staticmethod
    def Course_reset():
        course_data = semester.targeted_file()
        file = open(course_data, "w")
        file.close()
        print("File reset successfully!!")

    def checking_data(self):
        course_data = self.targeted_file()

        file = open(course_data, "r")
        data_fetched = file.read()

        if self.name in data_fetched:
            print(f"{self.name} courses already reistered!!")
            file.close()
        else: 
            self.ask_Course_Details()
    
    def ask_Course_Details(self):
                    
        print(f"\n-----------For {self.name}-----------")
        Courses = {}
        for i in range(1,self.n_courses+1):
                        
            X = input(f"Enter the {i}th Course name: ")
            Y = input("and its credit: ")
            elem = {X : Y}

            Courses.update(elem)
        
        course_data = self.targeted_file()
        file = open(course_data, "a")
        updating_in_file = file.write(f"{self.name} = "+str(Courses)+"\n")
        file.close()
        
        return Courses 
    
class Student_Record(semester):
    def __init__(self):
        self.subject_dict = self.retreiving_dict()      # Returns MASTER DICTIONARY {sem1:{CP:4, Comms:3}}
        self.grades = self.asking_grades()              # Returns all GRADES        {CP:'A+', Comms:'C'}
        
    def retreiving_dict(self):
        course_data = self.targeted_file()
        file = open(course_data, "r")
        line = file.readline()
        file.seek(0)

        Master_dict = {}
        
        for line in file: 
            if "=" in line:
                subjects_keypairs = line.split("=")

                subject_keys = subjects_keypairs[0].strip()
                subject_dict_str = subjects_keypairs[1].strip()
                    
                subject_dict_real = ast.literal_eval(subject_dict_str)
                cleaned_dict = {course: int(credit) for course, credit in subject_dict_real.items()}    
                Master_dict[subject_keys] = cleaned_dict

        file.close()
        return Master_dict
    
    def asking_grades(self):
        Master_dict = self.retreiving_dict()

        grades = {}
        for sem in Master_dict:
            x = Master_dict[sem]
            print(f"\nEnter your grades for {sem}: ")
            for course in x:
                
                grade = input(f"{course} :")
                grades[course] = grade.upper()

        return grades
    
    def SGPA_calculator(self):

        Master_dict = self.subject_dict
        grades = self.grades

        for sem in Master_dict:
            each_sem_data = Master_dict[sem]        #Eg: {'ADE': 4, 'EM2': 4, 'CS': 4, 'PSA': 4, 'PE': 4, 'RET': 4}
            sem_creds = sum(each_sem_data.values())
                
            sum_of_products = 0
            for sub in each_sem_data:
                sub_creds = int(each_sem_data[sub]) 
                sub_grade = grades[sub]
                eq_sub_grade = int(grades_eq[sub_grade])

                product = sub_creds*eq_sub_grade
                sum_of_products += product

            sgpa = (sum_of_products/sem_creds)
                        
            print(f"SGPA for {sem} = {sgpa:.2f}")

    def CGPA_calculator(self):
        Master_dict = self.subject_dict
        grades = self.grades
        
        grand_sum = 0
        total_creds = 0

        for sem in Master_dict:
            each_sem_data = Master_dict[sem]          
            sem_creds = sum(each_sem_data.values())
            total_creds += sem_creds
                
            
            for sub in each_sem_data:
                sub_creds = int(each_sem_data[sub]) 
                sub_grade = grades[sub]
                eq_sub_grade = int(grades_eq[sub_grade])

                product = sub_creds*eq_sub_grade
                
                grand_sum += product
        
        cgpa = (grand_sum/total_creds)
                        
        print(f"CGPA for curriculum is = {cgpa:.2f}")              