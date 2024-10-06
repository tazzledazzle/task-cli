"""
    main runner
"""
import argparse
import task # pylint: disable=import-error


def main(*args):
    """
    Entrypoint for runner
    :param args: arguments passed in
    :return:
    """
    # subparser to group commands
    parser = argparse.ArgumentParser('Task-Cli: take tasks on the command line')
    subparsers = parser.add_subparsers(dest='command')

    # add
    parser_add = subparsers.add_parser('add')
    parser_add.add_argument('description', type=str, help='Task description')

    # update
    parser_update = subparsers.add_parser('update')
    parser_update.add_argument('id', type=int, help='Task ID')
    parser_update.add_argument('description', type=str, help='Task description')

    # delete
    parser_delete = subparsers.add_parser('delete')
    parser_delete.add_argument('id', type=int, help='Task ID')

    # list
    parser_list = subparsers.add_parser('list')
    parser_list.add_argument('status', nargs='?',
                             choices=['todo', 'in-progress', 'complete'], help='Task status')

    # mark-in-progress
    parser_in_progress = subparsers.add_parser('in_progress')
    parser_in_progress.add_argument('id', type=int, help='Task ID')

    # mark as complete
    parser_complete = subparsers.add_parser('complete')
    parser_complete.add_argument('id', type=int, help='Task ID')

    args_in = parser.parse_args(args)

    # determine which command
    if args_in.command == 'add':
        print(f"Adding {args_in.description}")
        task.add_task(args_in.description)
    elif args_in.command == 'update':
        task.update_task(args_in.id, args_in.description)
    elif args_in.command == 'delete':
        task.delete_task(args_in.id)
    elif args_in.command == 'list':
        task.list_tasks(args_in.status)
    elif args_in.command == 'in_progress':
        task.mark_task_in_progress(args_in.id)
    elif args_in.command == 'complete':
        task.mark_task_complete(args_in.id)

if __name__ == '__main__':
    main()
