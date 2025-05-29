
from db import db_cursor

# 🔹 Load all URLs associated with a server
def cargar_urls(servidor_id):
    with db_cursor(dictionary=True) as cursor:
        sql = """
        SELECT url.url, servers.userId
        FROM url
        INNER JOIN servers ON url.serverId = servers.id
        WHERE servers.id = %s
        """
        cursor.execute(sql, (servidor_id,))
        return cursor.fetchall()


# 🔹 Get channel_id and message_id from a server
def cargar_mensaje_db(servidor_id):
    with db_cursor(dictionary=True) as cursor:
        sql = "SELECT channel_id, message_id FROM servers WHERE id = %s"
        cursor.execute(sql, (servidor_id,))
        return cursor.fetchone()


# 🔹 Update or save the embed message associated with a server
def guardar_mensaje_db(servidor_id, channel_id, message_id):
    with db_cursor() as cursor:
        sql = """
        UPDATE servers
        SET channel_id = %s,
            message_id = CASE WHEN message_id IS NULL THEN %s ELSE message_id END
        WHERE id = %s
        """
        cursor.execute(sql, (channel_id, message_id, servidor_id))


# 🔹 Check if a server exists
def servidor_existe(servidor_id):
    with db_cursor() as cursor:
        cursor.execute("SELECT id FROM servers WHERE id = %s", (servidor_id,))
        return cursor.fetchone() is not None


# 🔹 Create a new server if it doesn't exist
def crear_servidor_si_no_existe(servidor_id):
    if not servidor_existe(servidor_id):
        with db_cursor() as cursor:
            cursor.execute("INSERT INTO servers (id) VALUES (%s)", (servidor_id,))


def obtener_urls_autocompletado(server_id, user_id, filtro):
    with db_cursor(dictionary=True) as cursor:
        sql = """
        SELECT url FROM url
        WHERE serverId = %s AND userId = %s AND url LIKE %s
        LIMIT 25
        """
        cursor.execute(sql, (server_id, user_id, f"%{filtro}%"))
        return [row["url"] for row in cursor.fetchall()]
    
def eliminar_url(server_id, url):
    with db_cursor() as cursor:
        sql = "DELETE FROM url WHERE serverId = %s AND url = %s"
        cursor.execute(sql, (server_id, url))
        return cursor.rowcount > 0  

