#!/usr/bin/env python
# inference.py
import sys
import numpy as np
import robot


def Viterbi(all_possible_hidden_states,
            all_possible_observed_states,
            prior_distribution,
            transition_model,
            observation_model,
            observations):

    num_time_steps = len(observations)
    
    noinfo = robot.Distribution()
    for k in all_possible_hidden_states:
        noinfo[k] = 1.0
    
    epyx = {}
    for y in all_possible_observed_states:
        epyx[y] = robot.Distribution()
        for x in all_possible_hidden_states:
            v = observation_model(x)[y]
            if v != 0:
                epyx[y][x] = v
        epyx[y].renormalize()
    
    phiprime = [None] * len(observations)
    phiprime[0] = robot.Distribution(prior_distribution.copy())
    for i in range(1, len(observations)):
        phiprime[i] = robot.Distribution(noinfo.copy())
    for i in range(len(observations)):
        if observations[i] != None:
            for k in noinfo:
                phiprime[i][k] = phiprime[i][k] * epyx[observations[i]][k]
            phiprime[i].renormalize()
    for i in range(len(observations)):
        for k in noinfo:
            if phiprime[i][k] == 0:
                del phiprime[i][k]
    
    num_time_steps = len(observations)
    forward_messages = [None] * num_time_steps
    table = [None] * num_time_steps
    for i in range(num_time_steps):
        forward_messages[i] = robot.Distribution()
        table[i] = robot.Distribution()
    forward_messages[0] = noinfo.copy()
    for i in range(1,num_time_steps):
        mf = robot.Distribution(forward_messages[i-1].copy())
        for k in mf:
            mf[k] = mf[k] * phiprime[i-1][k] #fold
        for k in mf.keys():
            if mf[k] == 0:
                del mf[k]#fold
        mf.renormalize()
        for k in mf:
            nexf = transition_model(k)
            for kn in nexf:
                if forward_messages[i].get(kn,0) < nexf[kn] * mf[k]:
                    forward_messages[i][kn] = nexf[kn] * mf[k]
                    table[i][kn] = k
        forward_messages[i].renormalize()
        
    xt = robot.Distribution()
    for k in forward_messages[-1]:
        xt[k] = forward_messages[-1][k] * phiprime[-1].get(k,0)
    
    xmap = []
    maxval = max(xt.values())
    for k in xt:
        if xt[k] == maxval:
            x = k
    xmap.append(x)
    
    for i in range(1, num_time_steps):
        j = num_time_steps - i
        xpre = table[j][xmap[-1]]
        xmap.append(xpre)
    
    xmap.reverse()
    
    estimated_hidden_states = xmap

    return estimated_hidden_states



def inference(observations):
    use_graphics = False
    all_possible_hidden_states = robot.get_all_hidden_states()
    all_possible_observed_states = robot.get_all_observed_states()
    prior_distribution = robot.initial_distribution()

    print('Running Viterbi...')
    estimated_states = Viterbi(all_possible_hidden_states, all_possible_observed_states, prior_distribution, robot.transition_model, robot.observation_model, observations)
    print('Request handled.')
    print('Ready to infer robot behavior.')
    return estimated_states

table = {"stay":0, "right":4, "left":3, "up":1, "down":2}
reverse_table = {0:"stay", 4:"right", 3:"left", 1:"up", 2:"down"}
def translate(i):
    if i in table:
        return table[i]
    return i

def restore(i):
    return reverse_table[i]

def wrapped_infer(lst):
    observations = []
    for i in range(0,len(lst)-1,2):
        observations.append((lst[i],lst[i+1]))
    infer = inference(observations)
    result = []
    for state in infer:
        for entry in state:
            result.append(translate(entry))
    return result

