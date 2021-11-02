#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Oct 29 09:39:11 2021

@author: gabriel
"""
import matplotlib.pyplot as plt
#%% Data analysis

data_file = "dataset.txt"
my_data  = []
with open(data_file, "r") as my_file:
    for line in my_file:
        line = line.split()
        my_data.append([int(i) for i in line])


# my_data element : id id start_time end_time

#%% Intercontacts duration along time

my_start_times = []
my_intercontact_duration = []
for data in my_data:
    start_time = data[2]
    end_time = data[3]
    my_start_times.append(start_time)
    my_intercontact_duration.append(end_time - start_time)

plt.scatter(my_start_times, my_intercontact_duration)
plt.ylabel("intercontact duration")
plt.xlabel("time")
plt.title("Evolution of intercontact duration along time")

#%% Average and variance
my_average = 0
for intercontact in my_intercontact_duration:
    my_average += intercontact
my_average /= len(my_intercontact_duration)
print(f"Average intercontact duration {my_average}")
my_variance = 0
for intercontact in my_intercontact_duration:
    my_variance += pow(intercontact - my_average, 2)
my_variance /= len(my_intercontact_duration)
print(f"Variance of intercontact duration {my_variance}")

#%% Intercontact duration distribution
plt.hist(my_intercontact_duration, 300)
plt.xlim(-100, 7500)
plt.xlabel("Intercontact duration")
plt.ylabel("Frequency")
plt.title("Global intercontact duration distribution")

#%% Intercontact duration distribution individual
indiv_duration_dist = []
indiv = 1
for data in my_data:
    if data[0] == indiv:
        indiv_duration_dist.append(data[3] - data[2])
plt.hist(indiv_duration_dist, 300)
plt.xlabel("Intercontact duration")
plt.ylabel("Frequency")
plt.title("Individual intercontact duration distribution")

#%% time dependency
plt.scatter(my_intercontact_duration[0: len(my_intercontact_duration) - 1], my_intercontact_duration[1:])
plt.title("Lag plot of intercontact duration")