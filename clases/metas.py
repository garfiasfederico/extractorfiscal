def writeMeta(file, meta):
    try:
        f = open(file,"a")
        f.writelines(meta)
        f.close()
    except:
        pass
