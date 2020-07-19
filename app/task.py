from celery import Celery
from rectangle import RectangleOperations
from sqlalchemy.orm.exc import NoResultFound


app = Celery(
    'task',
    broker='redis://redis:6379/0',
    backend='redis://redis:6379/0'
)

operations = RectangleOperations()


@app.task
def update_rectangle(rectangle_id):
    rectangle_data = operations.update_rectangle(rectangle_id)
    return rectangle_data


if __name__ == '__main__':
    if operations.is_empty():
        operations.create_database_scheme()
        operations.insert_test_data()

    show_rectangle = True
    while True:
        if show_rectangle:
            print('*' * 100)
            print('List of Rectangles: ')
            operations.show_rectangle_data()

        rect_id = input('Enter the rectangle id: ')

        if not rect_id.isdigit():
            print('Wrong format! Please enter a integer.')
            show_rectangle = False
            continue

        result = update_rectangle.delay(rect_id)

        try:
            data = result.get()
        except NoResultFound:
            print(
                'Rectangle (rectangle_id {}) is not existed!'.format(rect_id)
            )
            break

        print('Updated Rectangle: ')
        operations.show_rectangle_data(data)

        is_exit = input('Do you want to quit (y/n)? ')
        if is_exit == 'y' or is_exit == 'n':
            if is_exit == 'y':
                break
        else:
            print('Wrong Answer!')
            break
        print('*' * 100)
