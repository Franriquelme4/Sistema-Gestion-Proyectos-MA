#import psycopg2
#import usuario

#con = psycopg2.connect(database="metodologias_agiles", user="postgres", password="postgres", host="127.0.0.1", port="5433")
#print("Database opened successfully")

#cur = con.cursor()

#cur.execute("INSERT INTO public.usuario_rol(id, nombre_rol, descripcion_rol) VALUES (1,'Administrador','Rol para administrar el sistema')");
#con.commit()

#print("Records inserted successfully")

#con.close()