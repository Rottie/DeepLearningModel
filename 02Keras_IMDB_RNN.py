
# coding: utf-8

# In[12]:


#步驟 1: 資料處理
#1A:讀取 IMdb資料集目錄

from keras.datasets import imdb
from keras.preprocessing import sequence
from keras.preprocessing.text import Tokenizer

#建立 rm_tag 函數移除文字中的 html tag
import re
def rm_tags(text):
    re_tag = re.compile(r'<[^>]+>')
    return re_tag.sub('',text)

#建立 read_files函數讀取 1MDb 檔案目錄
import os
def read_files(filetype):
    path = "C:/pythonwork/Keras/data/aclImdb/"
    file_list = []
    
    positive_path = path + filetype +"/pos/"
    for f in os.listdir(positive_path):
        file_list += [positive_path+f]
    
    negative_path = path + filetype +"/neg/"
    for f in os.listdir(negative_path):
        file_list += [negative_path+f]
    
    print('read',filetype,'files:',len(file_list))
    
    all_labels = ([1] * 12500 + [0] * 12500)
    all_texts = []
    
    for fi in file_list:
        with open(fi,encoding ='utf8') as file_input:
            all_texts += [rm_tags(" ".join(file_input.readlines()))]
    
    return all_labels,all_texts




# In[13]:


#1B.測試是否已經被讀取

#讀取訓練資料
y_train,train_text=read_files("train")

#讀取測試資料
y_test,test_text=read_files("test")


# In[14]:


#1C.建立 token 詞典

token=Tokenizer(num_words=3800)                            #詞典大小
token.fit_on_texts(train_text)

#1D. 將 [影評文字] 轉換成 [數字 list]

x_train_seq = token.texts_to_sequences(train_text)
x_test_seq  = token.texts_to_sequences(test_text)

#1E.截長補短讓所有 [數字 list] 長度都是 100

x_train=sequence.pad_sequences(x_train_seq, maxlen=380)
x_test =sequence.pad_sequences(x_test_seq , maxlen=380)


# In[15]:


#步驟 2:建立模型
#2A.將 Embedding 層將 [數字 list]  轉換為 [向量 list]

from keras.models import Sequential
from keras.layers.core import Dense,Dropout,Activation
from keras.layers.embeddings import Embedding
from keras.layers.recurrent import SimpleRNN

model=Sequential()

model.add(Embedding(output_dim=32,
                   input_dim=3800,                     # 維度 等於 詞典大小
                   input_length=380))

model.add(Dropout(0.35))

#2B.建立 RNN 層 (16 個神經元)
model.add(SimpleRNN(units=16))

#2C. 建立隱藏層 (256 個神經元)
model.add(Dense(units=256,activation='relu'))
model.add(Dropout(0.35))
          
#2D. 建立輸出層(1 個神經元)
model.add(Dense(units=1,activation='sigmoid'))


# In[16]:


#步驟 3: 查看模型的摘要
model.summary()


# In[17]:


#步驟 4:訓練模型
#4A.定義訓練方式

model.compile(loss='binary_crossentropy',
             optimizer='adam',
             metrics=['accuracy'])

#4B.開始訓練

train_history =model.fit(x_train,y_train,batch_size=100,
                        epochs=10,verbose=2,
                        validation_split=0.2)




# In[18]:


#步驟 5 評估模型準確率

scores = model.evaluate(x_test,y_test, verbose=1)
scores [1]


# In[19]:


#步驟6:進行預測
#6A.執行預測

predict= model.predict_classes(x_test)


# In[20]:


#步驟 6:查看測試資料預測結果
#7A.建立 display_test_Sentiment 函數

SentimentDict={1:'正面的',0:'負面的'}
def display_test_Sentiment(i):
    print(test_text[i])
    print('label真實值:',SentimentDict[y_test[i]],
         '預測結果:',SentimentDict[predict_classes[i]])



#7B.顯示第 2筆預測結果

display_test_Sentiment(2)

