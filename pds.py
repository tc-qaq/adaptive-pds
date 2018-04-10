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
    for line in fo1.readlines():
        term = line.strip().split(' ');
        station_data.append([float(term[0]),float(term[1])]);
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
#     for i in range(0,4500):
#         samples.append([dataset[i][2],dataset[i][3]]);
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

def add_coverage_attr(station_data,coverage_file):
    fr = open(coverage_file,'r',encoding='utf-8');
    index = 0;
    for line in fr.readlines():
        station_data[index].append(float(line));
        index += 1;
    
def add_ebt_attr(station_data,ebt_file):
    fr = open(ebt_file,'r',encoding='utf-8');
    index = 0;
    for line in fr.readlines():
        station_data[index].append(float(line));
        index += 1;

#def add_com_attr(station_data,name_file,name2id_file,id2label_file):
def add_com_attr(station_data,name_file,id2label_file):
    fr1 = open(name_file,'r',encoding='utf-8');
    #fr2 = open(name2id_file,'r',encoding='utf-8');
    fr3 = open(id2label_file,'r',encoding='utf-8');
#     dict_name2id ={};
#     index = 0;
#     for line in fr2.readlines():
#         term = line.strip().split(",");    
#         index += 1;
#         if (index > 1 ):
#             dict_name2id[term[1]] = term[0];
    dict_id2label ={};
    index = 0;
    for line in fr3.readlines():
        term = line.strip().split(',');
        index += 1;
        if (index > 1):
            dict_id2label[term[0]] = term[1];
                
    index = 0;
    for line in fr1.readlines():
        term = line.strip().split('-')     
#         labelA = dict_id2label[ dict_name2id[term[0]] ]; 
#         labelB = dict_id2label[ dict_name2id[term[1]] ];
        labelA = dict_id2label[ term[0] ]; 
        labelB = dict_id2label[ term[1] ]; 
        if(labelA == labelB):
            station_data[index].append(labelA+'-'+labelB);
        else:
            station_data[index].append(labelA+'-'+labelB);
        index += 1;

def remove_coverage(samplers,samplers_index,all_data):    
    len_samplers = len(samplers);
    for i in range(0,len_samplers):
        maxC = -1;  index_j = 0;  temp_c = samplers[i][2][0];        
        len_j = len(samplers_index[i]);
        for j in range(0,len_j):
            j = j + random.randint(0,int(len_j/10));
            if(j >= len_j):
                break;
            tbd = samplers_index[i][j];                  
            c = tbd[2][0];
            if(temp_c > c and maxC < temp_c - c):               
                maxC = temp_c - c;
                index_j =j;            
        if(index_j == 0):
            continue;
        print(samplers_index[i][index_j]);
        temp = samplers[i];
        samplers[i] = samplers_index[i][index_j];
        samplers_index[i][index_j] = temp;        
        
def increase_ebt(samplers,samplers_index,all_data):
    len_samplers = len(samplers);
    for i in range(0,len_samplers):
        minE = -1;  index_j = 0;  temp_e = samplers[i][2][1];        
        len_j = len(samplers_index[i]);
        for j in range(0,len_j):
            j = j + random.randint(0,int(len_j/10));
            if(j >= len_j):
                break;
            tbd = samplers_index[i][j];                  
            e = tbd[2][1];
            if(temp_e < e and minE < e - temp_e):               
                minE = e - temp_e;
                index_j =j;            
        if(index_j == 0):
            continue;
        print(samplers_index[i][index_j]);
        temp = samplers[i];
        samplers[i] = samplers_index[i][index_j];
        samplers_index[i][index_j] = temp;
        
        
def calcDistribution(samplers,all_data):
    interConnect = [];
    for item in all_data:
        if(type(item) != list):
            continue;
        if(item[7] != '0'):
            interConnect.append(item[7]);
    interConnect1 = [];
    for item in samplers:
        if(type(item) != list):
            continue;
        if(item[2][2] != '0'):
            interConnect1.append(item[2][2]);
    l1 = interConnect;
    l2 = [];
    [l2.append(i) for i in l1 if not i in l2];
    com_list= [];
    ori_dis = [];  
    sam_dis = [];  
    dict_con2index = {};
    index = 0;
    for item in l2:
        dict_con2index[item] = index;
        com_list.append(item);
        ori_dis.append(0);
        sam_dis.append(0);
        index += 1;    
    for item in interConnect:
        index = dict_con2index[item];
        ori_dis[index] += 1;
    for item in interConnect1:
        index = dict_con2index[item];
        sam_dis[index] += 1;
    
    ori_pre = [];
    sam_pre = [];
    ori_sum = sum(ori_dis);
    sam_sum = sum(sam_dis);
    for item in ori_dis:
        ori_pre.append(item/ori_sum);
    for item in sam_dis:
        sam_pre.append(item/sam_sum);
    adjust = [];
    for i,j in zip(ori_pre,sam_pre):
        ad = int((i-j)*sam_sum);
        adjust.append(ad);
    dict_adjust = {};
    for i,j in zip(com_list,adjust):
        dict_adjust[i] = j;
    sum1 = 0;
    for key in dict_adjust.keys():
        sum1 += dict_adjust[key];
    print(sum1);
    return dict_adjust;
    
