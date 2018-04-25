#encoding= utf-8
import random
import math
import pygame # draw point
import numpy as np
from scipy import stats
import copy

#station_data format
#pos_x pos_y nor_x nor_y isSampled coverage ebt com_label
#samples   format
#nor_x nor_y [coverage ebt com_label index_in_all  ]

def readData(w2v_file):
    station_data = [];
    fo1 = open(w2v_file,'r',encoding="utf-8");    
    index = 0;
    for line in fo1.readlines():
        term = line.strip().split(' ');
        if (index > 0):
            station_data.append([float(term[0]),float(term[1])]);
        index +=1;
    v1 = [x[0] for x in station_data];v2 = [x[1] for x in station_data]; 
    max1 = max(v1);min1 = min(v1);max2 = max(v2);min2 = min(v2);
    nor1 = max1 - min1;nor2 = max2 - min2;
    index = 0;
    for item in station_data:
        x = item[0];        y = item[1];
        station_data[index].append((x-min1)/nor1);
        station_data[index].append((y-min2)/nor2);
        station_data[index].append(0);
        index +=1;
    return station_data;
    
def distance(p1, p2):
    p_diff = (p2[0] - p1[0], p2[1] - p1[1]);
    return math.sqrt(math.pow(p_diff[0], 2) + math.pow(p_diff[1], 2));
    
def is_in_circle(p):
    #d = distance(p, (0, 0));
    if(p[0]<1 and p[0]> 0 and p[1]< 1 and p[1]>0):
        return True;
    else:
        return False;

def generate_random_point(o, r,dataset):
    # Generate random point form dataset
    i = int(random.random()*len(dataset));
    ix = dataset[i][2];
    iy = dataset[i][3];        
    return [ix, iy];

def kde_fun(data):
    data1 = [];               
    for item in data:
        data1.append([item[2],item[3]]);
    data1 = np.array(data1);
    values = data1.T;  
    kde = stats.gaussian_kde(values);
    return kde;

def generate_points(kde_function,dataset,oriset,radius):
    samples = [];
    samples_index = [];
    active_list = [];  
    len_s = len(dataset);
    # Choose a point randomly in the domain.
    i  = int(random.random()*len_s);
    ix = dataset[i][2];
    iy = dataset[i][3];   
    initial_point = [ix, iy];
    samples.append(initial_point);
    del(dataset[i]);
    # remove the adj of initial point
    minimum_dist = float(kde_function(np.array(initial_point)));
    minimum_dist = radius * 1/(minimum_dist * 1000)
    index = 0;
    points = [];
    while (index < len(dataset)):
        ix = dataset[index][2];
        iy = dataset[index][3];
        if(distance(initial_point, [ix,iy])< minimum_dist):
            points.append([ix,iy]);        
            del(dataset[index]);
        index+=1;
    samples_index.append(points);
    
    active_list.append(initial_point);        
    while len(active_list) > 0:
        # Choose a random point from the active list.
        p_index = random.randint(0, len(active_list) - 1);
        random_p = active_list[p_index];
        
        found = False;        
        # Generate up to k points chosen uniformly at random from dataset
        k = 30
        for it in range(k):
            minimum_dist = float(kde_function(np.array(random_p)));
            minimum_dist = radius * 1/(minimum_dist * 1000)
            pn = generate_random_point(random_p, minimum_dist,dataset);            
            fits = True;
            # TODO: Optimize.  Maintain a grid of existing samples, and only check viable nearest neighbors.
            for point in samples:
                if distance(point, pn) < minimum_dist:
                    fits = False;
                    break                    
            if fits:
                samples.append(pn);
                active_list.append(pn);
                index = 0;
                points = [];
                while (index < len(dataset)):
                    ix = dataset[index][2];
                    iy = dataset[index][3];
                    if(distance(pn, [ix,iy])< minimum_dist):
                        points.append([ix,iy]);
                        del(dataset[index]);                        
                    index+=1;
                samples_index.append(points);
                found = True;
                print(str(len(samples)) + " :" + str(len(dataset)) + "-" + str(minimum_dist));
                break;
        
        if not found:
            active_list.remove(random_p);
            print(len(active_list));
    # Print the samples in a form that can be copy-pasted into other code.
    #print("There are %d samples:" % len(samples))
    #for point in samples:
    #    print("\t{%08f,\t%08f}," % (point[0], point[1])) 
    
    return samples,samples_index;


