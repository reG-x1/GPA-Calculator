import json,os

class Record:
    Grade_eq = {"A+": 10, "A": 9, "B+": 8, "B": 7, "C+": 6, "C": 5, "D": 4 }
    branches_avail = ('CS','DS','Aero','ECE','VLSI','Ele','Mech','Civil','Prod','Meta')
    avail_sem = ["sem1","sem2","sem3","sem4","sem5","sem6","sem7","sem8"]

    def __init__(self,name,branch,batch):
        self.name = name
        self.branch = branch
        self.batch = str(batch)
        self.sem = self.deducing_sems()

    def add_course_data(self):
        branch = self.branch
        batch = str(self.batch)
        sem = int(self.sem)

        CourseDict = self._file_opening("CourseDict.json")                             # HELPER 1
        CourseDict = self._shell_creation(CourseDict,branch,batch)                     # HELPER 2
        rem_branch_data = self._finding_missing_sems(CourseDict,branch,batch,sem)      # HELPER 3
        
        if not rem_branch_data:
            print(f"All courses already registered for {branch} {batch}!")
            print("(switch to mode1 to view or mode5 to edit the Course details.)")
            return
        
        for missing_sem in rem_branch_data:
            i = 0
            course_list = []
            cred_list = []

            print(f"\nEntering {missing_sem.upper()} details:")
            while True:
                i +=1
                new_course = input(f"Course {i}: ")
                if new_course == '':
                    break
                course_credit = int(input("Credit: "))

                course_list.append(new_course)
                cred_list.append(course_credit)
            
            new_course_dict = dict(zip(course_list,cred_list))
            CourseDict[batch][branch][missing_sem] = new_course_dict

            self._file_writing(CourseDict,"CourseDict.json")

    def deducing_sems(self):
        grad_year = int(self.batch)                   # graduating year

        from datetime import datetime

        current_time = datetime.now()
        current_year = current_time.year
        current_month = current_time.month
        join_year = grad_year - 4

        if current_year > grad_year:
            return 8
        
        sems = 0
        for year in range(join_year,current_year+1):
                
            if year < current_year:
                if year == join_year:
                    sems +=1
                else:
                    sems +=2
            
            elif year == current_year:
                if current_year == join_year and current_month <8:
                    pass

                elif current_month <8:
                    sems +=1
                else:
                    sems +=2
        return sems   

    def _file_opening(self,file_name:str):
        with open(file_name,'r') as f:
            fileDict = json.load(f)
        return fileDict
    
    def _file_writing(self,data_to_write,file_name:str):
        try:  
            with open("file_exchange.tmp",'w') as f:
                json.dump(data_to_write,f,indent=4)
            os.replace("file_exchange.tmp",file_name)
        except Exception as e:
            print(f"Critical ERROR!! Could not save {file_name}.")
            print(f"Reason: {e}")

    def _shell_creation(self,CourseDict,branch,batch):

        if batch not in CourseDict:
            CourseDict[batch] = {}

        if branch not in CourseDict[batch]:
            CourseDict[batch][branch] = {}

        return CourseDict 

    def _finding_missing_sems(self,CourseDict,branch,batch,sem):
        batch_data = CourseDict[batch]
        branch_data = batch_data[branch]

        expected_sems = Record.avail_sem[:sem]
        missing_sems = []
        for curr_sem in expected_sems:
            if curr_sem not in branch_data.keys() or not branch_data[curr_sem]:
                missing_sems.append(curr_sem)
        rem_branch_data = {key:dict() for key in missing_sems}
        
        return rem_branch_data     


