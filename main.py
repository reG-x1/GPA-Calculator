class Record:

    Grade_eq = {"A+": 10, "A": 9, "B+": 8, "B": 7, "C+": 6, "C": 5, "D": 4 }
    branches_avail = ('CS','DS','AI/ML','Aero','ECE','VLSI','Ele','Mech','Civil','Prod','Meta')
    
    def __init__(self,name,branch,batch):
        self.name = name
        self.branch = branch
        self.batch = batch
        self.sem = self.deducing_sems()

    def __str__(self):
        pass

    def add_course_data(self):
        branch = self.__branch

    def deducing_sems(self,year):
        year = self.__batch

        from datetime import datetime

        current_time = datetime.now()
        current_year = current_time.year
        current_month = current_time.month
        join_year = year - 4

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


class Student(Record):
    def __init__(self,name,branch,batch):
        super().__init__(name,branch,batch)
        
        self.menu()

    def __str__(self):
        pass
 
    def menu(self):
        print(f"========================= HOME =========================")
        print(f"Select from the following modes: ")
        print(f"1. View/Edit Course Info\n2. View Student Info\n3. Check your rank\n4. Others\n5. Exit")
        
        try:
            mode = int(input("Enter the mode: "))

            if mode == 1:
                self.CourseInfo()

            elif mode == 2:
                self.StudentInfo()

            elif mode == 3:
                self.Rankings()

            elif mode == 4:
                self.others()

            elif mode == 5:
                print("Thanks for visiting!!")

            else:
                print("MODE NOT FOUND!!!No such modes available, please select from the availabe modes.\n")
                self.menu()
        except:
            print("INVALID INPUT!!!Please enter a number to choose from the available modes.\n")
            self.menu()
            
    def CourseInfo(self):
        pass

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


user1 = Student("Naveen", "Ele", 4)
