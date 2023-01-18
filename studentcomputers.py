# used the priority queue implementation from my Lab 08 

import random
from specs.weapons import Railgun, Laser, Torpedo
from specs.ships import Fighter, Destroyer, Cruiser, Battleship


def set_targets(myFleet, enemyFleet):
  '''
  This should ensure that each weapon of the attacker's ships 
  points towards a valid target (ship) of the defender.
  This function must only change weapons's target property!
  The target property must be a ship in the enemy Fleet.
  '''
  # TODO Phase 3

  # do not shoot at destroyed ships
  valid_ships = []
  for ship in enemyFleet.ships:
    if ship.hull > 0:
      valid_ships.append(ship)
    
  # shoot at a random target
  for ship in myFleet.ships:
    for weapon in ship.weapons:
      if len(valid_ships) > 0:
        weapon.target = random.choice(valid_ships)
        
      else:
        # to prevent weapons shoot on anihalated fleets
        weapon.target = None

  # creates a priority queue to sort the hull values of the enemy fleet's ships 
  sorted_hull = PriorityQueue()
  for ship in valid_ships:
    hull_health = ship.hull 
    sorted_hull.enqueue(hull_health, ship)

  # creates a priority queue to sort the armor values of the enemy fleet's ships 
  sorted_armor = PriorityQueue()
  for ship in valid_ships:
    armor_health = ship.armor 
    sorted_armor.enqueue(armor_health, ship)
  
  # creates a priority queue to sort the shield values of the enemy fleet's ships 
  # creates a separate priority queue for ships in the enemy's fleet with no shields left 
  no_shields = PriorityQueue()
  sorted_shields = PriorityQueue()
  for ship in valid_ships:
    # enqueue ships with shield health to a priority queue 
    if ship.shields > 0:
      shield_health = ship.shields 
      sorted_shields.enqueue(shield_health,ship)
    # enqueues ships with no shield to their own queue 
    else:
      shield_health = 0
      no_shields.enqueue(shield_health,ship)

  # creates a priority queue to organize the ships from smallest to largest 
  ships_queue = PriorityQueue()
  for ship in valid_ships:
    # enqueues enemy fighter ships with the priority of 1
    if isinstance(ship,Fighter):
      ships_queue.enqueue(1, ship)
    # enqueues enemy destroyer ships with the priority of 2
    elif isinstance(ship,Destroyer):
      ships_queue.enqueue(2,ship)
    # enqueues enemy cruiser ships with the priority of 3
    elif isinstance(ship,Cruiser):
      ships_queue.enqueue(3, ship)
    # enqueues enemy fighter ships with the priority of 4
    else: 
      ships_queue.enqueue(4, ship)

  # creates a queue that ranks the health of the enemy's ships from smallest to largest 
  health_queue = PriorityQueue()
  for ship in valid_ships:
    # calculates the health of each valid and enemy ship and enqueues them with their health as the priority 
    health = ship.hull + ship.armor + ship.shields
    health_queue.enqueue(health, ship)


  # loops through our own fleet and weapons within each ship in the fleet 
  for ship in myFleet.ships: 
    for weapon in ship.weapons: 
      
      # strategy 1: use Lasers to target ships with no shields
      if isinstance(weapon,Laser):
        # checks if there is data in the no_shields queue before dequeueing from it 
        if no_shields.__len__() > 0: 
          target_ship = no_shields.dequeue()
          weapon.target = target_ship

      # strategy 2: use Railguns to target ships with shields
      elif isinstance(weapon,Railgun):
        # checks if there is data in the sorted_shields queue before dequeueing from it 
        if sorted_shields.__len__() > 0: 
          target_ship = sorted_shields.dequeue()
          weapon.target = target_ship 
        
        # strategy #3: Use Railguns to target ships with very little hull 
        # checks if there is data in the sorted_hull queue before dequeueing from it 
        if sorted_hull.__len__() > 0:
          ship_hull_health = sorted_hull.dequeue()
          # checks if the hull of the ship is small (<100)
          if ship_hull_health.hull < 100:
            weapon.target = ship_hull_health

      # strategy 4: have small ships finish off low health targets while our battle ships do the heavy lifting
      if isinstance(ship, Fighter) or isinstance(ship, Destroyer):
        # checks if there is data in the health_queue queue before dequeueing from it 
        if health_queue.__len__() > 0:
          target_ship = health_queue.dequeue()
          # checks if the health of the target ship is less than 200 (considered to be low health)
          if (target_ship.hull + target_ship.armor + target_ship.shields) < 200:
            weapon.target = target_ship

      # strategy 5: ships target ships in their size first
      # each if statement checks if the enemy's ship and our ship are the same type 
      if ships_queue.__len__() > 0: 
        target_ship = ships_queue.dequeue()
        if isinstance(target_ship, Fighter) and isinstance(ship, Fighter):
          weapon.target = target_ship 
        elif isinstance(target_ship, Cruiser) and isinstance(ship, Cruiser):
          weapon.target = target_ship 
        elif isinstance(target_ship, Destroyer) and isinstance(ship, Destroyer):
          weapon.target = target_ship 
        else:
          weapon.target = target_ship
        

  # strategy 6: avoids firing at enemy ships with a higher point defense 
  # do not want to shoot torpedos at these ships as they have a high chance of shooting these down 
  for ship in valid_ships:
    # checks the point defense of the enemy's ship 
    if ship.pd > 0.66:
      weapon.target = None

    # strategy 7: use Torpedos  to target small ships with high evasion 
    if isinstance(ship,Fighter) and ship.evasion > 0.7:
      for weapon in ship.weapons: 
        if isinstance(ship,Torpedo):
          weapon.target = ship 
          weapon.shots_torpedo += 1
          if weapon.shots_torpedo > 3: 
            weapon.target = None

  # strategy 8: Our own strategy 
  # Since we have four battleships in our own composition, we are checking our own fleet and seeing if the ship is a battleship. If it is we are checking the health of the ship and if it less than zero we are adding it to our priority queue. We are then checking if the length of our queue is greater than 2 and if it is, then we are looping through our enemy's fleet and checking if they are using a fighter and if so we are targeting their fighter ship. 
  no_battleships = PriorityQueue()
  for ship in myFleet.ships:
    for weapons in ship.weapons: 
      if isinstance(ship,Battleship):
        health = ship.hull + ship.armor + ship.shields
        if health <= 0: 
          no_battleships.enqueue(health, ship)
          if no_battleships.__len__() >= 2:
            for ship in enemyFleet.ships:
              if isinstance(ship,Fighter):
                weapon.target = ship

