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
            self._box_header("ADD COURSE DATA")
            print(f"\nAll courses already registered for {branch} {batch}!")
            print("(switch to mode1 to view or mode3 to edit the Course details.)")
            print("-"*40)
            return
        
        self._box_header("ADD COURSE DATA")
        print(f"Adding Course details for {self.branch} {self.batch}:\n")
        print("(press ENTER on a blank course to save and jump to next.)")    

        for missing_sem in rem_branch_data:
            i = 0
            course_list = []
            cred_list = []

            self._section(f"Entering {missing_sem.upper()} details:")
            while True:
                i +=1
                new_course = input(f"Course {i}: ")
                if new_course == '':
                    break
                while True:
                    try:
                        course_credit = int(input("Credit: "))
                        break
                    except ValueError:
                        print("Invalid Credit! Please Enter a whole number (eg. 1,2,3,4...)")
                course_list.append(new_course)
                cred_list.append(course_credit)
            
            new_course_dict = dict(zip(course_list,cred_list))
            CourseDict[batch][branch][missing_sem] = new_course_dict

            self._file_writing(CourseDict,"CourseDict.json")
        self._box_footer()

    def edit_course_data(self,target_sem = None):

        CourseDict = self._file_opening("CourseDict.json")              
        if target_sem == None:
            target_sem = input("Which sem data you want to make changes in?: ")
        if target_sem not in CourseDict[self.batch][self.branch]:
            print(f"Error: {target_sem} does not exist.")
            return
        sem_to_edit = CourseDict[self.batch][self.branch][target_sem]

        i = 0
        self._box_header(f"ECIT {target_sem.upper()}")
        print("(Press ENTER to skip or anything else to edit the current)")
        for (sub,cred) in list(sem_to_edit.items()):
            i+=1
            change = False

            print(f"{i}. {sub}: {cred}")
            intent = input(f"edit? ")
            if intent == "":
                continue
            else:
                new_key = input(f"Enter updated subject  | (prev - {sub})  |: ")
                new_value = (input(f"Enter updated credit   | (prev - {cred}) |: "))

                if new_key != "":
                    change = True

                    old_cred = sem_to_edit.pop(sub)
                else:
                    new_key = sub
                    old_cred = cred

                if new_value != "":
                    new_value = int(new_value)
                    change = True
                else:
                    new_value = old_cred

            if change == True:
                sem_to_edit[new_key] = new_value
                print("-"*35)
                print(f"{sub}:{cred} --> {new_key}:{new_value}")
                print(f"Course Data updated successfully!!\n")
            else:
                continue

        self._file_writing(CourseDict,"CourseDict.json")
        self._box_footer()
        
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

    def _box_header(self,title):
        print("\n" + "="*45)
        print(title.center(45))
        print("="*45)
    
    def _box_footer(self):
        print("="*45)

    def _section(self,title):
        print(f"\n{title}")
        print("-"*45)

