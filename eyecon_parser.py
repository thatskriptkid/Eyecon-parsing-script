import requests
import sqlite3
from sqlite3 import Error
import signal
import shutil

path = '/root/eyecon/photo/'

payload = {'cli': '7778xxxxxxxx', 'size': 'big', 'type':'1'}

headers = {'User-Agent': 'Dalvik/2.1.0 (Linux; U; Android 7.1.2; GT-I9195 Build/NJH47F)',
			'e-auth-v':'e1',
			'e-auth':'a578e279-e3f8-4dd8-a954-7e663f1f8375',
			'e-auth-c':'45',
			'Connection':'close',
			'Accept-Encoding':'gzip, deflate'}

def create_connection(db_file):
	try:
		conn = sqlite3.connect(db_file)
		return conn
	except Error as e:
		print(e)

	return None


def main():
	tokens = [
				('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', '31'),
				('xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx', '25'),
				('xxxxxxxxxxxxxxxxxxxxxxx','45'),
				('xxxxxxxxxxxxxxxxxxxxxxx','23')
			]

	database = 'GetContact.db'

	conn = create_connection(database)
	cur = conn.cursor()
	cur.execute("SELECT DISTINCT number FROM GetContact WHERE number LIKE \'7%\' ORDER BY number ASC")

	rows = cur.fetchall()

	i = 0

	for row in rows:
		try:
			number = row[0]

			payload['cli'] = str(number)

		 	r = requests.get('https://api.eyecon-app.com/app/pic', params=payload, headers=headers, stream=True)
			#print('number:%d | status code:%d' % (number, r.status_code))

			if r.status_code == 200:
				with open(path + str(number) + '.jpg', 'wb') as f:
					r.raw.decode_content = True
					shutil.copyfileobj(r.raw, f)

			if r.status_code == 401:
				if i == 4:
					print('Tokens kon4ilis!')
					break

				print('401 error! stop on number:%d, token used:%s' % (number, headers['e-auth']))
				print('set new token: %s' % tokens[i][0])
				headers['e-auth'] = tokens[i][0]
				headers['e-auth-c'] = tokens[i][1]
				i = i +1

		except:
			continue

if __name__ == '__main__':
	main()