class Queue:
    """Queue ADT implemented as a linked list (options for bounded and unbounded)."""

    def __init__(self, bound = None):
        """ Constructor for the Queue class """
        self.head = None
        self.tail = None 
        self.size = 0  
        self.bound = bound 
        
    def __len__( self ):
        """ Return the current size of the queue. """
        return self.size 

    def is_empty(self):
        """ Returns true if the queue is empty, false otherwise. """
        if self.size == 0: 
          return True
        else: 
          return False 

    def enqueue(self, item):
        """ Adds item to the front of the queue
      """
        if self.is_empty():
          node = Node(item, None)
          self.head = node 
          self.tail = node 
          self.size += 1 
        
        else: 
          node = Node(item, None)
          self.tail.next = node 
          self.tail = node 
          self.size += 1 

    def dequeue(self):
        """ DeQ and return item. If empty, return None. """
        if self.is_empty():
          return None
        else: 
          #set top as head node 
          top = self.head
          #move head to the next node
          self.head = self.head.next 
          self.size -= 1 
          #return top value
          return top.value 

    def peek(self):
        """ Return the item that would be dequeue'd next.
            If empty, return None. """
        if self.is_empty():
          return None
        else: 
          return self.head.value 
    
class Node:
  '''
  Node Class to help construct Queue ADT through a singily linked list
  '''
  def __init__(self, value, next):
    '''
    Constuctor for Node class
    Prameters:
      value; the item that represents the node
    '''
    self.value = value 
    self.next = next

class PriorityQueue(Queue):
    def __init__(self, priority = None):
      '''
      Constructor of the Priority Queue Class
      Inherits the constructor from the Queue class
      Parameters: 
        priority; the priority of the node 
      '''
      super().__init__()

    def enqueue(self, priority, item):
        '''
        Adds the item to the queue depending upon its priority 
        Parameters; 
          priority; the priority of the item being added 
          item; the item being added to the queue 
        Returns: N/A 
        '''
        #Creates node to be added
        node = PNode(priority, item)
        # If queue is empty set node as head and tail
        if self.is_empty():
            self.head = node
            self.tail = node
            self.size += 1
          
        #If new node has the lowest priority set new node as head
        elif (node.priority < self.head.priority):
            node.next = self.head
            self.head = node
            self.size += 1
        #If new node has largest priority set as tail
        elif (node.priority >= self.tail.priority):
            self.tail.next = node
            self.tail = node
            self.size += 1
        #If the priority is a middle level priority
        else:
            #set node holder as head
            node_holder = self.head
            # If the next item after the node holder is not None and the next node's priority is less than the current node's priority move node holder to next
            while node_holder.next != None and node_holder.next.priority <= node.priority:
                node_holder = node_holder.next
            #set node's next as node holder's next
            node.next = node_holder.next
            #set node holder's next as node
            node_holder.next = node 
            self.size += 1 


class PNode(Node):
  '''
  PNode Class to help construct the priority queue through a singly linked list
  Inherits the Node Class
  '''
  
  def __init__(self, priority, value):
    '''
    Constructor for the PNode class which inherits the constructor from the node class
    Parameters:
      priority; the priority of the node
      value; the items that represents the node
    '''
    super().__init__(value, next)
    self.priority = priority
    self.next = None


      