class Student(Record):
    def __init__(self,name,sid:int,branch,batch):
        super().__init__(name,branch,batch)
        self.sid = str(sid)

    def __str__(self):
        return f"{self.name} ({self.sid}) - {self.branch} {self.batch}"
 
    def menu(self):
        while True:
            self._box_header("HOME")
            print(f"Select from the following modes:")

            print("\n[ COURSE MANAGEMENT ]")
            print("1. View Course Info")
            print("2. Add Course Info")
            print("3. Edit Course Info")

            print("\n[ Student & Grades ]")
            print("4. View Student Profile")
            print("5. Add Grades")
            print("6. Edit Grades")

            print("\n[ Analytics & Progress ]")
            print("7. View Rankings")
            print("8. Future GPA Chart (coming soon)")
            
            print("\n9. Exit")
            self._box_footer()
            
            try:
                mode = int(input("Enter the mode: "))

                if mode == 1:
                    print("="*45)
                    print(" "*12 +"COURSE DETAILS")
                    print("="*45)
                    self.CourseInfo()
                    print("="*45)

                elif mode == 2:
                    print("-"*40)
                    self.add_course_data()

                elif mode == 3:
                    self.edit_course_data()
                    
                elif mode == 4:
                    self.StudentInfo()
                    self.gpa_calculate()

                elif mode == 5:
                    self.add_grades()
                    self.gpa_calculate()

                elif mode == 6:
                    self.edit_grades()

                elif mode == 7:
                    self.Rankings()

                elif mode == 8:
                    self.gpa_prediction()

                elif mode == 9:
                    print("\nThanks for visiting!")
                
                else:
                    print("MODE NOT FOUND!!!")
                    print("No such modes available, please select from the availabe modes.\n")
                    self.menu()
            except ValueError:
                print("INVALID INPUT!!!Please enter a number to choose from the available modes.\n")
            self.menu()
            
    def CourseInfo(self):
        self._box_header("COURSE DETAILS")
        try:
            CourseDict = self._file_opening("CourseDict.json")

            req_data = CourseDict[str(self.batch)][self.branch]

            print(f"Branch: {self.branch} {self.batch}:\n")
            for sem_name, courses in req_data.items():
                self._section(sem_name.upper())
                for course_name,credits in courses.items():
                    print(f"  {course_name:<20}{credits:>5}")
                print()
            print("-"*40)
        except KeyError:
            print(f"No Data Availabe.\n(Switch to Mode 2 to add course details.)")
        self._box_footer()

    def StudentInfo(self):
        sid = self.sid
        StudentRecord = self._Student_shell()                   # HELPER
        user = StudentRecord[sid]

        while True:
            self._box_header("STUDENT DASHBOARD")

            print(f"Name          : {user["Name"]}")
            print(f"SID           : {self.sid}")
            print(f"Program       : {user["Branch"]} {user["Batch"]}")
            print(f"Current sem   : {self.sem}")
            print("-"*45)

            print(f"Current CGPA: {user["CGPA"]}" + " "*9 + f"Target CGPA : {user["Target CGPA"]}")
            print("-"*45)
            print(f"Semwise SGPA: ")

            if not user["SGPA"]:
                print(" "*13 + "Nothing to show yet")
            else:
                for sem,sg in user["SGPA"].items():                
                    print(f"{sem.upper()}: {sg}")
            self._box_footer()

            self._section("MINI MENU")
            print(f"[1] View Detailed Semester Grades")
            print(f"[2] Set 'Target CGPA'")
            print(f"[3] Return Main Menu")
            print(f"[4] Exit app")
            choice = (input("Select an option: "))
            print()

            if choice == "1":
                self.view_grades()
            elif choice == "2":
                try:
                    target_cg = float(input("Enter your target CGPA: "))
                    user["Target CGPA"] = round(target_cg,2)
                    self._file_writing(StudentRecord,"StudentRecord.json")
                    print("Target CGPA saved successfully.")
                except ValueError:
                    print("Invalid input! Please enter a numeric decimal value.")
            elif choice == "3":
                self.menu()
            elif choice == "4":
                exit()
            else:
                print("Invalid Option! Choose a number from 1 to 4")
            print("="*45)

    def _Student_shell(self):
        StudentRecord = self._file_opening("StudentRecord.json")
        if self.sid not in StudentRecord:
            StudentRecord[self.sid] = {
                "Name":self.name,
                "Branch":self.branch,
                "Batch":self.batch,
                "Grades":{},
                "SGPA":{},
                "CGPA":None,
                "Target CGPA":None
                }
        self._file_writing(StudentRecord,"StudentRecord.json")

        return StudentRecord

    def add_grades(self):
        batch = self.batch
        branch = self.branch
        StudentRecord = self._Student_shell()                   # HELPER

        CourseDict = self._file_opening("CourseDict.json")
        all_sem_data = CourseDict[batch][branch]
        new_grades_added = False

        self._box_header("ADD GRADES")
        for sem in all_sem_data:
            if sem not in StudentRecord[self.sid]["Grades"]:
                StudentRecord[self.sid]["Grades"][sem] = {}

            if StudentRecord[self.sid]["Grades"][sem] == {}:
                self._section(f"{sem.upper()} GRADES")
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
            print("(switch to mode 6 to edit existing grades)")
        self._box_footer()

    def edit_grades(self):
        StudentRecord = self._file_opening("StudentRecord.json")
        grades = StudentRecord[self.sid]["Grades"]

        target_sem = input("Which sem grades do you want to update?: ")
        if target_sem not in grades:
            print(f"ERROR! No grades found for {target_sem}.")
            return

        self._box_header(f"UPDATE GRADES - {target_sem.upper()}")
        print("\n"+"="*20 + f" UPDATING GRADES for {target_sem.upper()} "+"="*20)
        print("(press ENTER to skip and anything else to edit the current)\n")
        i =0
        change = False
        for sub,grade in grades[target_sem].items():
            i+=1
            
            print(f"{i}. {sub}: {grade}")
            intent = input("skip? ")
            if intent == "":
                continue

            while True:
                updated_grade = input(f"\nEnter updated grade for {sub}: ").upper()
                if updated_grade in Record.Grade_eq:
                    grades[target_sem][sub] = updated_grade
                    print(f"Grade for {sub} updated successfully.")
                    print(f"{sub}: '{grade}' --> '{updated_grade}'\n")
                    change = True
                    break
                else:
                    print(f"Invalid Grade! Please enter valid grade (eg. A+, A, B+.....)")

        self._file_writing(StudentRecord,"StudentRecord.json")
        if change:
            print(f"Grades updated for {target_sem}...")
        else:
            print("No updates were made.")
        self._box_footer()

    def view_grades(self):
        StudentRecord = self._file_opening("StudentRecord.json")
        CourseDict = self._file_opening("CourseDict.json")
        creds = CourseDict[self.batch][self.branch]
        grades = StudentRecord[self.sid]["Grades"]

        self._box_header("GRADE REPORT")
        
        for sem in grades:
            print(f"{sem.upper()}"+" "*31 +f"SGPA: {StudentRecord[self.sid]["SGPA"][sem]}")
            i=0
            for sub,grade in grades[sem].items():
                i+=1
                print(f"{i}. {sub:<15}:{grade:<2}"+" "*22+f":{creds[sem][sub]}")
            print("-"*45)
        print(" "*13 + "End of Grade Report")
        self._box_footer()
    
    def Rankings(self):
        StudentRecord = self._file_opening("StudentRecord.json")

        rank_list = []
        print("(Enter your branch/batch or press [ENTER] for overall ranking)")
        batch_choice = input("Select batch: ")
        branch_choice = input("Select branch: ")

        for sid,data in StudentRecord.items():
            if data["CGPA"] == None:
                data["CGPA"] = 0.0            
            stud = {"Name":data["Name"],
                    "SID":sid,
                    "branch":data["Branch"],
                    "batch":data["Batch"],
                    "CGPA":data["CGPA"]}
            
            if batch_choice == "":
                pass
            elif batch_choice != data["Batch"]:
                continue
            if branch_choice == "":
                pass
            elif branch_choice != data["Branch"]:
                continue

            rank_list.append(stud)

        def merge_sort(arr):                                    # time complexity: O(n) = n logn
            n = len(arr)                                        # Space complexity: O(n) = n
            if n >1 :
                mid = n // 2
                left = arr[:mid]
                right = arr[mid:]
                merge_sort(left)
                merge_sort(right)
                i, j, k = 0,0,0                                
                while i < len(left) and j < len(right):
                    if left[i]["CGPA"] <= right[j]["CGPA"]:
                        arr[k] = left[i]
                        i +=1
                        k +=1
                    elif right[j]["CGPA"] < left[i]["CGPA"]:
                        arr[k] = right[j]
                        j +=1
                        k +=1
                while i < len(left):
                    arr[k] = left[i]
                    i +=1
                    k +=1
                while j < len(right):
                    arr[k] = right[j]
                    j +=1
                    k +=1
            return arr        
        ranked_list = merge_sort(rank_list)
        ranked_list.reverse()

        self._box_header("RANKINGS")
        print("Rank"+" "*2+"Name"+" "*20+"Batch"+" "*6+"CGPA")
        i = 0
        for ele in ranked_list:
            i +=1
            if ele["SID"] == self.sid:
                print("-"*45)
            print(f"{i:>2}.   {ele["Name"]:<20}  {ele["branch"]:<4} {ele["batch"]}    {ele["CGPA"]:.2f}")
            if ele["SID"] == self.sid:
                print("-"*45)
        self._box_footer()
    
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

    def gpa_prediction(self):
        pass



s0 = Student("Harshit Gupta",24104059,"Ele",2028)
s1 = Student("Naveen Kumar",24104101,"Ele",2028)
s2 = Student("Avijit", 24107068,"Mech",2028)

s1.menu()
