from random import random
class map:
   """
   store the car's position, update status
   and decide where to go next
   """
   def  __init__(self):
       self.pos = 4
       self.decide()

   # make a choice based on current position
   def decide(self):
      if self.pos == 1:
         if random() > 0.5:
            self.choice = "l"
         else:
            self.choice = "s"

      elif self.pos == 2:
         rand = random()
         if rand > 0.66:
            self.choice = "l"
         elif rand < 0.66 and rand > 0.33:
            self.choice = "s"
         else:
            self.choice = "r"

      elif self.pos == 3:
         if random() > 0.5:
            self.choice = "l"
         else:
            self.choice = "r"

      else:
         if random() > 0.5:
            self.choice = "r"
         else:
            self.choice = "s"

   # get new pos based on current pos and action
   def transition(self):
      action = self.choice
      if self.pos == 1:
         if action == "s":
            self.pos = 1
         else:
            self.pos = 2

      elif self.pos == 2:
         self.pos = 3

      elif self.pos == 3:
         if action == "l":
            self.pos = 1
         else:
            self.pos = 4

      else:
         if action == "r":
            self.pos = 2
         else:
            self.pos = 4

   # action taken, update status
   def update(self):
       action = self.choice
       self.transition()
       self.decide()
       return action

   # get position
   def get_pos(self):
      return self.pos