def labelData(samples,samples_index,station_data):
    index = 0;
    for item1 in station_data:
        index2 = 0;
        for item2 in samples:            
            if(item1[2] == item2[0] and item1[3] == item2[1]):
                station_data[index][4] = 1;
                samples[index2].append([item1[5],item1[6],item1[7],index]);
                break;
            index2 += 1;                
        index +=1;

    for indexI in range(len(samples_index)):
        for indexJ in range(0,len(samples_index[indexI])):
            for itemS in station_data:
                item = samples_index[indexI][indexJ];
                if(item[0] == itemS[2] and item[1] == itemS[3]):
                    samples_index[indexI][indexJ].append([item1[5],item1[6],item1[7],index]);
                    break;

def generate_data(samples,station_data,w2v_name_file,samples_pos_file,samples_name_file):
    fo  = open(w2v_name_file,'r',encoding="utf-8");
    fw1 = open(samples_pos_file,'w',encoding="utf-8");
    fw2 = open(samples_name_file,'w',encoding="utf-8");
    output_data =[];
    index = 0;
    for line in fo.readlines():
        station_data[index].append(line);
        index +=1;
    for item1 in samples:
        for item in station_data:
            if(item[2] == item1[0] and item[3] == item1[1]):
                output_data.append(item);
    fw1.write(str(len(output_data)) + " 2\n")
    print(len(station_data),len(samples),len(output_data))

    for item in output_data:
        fw1.write(str(item[0])+ " "+str(item[1])+"\n");
        fw2.write(item[8]);
    fw1.close();
    fw2.close();

def samples_label(all_labels_file,samples_name_file,samples_label_file):
    fo1 = open(all_labels_file,'r',encoding="utf-8");
    fo2 = open(samples_name_file,'r',encoding="utf-8");
    fw = open(samples_label_file,'w',encoding="utf-8");
    
    dict_stations = {};
    index = 0;
    for line in fo1.readlines():
        term = line.strip().split(",");    
        index += 1;
        if (index > 1 ):
            dict_stations[term[1]] = term[2];
    label_list =[];
    for line in fo2.readlines():
        term = line.strip().split("-");
        if(dict_stations[term[0]] == dict_stations[term[1]]):
            label = dict_stations[term[0]];
        else:
            label = "-1";
        label_list.append(label);
        fw.write(label + "\n");
    print("end!");

    l1 = label_list;
    l2 = [];
    [l2.append(i) for i in l1 if not i in l2] 
    print(len(l2));
    print(l2);

def display(samples):
    pygame.init();
    screen = pygame.display.set_mode((500, 500));
    clock = pygame.time.Clock();
    while True:
        break_loop = False;
        clock.tick(60);    
        screen.fill((0,0,0));
        pygame.draw.circle(screen, (50, 50, 200), (250, 250), 250, 1);    
        for point in samples:
            lx = 250 + int((point[0]-0.5) * 250);
            ly = 250 + int((point[1]-0.5) * 250);
            pygame.draw.circle(screen, (255,255,255), (lx, ly), 2);
                 
        pygame.display.flip();
        if break_loop:
            break


#---------main program--------
#init data file
w_size = 200;   w_fre = 1;
name_file = 'data/year-data/bike_w2v'+str(w_size)+str(w_fre)+'2D_name.txt';
pos_file = 'data/year-data/bike_w2v'+str(w_size)+str(w_fre)+'2D.txt';
label_file= 'data/year-data/bike_w2v'+str(w_size)+str(w_fre)+'2D_label.txt';

pds_r = 50;
seq = [0,1,2];
max_iteration = 1;

labels_file = 'data/All_data_community.csv';
id2com_file = 'data/Bike_all_com_new.csv';
#coverage_file      = 'data/year-data/bike_w2v'+str(w_size)+str(w_fre)+'2D_coverage.txt';
#ebt_file           = 'data/year-data/bike_w2v'+str(w_size)+str(w_fre)+'2D_ebt.txt';

samples_pos_file   = 'data/year-data/sampling/bike_w2v'+str(w_size)+str(w_fre)+'2D_pds'+str(pds_r)+'.txt';
samples_name_file  = 'data/year-data/sampling/bike_w2v'+str(w_size)+str(w_fre)+'2D_pds'+str(pds_r)+'_name.txt';
samples_label_file = 'data/year-data/sampling/bike_w2v'+str(w_size)+str(w_fre)+'2D_pds'+str(pds_r)+'_label.txt';

# read points
station_data = readData(pos_file);
#kde for adptive sampling
kde = kde_fun(station_data);
#sampling
gene_data = copy.deepcopy(station_data);
samples, samples_index  = generate_points(kde,gene_data,station_data,pds_r);

labelData(samples,samples_index,station_data);

#write data
print('number of samplers',len(samples));
generate_data(samples,station_data,name_file,samples_pos_file,samples_name_file);
samples_label(labels_file,samples_name_file,samples_label_file);
print("end!");
# display
display(samples);

