# -*- coding: utf-8 -*-
"""
Created on Tue Jun 14 23:29:21 2022

@author: ht
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns 
import numpy as np 
import matplotlib.pyplot as plt
from datetime import datetime 
import matplotlib.path as mpath
import pymysql 
import streamlit as st
import plotly.graph_objects as go

# 동시 출력 
from IPython.core.interactiveshell import InteractiveShell
InteractiveShell.ast_node_interactivity = "all"

# 한글 폰트 설정
from matplotlib import font_manager, rc
font_name = font_manager.FontProperties(fname="c:/Windows/Fonts/malgun.ttf").get_name()
rc('font', family=font_name)

# DB 연동
connect=pymysql.connect(host='localhost',user='root',password='1234',
                        db='lcc_db',charset='utf8')
cur=connect.cursor(pymysql.cursors.DictCursor)
query1="SELECT * FROM lcc_db.plot1"
query2="SELECT * FROM lcc_db.plot2"

cur.execute(query1)
Data1=cur.fetchall()
Data1=pd.DataFrame(Data1)

cur.execute(query2)
Data2=cur.fetchall()
Data2=pd.DataFrame(Data2)


# Nemosis 기존 시각화 
def Nemosis_plot(df):
    plt.figure(figsize=(10,5))
    plt.bar(df['교체횟수'],df['교환비용'],color='blue',alpha=0.5,label='교환비용')
    plt.bar(df['교체횟수'],df['고장정비비용'],color='g',alpha=0.5,label='고장정비비용')
    plt.bar(df['교체횟수'],df['서비스지연비용'],color='y',alpha=0.4,label='서비스지연비용')
    plt.legend(loc='upper center')
    
    return plt.show()

# base line  (total cost 추가)
def base_plot(df):
    plt.figure(figsize=(10,5))
    plt.bar(df['교체횟수'],df['교환비용'],color='blue',alpha=0.5,label='교환비용')
    plt.bar(df['교체횟수'],df['고장정비비용'],color='g',alpha=0.5,label='고장정비비용')
    plt.bar(df['교체횟수'],df['서비스지연비용'],color='y',alpha=0.4,label='서비스지연비용')
    plt.plot(df['교체횟수'],df['총비용'],'r',linewidth=4,label='총비용')
    plt.legend(loc='upper center')
    
    return plt.show()

# pie chart
def list_mean(L):
    return sum(L)/len(L)

def pie_plot(df):
    ratio1=list(100*df['고장정비비용']/df['총비용'])
    ratio2=list(100*df['교환비용']/df['총비용'])
    ratio3=list(100*df['서비스지연비용']/df['총비용'])

    ratio=[list_mean(ratio1),list_mean(ratio2),list_mean(ratio3)]
    labels=['고장정비비용','교환비용','서비스지연비용']
    explode=[0,0.2,0.4]

    plt.pie(ratio,labels=labels,autopct='%.1f%%',startangle=260,
            counterclock=False,explode=explode)
    return plt.show()

# multiple bar
def multiple_bar(df):
    idx=pd.date_range(start="2007-01-01 00:00:00",periods=50,freq='S')
    df.index=idx
    D=df.resample('10S').mean()

    circle=mpath.Path.unit_circle()
    star=mpath.Path.unit_regular_star(6) 
    verts=np.concatenate([circle.vertices, star.vertices[::-1, ...]])
    codes=np.concatenate([circle.codes, star.codes])
    cut_star=mpath.Path(verts, codes)

    fig, ax = plt.subplots(figsize=(12,6))
    bar_width = 0.25
    index = np.arange(5)
    plt.bar(index,D['교환비용'],bar_width,alpha=0.4,color='blue',label='교환비용')
    plt.bar(index+bar_width,D['고장정비비용'],bar_width,alpha=0.4,color='g',label='고장정비비용')
    plt.bar(index +2*bar_width,D['서비스지연비용'],bar_width,alpha=0.4,color='y',label='서비스지연비용')
    plt.plot(np.arange(bar_width,5+bar_width,1),D['총비용'],'r',marker=cut_star,
             markersize=20,linewidth=4,label='총비용')
    plt.xticks(np.arange(bar_width,5+bar_width,1),D['교체횟수'])
    plt.xlabel('교체횟수',size=15)
    plt.ylabel('비용',size=15,rotation=45)
    #plt.text(-0.2,265000000,'단위 : 천만원',fontsize=20,color='black')
    plt.text(4.24,10000000,'단위 : 천만원',fontsize=13,color='black')
    plt.legend(fontsize=15)
    return plt.show()

# 2axes plot 

def twoaxes_plot(df):
    idx=pd.date_range(start="2007-01-01 00:00:00",periods=50,freq='S')
    df.index=idx
    D=df.resample('10S').mean()

    circle=mpath.Path.unit_circle()
    star=mpath.Path.unit_regular_star(6) 
    verts=np.concatenate([circle.vertices, star.vertices[::-1, ...]])
    codes=np.concatenate([circle.codes, star.codes])
    cut_star=mpath.Path(verts, codes)
    
    fig,ax1 = plt.subplots(figsize=(14,8))
    bar_width = 0.25
    index = np.arange(5)
    ax1.bar(index,D['교환비용'],bar_width,alpha=0.4,color='blue',label='교환비용')
    ax1.bar(index+bar_width,D['고장정비비용'],bar_width,alpha=0.4,color='g',label='고장정비비용')
    ax1.bar(index +2*bar_width,D['서비스지연비용'],bar_width,alpha=0.4,color='y',label='서비스지연비용')
    ax1.plot(np.arange(bar_width,5+bar_width,1),D['총비용'],'r',marker=cut_star,
             markersize=20,linewidth=4,label='총비용')
    plt.xticks(np.arange(bar_width,5+bar_width,1),D['교체횟수'])
    ax1.set_xlabel('교체횟수',size=15)
    ax1.set_ylabel('비용',size=15,rotation=45)
    ax1.text(-0.1,280000000,'단위 : 천만원',fontsize=13,color='black')
    ax1.legend(fontsize=13,loc='center left')
    
    ax2=ax1.twinx()
    ax2.plot(np.arange(bar_width,5+bar_width,1),D['기대수명'],'deeppink',marker='o',
             markersize=15,linewidth=3,label='기대수명')
    ax2.set_ylabel('기대수명',size=15,rotation=45)
    ax2.legend(fontsize=13,loc='center right')           
    return plt.show()


# 웹페이지 빌드

st.set_option('deprecation.showPyplotGlobalUse', False)
st.title("신뢰성공학 프로젝트")
st.markdown("LCC분석 시각화")

st.sidebar.title("차트 선택")
st.sidebar.markdown("원하는 차트 타입을 선택하세요")

chart_style=st.sidebar.selectbox('시각화 타입',('기존 차트','기본 차트',
                                           '다중 막대 차트','파이 차트','이중축 차트'))

st.sidebar.checkbox("수리 가능 여부",True,key=1)
repair_status=st.sidebar.selectbox('수리 가능 여부 선택',options=['수리 가능','수리 불가능'])


if chart_style=='기존 차트':
    if repair_status=='수리 가능':
        st.header("기존 차트")
        st.markdown("수리 가능")
        st.pyplot(Nemosis_plot(Data2))
    if repair_status=='수리 불가능':
        st.header("기존 차트")
        st.markdown("수리 불가능")
        st.pyplot(Nemosis_plot(Data1))

elif chart_style=='기본 차트':
    if repair_status=='수리 가능':
        st.header("기본 차트")
        st.markdown("수리 가능")
        st.pyplot(base_plot(Data2))
    if repair_status=='수리 불가능':
        st.header("기본 차트")
        st.markdown("수리 불가능")
        st.pyplot(base_plot(Data1))

elif chart_style=='다중 막대 차트':
    if repair_status=='수리 가능':
        st.header("다중 막대 차트")
        st.markdown("수리 가능")
        st.pyplot(multiple_bar(Data2))
    if repair_status=='수리 불가능':
        st.header("다중 막대 차트 수리 불가능")
        st.markdown("수리 불가능")
        st.pyplot(multiple_bar(Data1))

elif chart_style=='파이 차트':
    if repair_status=='수리 가능':
        st.header("파이 차트")
        st.markdown("수리 가능")
        st.pyplot(pie_plot(Data2))
    if repair_status=='수리 불가능':
        st.header("파이 차트")
        st.markdown("수리 불가능")
        st.pyplot(pie_plot(Data1))

elif chart_style=='이중축 차트':
    if repair_status=='수리 가능':
        st.header("이중축 차트")
        st.markdown("수리 가능")
        st.pyplot(twoaxes_plot(Data2))
    if repair_status=='수리 불가능':
        st.header("이중축 차트")
        st.markdown("수리 불가능")
        st.pyplot(twoaxes_plot(Data1))





