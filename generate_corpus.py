#encoding = 'utf-8'
import datetime


#ori data format
#TRIP ID,START TIME,STOP TIME,BIKE ID,TRIP DURATION,------4
#FROM STATION ID,FROM STATION NAME,TO STATION ID,TO STATION NAME,---8
#USER TYPE,GENDER,BIRTH YEAR,FROM LATITUDE,FROM LONGITUDE,--13
#FROM LOCATION,TO LATITUDE,TO LONGITUDE,TO LOCATION,-- 17
#Boundaries - ZIP Codes,Zip Codes,Community Areas,Wards

#bike_data.txt format
#START TIME,BIKE ID,FROM STATION ID,TO STATION ID

#bike_coord.txt format
#FROM STATION ID,FROM LATITUDE,FROM LONGITUDE
def generate_coord(fr_name,fw_name):
    fw = open(fw_name,'w',encoding='utf-8'); 
    index = 0;    
    with open(fr_name) as f:        
        while True: 
            index+=1;
            temp_data = f.readline();          
            if not temp_data:
                break;
            term = temp_data.strip().split(',');
            if(len(term) > 10):
                if(index == 1):
                    fw.write(term[5]+","+term[12]+term[13]+"\n");
                    continue;
                source = int(term[5]);
                target = int(term[7])
                if(source >= target):
                    temp = source;
                    source = target;
                    target = temp;
                fw.write(term[5]+","+term[12]+term[13]+"\n");
                print(index/100000);
    fw.close();

def generate_coord1(fr_name,fw_name):
    fw = open(fw_name,'w',encoding='utf-8');
    
    coords = [];
    for i in range(0,630):
        coords.append(str(i)+',');
     
    index = 0;    
    with open(fr_name) as f:        
        while True: 
            index+=1;
            temp_data = f.readline();          
            if not temp_data:
                break;
            term = temp_data.strip().split(',');
            if(index > 1):
                term = temp_data.strip().split(',');
                temp_index = int(term[0]);
                coor = term[1].strip().split('-');
                if(coords[temp_index] == str(temp_index)+','):
                    coords[temp_index] += (coor[0]+',-'+coor[1]);
                print(index/100000);
    for line in coords:
        if(line != ''):
            fw.write(line+'\n');
    fw.close();

def generate_data(fr_name,fw_name):
    fw = open(fw_name,'w',encoding='utf-8'); 
    index = 0;    
    with open(fr_name) as f:        
        while True: 
            index+=1;
            temp_data = f.readline();          
            if not temp_data:
                break;
            term = temp_data.strip().split(',');
            if(len(term) > 10):
                if(index == 1):
                    fw.write(term[1]+","+term[3]+","+term[5]+","+term[7]+"\n");
                    continue;
                source = int(term[5]);
                target = int(term[7])
                if(source >= target):
                    temp = source;
                    source = target;
                    target = temp;
                fw.write(term[1][0:10]+","+term[3]+","+str(source)+","+str(target)+"\n");
                print(index/100000);
    fw.close();

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
def generate_dict_id2_name(dict_name):
    fr = open(dict_name,'r',encoding='utf-8');
    dict_stations = {};
    index = 0;
    for line in fr.readlines():
        term = line.strip().split(",");    
        index += 1;
        if (index > 1 ):
            dict_stations[term[0]] = term[1];
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

def generate_corpus(fr_name,fw_name,dict_bike):
    fw = open(fw_name,'w',encoding='utf-8'); 
    
    bike_traj = [];
    for i in range(0,6000):
        bike_traj.append('');
    
    index = 0;    
    with open(fr_name) as f:        
        while True: 
            index+=1;
            temp_data = f.readline();          
            if not temp_data:
                break;
            if(index > 1):
                term = temp_data.strip().split(',');
                temp_index = int(term[1]);
                bike_traj[temp_index] += (dict_bike[term[2]]+'-'+dict_bike[term[3]]+' ');
                print(index/100000);
    for line in bike_traj:
        if(line != ''):
            fw.write(line+'\n');
    fw.close();

def generate_corpus_month(fr_name,fw_name,dict_bike,month):
    fw = open(fw_name,'w',encoding='utf-8'); 
    
    bike_traj = [];
    for i in range(0,6000):
        bike_traj.append('');
        
    index = 0;    
    with open(fr_name) as f:        
        while True: 
            index+=1;
            temp_data = f.readline();          
            if not temp_data:
                break;
            if(index > 1):
                term = temp_data.strip().split(',');
                m = term[0].strip().split('/');
                if(m[2] == month):
                    temp_index = int(term[1]);
                    bike_traj[temp_index] += (dict_bike[term[2]]+'-'+dict_bike[term[3]]+' ');
                    print(index/100000);
    
    for line in bike_traj:
        if(line != ''):
            fw.write(line+'\n');
    fw.close();
    print('end!');



def generate_lines(line_file,fw_file,dict_name2id,dict_id2loc):
    fr = open(line_file, 'r', encoding='utf-8');
    fw = open(fw_file,'w',encoding='utf-8');
    line_name = [];
    for line in fr.readlines():
        term = line.strip().split('-');
        line_name.append([term[0],term[1]]);
    index = 0;
    for line in line_name:
        x = dict_id2loc[ dict_name2id[line[0]] ];
        y = dict_id2loc[ dict_name2id[line[1]] ];
        fw.write(x+','+y+'\n');
        index +=1;
        print(float(index/1000));

def statistical_line_fre(line_file,corpus_file,fw_file):
    fr1 = open(line_file,'r',encoding='utf-8');
    fr2 = open(corpus_file,'r',encoding='utf-8');
    fw  = open(fw_file,'w',encoding='utf-8');
    dict_line2index = {};
    line_fre = [];
    names = [];
    index = 0;    
    for item in fr1.readlines():
        dict_line2index[item[:-1]] = index;
        line_fre.append(0);
        names.append(item[:-1]);
        index += 1;   
    
    for line in fr2.readlines():
        term = line.strip().split(' ');
        for item in term:
            line_fre[ dict_line2index[item] ] +=1;
    for item in line_fre:
        fw.write(str(item) + '\n');
    fw.close();
    
#Main program
fr_name = 'ori_data/Divvy_Trips.csv';
fw_name = 'data/bike_data.csv';
fw1_name = 'data/bike_corpus.txt';
fw2_name = 'data/bike_corpus_month_16.txt';
fw_fre = 'data/line_fre_month_16.txt';

dict_name2id = 'data/All_data_community.csv';
dict_id2loc  = 'data/coord.txt';
coord_name = 'data/pre_coord.txt';
coord_name1 = 'data/coord.txt';
line_file = 'data/bkike_w2v1001D_name.txt';
line1_file = 'data/year-data/bike_w2v20012D_name.txt';
location_file = 'data/line_loc.txt';

#generate_data(fr_name, fw_name);
#generate_coord(fr_name, coord_name);
#generate_coord1(coord_name,coord_name1);

#dict_bike = generate_dict(dict_name2id);
#dict_loc  = generate_dict1(dict_id2loc);
#dict_id2name = generate_dict_id2_name(dict_name2id);
#generate_lines(line_file, location_file, dict_bike, dict_loc);

#generate_corpus(fw_name, fw1_name,dict_bike);

#generate_corpus_month(fw_name,fw2_name,dict_id2name,'2016');

statistical_line_fre(line1_file, fw2_name, fw_fre);
