from sqlalchemy import create_engine, Column, Integer, String, Date
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from datetime import datetime, date, timedelta

# Creating the database
engine = create_engine('sqlite:///todo.db? check_same_thread=False')

# Creating the table
Base = declarative_base()


class Task(Base):
	__tablename__ = 'task'
	id = Column(Integer, primary_key=True)
	task = Column(String)
	deadline = Column(Date, default=date.today())

	def __repr__(self):
		return self.task


# Create a session
Base.metadata.create_all(engine)
Session = sessionmaker(bind=engine)
session = Session()


def menu():
	while True:
		action = input(
			'''
1) Today's tasks
2) Week's tasks
3) All tasks
4) Missed tasks
5) Add task
6) Delete task
0) Exit
''')
		if action == '1':
			today_tasks()
		elif action == '2':
			weeks_tasks()
		elif action == '3':
			all_tasks()
		elif action == '4':
			missed_tasks()
		elif action == '5':
			add_task()
		elif action == '6':
			delete_task()
		elif action == '0':
			print('Bye!')
			break


def today_tasks():
	rows = session.query(Task).filter(Task.deadline == date.today()).all()
	if not rows:
		print(f'Today {date.today().strftime("%d %b")}:\nNothing to do!')
	else:
		print(f'Today {date.today().strftime("%d %b")}:')
		for num, task in enumerate(rows):
			print(num + 1, task, sep='. ')


def weeks_tasks():
	session.query(Task.task).order_by(Task.deadline).all()
	for day in range(7):
		weekly_tasks = date.today() + timedelta(days=day)
		daily_task = session.query(Task).filter(Task.deadline == weekly_tasks).all()
		if daily_task:
			print(f'\n{weekly_tasks.strftime("%A %d %b")}:')
			for num, task in enumerate(daily_task):
				print(num + 1, task, sep='. ')
		else:
			print(f'\n{weekly_tasks.strftime("%A %d %b")}:\nNothing to do!')


def all_tasks():
	rows_ = session.query(Task).order_by(Task.deadline).all()
	print('All tasks:')
	for num, task in enumerate(rows_):
		print(f"{num + 1}. {task}. {task.deadline.day} {task.deadline.strftime('%b')}", sep='. ')


def add_task():
	task = input('Enter task\n')
	date_string = input('Enter deadline\n')
	new_row = Task(
		task=task,
		deadline=datetime.strptime(date_string, '%Y-%m-%d').date()
	)
	session.add(new_row)
	session.commit()
	print('The task has been added!')


def missed_tasks():
	rows = session.query(Task).filter(Task.deadline <= datetime.today().date()).order_by(Task.deadline).all()
	print('Missed tasks:')
	if rows:
		for num, task in enumerate(rows):
			print(f'{num + 1}. {task}. {rows[num].deadline.strftime("%d %b")}')
	else:
		print('Nothing is missed!')


def delete_task():
	rows = session.query(Task).filter(Task.deadline <= date.today()).order_by(Task.deadline).all()
	print('Choose the number of the task you want to delete:')
	if rows:
		for num, task in enumerate(rows):
			print(f'{num + 1}. {task}. {rows[num].deadline.strftime("%d %b")}')
		specific_row = rows[int(input()) - 1]
		session.delete(specific_row)
		session.commit()
		print('The task has been deleted!')


if __name__ == '__main__':
	menu()
