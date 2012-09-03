#!/usr/bin/awk -f

## This awk script conducts analysis to get histogram data of raw data.

BEGIN{
    FS=","; # Separation operator
    bar_array[0] = 0;   # Store the final histogram data.
    item_freq_ct = 0;   # The count of each entry.
    cache_entry = "";   # Cache the last entry.

    #if (output_file == "")
    #{
    #    print "Not specify the output file name when starting script.";
    #    exit 0;
    #}
    #if (field == "")
    #{
    #    print "Not specify the output file name when starting script.";
    #    exit 0;
    #}
}

{
    ## Current entry not euqal to previous entry
    if ($1 != cache_entry){
        bar_array[item_freq_ct]++;
        cache_entry = $1;
        item_freq_ct = 1;
    }
    ## Equal 
    else{
        item_freq_ct++;
    }
}

END{
    ## Record the last entry
    bar_array[item_freq_ct]++;
    
    ## Output the statistical data
    bar_cn = length(bar_array);
    for (i = 1; i < bar_cn; i++)
    {
        if (bar_array[i] != "")
            print i" "bar_array[i];
    }
}
