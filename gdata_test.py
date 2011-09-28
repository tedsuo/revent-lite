import gdata.spreadsheet.text_db

client = gdata.spreadsheet.text_db.DatabaseClient(username='ted@radicaldesigns.org',password='ryogas12')
db = client.GetDatabases(spreadsheet_key='0Audib9Y4DZuxdDMtX3Voa0ZGcldzSzR4TGwxLWtWMUE')
table = db[0].GetTables(name='foo')
row = table[0].AddRecord(data={ 'bar':'none', 'manchu':'ria' })
