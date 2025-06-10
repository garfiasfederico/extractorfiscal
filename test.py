from clases.logs import Log
import pymssql 

conn = pymssql.connect(server="198.71.50.76", user="develop", password="Contasix2021De5", database="contabilidad") or ("No fue posible la conexion")
cursor = conn.cursor(as_dict=True)

cursor.execute('SELECT * FROM sat.tax_complax WITH (SNAPSHOT)')
for row in cursor:
    print("ID=%d, Compania=%s" % (row['_id'], row['company_id']))

conn.close()

#log = Log("logs/log_declaraciones.log")
#log.write("info","Hola que tal")
