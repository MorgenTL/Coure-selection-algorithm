# -*- coding: utf-8 -*-
"""
Created on Mon Mar  9 20:13:14 2020

@author: Morgan
"""
import copy

def inputfile (filename):
    """
    I need to sort the class list from the earliest to latest
    To prvent clogging the DFS 
    
    
    """
    classdict = {}
    with open(filename, 'r') as f:
        for line in f: 
            try:
                temp = line.replace(',', '')
                temp = temp.split()
                time = course(int(temp[1]), int(temp[2]), int(temp[3]), int(temp[4]))
                name = temp[0]
                if name not in classdict:
                    classdict[name] = [time]
                else:
                    classdict[name] += [time]
            except:
                pass

    return classdict


class course(object):
    def __init__ (self, start, end, weekday, sem):
        """
        
        start or end:  in the form of 1430
        weekday: 0 = Mon, 1 = Tue etc
        sem: 1 or 2
        
        """
        self.start = start
        self.end = end
        self.weekday = weekday
        self.sem = sem
        
        #realstart or end is in minute form 
        #it is used to aid further caculation
        self.realstart = (start//100)*60 + (start%100)
        self.realend = (end//100)*60 + (end%100)
    
    def get_start(self):
        return self.start
    
    def get_end(self):
        return self.end
    
    
    def get_realstart(self):
        return self.realstart
    
    def get_realend(self):
        return self.realend
    
    def get_weekday(self):
        return self.weekday
    
    def get_sem(self):
        return self.sem
    
    def timecrash(self, other):
        """
        This function do not take the semester and weekday into account
        
        
        """
        myrange = range (self.get_realstart(), self.get_realend())
        otherrange = range (other.get_realstart(), other.get_realend())
        
        if self.get_realstart() == other.get_realend() or other.get_realstart() == self.get_realend():
            pass                  
        else:
            if self.get_realend() in  otherrange or self.get_realstart() in  otherrange:
                raise ValueError
            
            if other.get_realend() in  myrange or other.get_realstart() in  myrange:
                raise ValueError
        
    def timediff(self, other):
        """
        This function find the time difference between target and self
        
        return: minute
        """        
        diff1 = self.get_realstart() - other.get_realend()
        diff2 = self.get_realend() - other.get_realstart()
        
        return min(abs(diff1), abs(diff2))
    
    def __str__(self):
        weekdaydict = {0:'Mon',1:'Tue',2:'Wed',3:'Thur',4:'Fri',5:'Sat',6:'Sun'}
        weekday = weekdaydict[self.get_weekday()]
        return str(self.get_start()) + " -> " + str(self.get_end()) + " (" + weekday + ") in sem " + str(self.get_sem())
    
    

def sort_timelist(OG_list, courseX):
    """
    This function sort the class_list (OG_list) from earliest to latest
    """
    for i in range(len(OG_list)):
        temp = OG_list[i]
        if courseX.get_realend() <= temp.get_realstart():
            return OG_list[:i] + [courseX] + OG_list[i:]
        
    return OG_list + [courseX]

def timelist_diff(OG_list, courseX):
    """
    This function return the time difference of the OG_list and the newly list w/ courseX
       
    return: +ve int or -ve int
    
    """
        
    OG_time = 0
    new_time = 0    
    
    if len(OG_list) >= 2:
        for i in range(len(OG_list)-1):
            OG_time += OG_list[i].timediff(OG_list[i+1])       
        
    
    newlist = sort_timelist(OG_list,courseX)
    
    for i in range(len(newlist)-1):
        new_time += newlist[i].timediff(newlist[i+1])
        
    return new_time - OG_time
    
    
        

def printlist(OG_list):
    for course in OG_list:
        print(course)


class timetable(object):
    def __init__(self):
        self.sem1 = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:0}
        self.sem2 = {0:[], 1:[], 2:[], 3:[], 4:[], 5:[], 6:0}
        self.history = []

    def get_sem1(self):
        return self.sem1
    
    def get_sem2(self):
        return self.sem2
    
    def get_history(self):
        return self.history
    
    def add(self,timetable ,courseX):
        
        day = timetable[courseX.get_weekday()]
        history = self.get_history()
        
        for c in day:              #This check if the courseX timecrash with courses in timetable!!
            courseX.timecrash(c)
            
        timetable[6] += timelist_diff(day,courseX)  
        history += [courseX]
        
        
        day = sort_timelist(day, courseX)
        timetable[courseX.get_weekday()] = day
        
        return timetable
    
    
    
    def addcourse(self,courseX):
        if courseX.get_sem() == 1:
            return self.add(self.get_sem1(), courseX)
        
        elif courseX.get_sem() == 2:
            return self.add(self.get_sem2(), courseX)
    
    def __len__(self):
        return (self.get_sem1()[6] + self.get_sem2()[6])
    
    
    

def printtimetable(timetable):
    """
    This function print out the timetable in a readable formate
    
    """
    print("Sem 1 time table")
    sem1 = timetable.get_sem1()
    sem2 = timetable.get_sem2()
    for i in range(6):
        printlist(sem1[i])
    print("There are in total", sem1[6], "minute(s) between lessons")
    
    print('-----------------')
    print("Sem 2 time table")
    for i in range(6):
        printlist(sem2[i])
    
    print("There are in total", sem2[6], "minute(s) between lessons")
        
        
def DFS(graph, classlist, shortest, path = timetable()):
    """
    This algorithm assume you must select all the class you inputed!!!
    
    
    graph: {class name: [opt1, opt2], etc..}
    classlist: just a list of class name
    shortest: the timetable with the least time diff between lesson
    path: current timetable   
    
    """
    if not classlist:
        return path
    
    for time in graph[classlist[0]]:
        temp = copy.deepcopy(path)
        
        try:
            temp.addcourse(time)
            newpath = DFS(graph, classlist[1:], shortest, temp)
            if newpath != None and (shortest == None or len(shortest) > len(newpath)):
                shortest = newpath                    
        except:
            pass
            #this prevent the timecrashed timetable to go any further!!!
        
    return shortest
            
        
def find_timetable(graph, classlist):   
    return DFS(graph, classlist, None)

def couretime(timetable, classlist):
    """
    This function can print out the course inputed
    with respect to the time
    
    timetable: custom object
    classlist: ordered list with respect to the order added to the timetable
    
    return: a nice string
    
    """
    history = timetable.get_history()
    for c in range(len(classlist)):        
        print(classlist[c],end="")
        print(": ",end="")
        print(history[c])
     
    
    
def basicsorting(filename):
    graph = inputfile(filename)
    classlist = list(graph.keys())
    timetable = find_timetable(graph, classlist)
    print('-----------------')
    print('Loading...')
    printtimetable(timetable)
    print('-----------------')
    print('The following is selected course:')
    couretime(timetable, classlist)


        

        
a = course(1100,1230,1,1)

b = course(1330,1420,1,1)
c = course(1430,1800,1,1)

d = course(1700,1800,1,1)
e = course(1800,1900,1,1)

f = course(2000,2030,1,1)
g = course(1430,1700,1,1)

graph = {"CC":[c,b], "E1":[a],"E2":[d,e],"E3":[f,g],"E4":[a]}
classlist = ['E3',"CC",'E1','E2']


basicsorting('input.txt')
        

        
        
        
        
        
        