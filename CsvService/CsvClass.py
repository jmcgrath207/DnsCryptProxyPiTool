import csv



class CsvClass(object):




    def GetDnsCryptProxyNames(self,DnsCryptResolverDir: str):
        with open(DnsCryptResolverDir + "/dnscrypt-resolvers.csv", 'r') as f:
            reader = csv.reader(f)
            resolverList = list(reader)
            if 'Description' in resolverList[0]:
                resolverList.pop(0)
            resolverNameList = [resolverList[resolverList.index(row)][0] for row in resolverList]
            f.close()

        return resolverNameList
