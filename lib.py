import csv
import base64
import tiktoken
import shortuuid

encoding = tiktoken.encoding_for_model("gpt-3.5-turbo")

class DictArrayManager:
	def __init__(self):
		self.logfile = "log.csv"
		self.clear()
		
	def clear(self):
		self.array = []
		self.tokens = []
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
		while self.count() > num:
			self.array = self.array[1:]

	def serialize(self):
		import json
		return json.dumps(self.array)

	def deserialize(self, json_string):
		import json
		try:
			deserialized = json.loads(json_string)
			for item in deserialized:
				if set(item.keys()) != {'role', 'content'}:
					raise ValueError("Invalid dictionary format")
			self.array = deserialized
		except json.JSONDecodeError:
			raise ValueError("Invalid JSON string format")

	def log_latest(self):
		latest = self.array[-1]
		with open(self.logfile, mode='a', newline='') as log_file:
			csv_writer = csv.writer(log_file, delimiter=',', quotechar='"', quoting=csv.QUOTE_MINIMAL)
			csv_writer.writerow([self.sessionid, latest["role"], self.encode(latest["content"])])

	def encode(self, data):
		content_bytes = data.encode("utf-8")
		base64_byte = base64.b64encode(content_bytes)
		base64_string = base64_byte.decode("utf-8")
		return base64_string
