from wolai.auth import get_authed_context
from wolai.database import get_database, insert_database
from wolai.encoder import to_json

try:
    from local_settings import APP_ID, APP_SECRET
except ImportError:
    APP_ID = '4X96H9ovsa7pyK6xmPgBHm'
    APP_SECRET = '5086c508ef0711543ca932d375f1fb3d4222d3fd69c69f2b15e17e1c0188bddf'

PARENT_ID = 'vtMAoPV9LUDprjR6UA9vu4'
IMAGE = 'https://img2.baidu.com/it/u=3202947311,1179654885&fm=253&fmt=auto&app=138&f=JPEG?w=800&h=500'


def main():
    # get authed context
    ctx = get_authed_context(APP_ID, APP_SECRET)
    db = get_database(ctx, 'vtMAoPV9LUDprjR6UA9vu4')
    for row in db.rows:
        print(to_json(row))
        print(row.to_create_database_row())
    print(insert_database(ctx, 'vtMAoPV9LUDprjR6UA9vu4', rows=db.rows))


if __name__ == '__main__':
    main()
