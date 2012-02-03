import pygame
import numpy as np
import random as rndm

max_wander_rotation = 15    #degrees
maximum_seek_distance  = 65 #pixels
minimum_avoid_distance = 200 #pixels


def seek(agent, target_position, time_passed_seconds):
    """
    Kinematic Seek Behavior
    Calculate a vector from the agent to the target_position.  (Towards target.)
    """
      
    seek_vector = target_position - agent.position
    normalized_seek_vector = seek_vector / np.sqrt(np.dot(seek_vector, seek_vector))
    agent.move(normalized_seek_vector, time_passed_seconds) 


def flee(agent, target_position, time_passed_seconds):
    """
    Kinematic Flee Behavior
    Calculate a vector from the target_position to the agent.  (Away from target.)
    """
    
    flee_vector = agent.position - target_position
    normalized_flee_vector = flee_vector / np.sqrt(np.dot(flee_vector, flee_vector))
    agent.move(normalized_flee_vector, time_passed_seconds)
    

def avoid(agent, target_position, time_passed_seconds):
    """
    Kinematic Avoid Behavior
    Flee only if my target is close to me (as defined by minimum_avoid_distance).
    """
    
    
    #distance_tuple is an array containing: [x dist. to target, y dist. to target] 
    distance_tuple = target_position - agent.position   
    distance_to_target = np.sqrt(np.dot(distance_tuple, distance_tuple))
    
    if distance_to_target < minimum_avoid_distance:
        flee(agent, target_position, time_passed_seconds)
    
    
    

def arrive(agent, target_position, time_passed_seconds):
    """
    Kinematic Arrive Behavior
    Seek only if my target is too far from me (as defined by maximum_seek_behavior).
    """
  
    arrive_vector = target_position - agent.position
    distance_to_target = np.sqrt(np.dot(arrive_vector, arrive_vector))
    normalized_seek_vector = arrive_vector / distance_to_target
    
    if distance_to_target > maximum_seek_distance:
        agent.move(normalized_seek_vector, time_passed_seconds)
    
    


def wander(agent, time_passed_seconds):
    """
    Kinematic Wander Behavior
    Slightly adjust your direction randomly and move about.
    """
    
    if (np.array_equal(agent.velocity, np.zeros(2))): #if the agent has no velocity
        acceleration_vector = np.array([random_binomial(),random_binomial()]) #go to the right
        agent.move(acceleration_vector, time_passed_seconds)
    
    else:
        rotation_degrees = max_wander_rotation * random_binomial()
        wander_vector = rotate_vector_counterclockwise(agent.velocity, rotation_degrees)
        normalized_wander_vector = wander_vector / np.sqrt(np.dot(wander_vector, wander_vector))
        agent.move(normalized_wander_vector, time_passed_seconds)
        
    pass
    

def rotate_vector_counterclockwise(vector, angle_in_degrees):
    print angle_in_degrees
    angle_in_radians = (angle_in_degrees / 180) * np.pi
    
    sine_of_angle   = np.sin(angle_in_radians)
    cosine_of_angle = np.cos(angle_in_radians)
    
    transformation_matrix = np.array([
                                      [cosine_of_angle, -sine_of_angle],
                                      [sine_of_angle,  cosine_of_angle]
                                     ])

    
    rotated_vector = np.linalg.solve(transformation_matrix, vector)
    
    print vector
    print 'was transformed to'
    
    
    return rotated_vector
    

def random_binomial():
    return rndm.random() - rndm.random()




