# -*- coding: utf-8 -*-
"""
Created on Tue Oct 11 14:42:14 2016

@author: Eric Schmidt
"""

import numpy as np
import matplotlib.pyplot as plt
import csv
import os
import glob
    
def main():
    
    ts = 12
#    extra = "_angle" # Note the underscore that should be added
    extra = ""
    
#==============================================================================
# Particles
#==============================================================================
    
    particle_file = glob.glob("%s/../Output/particle_matrix%s_%d.csv"%(
                                os.getcwd(),extra,ts))
    particle_file = particle_file[0]
    
    with open(particle_file, "rt") as inf:
        reader = csv.reader(inf, delimiter=',')
        next(reader, None)  # skip the headers
        stuff = list(reader)
        
        '''
        Particle #                          0
        Steps                               1
        Kill Event                          2
        Charge                              3
        Starting Global x-Position (mm)	 4
        Starting Global y-Position (mm)	 5
        Starting Global z-Position (mm)     6
        Ending Calorimeter x (mm)           7
        Ending Calorimeter y (mm)           8
        Starting Momentum (GeV/c)           9
        Ending Momentum (GeV/c)             10
        Delta Momentum (GeV/c)              11
        Steps Inside Short Quad             12
        Distance Inside Short Quad (cm)	 13
        Total # of Photons Released         14
        # of Detectable Photons Released	 15
        Steps Inside Long Quad              16
        Distance Inside Long Quad (cm)	 17
        Total # of Photons Released         18
        # of Detectable Photons Released	 19
        Steps Inside Standoff Plate         20
        Distance Inside Standoff Plate (cm) 21
        Total # of Photons Released         22
        # of Detectable Photons Released	 23
        Steps Inside HV Standoff            24
        Distance Inside HV Standoff (cm)	 25
        Total # of Photons Released         26
        # of Detectable Photons Released	 27
        Steps Inside HV Standoff Screws     28
        Distance Inside HV Standoff Screws	 29
        Total # of Photons Released         30
        # of Detectable Photons Released	 31
        dt                                  32
        Pair Produced (0 or 1)              33
        Kill Timestamp                      34
        x Calorimeter Angle                 35
        y Calorimeter Angle                 36
        Total Calorimeter Angle             37
        '''
        
        N_particles = len(stuff)
        i = 0
        
        # [Kill event,dt,charge]
        particle = np.zeros((N_particles,3),dtype=object)
        
        # [x,y,z] Global muon position at decay
        x = np.zeros((N_particles,3))       # (mm) 
        
        # [Starting, Ending, Difference]
        p = np.zeros((N_particles,3))       # (GeV/c)
        
        # Calorimeter contact position [x,y]
        x_cal = np.zeros((N_particles,2))
        
        # Inside matter [steps, distance (cm),total photons, HE photons]
        
        in_sqel = np.zeros((N_particles,4))
        in_dqel = np.zeros((N_particles,4))
        in_sp = np.zeros((N_particles,4))
        in_so = np.zeros((N_particles,4))
        in_sos = np.zeros((N_particles,4))
                
        # Counters
        
        cal_con_particle = 0        # Calorimeter contact
        so_contact = 0              # HV standoff contact
        sos_contact = 0             # HV standoff screw contact
        sqel_contact = 0            # Single quad contact
        dqel_contact = 0            # Double quad contact
        sp_contact = 0              # Standoff plate contact
        cal_con_particle_so = 0     # Calorimeter and HV standoff contact
        
        for row in stuff:
            
            particle[i,0] = row[2]
            particle[i,1] = row[32]
            particle[i,2] = row[3]
            
            if row[2] == "Calorimeter Contact":
                cal_con_particle = cal_con_particle + 1
            
            x[i,0] = row[4]         
            x[i,1] = row[5]         
            x[i,2] = row[6]
            
            x_cal[i,0] = row[7]
            x_cal[i,1] = row[8]
            
            p[i,0] = row[9]
            p[i,1] = row[10]
            p[i,2] = row[11]
            
            in_sqel[i,0] = row[12]
            in_sqel[i,1] = row[13]
            in_sqel[i,2] = row[14]
            in_sqel[i,3] = row[15]
            
            if float(row[12]) > 0:
                sqel_contact = sqel_contact + 1
            
            in_dqel[i,0] = row[16]
            in_dqel[i,1] = row[17]
            in_dqel[i,2] = row[18]
            in_dqel[i,3] = row[19]
            
            if float(row[16]) > 0:
                dqel_contact = dqel_contact + 1
            
            in_sp[i,0] = row[20]
            in_sp[i,1] = row[21]
            in_sp[i,2] = row[22]
            in_sp[i,3] = row[23]
            
            if float(row[20]) > 0:
                sp_contact = sp_contact + 1
            
            in_so[i,0] = row[24]
            in_so[i,1] = row[25]
            in_so[i,2] = row[26]
            in_so[i,3] = row[27]
            
            if float(row[24]) > 0:
                so_contact = so_contact + 1
            
            in_sos[i,0] = row[28]
            in_sos[i,1] = row[29]
            in_sos[i,2] = row[30]
            in_sos[i,3] = row[31]
            
            if float(row[28]) > 0:
                sos_contact = sos_contact + 1
            
            if row[2] == "Calorimeter Contact" and \
                (float(row[24]) > 0 or float(row[28]) > 0):
                cal_con_particle_so = cal_con_particle_so + 1
                
            i = i + 1
            
