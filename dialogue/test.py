def getObjectsFromUrl(url):
    # sample = "/dialogue-group/23"
    data = url.lstrip("/").rstrip("/").split("/")
    #sample = ["dialogue-group","23"]
    st = ""
    inti = ""
    for item in data:
        if (item.isdigit()):
            inti = int(item)
        else:
            st = item    
    return [st,inti]





print(getObjectsFromUrl("/dialogue-gourp/23"))