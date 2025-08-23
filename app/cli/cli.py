from typer import Typer

from routes.habits import router as habit_router
from routes.records import router as record_router 

app = Typer(name="my_cli_app", help="A simple CLI application example.")

 