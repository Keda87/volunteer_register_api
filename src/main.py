import asyncio
import os

from sanic import Sanic
from sanic.response import json

from .models import db, Participant

app = Sanic()
app.config.DB_HOST = 'db'
app.config.DB_PORT = os.environ.get('POSTGRES_PORT', '5432')
app.config.DB_USER = os.environ.get('POSTGRES_USER', 'postgres')
app.config.DB_PASSWORD = os.environ.get('POSTGRES_PASSWORD', 'postgres')
app.config.DB_DATABASE = os.environ.get('POSTGRES_DB', 'postgres')


async def initial_db(app):
    try:
        db.init_app(app)
        db_config = app.config

        # Create tables.
        await db.set_bind(f'postgresql://'
                          f'{db_config.DB_USER}:{db_config.DB_PASSWORD}@'
                          f'{db_config.DB_HOST}:{db_config.DB_PORT}/'
                          f'{db_config.DB_DATABASE}')
        await db.gino.create_all()
        print('--------------- Database initialization finished -----------')
    except Exception as ex:
        print(f'--------------- Failed to initialize database: {ex} -----------')
        print('Trying reconnect in 5 seconds...')
        await asyncio.sleep(5)
        await initial_db(app)


@app.listener('before_server_start')
async def before_server_start(app, loop):
    await initial_db(app)


@app.route('/api/participants/', methods=['POST', 'GET'])
async def participants(request):
    if request.method == 'POST':
        try:
            data = request.json

            await Participant.create(
                name=data['name'],
                email=data['email'],
                phone_1=data['phone_1'],
                phone_2=data['phone_2'],
                age=data['age'],
                payment_proof=data['payment_proof']
            )
        except (KeyError, TypeError):
            return json({'success': False}, 400)

    # Iterate over the results of a large query in a transaction as required
    async with db.transaction():
        async for u in Participant.query.gino.iterate():
            print(u.as_dict, flush=True)
    return json({'success': True}, 201)
