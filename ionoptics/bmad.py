import pandas as pd
from matplotlib import pyplot as plt
import matplotlib.ticker as ticker

def plot_phase_space(df,ele_w = False,**kwargs):
    '''
    @param df: dataframe with 7 columns (turn, spatial coordinates, momentum space coordinates)
    @param ele_w: True - element-wise plotting of phase spaces
    @param **kwargs: figure keywords
    @return axes: axes object
    '''
    df_start = df[df.iloc[:,0] == 0]
    df_end = df[df.iloc[:,0] != 0]
    
    
    rows = df['element'].nunique()-1 #drop beginning element

    #figsize specified? element-wise layout?
    if 'figsize' in kwargs.keys():
        if ele_w==True:
            #TODO: replace this dirty combination by gridspec (rows+2,2)
            fig, axes = plt.subplots(rows+1,2, figsize=kwargs['figsize']) #take end element
            ax = plt.subplot2grid((rows+2,2),(rows,0), rowspan = 2, colspan = 2)
        else:
            fig = plt.figure(figsize=kwargs['figsize'])

            gs = fig.add_gridspec(2,3)
            
            ax = fig.add_subplot(gs[:,:2])
            ax0 = fig.add_subplot(gs[0,2])
            ax1 = fig.add_subplot(gs[1,2])
    else:
        if ele_w==True:
            fig, axes = plt.subplots(rows+1,2)
            ax = plt.subplot2grid((rows+2,2),(rows,0), rowspan = 2, colspan = 2)
        else:
            fig, axes = plt.subplots(1,2)
            ax = plt.subplot2grid((3,2),(1,0), rowspan = 2, colspan = 2)
    

    plt.subplots_adjust(hspace=0.5,wspace=0.3)

    eles = df['element'].unique()
    eles = eles[1:] #drop beginning element
    
    
    
    df_xmax = df_start[df_start['x'] == df_start['x'].max()]
    df_xmin = df_start[df_start['x'] == df_start['x'].min()]
    df_xrms = df_start.groupby('s').agg({'x':'std'}).reset_index()

    df_ymax = df_start[df_start['y'] == df_start['y'].max()]
    df_ymin = df_start[df_start['y'] == df_start['y'].min()]
    df_yrms = df_start.groupby('s').agg({'y':'std'}).reset_index()
    
    for i,ele in enumerate(eles):
        df_end_ele = df_end[df_end['element']==ele]

        if ele_w==True:
        
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
        df_xmin = df_xmin.append(df_end_ele[df_end_ele['x'] == df_end_ele['x'].min()])
        df_xrms = df_xrms.append(df_end_ele.groupby('s').agg({'x':'std'}).reset_index())
        df_xrms['-x'] = -df_xrms['x']

        df_ymax = df_ymax.append(df_end_ele[df_end_ele['y'] == df_end_ele['y'].max()])
        df_ymin = df_ymin.append(df_end_ele[df_end_ele['y'] == df_end_ele['y'].min()])
        df_yrms = df_yrms.append(df_end_ele.groupby('s').agg({'y':'std'}).reset_index())
        df_yrms['-y'] = -df_yrms['y']

    if ele_w==False:

        df_start.plot(x = 'x',
                      y = 'xp', 
                      kind = 'scatter',
                      ax = ax0,
                      c = 'r'
                      )

        df_end_ele.plot(x = 'x',
                        y = 'xp', 
                        kind = 'scatter',
                        ax = ax0
                       )

        df_start.plot(x = 'y',
                      y = 'yp', 
                      kind = 'scatter',
                      ax = ax1,
                      c = 'r'
                     )

        df_end_ele.plot(x = 'y',
                        y = 'yp', 
                        kind = 'scatter',
                        ax = ax1
                       )

        ax0.legend(['start','end'])

        # convert ticks into mm
        ticks_ax0_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/1e-3))
        ticks_ax0_y = ticker.FuncFormatter(lambda y, pos: '{0:g}'.format(y/1e-3))
        ax0.xaxis.set_major_formatter(ticks_ax0_x)
        ax0.yaxis.set_major_formatter(ticks_ax0_y)
        ax0.set_xlabel('x in mm')
        ax0.set_ylabel('x´ in mrad')

        ticks_ax1_x = ticker.FuncFormatter(lambda x, pos: '{0:g}'.format(x/1e-3))
        ticks_ax1_y = ticker.FuncFormatter(lambda y, pos: '{0:g}'.format(y/1e-3))
        ax1.xaxis.set_major_formatter(ticks_ax1_x)
        ax1.yaxis.set_major_formatter(ticks_ax1_y)
        ax1.set_xlabel('y in mm')
        ax1.set_ylabel('y´ in mrad')

        
        
        
    df_xmax.plot(x = 's',
                 y = 'x',
                 ax = ax,
                 marker = 'o',
                 c = 'g'
                )

    df_xmin.plot(x = 's',
                 y = 'x',
                 ax = ax,
                 marker = 'o',
                 c = 'g'
                )

    x_fill=ax.fill_between(df_xrms['s'],
                           df_xrms['x'],
                           df_xrms['-x'],
                           linestyle = '--',
                           color = 'g',
                           alpha = 0.5
                          )          


    
    df_ymax.plot(x = 's',
                 y = 'y',
                 ax = ax,
                 marker = 'o',
                 c = 'm'
                )

    df_ymin.plot(x = 's',
                 y = 'y',
                 ax = ax,
                 marker = 'o',
                 c = 'm'
                )


    y_fill=ax.fill_between(df_yrms['s'],
                           df_yrms['y'],
                           df_yrms['-y'],
                           linestyle = '--',
                           color = 'm',
                           alpha = 0.5
                          )

    h,_ = ax.get_legend_handles_labels()
    ax.legend([h[0],h[2],x_fill,y_fill],['x_max','y_max','x_RMS','y_RMS'])
    

    ticks_ax_y = ticker.FuncFormatter(lambda y, pos: '{0:g}'.format(y/1e-3))
    ax.yaxis.set_major_formatter(ticks_ax_y)
    ax.set_ylabel('beam size in mm')
    ax.set_xlabel('s in m')


    
    # print initial ellipse size
    print('xmax @  start:', df_xmax[df_xmax['s']==0]['x'].iloc[0])
    print('xrms @  start:', df_xrms[df_xrms['s']==0]['x'].iloc[0])
    print('\n')

    print('xmax @  end:', df_xmax[df_xmax['s']==df_xmax['s'].max()]['x'].iloc[0])
    print('xrms @  end:', df_xrms[df_xrms['s']==df_xrms['s'].max()]['x'].iloc[0])
    print('\n')

    print('ymax @  start:', df_ymax[df_ymax['s']==0]['y'].iloc[0])
    print('yrms @  start:', df_yrms[df_yrms['s']==0]['y'].iloc[0])
    print('\n')

    print('ymax @  end:', df_ymax[df_ymax['s']==df_ymax['s'].max()]['y'].iloc[0])
    print('yrms @  end:', df_yrms[df_yrms['s']==df_ymax['s'].max()]['y'].iloc[0])
    print('\n')

    print('particle loss/%:', df_end_ele[df_end_ele['x']==0].shape[0]/df_end_ele.shape[0]*100)
    

    return fig

def txt_to_df(PATH_TO_DATA,FILENAME):
  df_ele=pd.read_table(PATH_TO_DATA + FILENAME,
                     sep='\s+',
                     header=None,
                     names=['turn','element','s','x','xp','y','yp'],
                     usecols=[1,2,3,4,5,6,7]
                    )

  return df_ele



        

