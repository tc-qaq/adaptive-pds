from MulticoreTSNE import MulticoreTSNE as TSNE
import random
import math
import pygame # draw point
import numpy as np  
from scipy import stats  
import copy
from pygame import display


def cos_angle(x1,y1,x2,y2):
    if(x1 == x2):
        return math.sin(math.pi/2);
    else:
        k = (y2 - y1)/(x2 - x1);
        angle = math.atan(k);
        return math.cos(angle);
    
def line_length(x1,y1,x2,y2):
    x = x1 - x2;
    y = y1 - y2;
    return math.sqrt(x*x + y*y);

def read_pos_Data(localPath):
    file_object = open(localPath)
    try:
        all_the_text = file_object.read()
        raw = all_the_text.split('\n')
        if(raw[len(raw)-1]==''):
            print('yes')
            raw = raw[0:len(raw)-1]
        for index in range(len(raw)):
            raw[index] = raw[index].strip().split(' ')
            for sub_ind in range(len(raw[index])):
                raw[index][sub_ind] = float(raw[index][sub_ind])
    finally:
        file_object.close()
    return raw

def list2nda(list_raw):
    embeddings = [];

    for i in range(len(list_raw)):
        embeddings.append(list_raw[i]);
        
    return np.array(embeddings);

def tsne_output(highD_data,output_file):
    tsne=TSNE(metric='cosine',n_iter=2000,perplexity=50,learning_rate=400,n_jobs=4)
    data_tsne = tsne.fit_transform(highD_data)
    
    fw = open(output_file,'w',encoding="utf-8");
    fw.write(str(len(data_tsne))+" 2 \n");
    for line in data_tsne:
        fw.write(str(line[0])+" "+str(line[1])+"\n");
    print("end!")
    fw.close();
    return data_tsne;
    
    return data_tsne;

def generate_dict(dic_name):
    fr = open(dic_name,'r',encoding='utf-8');
    dict_stations = {};
    index = 0;
    for line in fr.readlines():
        term = line.strip().split(",");    
        index += 1;
        if (index > 1 ):
            dict_stations[term[1]] = term[0];
    return dict_stations;

def generate_dict1(dic_name):
    fr = open(dic_name,'r',encoding='utf-8');
    dict_stations = {};
    index = 0;
    for line in fr.readlines():
        term = line.strip().split(",");    
        index += 1;
        if (index > 1 ):
            dict_stations[term[0]] = term[1]+','+term[2];
    return dict_stations;

def name2geo(name_file,diction_name2id,diction_id2geo):
    fr = open(name_file,'r',encoding='utf-8');
    line_name = [];
    for line in fr.readlines():
        term = line.strip().split('-');
        line_name.append([term[0],term[1]]);
    index = 0;
    geos = [];
    for line in line_name:
        x = diction_id2geo[ diction_name2id[line[0]] ];
        y = diction_id2geo[ diction_name2id[line[1]] ];
        termx = x.strip().split(',');
        termy = y.strip().split(',');
        geos.append([float(termx[0]),float(termx[1]),float(termy[0]),float(termy[1])]);
        index +=1;
        print(float(index/1000));
    return geos;

