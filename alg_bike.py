#encoding= utf-8
from gensim.models import  word2vec
from MulticoreTSNE import MulticoreTSNE as TSNE
import numpy as np
import logging
# 09/2016
# 5159 bikes 17.1MB
# 32k word types | 439k raw words
# min_count=5 15K,   min_count=10 10k    

# 2016 year
# 5748 bikes 140MB
# 54k word types | 3595k raw words
# min_count=5 35k,   min_count=10 27k

#3 years
# 64266 word types | 99929991 raw words
# min_count=5 45k, min_count=10 38k min_count=20 31k, min_count = 50 22k

def w2v(corpus,w_size,w_fre,pos_file,name_file,bikeModel):
    logging.basicConfig(format='%(asctime)s:%(levelname)s: %(message)s', level=logging.INFO)  
    sentences =word2vec.Text8Corpus(corpus,max_sentence_length=10000);  # loading   
    model =word2vec.Word2Vec(sentences, size=w_size,min_count=w_fre);  # train skip-gram model default window=5  
    print (model);    
    fo1 = open(pos_file,'w',encoding="utf-8");
    fo2 = open(name_file,'w',encoding="utf-8");    
    name_list =[];
    vec_list = [];
    for item in model.wv.vocab:
        name_list.append(item);
        vec_list.append(model.wv[item]);
        str_vec = "";
        for v in model.wv[item]:
            str_vec += str(v) + " ";
        fo1.write(str_vec+"\n");
        fo2.write(item+"\n")
    fo1.close();
    fo2.close();
    print(len(name_list));
    model.save(bikeModel)
    print("end!!!");
    
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
    labels = [];
    for i in range(len(list_raw)):
        labels.append(list_raw[i][0]);
        embeddings.append(list_raw[i][0:len(list_raw[i])-1]);
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

def tsne_bike(fr_file,fw_file):    
    raw = read_pos_Data(fr_file);
    vec_list = list2nda(raw);
    tsne_output(vec_list,fw_file);
      
def label_data(id2labels_file,names_file,output_file):
    fo2 = open(id2labels_file,'r',encoding='utf-8');
    fo3 = open(names_file,'r',encoding="utf-8");
    fw = open(output_file,'w',encoding="utf-8");        
    
    dict_id2label ={};
    index = 0;
    for line in fo2.readlines():
        term = line.strip().split(',');
        index += 1;
        if (index > 1):
            dict_id2label[term[0]] = term[1];
            
    label_list =[];
    for line in fo3.readlines():
        term = line.strip().split("-");
        labelA = dict_id2label[ term[0] ];
        labelB = dict_id2label[ term[1] ];        
        if(labelA == labelB):
            label = labelA;
        else:
            label = "-1";
        label_list.append(label);
        fw.write(label + "\n");
    print("end!");
    

#main program

#name2ids = "data/All_data_community.csv";
id2lables = "data/shenzhen/SZ_Com.csv";
corpus = "data/shenzhen/word_2_vec_undir.txt";
w_size = 200;
w_fre = 10;
gene_file = 'data/shenzhen/taxi_w2v'+str(w_size)+str(w_fre);
bike_model = gene_file+'.model';
pos_file = gene_file+'D.txt';
name_file = gene_file+'2D_name.txt';
pos2_file = gene_file+'2D.txt';
label_file= gene_file+'2D_label.txt';
# word2vec -> tsne ----blue noise sampling
#w2v(corpus, w_size, w_fre, pos_file, name_file,bike_model);
#label_data(id2lables,name_file,label_file);
#tsne_bike(pos_file, pos2_file);

