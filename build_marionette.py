import sys

import marionette_windows.tasks

marionette_windows.util.debug = True

def main():
    tasks_to_do = [
        #marionette_windows.tasks.MakeBinDirTask,
        #marionette_windows.tasks.MakeLibDirTask,
        #marionette_windows.tasks.InstallPrereqsTask,
        #marionette_windows.tasks.InitWineTask,
        #marionette_windows.tasks.InstallPythonTask,
        #marionette_windows.tasks.InstallSetuptoolsTask,
        #marionette_windows.tasks.InstallPy2EXETask,
        #marionette_windows.tasks.InstallWineWrappers,
        #marionette_windows.tasks.InstallDlfcnTask,
        #marionette_windows.tasks.InstallMmanTask,
        marionette_windows.tasks.InstallRegex2DFATask_openfst,
        marionette_windows.tasks.InstallRegex2DFATask_re2,
        marionette_windows.tasks.InstallRegex2DFATask,
    ]
    for task in tasks_to_do:
        task_obj = task()

        actually_ran = False
        desc = task_obj.get_desc()
        if not task_obj.is_successful():
            task_obj.do_task()
            actually_ran = True

        if task_obj.is_successful():
            suffix = ''
            if not actually_ran: suffix = ' [cached]'
            print desc + ' ... ' + 'done' + suffix
        else:
            print desc + ' ... ' + 'failed'
            sys.exit(1)

if __name__ == "__main__":
    main()