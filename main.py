import os
import rasa 
import nest_asyncio
from rasa.jupyter import chat

nest_asyncio.apply()

os.chdir("Project_data")
config = "config.yml"
training_files = "data/"
domain = "domain.yml"
output = "./"

print(config, training_files, domain, output)
model_path = rasa.train(domain, config, [training_files], output)
print(model_path)

# endpoints = 'endpoints.yml'
chat(model_path)