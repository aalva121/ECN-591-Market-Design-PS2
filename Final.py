#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Feb 22 23:53:31 2026

@author: alyssaalvarez
"""

import random

#Part 1: Market Setup

#Create sets and capacity
students = [f"i{j}" for j in range(1, 19)]
schools = ["s1", "s2", "s3"]
capacity = {school: 6 for school in schools}

print("Students:", students)
print("Schools", schools)
print("Capacities", capacity)

#Student Preferences
student_preferences = {}
for student in students:
    student_preferences[student] = random.sample(schools, len(schools))
    
print("\nStudent Preferences:")
for s in student_preferences:
    print(s, ":", student_preferences[s])
    
#School Priorities
school_priorities = {}
for school in schools:
    school_priorities[school] = random.sample(students, len(students))
    
print("\nSchool Priorities:")
for s in school_priorities:
    print(s, ":", school_priorities[s])

import pandas as pd

student_preferences_table = pd.DataFrame({
    "Student": sorted(students),
    "1st Choice": [student_preferences[s][0] for s in sorted(students)],
    "2nd Choice": [student_preferences[s][0] for s in sorted(students)],
    "3rd Choice": [student_preferences[s][0] for s in sorted(students)]
})

print(student_preferences_table)
print(student_preferences_table.to_latex(index=False))

school_priorities_table = pd.DataFrame({
    "School": schools,
    "Priority 1": [school_priorities[s][0] for s in schools],
    "Priority 2": [school_priorities[s][1] for s in schools],
    "Priority 3": [school_priorities[s][2] for s in schools],
    "Priority 4": [school_priorities[s][3] for s in schools],
    "Priority 5": [school_priorities[s][4] for s in schools],
})
       
print(school_priorities_table)
print(school_priorities_table.to_latex(index=False))
 
#Part 2: Matching Mechanism

#Deferred Acceptance (DA)
priority_rank = {}

for school in schools:
    priority_rank[school] = {
        student: rank
        for rank, student in enumerate(school_priorities[school])
    }
    
matches = {school: [] for school in schools}
new_proposal = {student: 0 for student in students}
unmatched = set(students)

while unmatched: 
    student = unmatched.pop()
    school = student_preferences[student][new_proposal[student]]
    new_proposal[student] += 1 
    matches[school].append(student)
    if len(matches[school]) > capacity[school]:
        matches[school].sort(key=lambda x: priority_rank[school][x])
        rejected = matches[school].pop()
        unmatched.add(rejected)
        
final_matching_DA = {}
for school in matches:
    for student in matches[school]:
        final_matching_DA[student] = school
        
print("\Final Matching DA:")
for student in sorted(final_matching_DA):
    print(student, "→", final_matching_DA[student])
    
#Immediate Acceptance (IA)
matches_IA = {school: [] for school in schools}
assigned = {}
unassigned = set(students)

for round_number in range(len(schools)):
    applications = {school: [] for school in schools}
    for student in unassigned:
        school = student_preferences[student][round_number]
        applications[school].append(student)
    
    for school in schools:
        candidates = matches_IA[school] + applications[school]
        candidates.sort(key=lambda x: priority_rank[school][x])
        accepted = candidates[:capacity[school]]
        matches_IA[school] = accepted
        rejected = set(candidates[capacity[school]:])
   
    new_unassigned = set()
    for school in schools:
        for student in matches_IA[school]:
            assigned[student] = school
    for student in students:
        if student not in assigned:
            new_unassigned.add(student)
    unassigned = new_unassigned
    
print("\Final Matching IA:")
for student in sorted(assigned):
    print(student, "→", assigned[student])
    
#Top Trading Cycles (TTCs)
def run_TTC(students, schools, capacity, students_preferences, school_priorities):
    remaining_students = set(students)
    remaining_capacity = capacity.copy()
    remaining_preferences = {
        s: list(student_preferences[s]) for s in students
    }

    matching = {}

    while remaining_students:
        points_student = {}
        for s in remaining_students:
            while remaining_preferences[s] and remaining_capacity[remaining_preferences[s][0]] == 0:
                remaining_preferences[s].pop(0)
            if remaining_preferences[s]:
                points_student[s] = remaining_preferences[s][0]
   
        points_school = {}
        for school in schools:
            if remaining_capacity[school] > 0:
                for candidate in school_priorities[school]:
                    if candidate in remaining_students:
                        points_school[school] = candidate
                        break
                
        visited = set()
        for s in list(remaining_students):
            if s in visited:
                continue
            path = []
            current = s
            while current not in path:
                path.append(current)
                school = points_student[current]
                if school not in points_school:
                    break
                current = points_school[school]
            if current in path:
                cycle_begins = path.index(current)
                cycle = path[cycle_begins:]
                for student_cycle in cycle:
                    assigned_school = points_student[student_cycle]
                    matching[student_cycle] = assigned_school
                    remaining_capacity[assigned_school] -= 1 
                remaining_students -= set(cycle)
                visited.update(cycle)
    return matching

matching_TTC = run_TTC(
    students,
    schools,
    capacity,
    student_preferences,
    school_priorities
)
    
print("\nFinal Matching TTC:")
for student in sorted(matching_TTC):
    print(student, "→", matching_TTC[student])


import pandas as pd

matching_mechanisms_table = pd.DataFrame({
    "Student": sorted(students),
    "DA": [final_matching_DA.get(s, "Unmatched") for s in sorted(students)],
    "IA": [assigned.get(s, "Unmatched") for s in sorted(students)],
    "TTC": [matching_TTC.get(s, "Unmatched") for s in sorted(students)]})

print(matching_mechanisms_table)

print(matching_mechanisms_table.to_latex(index=False))

#Part 3: Efficiency Analysis

#Deferred Acceptance (DA) - N=1000
def run_DA(students, schools, capacity, student_preferences, priority_rank):
    matches_newDA = {school: [] for school in schools}
    new_proposalDA = {student: 0 for student in students}
    unmatched_DA = set(students)
    
    while unmatched_DA: 
        student = unmatched_DA.pop()
        school = student_preferences[student][new_proposalDA[student]]
        new_proposalDA[student] += 1 
        matches_newDA[school].append(student)
        if len(matches_newDA[school]) > capacity[school]:
            matches_newDA[school].sort(key=lambda x: priority_rank[school][x])
            rejected_newDA = matches_newDA[school].pop()
            unmatched_DA.add(rejected_newDA)
    
    final_matching_newDA = {}
    for school in matches_newDA:
        for student in matches_newDA[school]:
            final_matching_newDA[student] = school
            
    return final_matching_newDA

#Immediate Acceptance (IA) - N=1000
def run_IA(studets, schools, capacity, student_preferences, priority_rank):
    matches_newIA = {school:[] for school in schools}
    assigned_newIA = {}
    unassigned_IA = set(students)
    round_number = 0
    
    while unassigned_IA and round_number < len(schools):
        applications_newIA = {school: [] for school in schools}
        for student in unassigned_IA:
            school = student_preferences[student][round_number]
            applications_newIA[school].append(student)
            
        for school in schools:
            candidates_newIA = matches_newIA[school] + applications_newIA[school]
            candidates_newIA.sort(key=lambda x: priority_rank[school][x])
            accepted_newIA = candidates_newIA[:capacity[school]]
            matches_newIA[school] = accepted_newIA
    
        assigned_newIA = {}
        for school in schools:
            for student in matches_newIA[school]:
                assigned_newIA[student] = school
        unassigned_IA = set(students) - set(assigned_newIA.keys())
        round_number += 1
    return assigned_newIA

#Top Trending Cyles (TTC) - N=1000
def run_TTC(students, schools, capacity, student_preferences, school_priorities):
    remaining_students_new = set(students)
    remaining_capacity_new = capacity.copy()
    remaining_preferences_new = {
        s: list(student_preferences[s]) for s in students
    }
    
    matches_newTTC = {}
    
    while remaining_students_new:
        
        points_student_new = {}
        for s in remaining_students_new:
            
            while (
                remaining_preferences_new[s]
                and remaining_capacity_new[remaining_preferences_new[s][0]]==0):
                remaining_preferences_new[s].pop(0)
                
            if remaining_preferences_new[s]:
                points_student_new[s] = remaining_preferences_new[s][0]
                
        points_school_new = {}
        
        for school in schools:
            if remaining_capacity_new[school] > 0:
                for s in school_priorities[school]:
                    if s in remaining_students_new:
                        points_school_new[school] = s
                        break
       
        visited_new = set()
        
        for s in list(remaining_students_new):
            if s in visited_new:
                continue
            path_new = []
            current_new = s
            while current_new not in path_new:
                path_new.append(current_new)
                school_TTCnew = points_student_new[current_new]
                if school_TTCnew not in points_school_new:
                    break
                current_new = points_school_new[school_TTCnew]
            if current_new in path_new:
                cycle_begins_new = path_new.index(current_new)
                cycle_new = path_new[cycle_begins_new:]
                for student in cycle_new:
                    assigned_school_TTC = points_student_new[student]
                    matches[student] = assigned_school_TTC
                    remaining_capacity_new[assigned_school_TTC] -= 1
            remaining_students_new -= set(cycle_new)
            visited_new.update(cycle_new)
    return matches_newTTC

#Create new student preferences and school priorities under N=1000
N = 1000

DA_rank = []
IA_rank = []
TTC_rank = []

for _ in range(N):
    student_preferences = {
        student: random.sample(schools, len(schools))
        for student in students
    }
    school_priorities = {
        school: random.sample(students, len(students))
        for school in schools
    }
    priority_rank = {
        school: {
            student: rank
            for rank, student in enumerate(school_priorities[school])
        }
        for school in schools
    }  
    matching_DA = run_DA(
        students,
        schools,
        capacity,
        student_preferences,
        priority_rank
    )
    matching_IA = run_IA(
        students,
        schools,
        capacity,
        student_preferences,
        priority_rank
    )
    matching_TTC = run_TTC(
        students,
        schools,
        capacity,
        student_preferences,
        school_priorities
    )
    
    for student in students: 
        assigned_school_DA = matching_DA[student]
        rank_DA = student_preferences[student].index(assigned_school_DA) + 1 
        DA_rank.append(rank_DA)
    for student in students:
        if student in matching_IA:
            assigned_school_IA = matching_IA[student]
            rank_IA = student_preferences[student].index(assigned_school_IA) + 1 
        else:
            rank_IA = len(schools) + 1
        IA_rank.append(rank_IA)
    for student in students:
        if student in matching_TTC:
            assigned_school_TTC = matching_TTC[student]
            rank_TTC = student_preferences[student].index(assigned_school_TTC) + 1 
        else:
            rank_TTC = len(schools) + 1
        TTC_rank.append(rank_TTC)
        
rank_table = pd.DataFrame({
    "Student": sorted(students),
    "DA_rank": [
        student_preferences[s].index(matching_DA[s]) + 1
        for s in sorted(students)
    ],
    "IA_rank": [
        student_preferences[s].index(matching_IA[s]) + 1
        if s in matching_IA else len(schools) + 1
        for s in sorted(students)
    ],
    "TTC_rank": [
        student_preferences[s].index(matching_TTC[s]) + 1
        if s in matching_TTC else len(schools) + 1
        for s in sorted(students)
    ]
})

print("\nRank of Assigned School")
print(rank_table)

print(rank_table.to_latex(index=False))
        
avg_DA = sum(DA_rank)/len(DA_rank)
avg_IA = sum(IA_rank)/len(IA_rank)
avg_TTC = sum(TTC_rank)/len(TTC_rank)

print(len(DA_rank), len(IA_rank), len(TTC_rank))

print("\nAverage Student Rank Across 1000 Simulations")
print(f"DA : {avg_DA:.3f}")
print(f"IA : {avg_IA:.3f}")
print(f"TTC : {avg_TTC:.3f}")

avg_table = pd.DataFrame({
    "Mechanism": ["Deferred Acceptance (DA)",
                  "Immediate Acceptance (IA)",
                  "Top Trading Cycles (TTCs)"],
    "Average Rank": [avg_DA, avg_IA, avg_TTC]
})

print("\nAverage Student Rank Across 1000 Simulations")
print(avg_table)

print(avg_table.to_latex(index=False))