class Student(Record):
    def __init__(self,name,sid:int,branch,batch):
        super().__init__(name,branch,batch)
        self.sid = str(sid)

    def __str__(self):
        self.StudentInfo()
 
    def menu(self):
        print(f"========================= HOME =========================")
        print(f"Select from the following modes: ")
        print("1. View Course Info\n2. Add Course Info\n3. View Student Profile")
        print("4. Add student grades\n5. Edit grades\n6. View Rankings")
        print("7. not decied yet>>>>>\n8. Exit")
        
        try:
            mode = int(input("\nEnter the mode: "))

            if mode == 1:
                self.CourseInfo()

            elif mode == 2:
                print("-"*40)
                print(f"\nAdding Course details for {self.branch} {self.batch}:\n")
                print("(press ENTER on a blank course to save and jump to next.)")

                self.add_course_data()

            elif mode == 3:
                self.gpa_calculate()
                self.StudentInfo()
                
            elif mode == 4:
                self.add_grades()
                self.gpa_calculate()

            elif mode == 5:
                self.edit_grades()
                self.gpa_calculate()

            elif mode == 6:
                self.Rankings()

            elif mode == 7:
                pass

            elif mode == 8:
                print("\nThanks for visiting!")
                print("_"*40)
            
            else:
                print("MODE NOT FOUND!!!")
                print("No such modes available, please select from the availabe modes.\n")
                self.menu()
        except ValueError:
            print("INVALID INPUT!!!Please enter a number to choose from the available modes.\n")
            self.menu()
            
    def CourseInfo(self):
        try:
            CourseDict = self._file_opening()

            req_data = CourseDict[str(self.batch)][self.branch]

            print("-"*40)
            print(f"Viewing Course details for {self.branch} {self.batch}:\n")
            for sem_name, courses in req_data.items():
                print(f"======== {sem_name.upper()} ========")
                for course_name,credits in courses.items():
                    print(f"  {course_name:<16} | {credits}")
                print()
            print("-"*40)
        except KeyError:
            print(f"No Data Availabe.\n(Switch to Mode 2 to add course details.)")

    def StudentInfo(self):
        sid = str(self.sid)
        name = self.name
        branch = self.branch
        batch = self.batch

        StudentRecord = self._Student_shell()                   # HELPER

    def _Student_shell(self):
        StudentRecord = self._file_opening("StudentRecord.json")
        if self.sid not in StudentRecord:
            StudentRecord[self.sid] = {
                "Name":self.name,
                "Branch":self.branch,
                "Batch":self.batch,
                "Grades":{},
                "SGPA":{},
                "CGPA":None
                }
        try:  
            with open("StudentRecord.tmp",'w') as f:
                json.dump(StudentRecord,f,indent=4)
            os.replace("StudentRecord.tmp","StudentRecord.json")
        except Exception as e:
            print(f"Critical ERROR!! Could not save Student record.")
            print(f"Reason: {e}")

        return StudentRecord

    def add_grades(self):
        batch = self.batch
        branch = self.branch
        StudentRecord = self._Student_shell()                   # HELPER

        CourseDict = self._file_opening("CourseDict.json")
        all_sem_data = CourseDict[batch][branch]
        new_grades_added = False

        for sem in all_sem_data:
            if sem not in StudentRecord[self.sid]["Grades"]:
                StudentRecord[self.sid]["Grades"][sem] = {}

            if StudentRecord[self.sid]["Grades"][sem] == {}:
                print(f"\n===== {sem.upper()} GRADES =====")
                choice = input(f"Enter grades for {sem} now? (Y/N): ").strip().upper()

                if choice != "Y":
                    print(f"Skipping {sem}......")
                    continue

                each_sem_data = all_sem_data[sem]
                for subject in each_sem_data:
                    sub_grade = (input(f"{subject}: ")).upper()
                    StudentRecord[self.sid]["Grades"][sem][subject] = sub_grade
                new_grades_added = True
            
            else:
                print(f"Grades already saved for {sem}.")
        if new_grades_added:
            self._file_writing(StudentRecord,"StudentRecord.json")
            print("\nGrades saved successfully.")

        else:
            print("\nAll sem grades are already saved.")
            print("(switch to mode 5 to edit existing grades)")

    def edit_grades(self):
        pass

    def Rankings(self):
        pass
    
    def gpa_calculate(self):
        StudentRecord = self._file_opening("StudentRecord.json")
        CourseDict = self._file_opening("CourseDict.json")
        all_sem_grades = StudentRecord[self.sid]["Grades"]
        all_sem_creds = CourseDict[self.batch][self.branch]

        grand_creds = 0
        grand_sum_of_product = 0

        for sem in all_sem_grades.keys():
            sub_grade_pairs = all_sem_grades[sem]
            sub_cred_pairs = all_sem_creds[sem]

            sem_creds = 0
            sum_of_prod = 0

            for sub in sub_grade_pairs:

                grade = sub_grade_pairs[sub]
                eq_grad = Record.Grade_eq[grade] 
                creds = sub_cred_pairs[sub]
                
                product = creds*eq_grad
                
                sem_creds += creds
                sum_of_prod += product

            sgpa = sum_of_prod/sem_creds
            StudentRecord[self.sid]["SGPA"][sem] = round(sgpa,2)

            grand_creds += sem_creds
            grand_sum_of_product += sem_creds*sgpa
        
        cgpa = grand_sum_of_product/grand_creds
        StudentRecord[self.sid]["CGPA"] = round(cgpa,2)
        self._file_writing(StudentRecord,"StudentRecord.json")

s1 = Student("Naveen Kumar",24104101,"Ele",2028)
s1.menu()