import sqlite3


class DBase:
    def __init__(self, name='exert.db'):
        self.name = name

    def init(self):
        '''
        初始化数据库
        '''

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute('''
        CREATE TABLE IF NOT EXISTS id_path (
            id   BIGINT PRIMARY KEY NOT NULL,
            path STRING
        );
        ''')
        conn.commit()
        conn.close()

    def insert(self, id, path):
        '''
        '''

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        cursor.execute(f'''
        INSERT INTO id_path
        (
            id, path
        )
        VALUES
        ({id}, '{path}')
        ''')
        conn.commit()
        conn.close()

    def get_by_ids(self, ids):
        '''
        '''

        order = [f'WHEN {v} THEN {i}' for i, v in enumerate(ids)]
        ordersql = ' \n '.join(order)
        idsql = ','.join([str(i) for i in ids])

        conn = sqlite3.connect(self.name)
        cursor = conn.cursor()
        sql = f'''
        SELECT * FROM id_path
        WHERE id IN ({idsql})
        ORDER BY CASE id {ordersql} END
        '''
        
        cursor.execute(sql)
        rows = cursor.fetchall()
        conn.close()
        return rows
