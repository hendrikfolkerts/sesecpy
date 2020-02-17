clc
clear all

%files to plot as cell array
files = {'Feedback_p_simNum0_f_models.csv', ...
         'Feedback_p_simNum1_f_models.csv', ...
         'Feedback_p_simNum2_f_models.csv', ...
         'Feedback_p_simNum3_f_models.csv'};

for f=1:length(files)
    
    disp(strcat("Plot file ", files{f}))
    
    %%read the data from file
    csvdata = fopen(files{f});
    csvlines = textscan(csvdata,'%s','Delimiter','\n');
    fclose(csvdata);
    csvlines = csvlines{1,1};

    %%split the data
    %count number of ; -> number of plots
    numPlots = count(csvlines{1},';');
    %create variable to split into plots
    rawplots = cell(numPlots,0);
    %split into plots
    for i=1:length(csvlines)   %index i for lines
        j = 1;
        while j <= numPlots    %index j for plots
            rawplotssplit = strsplit(csvlines{i},';','CollapseDelimiters', false);    %split plots
            rawplotssplit = rawplotssplit(~cellfun('isempty',rawplotssplit));    %remove empty cells
            rawplots{j}(i,1) = string(rawplotssplit{j});    %create cell array rawplots with the plots
            j = j + 1;
        end
    end
    %create variable to split the lines of the plots
    plotsheaders = cell(numPlots,0);
    plots = cell(numPlots,0);
    %split the plots
    for j=1:numPlots
        for i=1:length(rawplots{j})
            plotssplit = strsplit(rawplots{j}(i),',','CollapseDelimiters', false);    %split lines in plot
            for k=1:length(plotssplit)
                try
                    plots{j}(i,k) = str2num(plotssplit{k});
                catch
                    plotsheaders{j}(i,k) = string(plotssplit{k});
                end
            end
        end
    end
    %everything now in the variable "plots"

    %%plot
    figure('Name',files{f},'OuterPosition', [1, 1, 500, 600]);
    for i=1:numPlots
        subplot(numPlots,1,i)
        hold on
        x = plots{i}(1:end,1);
        ylabelstring = '';
        sizeplotsi = size(plots{i});
        legendsentries = cell(sizeplotsi(2)-1,0);
        for j=2:sizeplotsi(2)
            y = plots{i}(1:end,j);
            plot(x,y,'Linewidth',2);
            if isempty(ylabelstring)
                ylabelstring = strrep(plotsheaders{i}(3,j),'_',' ');
            else
                ylabelstring = strcat(ylabelstring, ", ",strrep(plotsheaders{i}(3,j),'_',' '));
            end
            legendsentries{j-1} = strrep(plotsheaders{i}(3,j),'_',' ');
        end
        ylabel(ylabelstring)
        xlabel(strrep(plotsheaders{i}(3,1),'_',' '))
        titletext = strrep(plotsheaders{i}(1,1),'_',' ');
        titletext = erase(titletext,'.mo');
        titletext = erase(titletext,'.m');
        title(titletext)
        legend(legendsentries,'Location','northeast','Orientation','vertical')
        grid minor
        hold off
    end
end

clear all