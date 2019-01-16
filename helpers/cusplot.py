def add_axis(ax,axis,formula,name):
    '''function that adds 2nd x or y axis
	@param ax: axes object
	@param axis: 'x' or 'y'
	@param formula: function
	@param name: axis name'''    
    if axis == 'x':
        values = ax.get_xticks().tolist()
        ax_new = ax.twiny()
    elif axis == 'y':
        values = ax.get_yticks().tolist()
        ax_new = ax.twinx()
        
    new_ticks = [formula(tick) for tick in values]
    
    if axis == 'x':
        ax_new.set_xticklabels(new_ticks)
        ax_new.set_xlabel(name)
        ax_new.xaxis.set_ticks_position('bottom')
        ax_new.xaxis.set_label_position('bottom')
        ax_new.spines['bottom'].set_position(('outward', 40))
        ax_new.set_xlim(ax.get_xlim())
    elif axis == 'y':
        ax_new.set_yticklabels(new_ticks)
        ax_new.set_ylabel(name)
        ax_new.yaxis.set_ticks_position('left')
        ax_new.yaxis.set_label_position('left')
        ax_new.spines['left'].set_position(('outward', 60))
        ax_new.set_ylim(ax.get_ylim())
        
    return ax_new