def abjustInterConnectInCommunity(samplers,samplers_index,all_data,dict_adjustC):
    len_samplers = len(samplers);
    for i in range(0,len_samplers):
        temp_adjustC = samplers[i][2][2];
        if(temp_adjustC not in dict_adjustC):
            continue;
        temp_C = dict_adjustC[temp_adjustC];
        adjustC = '';
        C = 0;
        index_j = 0;
        if(temp_C == 0):
            continue;      
        elif(temp_C > 0):
            min = 100;
            len_j = len(samplers_index[i]);
            for j in range(0,len_j):
                j = j + random.randint(0,int(len_j/10));
                if(j >= len_j):
                    break;
                tbd = samplers_index[i][j];
                ajustC = tbd[2][2];
                if(ajustC not in dict_adjustC):
                    continue;
                C = dict_adjustC[ajustC];
                if(C < 0 and min > C):
                    min = C;
                    index_j =j;          
            
            if(index_j == 0):
                continue;
            temp = samplers[i];
            samplers[i] = samplers_index[i][index_j];
            samplers_index[i][index_j] = temp;
            dict_adjustC.update(temp_adjustC=temp_C-1);
            dict_adjustC.update(adjustC=C+1);
        else:
            max = -100;
            len_j = len(samplers_index[i]);
            for j in range(0,len_j):
                j = j + random.randint(0,int(len_j/10));
                if(j >= len_j):
                    break;
                tbd = samplers_index[i][j];
                ajustC = tbd[2][2];
                if(ajustC not in dict_adjustC):
                    continue;
                C = dict_adjustC[ajustC];
                if(C > 0 and max < C):
                    max = C;
                    index_j =j;          
            
            if(index_j == 0):
                continue;
            temp = samplers[i];
            samplers[i] = samplers_index[i][index_j];
            samplers_index[i][index_j] = temp;
            dict_adjustC.update(temp_adjustC=temp_C+1);
            dict_adjustC.update(adjustC=C-1);
             
# iteator
#   object: maintain the constraint community distribution,
#           high betweenness,line length distribution,
#   manner: set the seq and max Iters to replace the point
def ite_op(sampling_data,sampling_index,all_data,seq,max_iteration):    
    iterations = 0;
    while (iterations <= max_iteration):
        iterations += 1;
        for k in seq:
            if (k == 0):                
                remove_coverage(sampling_data,sampling_index,all_data);
            elif(k ==  1):
                increase_ebt(sampling_data,sampling_index,all_data);
            else:
                dict_adjust = calcDistribution(sampling_data,all_data);
                abjustInterConnectInCommunity(sampling_data,sampling_index,all_data,dict_adjust);
            
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
                    
                    samples_index[indexI][indexJ].append([itemS[5],itemS[6],itemS[7]]);
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
            dict_stations[term[0]] = term[1];
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
w_size = 200;   w_fre = 10;
ori_file = 'data/shenzhen/taxi_w2v'+str(w_size)+str(w_fre)+'2D';

name_file    = ori_file+ '_name.txt';
pos_file     = ori_file+      '.txt';
label_file   = ori_file+'_label.txt';
coverage_file= ori_file+'_coverage.txt';
ebt_file     = ori_file+'_ebt.txt';

#labels_file = 'data/All_data_community.csv';
#id2com_file = 'data/year-data/2016_Com.csv';

id2com_file = 'data/shenzhen/SZ_Com.csv';

pds_r = 10;seq = [2];max_iteration = 10;

sam_file = 'data/shenzhen/sampling/taxi_w2v' + str(w_size)+str(w_fre)+'2D_MCpds'+str(pds_r);

samples_pos_file   = sam_file +'.txt';
samples_name_file  = sam_file +'_name.txt';
samples_label_file = sam_file +'_label.txt';

# read points
station_data = readData(pos_file);
#kde for adptive sampling
kde = kde_fun(station_data);
#sampling
gene_data = copy.deepcopy(station_data);
samples, samples_index  = generate_points(kde,gene_data,station_data,pds_r);

add_coverage_attr(station_data,coverage_file);
add_ebt_attr(station_data,ebt_file);
#add_com_attr(station_data, name_file, labels_file, id2com_file);
add_com_attr(station_data, name_file, id2com_file);
labelData(samples,samples_index,station_data);
print('begin ite_op');
ite_op(samples, samples_index, station_data, seq, max_iteration);


#write data
print('number of samplers',len(samples));
generate_data(samples,station_data,name_file,samples_pos_file,samples_name_file);
#samples_label(labels_file,samples_name_file,samples_label_file);
samples_label(id2com_file,samples_name_file,samples_label_file);
print("end!");
# display
display(samples);

