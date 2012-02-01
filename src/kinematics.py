#@PydevCodeAnalysisIgnore
import pygame
import numpy as np

'''
    Kinematic Seek Behavior
'''
def seek(avatar, target_position, time_passed_seconds):
    seek_vector = target_position - avatar.position
    normalized_seek_vector = seek_vector / np.sqrt(np.dot(seek_vector, seek_vector))
    avatar.move(normalized_seek_vector, time_passed_seconds) 
    pass

def flee(avatar, target_position, time_passed_seconds):
    flee_vector = avatar.position - target_position
    normalized_flee_vector = flee_vector / np.sqrt(np.dot(flee_vector, flee_vector))
    avatar.move(normalized_flee_vector, time_passed_seconds)