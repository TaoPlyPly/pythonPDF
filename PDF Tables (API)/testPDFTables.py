import pdftables_api
from pdftables_api import Client, APIException
c = pdftables_api.Client('78vps727w9f5')
c.csv('testPDFTables.pdf','testPDFTables.csv')
