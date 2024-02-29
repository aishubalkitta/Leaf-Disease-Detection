import pandas as pd
import numpy as np
import cv2
import matplotlib.pyplot as plt
from matplotlib.pyplot import imshow
from tensorflow.keras.models import Model, load_model, Sequential
def predictor(img): 
    csv_path="C:\\Users\\Akshwarya\\Downloads\\disease_names.csv"
    model_path="C:\\Users\\Akshwarya\\Downloads\\EfficientNetB3-skin disease-83.83.h5"
    crop_image=False  
    class_df=pd.read_csv(csv_path)    
    img_height=int(class_df['height'].iloc[0])
    img_width =int(class_df['width'].iloc[0])
    img_size=(img_width, img_height)
    scale=class_df['scale by'].iloc[0] 
    try: 
        s=int(scale)
        s2=1
        s1=0
    except:
        split=scale.split('-')
        s1=float(split[1])
        s2=float(split[0].split('*')[1]) 
        print (s1,s2)
    print ('Model is getting loaded - this will take some time')
    model=load_model(model_path)
    index_list=[] 
    prob_list=[]
    cropped_image_list=[]
    good_image_count=0      
    if crop_image == True:
      status, img=crop(img)
    else:
      status=True
    if status== True:
      good_image_count +=1 
      img=np.array(img)
      img=cv2.resize(img, (300,300))         
      cropped_image_list.append(img)
      img=img*s2 - s1
      img=np.expand_dims(img, axis=0)
      p= np.squeeze (model.predict(img))           
      index=np.argmax(p)            
      prob=p[index]
      index_list.append(index)
      prob_list.append(prob)
    if good_image_count==1:
      class_name= class_df['class'].iloc[index_list[0]]
      probability= prob_list[0]
      img=cropped_image_list [0] 
      plt.title(class_name, color='blue', fontsize=16)
      plt.axis('off')
      plt.imshow(img)
      return class_name, probability
    elif good_image_count == 0:
      return None, None
    most=0
    for i in range (len(index_list)-1):
        key= index_list[i]
        keycount=0
        for j in range (i+1, len(index_list)):
            nkey= index_list[j]            
            if nkey == key:
                keycount +=1                
        if keycount> most:
            most=keycount
            isave=i             
    best_index=index_list[isave] 
    psum=0
    bestsum=0
    for i in range (len(index_list)):
        psum += prob_list[i]
        if index_list[i]==best_index:
            bestsum += prob_list[i]  
    img= cropped_image_list[isave]/255  
    class_name=class_df['class'].iloc[best_index]
    plt.title(class_name, color='blue', fontsize=16)
    plt.axis('off')
    plt.imshow(img)
    return class_name, bestsum