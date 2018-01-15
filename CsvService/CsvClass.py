import csv



class CsvClass(object):


    def __init__(self, DnsCryptResolverDir: str):
        self.DnsCryptResolverDir = DnsCryptResolverDir
        pass

    def GetDnsCryptProxyNames(self):
        with open(self.DnsCryptResolverDir + "/dnscrypt-resolvers.csv", 'r') as f:
            reader = csv.reader(f)
            resolverList = list(reader)
            if 'Description' in resolverList[0]:
                resolverList.pop(0)
            resolverNameList = [resolverList[resolverList.index(row)][0] for row in resolverList]
            f.close()

            print("hello")
        return resolverNameList
