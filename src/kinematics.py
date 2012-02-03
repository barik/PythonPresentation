import pygame
import numpy as np
import random as rndm

MAX_WANDER_ROTATION = 15    #degrees
MAXIMUM_SEEK_DISTANCE  = 65 #pixels
MINIMUM_AVOID_DISTANCE = 200 #pixels


def seek(agent, target_position, time_passed_seconds):
    """
    Kinematic Seek Behavior
    Calculate a vector from the agent to the target_position.  (Towards target.)
    """
      
    seek_vector = target_position - agent.position
    normalized_seek_vector = seek_vector / np.sqrt(np.dot(seek_vector, seek_vector))
    agent.update(normalized_seek_vector, time_passed_seconds) 


def flee(agent, target_position, time_passed_seconds):
    """
    Kinematic Flee Behavior
    Calculate a vector from the target_position to the agent.  (Away from target.)
    """
    
    flee_vector = agent.position - target_position
    normalized_flee_vector = flee_vector / np.sqrt(np.dot(flee_vector, flee_vector))
    agent.update(normalized_flee_vector, time_passed_seconds)
    

def avoid(agent, target_position, time_passed_seconds):
    """
    Kinematic Avoid Behavior
    Flee only if my target is close to me (as defined by MINIMUM_AVOID_DISTANCE).
    """
    
    
    #distance_tuple is an array containing: [x dist. to target, y dist. to target] 
    distance_tuple = target_position - agent.position   
    distance_to_target = np.sqrt(np.dot(distance_tuple, distance_tuple))
    
    if distance_to_target < MINIMUM_AVOID_DISTANCE:
        flee(agent, target_position, time_passed_seconds)
    

def arrive(agent, target_position, time_passed_seconds):
    """
    Kinematic Arrive Behavior
    Seek only if my target is too far from me (as defined by maximum_seek_behavior).
    """
  
    arrive_vector = target_position - agent.position
    distance_to_target = np.sqrt(np.dot(arrive_vector, arrive_vector))
    normalized_seek_vector = arrive_vector / distance_to_target
    
    if distance_to_target > MAXIMUM_SEEK_DISTANCE:
        agent.update(normalized_seek_vector, time_passed_seconds)
    
    

def wander(agent, time_passed_seconds):
    """
    Kinematic Wander Behavior
    Slightly adjust your direction randomly and update about.
    """
    
    if (np.array_equal(agent.velocity, np.zeros(2))): #if the agent has no velocity
        acceleration_vector = np.array([randomBinomial(),randomBinomial()]) #go to random direction
        agent.update(acceleration_vector, time_passed_seconds)
    
    else:
        rotation_degrees = MAX_WANDER_ROTATION * randomBinomial()
        wander_vector = rotateVectorCounterclockwise(agent.velocity, rotation_degrees)
        normalized_wander_vector = wander_vector / np.sqrt(np.dot(wander_vector, wander_vector))
        agent.update(normalized_wander_vector, time_passed_seconds)
        
    pass
    

def rotateVectorCounterclockwise(vector, angle_in_degrees):
    angle_in_radians = (angle_in_degrees / 180) * np.pi
    
    sine_of_angle   = np.sin(angle_in_radians)
    cosine_of_angle = np.cos(angle_in_radians)
    
    transformation_matrix = np.array([
                                      [cosine_of_angle, -sine_of_angle],
                                      [sine_of_angle,  cosine_of_angle]
                                     ])

    
    rotated_vector = np.linalg.solve(transformation_matrix, vector)
    
    return rotated_vector
    

def randomBinomial():
    return rndm.random() - rndm.random()




