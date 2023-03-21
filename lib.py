import csv
import base64
import tiktoken
import shortuuid
import os

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

class DictArrayManager:
	def __init__(self):
		self.logfile = "log.csv"
		self.clear()

	def get_recent_history(self, tokens):
			result = []
			total = 0
			for i in range(len(self.history)-1,0,-1):
				if total >= tokens:
					break
				result.append(self.history[i])
				total += self.token_history[i]
			return list(reversed(result))

	def clear(self):
		self.array = []
		self.history = []
		self.tokens = []
		self.token_history = []
		self.sessionid = shortuuid.uuid()

	def add(self, role, content):
		self.array.append({'role': role, 'content': content})
		num_tokens = len(encoding.encode(role + " " + content))
		self.tokens.append(num_tokens)
		self.log_latest()

	def unshift(self, role, content):
		self.array.insert(0, {'role': role, 'content': content})

	def shift(self, num):
		if num > len(self.array):
			self.clear()
		else:
			self.array = self.array[num:]

	def count(self):
		count = 0
		for item in self.array:
			for value in item.values():
				count += len(value.split())
		return count

	def truncate(self, num):
		did_truncate = False
		while self.count() > num:
			self.history.append(self.array.pop(1))
			self.token_history.append(self.tokens.pop(1))
			print(self.history[-1])
			did_truncate = True
		return did_truncate

	def log_latest(self):
		if not os.path.exists(self.logfile):
			with open(self.logfile, mode='a', newline='') as log_file:
				csv_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
				csv_writer.writerow(["id","role","message"])
		latest = self.array[-1]
		with open(self.logfile, mode='a', newline='') as log_file:
			csv_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csv_writer.writerow([self.sessionid, latest["role"], self.encode(latest["content"])])

	def encode(self, data):
		content_bytes = data.encode("utf-8")
		base64_byte = base64.b64encode(content_bytes)
		base64_string = base64_byte.decode("utf-8")
		return base64_string

	def get_log(self):
		log_lines = []
		with open('log.csv', newline='') as log_file:
			csv_reader = csv.DictReader(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			for row in csv_reader:
				for i in row:
					if self.is_base64(row[i]):
						row[i] = base64.b64decode(row[i]).decode("utf-8")
				log_lines.append(row)
		return log_lines

	def is_base64(self, s):
		try:
			decoded_string = base64.b64decode(s).decode("utf-8")
			if self.encode(decoded_string) == s:
				return True
			else:
				return False
		except:
			return False