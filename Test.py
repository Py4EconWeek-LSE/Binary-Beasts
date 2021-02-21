#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Feb  4 11:57:58 2021

@author: samuelzhu
"""
class Zoo:
    def __init__(self, capacity = 0, animals = []):
        self.capacity = capacity
        self.animals = animals
    def add_animal(self,animal):
        self.animals.append(animal)
        
    
instance = Zoo(1, ['dog'])
instance.add_animal('cat')
print(instance.animals)
