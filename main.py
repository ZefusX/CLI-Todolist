import click
from rich import box
from rich.console import Console
from rich.table import Table

TODO_FILE = "todos.txt"


#Créé le fichier si il n'existe pas
with open(TODO_FILE, "a"):
  pass

with open(TODO_FILE, 'r') as file: 
    line_count = sum(1 for line in file)

choice_names = [str(i) for i in range(1, line_count)]

console = Console()

@click.group
def commands():
  pass

@click.command()
@click.option('-n', "--name", help="Add a task to the list")
def add(name):
  if name is None:
    name = console.input("[blue bold]Enter a [green underline]task[/green underline] : [/blue bold]")
  with open(TODO_FILE, "a+") as f:
    f.write(f"{name}\n")
  
@click.command()
@click.option('-i', "--index", help="Delete a task from the list", type=click.Choice(choice_names)) 
def delete(index: int):
  if index is None:
    valid=False
    while valid!=True:
      c=" ".join(choice_names)
      index = console.input(f"[blue bold]Enter the [green underline]index[/green underline] of the task to delete ([green]{c}[/green]): [/blue bold]")
      if not 0<=int(index)<line_count:
        console.print("[red]Please enter a valid index [/red]")
      else:
        valid=True
  with open(TODO_FILE, "r") as f:
    todo_list = f.read().splitlines()
    todo_list.pop(int(index))
  with open(TODO_FILE, "w") as f:
    f.write("\n".join(todo_list))
    f.write("\n")

@click.command()
@click.option('-i', "--index", help="Update the task at the index", type=click.Choice(choice_names))
@click.option('-n', "--name", help="Add a task to the list")
def update(index: int, name: str):
  if index is None:
    valid=False
    while valid!=True:
      c=" ".join(choice_names)
      index = console.input(f"[blue bold]Enter the [green underline]index[/green underline] of the task to update ([green]{c}[/green]): [/blue bold]")
      if not 0<=int(index)<line_count:
        console.print("[red]Please enter a valid index [/red]")
      else:
        valid=True
        
  if name is None:
    name  = console.input(f"[blue bold]Enter the [green underline]name[/green underline] of the task to update : [/blue bold]")
  with open(TODO_FILE, "r") as f:
    todo_list = f.read().splitlines()
    todo_list[int(index)]=str(name)
  with open(TODO_FILE, "w") as f:
    f.write("\n".join(todo_list))
    f.write("\n")

@click.command()
def show():
  table = Table(show_header=True, header_style="bold blue", highlight=True, box=box.MINIMAL_DOUBLE_HEAD)
  table.add_column("Index", width=6)
  table.add_column("Todo", min_width=20)
  with open(TODO_FILE, "r") as f:
    todo_list = f.read().split("\n")
    if len(todo_list[0])==0 and len(todo_list)==1:
      console.print("[i]No data... [/i]")
      return
    for i, todo in enumerate(todo_list):
      if todo != "":
        table.add_row(f"[{str(i)}]", todo)
    console.print(table)
  
  
commands.add_command(add)
commands.add_command(add, name='a')

commands.add_command(delete)
commands.add_command(delete, name="d")

commands.add_command(show)
commands.add_command(show, name="s")

commands.add_command(update)
commands.add_command(update, name="u")

if __name__ == "__main__": 
  commands()