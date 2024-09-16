import aiosqlite as sq


async def create_db():
    print("Creating database...")
    global db

    db = await sq.connect('database.db')

    async with db.cursor() as cur:
        await cur.execute("""CREATE TABLE IF NOT EXISTS referrals(
            user_id INTEGER PRIMARY KEY,
            ref_link TEXT,
            ref_id TEXT
        )""")

        await cur.execute("""CREATE TABLE IF NOT EXISTS messages(
            message_id INTEGER PRIMARY KEY AUTOINCREMENT,
            user_id INTEGER
        )""")

    await db.commit()


async def add_user(user_id, ref_link, ref_id):
    async with db.cursor() as cur:
        await cur.execute('SELECT user_id FROM referrals WHERE user_id = ?', (user_id,))
        result = await cur.fetchone()

        if result:
            return False
        else:
            await cur.execute('INSERT INTO referrals (user_id, ref_link, ref_id) VALUES (?, ?, ?)',
                              (user_id, ref_link, ref_id))
            await db.commit()
            return True


async def insert_message(message_id, user_id):
    async with db.cursor() as cur:
        await cur.execute('INSERT INTO messages (message_id, user_id) VALUES (?, ?)', (message_id, user_id))
        await db.commit()


async def get_message(message_id):
    async with db.cursor() as cur:
        await cur.execute('SELECT * FROM messages WHERE message_id = ?', (message_id,))
        result = await cur.fetchone()
        return result


async def get_user_id_by_ref_id(ref_id):
    async with db.cursor() as cur:
        await cur.execute('SELECT user_id FROM referrals WHERE ref_id = ?', (ref_id,))
        result = await cur.fetchone()
        return result


async def get_user(user_id):
    async with db.cursor() as cur:
        user = await cur.execute('SELECT * FROM referrals WHERE user_id = ?', (user_id,))
        return await user.fetchone()