def tsne_geo_semantic(name_file,dict_name2id,dict_id2loc,sem_file,geo_tsne_file,geo_sem_file):
    # geo data + angle,length to tsne for 2D data
    dict_bike = generate_dict(dict_name2id);
    dict_loc  = generate_dict1(dict_id2loc);
     
    raw = name2geo(name_file,dict_bike,dict_loc);
    for i in range(0,len(raw)):
        p = raw[i];
        angleV  = cos_angle(p[0],p[1],p[2],p[3]);
        length = line_length(p[0],p[1],p[2],p[3]);
        raw[i].append(angleV * 40);
        raw[i].append(length);    
    vec_list = list2nda(raw);
    print(vec_list.ndim);
    tsne_geo =  tsne_output(vec_list, geo_tsne_file);
    # geo_semantic data to tsne for 2D data
    
    tsne_geo = read_pos_Data(geo_tsne_file);     
    raw = read_pos_Data(sem_file);    
    print(len(raw));
    print(len(tsne_geo));
    for i in range(0,len(raw)):
        raw[i].append(tsne_geo[i][0]);
        raw[i].append(tsne_geo[i][1]);
    del(raw[0]);
    vec_list = list2nda(raw);
    tsne_geo_sem =  tsne_output(vec_list,geo_sem_file);
    print(len(tsne_geo_sem));
    return tsne_geo_sem;
    
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
        x = station_data[index][0];
        y = station_data[index][1];
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
    return (ix, iy);

def generate_points(kde_function,dataset,radius):
    samples = [];
    active_list = [];  
#     for i in range(0,4500):
#         samples.append([dataset[i][2],dataset[i][3]]);
    len_s = len(dataset);
    # Choose a point randomly in the domain.
    initial_point = (0, 0);
    
    i  = int(random.random()*len_s);
    ix = dataset[i][2];
    iy = dataset[i][3];   
    initial_point = (ix, iy);
    samples.append(initial_point);
    dataset.pop(i);
    active_list.append(initial_point);
        
    while len(active_list) > 0:
        # Choose a random point from the active list.
        p_index = random.randint(0, len(active_list) - 1);
        random_p = active_list[p_index];
        
        found = False;        
        # Generate up to k points chosen uniformly at random from dataset
        k = 30
        for it in range(k):
            minimum_dist = float(kde_function(np.array(random_p))) * radius;
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
                while (index < len(dataset)):
                    ix = dataset[index][2];
                    iy = dataset[index][3];
                    if(distance(pn, (ix,iy))< minimum_dist):
                       del(dataset[index]);
                    index+=1;
                found = True;
                print(str(len(samples)) + " :" + str(len(dataset)) + "-" + str(minimum_dist));
                break
        
        if not found:
            active_list.remove(random_p);
            if(len(samples)>6000):
                print(len(active_list));
    # Print the samples in a form that can be copy-pasted into other code.
    print("There are %d samples:" % len(samples))
    for point in samples:
        print("\t{\t%08f,\t%08f\t}," % (point[0], point[1])) 
    return samples;

def generate_uniform_points(minimum_dist,dataset):
    samples = [];
    active_list = [];  
    len_s = len(dataset);
    i  = int(random.random()*len_s);
    ix = dataset[i][2];
    iy = dataset[i][3];   
    initial_point = (ix, iy);
    samples.append(initial_point);
    dataset.pop(i);
    active_list.append(initial_point);
        
    while len(active_list) > 0:
        # Choose a random point from the active list.
        p_index = random.randint(0, len(active_list) - 1);
        random_p = active_list[p_index];
        
        found = False;        
        # Generate up to k points chosen uniformly at random from dataset
        k = 30
        for it in range(k):
            
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
                while (index < len(dataset)):
                    ix = dataset[index][2];
                    iy = dataset[index][3];
                    if(distance(pn, (ix,iy))< minimum_dist):
                       del(dataset[index]);
                    index+=1;
                found = True;
                print(str(len(samples)) + " :" + str(len(dataset)) + "-" + str(minimum_dist));
                break
        
        if not found:
            active_list.remove(random_p);
            print(len(active_list));
    # Print the samples in a form that can be copy-pasted into other code.
    print("There are %d samples:" % len(samples))
    for point in samples:
        print("\t{\t%08f,\t%08f\t}," % (point[0], point[1])) 
    return samples;

def labelData(samples,station_data):
    index = 0;
    for item1 in station_data:
        for item2 in samples:
            if(item1[2] == item2[0] and item1[3] == item2[1]):
                station_data[index][4] = 1;
        index +=1;

