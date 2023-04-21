import openai, os

openai.api_key = os.environ.get('OPENAIAPIKEY')

promptentrada="dime un haiku sobre la lluvia"
response = openai.Completion.create(
  model="text-davinci-003",
  prompt=promptentrada,
  max_tokens=2000,
  temperature=0.6
)
print(response.choices[0].text)
