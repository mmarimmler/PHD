import pandas as pd
from matplotlib import pyplot as plt

def plot_phase_space(df,**kwargs):
    '''
    @param df: dataframe with 7 columns (turn, spatial coordinates, momentum space coordinates)
    @param axes: axes object
    '''
    df_start = df[df.iloc[:,0] == 0]
    df_end = df[df.iloc[:,0] != 0]
    
    
    rows = df['element'].nunique()-1 #drop beginning element

    if 'figsize' in kwargs.keys():
        fig, axes = plt.subplots(rows+1,2, figsize=kwargs['figsize']) #take end element
    else:
        fig, axes = plt.subplots(rows+1,2)
        
    ax = plt.subplot2grid((rows+1,2),(rows,0), colspan = 2)
    plt.subplots_adjust(hspace=0.5)

    eles = df['element'].unique()
    eles = eles[1:] #drop beginning element
    
    
    
    df_xmax = df_start[df_start['x'] == df_start['x'].max()]
    df_xrms = df_start.groupby('s').agg({'x':'std'}).reset_index()
    df_ymax = df_start[df_start['y'] == df_start['y'].max()]
    df_yrms = df_start.groupby('s').agg({'y':'std'}).reset_index()
    
    for i,ele in enumerate(eles):
        df_end_ele = df_end[df_end['element']==ele]
        
        df_start.plot(x = 'x',
                      y = 'xp', 
                      kind = 'scatter',
                      ax = axes[i][0],
                      c = 'r'
                     )

        df_end_ele.plot(x = 'x',
                    y = 'xp', 
                    kind = 'scatter',
                    ax = axes[i][0]
                   )
    
        df_start.plot(x = 'y',
                      y = 'yp', 
                      kind = 'scatter',
                      ax = axes[i][1],
                      c = 'r'
                     )

        df_end_ele.plot(x = 'y',
                    y = 'yp', 
                    kind = 'scatter',
                    ax = axes[i][1]
                   )
        
        axes[i][1].legend(['start','end'])
        axes[i][0].text(0.1,0.9,ele + ' s = {:.2f}'.format(df_end_ele['s'].drop_duplicates().tolist()[0]),transform=axes[i][0].transAxes)
        
        df_xmax = df_xmax.append(df_end_ele[df_end_ele['x'] == df_end_ele['x'].max()])
        df_xrms = df_xrms.append(df_end_ele.groupby('s').agg({'x':'std'}).reset_index())
        df_ymax = df_ymax.append(df_end_ele[df_end_ele['y'] == df_end_ele['y'].max()])
        df_yrms = df_yrms.append(df_end_ele.groupby('s').agg({'y':'std'}).reset_index())
        
        
    df_xmax.plot(x = 's',
                 y = 'x',
                 ax = ax,
                 marker = 'o',
                 c = 'g'
                )


    df_xrms.plot(x = 's',
                 y = 'x',
                 ax = ax,
                 marker = 'o',
                 linestyle = '--',
                 c = 'g'
                )


    
    df_ymax.plot(x = 's',
                 y = 'y',
                 ax = ax,
                 marker = 'o',
                 c = 'm'
                )


    df_yrms.plot(x = 's',
                 y = 'y',
                 ax = ax,
                 marker = 'o',
                 linestyle = '--',
                 c = 'm'
                )

    ax.legend(['x_max','x_rms','y_max','y_rms'])
    ax.set_ylabel('semi-axis [m]')
    ax.set_xlabel('s [m]')


    
    # print initial ellipse size
    print('xmax @  start:', df_xmax[df_xmax['s']==0]['x'].iloc[0])
    print('xmax @  end:', df_xmax[df_xmax['s']==df_xmax['s'].max()]['x'].iloc[0])
    print('ymax @  start:', df_ymax[df_ymax['s']==0]['y'].iloc[0])
    print('ymax @  end:', df_ymax[df_ymax['s']==df_ymax['s'].max()]['y'].iloc[0])

    return axes

def txt_to_df(PATH_TO_DATA,FILENAME):
  df_ele=pd.read_table(PATH_TO_DATA + FILENAME,
                     sep='\s+',
                     header=None,
                     names=['turn','element','s','x','xp','y','yp'],
                     usecols=[1,2,3,4,5,6,7]
                    )

  return df_ele



        

