function lableAndlegend(xlable_txt, ylable_txt, legend_txt)
%Define a function to set lables and legends

    xlabel(xlable_txt)
    ylabel(ylable_txt)
    legend(legend_txt, 'Location','NorthWest')
end