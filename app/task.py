from celery import Celery
from rectangle import RectangleOperations


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

    while True:
        print('List of Rectangles: ')
        operations.show_rectangle_data()

        rect_id = int(input('Enter the rectangle id: '))
        result = update_rectangle.delay(rect_id)

        data = result.get()

        print('Updated Rectangle: ')
        operations.show_rectangle_data(data)

        exit = input('Do you want to quit (yes/no)? ')
        if exit == 'yes':
            break
