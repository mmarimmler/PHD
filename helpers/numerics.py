def iterate(func,list_var1,start_var2,step_var2,limit,below=True):
    '''brute force to iterate to solution
    @param func: function with 2 free parameters
    @param list_var1: parameter space of 1st variable
    @param start_var2: initial value of 2nd variable 
    @param step_var2: increment of 2nd variable
    @param limit: threshold to fall below (default) / overshoot
    @param below: fall below threshold (default)'''
    
    d = {}

    for var1 in list_var1:
            var2 = start_var2
            try:
                f = func(var1,var2)[0]
            except IndexError:
                f = func(var1,var2)

            while f >= limit:
                var2 += step_var2
                try:
                    f = func(var1,var2)[0]
                except IndexError:
                    f = func(var1,var2)
            
            
            d[var1] = round(var2,3)
    
    return d