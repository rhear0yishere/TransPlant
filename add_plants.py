from peewee import *
from models import Plant

plants = [{"image": "static/Abutilon.jpg",
           "species": "Abutilon",
           "watering": 3,
           "light": 4,
           "Difficulty": 1
           },
          {"image": "static/african-daisy.jpg",
           "species": "African Daisies",
           "watering": 3,
           "light": 4,
           "Difficulty": 2
           },
          {"image": "static/Aloe.jpg",
           "species": "Aloe Vera",
           "watering": 3,
           "light": 4,
           "Difficulty": 3
           },
          {"image": "static/Crocus.jpg",
           "species": "Crocus",
           "watering": 3,
           "light": 4,
           "Difficulty": 1
           },
          {"image": "static/Cyclamen.jpg",
           "species": "Cyclamen",
           "watering": 3,
           "light": 4,
           "Difficulty": 2
           }
          ]
Plant.insert_many(plants).execute()
