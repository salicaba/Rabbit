#!/usr/bin/env python
import sqlite3
import aio_pika
from fastapi import FastAPI, HTTPException

app = FastAPI()

# --- FUNCIÓN AUXILIAR PARA RABBITMQ ---
async def enviar_a_rabbit(mensaje_texto: str):
    try:
        # Usamos 127.0.0.1 para que la conexión de WSL a Docker sea estable
        connection = await aio_pika.connect_robust("amqp://guest:guest@127.0.0.1/")
        async with connection:
            channel = await connection.channel()
            await channel.default_exchange.publish(
                aio_pika.Message(body=mensaje_texto.encode()),
                routing_key="unachlidts"
            )
    except Exception as e:
        print(f"Error conectando a RabbitMQ: {e}")

# --- RUTAS DE LA API (CRUD) ---

# 1. VER LISTA COMPLETA
@app.get("/usuarios/")
async def listar_usuarios():
    conn = sqlite3.connect('unach.db')
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM usuarios")
    datos = cursor.fetchall()
    conn.close()
    return {"usuarios": datos}

# 2. REGISTRAR NUEVO
@app.post("/registrar/")
async def registrar(usuario: str, contraseña: str):
    conn = sqlite3.connect('unach.db')
    cursor = conn.cursor()
    cursor.execute("INSERT INTO usuarios (nombre, clave) VALUES (?, ?)", (usuario, contraseña))
    conn.commit()
    conn.close()
    
    await enviar_a_rabbit(f"CREAR: Usuario '{usuario}' registrado en la DB.")
    return {"mensaje": "Usuario guardado exitosamente"}

# 3. ACTUALIZAR EXISTENTE
@app.put("/editar/{usuario_id}")
async def editar(usuario_id: int, nuevo_nombre: str, nueva_contraseña: str):
    conn = sqlite3.connect('unach.db')
    cursor = conn.cursor()
    cursor.execute("UPDATE usuarios SET nombre = ?, clave = ? WHERE id = ?", (nuevo_nombre, nueva_contraseña, usuario_id))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    conn.commit()
    conn.close()
    
    await enviar_a_rabbit(f"EDITAR: El ID {usuario_id} fue modificado a '{nuevo_nombre}'.")
    return {"mensaje": f"Usuario {usuario_id} actualizado"}

# 4. BORRAR
@app.delete("/eliminar/{usuario_id}")
async def eliminar(usuario_id: int):
    conn = sqlite3.connect('unach.db')
    cursor = conn.cursor()
    cursor.execute("DELETE FROM usuarios WHERE id = ?", (usuario_id,))
    
    if cursor.rowcount == 0:
        conn.close()
        raise HTTPException(status_code=404, detail="Usuario no encontrado")
        
    conn.commit()
    conn.close()
    
    await enviar_a_rabbit(f"ELIMINAR: El ID {usuario_id} fue borrado de la DB.")
    return {"mensaje": f"Usuario {usuario_id} eliminado"}