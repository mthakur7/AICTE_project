import sys
from operator import itemgetter

taskFile = 'task.txt'
completedFile = 'completed.txt'


with open(taskFile, 'a') as file:
    pass
with open(completedFile, 'a') as file:
    pass


def runApp(cmd=None, *args):  
    if cmd == 'help' or not cmd:
        help()
    else:
        cmds = {
            'ls':     listTask,
            'report': report
        }
        cmdsWithArgs = {
            'add':    add,
            'del':    delete,
            'done':   done,            
        }
        cmds = cmds.get(cmd, False)
        cmdsWithArgs = cmdsWithArgs.get(cmd, False)
        if not cmds:
            if not cmdsWithArgs:
                sys.stdout.buffer.write('command does not exists!'.encode('utf8'))
                sys.exit(0)
            else:
                cmdsWithArgs(*args)
        else:
            cmds()
 
def help(): 
    taskhelp=\
         """Usage :-
$ ./task add 2 hello world    # Add a new item with priority 2 and text \"hello world\" to the list
$ ./task ls                   # Show incomplete priority list items sorted by priority in ascending order
$ ./task del INDEX            # Delete the incomplete item with the given index
$ ./task done INDEX           # Mark the incomplete item with the given index as complete
$ ./task help                 # Show usage
$ ./task report               # Statistics"""
    
    sys.stdout.buffer.write(taskhelp.encode('utf8'))
                


def add(*args):   
   
    if len(args)!=2:
        error('add')
    else:
        priority=args[0]
        task_new=args[1]
        
        task_old = None
        with open(taskFile, 'r') as file:
            task_old = file.read()           
          
        with open(taskFile, 'w') as file: 
            if task_old:
                new=priority+' '+task_new+'\n'+task_old

                def Convert(string):
                    li = list(string.split("\n"))
                    return li
                
                lis=Convert(new)
                new_lis=[]
                for ele in lis:
                   num=[]
                   num.append(int(ele.split()[0]))
                   num.append(ele)
                   new_lis.append(num) 

                  
                arr=sorted(new_lis, key=itemgetter(0))
                print()
                str1=""
                for ele in arr:
                    if(str1==""):                    
                        str1 = str1+ele[1]
                    else:
                        str1 = str1+'\n'+ele[1]


                file.write(str1)
            else:
                file.write(priority+' '+task_new)
        sys.stdout.buffer.write('Added task: "{}" with priority {}'.format(task_new,priority).encode('utf8'))



def listTask():
    taskCount= pendingtask()
    if taskCount:
        with open(taskFile, 'r') as file:
            for idx, task in enumerate(file):
                str=""
                for word in task.split():
                    if not word.isdigit():
                        str+=word+' '
                sys.stdout.buffer.write('{}. {}[{}]\n'.format(idx+1, str,task.split()[0]).encode('utf8'))
        print()
    else:
        sys.stdout.buffer.write('There are no pending tasks!'.encode('utf8'))


def delete(toBeDeleted=None):   
    if not toBeDeleted:
        error('delete')
    else:
        toBeDeleted = int(toBeDeleted.strip())
        taskCount = pendingtask()
        if toBeDeleted > taskCount or toBeDeleted <= 0:
            error('missing_delete', toBeDeleted)
        else:
            remove_task(toBeDeleted)
            sys.stdout.buffer.write('Deleted task #{}'.format(toBeDeleted).encode('utf8'))


def done(toBeMarked=None):  
    if len(args) == 2:
        error('task')
    else:
        toBeMarked = int(toBeMarked.strip())
        taskCount = pendingtask()
        if toBeMarked > taskCount or toBeMarked <= 0:
            error('missing_task', toBeMarked)
        else:
            markedtask = remove_task(toBeMarked)
            str=""
            for word in markedtask.split():
                if not word.isdigit():
                    if(str==""):
                      str=word
                    else:  
                      str+=' '+word
            newCompletion = str+'\n'
            oldCompletions = None
            with open(completedFile, 'r') as file:
                oldCompletions = file.read()
            with open(completedFile, 'w') as file:
                if oldCompletions:
                    file.write( oldCompletions + newCompletion )
                else:
                    file.write(newCompletion)
                sys.stdout.buffer.write('Marked item as done.'.encode('utf8'))




def pendingtask():  
    with open(taskFile, 'r') as file:
        count = 0
        while file.readline():
            count += 1
        return count


def completedtask(): 
    with open(completedFile, 'r') as file:
        count = 0
        while file.readline():
            count += 1
        return count


def remove_task(toBeRemoved=None):  
    totaltask = pendingtask()
    currenttask = None
    lefttasks = ''
    removedtask = ''
    with open(taskFile, 'r') as file:
        for idx, task in enumerate(file):
            currenttask = idx+1
            if currenttask != toBeRemoved:
                lefttasks += task
            else:
                removedtask = task
    if toBeRemoved == totaltask:
        lefttasks = lefttasks[:-1]
    else:
        removedtask = removedtask[:-1]
    with open(taskFile, 'w') as file:
        file.write(lefttasks)
    return removedtask

  
def error(errType, taskNumber=None): 
    errors = {
        'add': 'Error: Missing tasks string. Nothing added!',
        'delete': 'Error: Missing NUMBER for deleting tasks.',   
        'missing_delete': 'Error: task with index #{} does not exist. Nothing deleted.',
        'missing_task': 'Error: no incomplete item with index #{} exists.',        
        'task': 'Error: Missing NUMBER for marking tasks as done.' 
    }
    error = errors.get(errType, 'Error: an unknown error occurred.')
    if taskNumber == None:
        print(error)
    else:
        print(error.format(taskNumber))
    

def report():  
    pending = pendingtask()
    completed = completedtask()    
    sys.stdout.buffer.write("Pending : {}\n".format(pending).encode('utf8'))
    
   
    if pending:
        with open(taskFile, 'r') as file:
            for idx, task in enumerate(file):
                str=""
                for word in task.split():
                    if not word.isdigit():
                        if(str==""):
                          str+=word
                        else:
                          str+=' '+word
                sys.stdout.buffer.write('{}. {} [{}]\n\n'.format(idx+1, str,task.split()[0]).encode('utf8'))
   
           

    sys.stdout.buffer.write("Completed : {}\n".format(completed).encode('utf8'))
  
    if completed:
        with open(completedFile, 'r') as file:
            for idx, task in enumerate(file):                
                sys.stdout.buffer.write('{}. {}'.format(idx+1, task).encode('utf8'))
                
          


if __name__ == '__main__':
    args = sys.argv
    runApp(*args[1:])
