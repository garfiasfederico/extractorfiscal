import pymssql 

contribuyente = ""
nombre = ""
path_cert = ""
path_key = ""
password_fiel = ""

def getDataCompany(rfc:str):
    global contribuyente, nombre, path_cert, path_key, password_fiel
    try:
        conn = pymssql.connect(server="198.71.50.76", user="develop", password="Contasix2021De5", database="contabilidad") or ("No fue posible la conexion")
        cursor = conn.cursor(as_dict=True)
        #cursor.execute('SELECT * FROM sat.tax_complax WITH (SNAPSHOT)')
        #for row in cursor:
        #    print("ID=%d, Compania=%s" % (row['_id'], row['company_id']))
        cursor.execute(
                    '''
                    SELECT TOP 1
                            c.tax_identification,
                            c.name_company,
                            cf.directory_cer,
                            cf.directory_key,
                            cf.password                    
                    FROM contabilidad.catalogs.company c  
                    INNER JOIN contabilidad.setting.configuration_files cf  ON c.id=cf.company_id 
                    WHERE C.status=1 AND c.tax_identification = %s
                    ''',
                    rfc
                    )    
        #print(len(cursor.fetchall()))        
        for row in cursor:
            #print("ID=%s, Compania=%s, Cert=%s, Key=%s, password=%s" % (row['tax_identification'], row['name_company'], row['directory_cer'], row['directory_key'], row['password']))    
            contribuyente = row['tax_identification']
            nombre = row['name_company']
            path_cert = row['directory_cer']
            path_key = row['directory_key']
            password_fiel = row['password']            
        conn.close()        
    except Exception as e:
        print(e.args)