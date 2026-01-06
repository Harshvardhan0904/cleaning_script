import logging
import os
import re
import warnings
import numpy as np
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
from pandas.api.types import is_numeric_dtype, is_string_dtype

warnings.filterwarnings('ignore')

if not os.path.exists("logs"):
    os.makedirs("logs")

logging.basicConfig(
    filename='logs/data_cleaning.log',  
    filemode='a',                        
    format='%(asctime)s - %(levelname)s - %(message)s',
    level=logging.INFO                    
)

class DataCleaner:
    def __init__(self,data):
        self.df = data

    def cleaning_data(self):

        # remove duplicates
        

        # format column names
        self.df.columns = [col.lower().strip().replace(" ","_") for col in self.df.columns]

        # detect date + id columns
        date_col = [col for col in self.df.columns if re.search(r"date", col)]
        id_col = [col for col in self.df.columns if re.search(r"id", col)]

        # convert all date columns safely 
        try:
            for col in date_col:
                self.df[col] = pd.to_datetime(self.df[col], errors="coerce")
                logging.info("Converted date(object) to date(date)")
        except:
            logging.error("Unable to convert to date column")

        # ---- Shape ----
        print(f"\n---- Shape ----\n{self.df.shape}\n")

        # ---- Null % ----
        print("---- Null % ----")
        for col in self.df.columns:
            print(f"{col}: {self.df[col].isnull().mean()*100:.2f}%")
        
        for col in self.df.columns:
            if is_numeric_dtype(self.df[col]):
                
                mean_val = self.df[col].mean()
                self.df[col] = self.df[col].fillna(mean_val)
                logging.info(f"Filled null val for: {col} with: {mean_val}")
                
            elif is_string_dtype(self.df[col]):
                
                mode_val = self.df[col].mode()[0] if not self.df[col].mode().empty else ""
                self.df[col] = self.df[col].fillna(mode_val)
                logging.info(f"Filled null val for: {col} with: {mode_val}")
                
            else:
                # date or boolean etc
                self.df[col] = self.df[col].fillna(method='ffill')
                logging.info(f"Filled null val for: {col} with: ffill")

        # ---- Duplicate values count per column ----
        print("\n---- Duplicate Count ----")
        for col in self.df.columns:
            print(f"{col}: {self.df[col].duplicated().sum()}")
            
        self.df = self.df.drop_duplicates()
        logging.info("Removed duplicate values")
        
        #----------computing Null-------------------------
        
        cat_col = self.df.select_dtypes("object").columns.to_list()
        numeric_col = self.df.select_dtypes("number").columns.to_list()
        
        for col in self.df.columns:
            if col in cat_col and self.df[col].isnull().sum()>0:
                self.df[col] = self.df[col].fillna(self.df[col].mode()[0])
                
            elif col in numeric_col and self.df[col].isnull().sum()>0:
                self.df[col] = self.df[col].fillna(self.df[col].median())
            
            else:
                self.df[col] = self.df[col].fillna(0) #You can add condition for treating date col null
                #self.df[col] = self.df[col].ffill().bfill() <-- use this for date col

            
        

        # ---- Stats ----
        print("\n---- Stats (Numeric only) ----")
        print(self.df.describe(include='number'))

        # ---- IQR for numeric columns ----
        num_cols = self.df.select_dtypes(include=[np.number]).columns
        print(num_cols)

        print("\n---- IQR Values ----")
        for idx,col in enumerate(num_cols):
            if col not in date_col and col not in id_col:
                q1 = self.df[col].quantile(0.25)
                q3 = self.df[col].quantile(0.75)
                iqr = q3 - q1
                print(f"\nColumn: {col}\nQ1: {q1}\nQ3: {q3}\nIQR: {iqr}")
        

        return df

    def graph_plot(self):
        
        numeric_col = self.df.select_dtypes("number").columns.to_list()
        cat_col = self.df.select_dtypes("object").columns.to_list()
        
        fig,ax = plt.subplots(1,len(numeric_col),figsize=(25,8))
        print("---------------Numerical columns------------------")
        for i,c in enumerate(numeric_col):
            sns.histplot(self.df[c], kde=True,ax=ax[i],color='blue')
            ax[i].set_title(f"{c}")
            ax[i].set_ylabel("Count",labelpad=-5)
        plt.show()
        
        fig,ax = plt.subplots(1,len(cat_col),figsize=(25,8))
        print("---------------Categorical columns------------------")
        for i,c in enumerate(cat_col):
            sns.histplot(self.df[c], kde=True,ax=ax[i],color='red')
            ax[i].set_title(f"{c}")
            ax[i].set_ylabel("Count",labelpad=-5)
            ax[i].tick_params(axis='x', rotation=45)
        
        print("----------------Scatter plot numeric column----------------------")
        if len(numeric_col)>2:
            fig,ax = plt.subplots(1,len(numeric_col),figsize=(25,6))
            for i in range(len(numeric_col)-1):
                ax[i].scatter(self.df[numeric_col[i]],self.df[numeric_col[i+1]],color='blue')
                ax[i].set_xlabel(numeric_col[i])
                ax[i].set_ylabel(numeric_col[i+1],labelpad=-10)
            plt.tight_layout()
            plt.show()
        
        print("----------------Scatter plot categorical column----------------------")

        if len(cat_col) > 2:
            fig, ax = plt.subplots(1, len(cat_col)-1, figsize=(25,6))  # len(cat_col)-1 because you loop like that
            for i in range(len(cat_col)-1):
                ax[i].scatter(self.df[cat_col[i]], self.df[cat_col[i+1]],
                              color='orange', edgecolor='black')
                ax[i].set_xlabel(cat_col[i])
                ax[i].set_ylabel(cat_col[i+1], labelpad=-10)
                ax[i].tick_params(axis='x', rotation=45)  # rotate x ticks
                ax[i].tick_params(axis='y', rotation=0)   # optional for y ticks

            plt.tight_layout()  # <-- tight_layout BEFORE show
            plt.show()
