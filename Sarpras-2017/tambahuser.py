hostname = 'localhost'
username = 'root'
password = ''
database = 'DBNAME'

# Simple routine to run a query on a database and print the results:
def doQuery( conn ) :
  cur = conn.cursor()
  query = "drop user if exists 'admin_penjadwalan'@'localhost'; create user 'admin_penjadwalan'@'localhost'; grant all privileges on sarpras_peminjamanruang.* to 'admin_penjadwalan'@'localhost'; grant all privileges on test_sarpras_peminjamanruang.* to 'admin_penjadwalan'@'localhost'; flush privileges;"
  cur.execute( query )
  print ("admin_penjadwalan creation has been success. Created at " + hostname + " by " + username)

if __name__ == '__main__':
	import MySQLdb
	import sys
	if len(sys.argv) > 1:
		password = sys.argv[1]
		myConnection = MySQLdb.connect( host=hostname, user=username, passwd=password )
	else:
		myConnection = MySQLdb.connect( host=hostname, user=username )
	doQuery( myConnection )
	myConnection.close()
