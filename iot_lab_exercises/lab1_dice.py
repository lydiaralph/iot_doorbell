# Python 3

from random import randint

while True:
  
  dice1 = randint(1, 6)
  dice2 = randint(1, 6)

  if(dice1 == dice2):
    print("Double thrown!")
    print(dice1)

    if(dice1 == 6):
      exit("Both dice show 6. Exiting program...")
  else:
      print("No match")
      print("Dice 1: ", dice1)
      print("Dice 2: ", dice2)
      
