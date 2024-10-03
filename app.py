import argparse
import sys


class AddFunction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        add_task(namespace, values)

class UpdateFunction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        update_task(namespace, values)

class ListFunction(argparse.Action):
    def __call__(self, *args, **kwargs):
        list_tasks(*args, **kwargs)

class DeleteFunction(argparse.Action):
    def __call__(self, parser, namespace, values, option_string=None):
        delete_task(namespace, values)

class InProgressFunction(argparse.Action):
    def __call__(self, *args, **kwargs):
        mark_task_in_progress(*args, **kwargs)

class CompletedFunction(argparse.Action):
    def __call__(self, *args, **kwargs):
        mark_task_done(*args, **kwargs)


def add_task(namespace, values):
    # check and see if JSON file exists
    # if not found create it and add to file
    # else append to found file
    pass

def update_task(namespace, values):
    # check if JSON file exists
    # check inputs
    # retrieve task based on id
    # update description with new task text
    # store in JSON file
    pass


def delete_task(namespace, values):
    # find task by id
    # return if not found
    # remove row from in memory store
    pass


def list_tasks(param, param1):
    # pretty print to the console
    pass

def mark_task_in_progress(param, param1):
    # retrieve task by id
    # change status of task
    # update records in JSON
    pass



def mark_task_done(param, param1):
    # retrieve task by id
    # change status of task
    # update records in JSON

    pass


def setup_arguments():
    parser = argparse.ArgumentParser('Task-Cli: take tasks on the command line')

    parser.add_argument('add', action=AddFunction, help='Tasks to execute')
    parser.add_argument('update', action=UpdateFunction, help='Tasks to execute')
    parser.add_argument('delete', action=DeleteFunction, help='Tasks to execute')
    parser.add_argument('list', action=ListFunction, help='Tasks to execute')
    parser.add_argument('mark-in-progress', action=InProgressFunction, help='Tasks to execute')
    parser.add_argument('mark-done', action=CompletedFunction, help='Tasks to execute')

    return parser.parse_args()


def main():
    print(sys.argv)
    args = setup_arguments()
    # while true, accept all input from users

if __name__ == '__main__':
    main()