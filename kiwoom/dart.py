from konfig import Config
cc = Config("./conf.ini")
print(cc.get_map("app")['OPENDARTAPI'])
