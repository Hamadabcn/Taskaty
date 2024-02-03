from .task import Task
from datetime import date
from tabulate import tabulate
from argparse import Namespace


class TaskController:
    def __init__(self, file_name):
        self.file_name = file_name

    def add_task(self, args):
        # 1. first we have to get start_date
        if not args.start_date:
            now = date.today().isoformat()
            args.start_date = now

        # 2. the task
        task = Task(
            args.title, args.description, args.start_date, args.end_date, args.done
        )
        # 3. open file and save information
        with open(self.file_name, "a") as file:
            file.write(str(task) + "\n")

    def list_tasks(self):
        unfinished_tasks = []
        with open(self.file_name, "r") as file:
            for line_number, line in enumerate(file, 1):
                values = line.split(", ")
                if len(values) < 4:
                    #print(f"Error on line {line_number}: {line}")
                    continue

                title, description, start_date, *rest = values
                end_date = None if not rest or rest[0] == "None" else rest[0]
                done = False if not rest or rest[-1].strip("\n") == "False" else True

                if done:
                    continue

                unfinished_tasks.append(
                    {
                        "title": title,
                        "description": description,
                        "start_date": start_date,
                        "end_date": end_date,
                    }
                )

        return unfinished_tasks

    def list_all_tasks(self):
        tasks = []
        with open(self.file_name, "r") as file:
            for line_number, line in enumerate(file, 1):
                values = line.split(", ")
                if len(values) < 5:
                    #print(f"Error on line {line_number}: {line}")
                    continue

                title, description, start_date, end_date, done = values
                end_date = None if end_date == "None" else end_date
                done = False if done.strip("\n") == "False" else True
                tasks.append(
                    {
                        "title": title,
                        "description": description,
                        "start_date": start_date,
                        "end_date": end_date,
                        "done": done,
                    }
                )

        return tasks

    def due_date(self, start, end):
        start_date = date.fromisoformat(start)
        end_date = date.fromisoformat(end)
        date_delta = end_date - start_date
        return f"{date_delta.days}, days left."

    def print_table(self, tasks):
        formatted_tasks = []
        for number, task in enumerate(tasks, 1):
            if task["start_date"] and task["end_date"]:
                due_date = self.due_date(task["start_date"], task["end_date"])
            else:
                due_date = "Open"
            formatted_tasks.append(
                {
                    "no.": number,
                    **task,
                    "due_date": due_date,
                }
            )

        print(tabulate(formatted_tasks, headers="keys"))

    def display(self, args):
        all_tasks = self.list_all_tasks()
        unchecked_tasks = self.list_tasks()

        if not all_tasks:
            print("There are no tasks to display. To add a task use add <task>")
            return

        if args.all:
            self.print_table(all_tasks)
        else:
            if unchecked_tasks:
                self.print_table(unchecked_tasks)
            else:
                print("All tasks are checked!")

    def check_task(self, args):
        index = args.task
        tasks = self.list_all_tasks()
        if index <= 0 or index > len(tasks):
            print(f"Task number ({index}) does not exist")
            return

        tasks[index - 1]["done"] = True
        with open(self.file_name, "w") as file:
            for task in tasks:
                self.add_task(Namespace(**task))

    def remove(self, args):
        tasks = self.list_all_tasks()
        if args.tasks:
            index = args.tasks
        else:
            index = len(tasks) - 1

        if index <= 0 or index > len(tasks):
            print(f"Task number ({index}) does not exist!")
            return

        tasks.pop(index - 1)

        with open(self.file_name, "w") as file:
            for task in tasks:
                self.add_task(Namespace(**task))

    def reset(self, *args):
        with open(self.file_name, "w") as file:
            file.write("")
            print("You have deleted all the tasks!")