def generate_data(w2v_name_file,samples_pos_file,samples_name_file):
    fo  = open(w2v_name_file,'r',encoding="utf-8");
    fw1 = open(samples_pos_file,'w',encoding="utf-8");
    fw2 = open(samples_name_file,'w',encoding="utf-8");
    output_data =[];
    index = 0;
    for line in fo.readlines():
        station_data[index].append(line);
        index +=1;
    for item in station_data:
        if(item[4] == 1):
            output_data.append(item);
    fw1.write(str(len(output_data)) + " 2\n")
    for item in output_data:
        fw1.write(str(item[0])+ " "+str(item[1])+"\n");
        fw2.write(item[5]);
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
    fw.close();
    l1 = label_list;
    l2 = [];
    [l2.append(i) for i in l1 if not i in l2] 
    print(len(l2));
    print(l2);

def geo_station2sem_staion(samples_name_file,pos_file,name_file,samples_pos1_file):
    fo1 = open(samples_name_file,'r',encoding="utf-8");
    fo2 = open(name_file,'r',encoding="utf-8");
    fo3 = open(pos_file,'r',encoding="utf-8");
    fw = open(samples_pos1_file,'w',encoding="utf-8");
    all_names = [];
    sampler_n = [];
    all_pos   = [];
    
    for line in fo2.readlines():
        all_names.append(line);
    for line in fo1.readlines():
        sampler_n.append(line);
    index = 0;
    for line in fo3.readlines():
        index += 1;
        if(index > 1):
            term = line.strip().split(' ');
            all_pos.append([term[0],term[1]]);
    fw.write(str(len(sampler_n))+' 2\n');
    index = 0
    for item1 in all_names:
        for item2 in sampler_n:
            if(item1 == item2):
                fw.write(all_pos[index][0] +' '+ all_pos[index][1] + '\n');
        index += 1;
    fw.close();
    print('end!');
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
labels_file        = 'data/All_data_community.csv';
dict_id2loc  = 'data/coord.txt';

w_size = 100;   w_fre = 10;
name_file = 'data/bike_w2v'+str(w_size)+str(w_fre)+'2D_name.txt';
pos_file = 'data/bike_w2v'+str(w_size)+str(w_fre)+'2D.txt';
label_file= 'data/bike_w2v'+str(w_size)+str(w_fre)+'2D_label.txt';

pds_r = 0.01;
geo_tsne_file      = 'data/sampling/bike_w2v'+str(w_size)+str(w_fre)+'geo_tsne'+'.txt';
geo_sem_file       = 'data/sampling/bike_w2v'+str(w_size)+str(w_fre)+'geo_sem_tsne'+'.txt';

samples_pos_file   = 'data/sampling/bike_w2v'+str(w_size)+str(w_fre)+'2D_samping'+str(pds_r)+'.txt';
samples_pos1_file  = 'data/sampling/bike_w2v'+str(w_size)+str(w_fre)+'2D_samping'+str(pds_r)+'_sem.txt';
samples_name_file  = 'data/sampling/bike_w2v'+str(w_size)+str(w_fre)+'2D_samping'+str(pds_r)+'_name.txt';
samples_label_file = 'data/sampling/bike_w2v'+str(w_size)+str(w_fre)+'2D_samping'+str(pds_r)+'_label.txt';
#tsne geo + semantic  for sampling
station_data = tsne_geo_semantic(name_file, labels_file, dict_id2loc, pos_file,geo_tsne_file,geo_sem_file);
station_data = readData(geo_sem_file);
#sampling
gene_data = copy.deepcopy(station_data);
samples   = generate_uniform_points(pds_r,gene_data);
labelData(samples,station_data);
generate_data(name_file,samples_pos_file,samples_name_file);
samples_label(labels_file,samples_name_file,samples_label_file);
geo_station2sem_staion(samples_name_file,pos_file,name_file,samples_pos1_file);
# display
display(samples);
