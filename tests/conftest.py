import pytest
from app import create_app
from app.models.task import Task
from app.models.goal import Goal
from app import db
from datetime import datetime
from flask.signals import request_finished



@pytest.fixture
def app():
    # create the app with a test config dictionary
    app = create_app({"TESTING": True})

    @request_finished.connect_via(app)
    def expire_session(sender, response, **extra):
        db.session.remove()

    with app.app_context():
        db.create_all()
        yield app

    # close and remove the temporary database
    with app.app_context():
        db.drop_all()


@pytest.fixture
def client(app):
    return app.test_client()


# This fixture gets called in every test that
# references "one_task"
# This fixture creates a task and saves it in the database
@pytest.fixture
def one_task(app):
    new_task = Task(
        title="Go on my daily walk 🏞", description="Notice something new every day", completed_at=None)
    db.session.add(new_task)
    db.session.commit()


# This fixture gets called in every test that
# references "three_tasks"
# This fixture creates three tasks and saves
# them in the database
@pytest.fixture
def three_tasks(app):
    db.session.add_all([
        Task(
            title="Water the garden 🌷", description="", completed_at=None),
        Task(
            title="Answer forgotten email 📧", description="", completed_at=None),
        Task(
            title="Pay my outstanding tickets 😭", description="", completed_at=None)
    ])
    db.session.commit()


# This fixture gets called in every test that
# references "completed_task"
# This fixture creates a task with a
# valid completed_at date
@pytest.fixture
def completed_task(app):
    new_task = Task(
        title="Go on my daily walk 🏞", description="Notice something new every day", completed_at=datetime.utcnow())
    db.session.add(new_task)
    db.session.commit()


# This fixture gets called in every test that
# references "one_goal"
# This fixture creates a goal and saves it in the database
@pytest.fixture
def one_goal(app):
    new_goal = Goal(title="Build a habit of going outside daily")
    db.session.add(new_goal)
    db.session.commit()


# This fixture gets called in every test that
# references "one_task_belongs_to_one_goal"
# This fixture creates a task and a goal
# It associates the goal and task, so that the
# goal has this task, and the task belongs to one goal
@pytest.fixture
def one_task_belongs_to_one_goal(app, one_goal, one_task):
    task = Task.query.first()
    goal = Goal.query.first()
    goal.tasks.append(task)
    db.session.commit()
