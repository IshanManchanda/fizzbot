import json

import requests

api = 'https://api.noopschallenge.com'


def start_interview():
	requests.get(api + '/fizzbot')
	requests.get(api + '/fizzbot/questions/1')
	answer = {'answer': 'Python'}
	return requests.post(api + '/fizzbot/questions/1', json=answer).json()


def try_answer(question_url, answer):
	return requests.post(api + question_url, json={'answer': answer}).json()


def get_answer(question):
	answer = []
	rules = {x['number']: x['response'] for x in question['rules']}
	divisors = sorted(rules.keys())
	print(rules)

	for num in question['numbers']:
		current_answer = []

		for divisor in divisors:
			if num % divisor == 0:
				current_answer.append(rules[divisor])

		if current_answer:
			answer.append(''.join(current_answer))
		else:
			answer.append(str(num))

	return ' '.join(answer)


def solve_question(question_url):
	print(f'Starting question: {question_url}')

	question = requests.get(api + question_url).json()

	answer = get_answer(question)
	print(f'Solution is: {answer}')

	response = try_answer(question_url, answer)
	if response['result'] == 'interview complete':
		print(json.dumps(response, indent=4))
		exit(0)

	elif response['result'] != 'correct':
		print('Hmmm, something doesn\'t seem right')
		print(f'Question URL: {question_url}')
		print('Question:', json.dumps(question, indent=4))
		print(f'Answer: {answer}')
		exit(0)

	return response['nextQuestion']


def main():
	print("Starting...")
	question_url = start_interview()['nextQuestion']
	print(f'Initial question URL is: {question_url}')

	while question_url:
		question_url = solve_question(question_url)


if __name__ == '__main__':
	main()