#==============================================================================
# Data Processing
#==============================================================================
                
    total_particles = len(x)
    total_photons = sum(in_sqel[:,2]) + sum(in_dqel[:,2]) + \
                    sum(in_sp[:,2]) + sum(in_so[:,2]) + sum(in_sos[:,2])
#    total_in_matter = sum(in_sqel[:,1]) + sum(in_dqel[:,1]) + \
#                      sum(in_sp[:,1]) + sum(in_so[:,1] + sum(in_sos[:,1]))
                      
#    print('Total muon decays: %d'%total_particles)
    print('Total particles: %d'%total_particles)
#    print('Total distance in matter: %0.3f cm'%(total_in_matter))
    print('Total photons: %d'%total_photons)
    print('Total single quad contacts: %d'%sqel_contact)
    print('Total double quad contacts: %d'%dqel_contact)
    print('Total standoff plate contacts: %d'%sp_contact)
    print('Total HV standoff contacts: %d'%so_contact)
    print('Total HV standoff screw contacts: %d'%sos_contact)
    print('Total particle calorimeter contacts: %d'%cal_con_particle)
    print('Total SO/SO screw contacts that hit the calorimeter: %d'\
            %cal_con_particle_so)
#==============================================================================
#     Plotting
#==============================================================================
        
    n = 0
    
    plt.figure(n)
    n = n + 1
    
    # Convert string to float
    x_cal = np.array(x_cal, dtype = float)
    
    # Remove 'zero' rows
    x_cal = x_cal[np.any(x_cal != 0, axis = 1)]
    
    ax = plt.subplot(1,1,1)
    ax.scatter(x_cal[:,0]*100, x_cal[:,1]*100,
               color='g',
               s = 0.7,
               label='Contact Points')
    ax.plot([-11.25,11.25],[7,7],'k-',label='Perimeter')
    ax.plot([-11.25,11.25],[-7,-7],'k-')
    ax.plot([-11.25,-11.25],[-7,7],'k-')
    ax.plot([11.25,11.25],[-7,7],'k-')
    plt.xlim(-24,24)
    plt.ylim(-15.5,15.5)
    ax.grid(True)
    ax.legend(bbox_to_anchor=(1.33,1.11))
    ax.set_title("Calorimeter Contact Position")
    ax.set_xlabel('x-Position (cm)')
    ax.set_ylabel('y-position (cm)')
    plt.axis('equal') # Prevents a skewed look
    
if __name__ == '__main__':

    main()