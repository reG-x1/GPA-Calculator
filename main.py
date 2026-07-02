import json,os

class Record:
    Grade_eq = {"A+": 10, "A": 9, "B+": 8, "B": 7, "C+": 6, "C": 5, "D": 4 }
    branches_avail = ('CS','DS','Aero','ECE','VLSI','Ele','Mech','Civil','Prod','Meta')
    avail_sem = ["sem1","sem2","sem3","sem4","sem5","sem6","sem7","sem8"]

    def __init__(self,name,branch,batch):
        self.name = name
        self.branch = branch
        self.batch = batch
        self.sem = self.deducing_sems()

    def __str__(self):
        pass

    def add_course_data(self):
        branch = self.branch
        batch = str(self.batch)
        sem = int(self.sem)

        CourseDict = self._file_opening()                                              # HELPER 1
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

            try:
                with open("CourseDict.tmp",'w') as f:
                    json.dump(CourseDict,f,indent=4)
                os.replace("CourseDict.tmp","CourseDict.json")
                print(f"{missing_sem.upper()} data saved successfully!")
            
            except Exception as e:
                print(f"CRITICAL ERROR! : Could not save data.\nReason: {e}")

    def deducing_sems(self):
        year = self.batch                   # graduating year

        from datetime import datetime

        current_time = datetime.now()
        current_year = current_time.year
        current_month = current_time.month
        join_year = year - 4

        if current_year > year:
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

    def _file_opening(self):
        with open("CourseDict.json",'r') as f:
            CourseDict = json.load(f)
        return CourseDict
    
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
    def __init__(self,name,branch,batch):
        super().__init__(name,branch,batch)

    def __str__(self):
        pass
 
    def menu(self):
        print(f"========================= HOME =========================")
        print(f"Select from the following modes: ")
        print("1. View Course Info\n2. Add Course Info\n3. View Student Info")
        print("4. View Rankings\n5. Others\n6. Exit")
        
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
                self.StudentInfo()

            elif mode == 4:
                self.Rankings()

            elif mode == 5:
                self.others()

            elif mode == 6:
                print("Thanks for visiting!!")

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
        except KeyError:
            print(f"No Data Availabe.\n(Switch to Mode 2 to add course details.)")

    def StudentInfo(self):
        pass

    def Rankings(self):
        pass

    def others(self):
        pass

    def sgpa_calculate(self):
        pass

    def cgpa_calculate(self):
        pass


s1 = Student("Naveen", "Ele", 2028)
s2 = Student("Avijit","Mech",2028)
s3 = Student("Rudra","Ele", 2029)
