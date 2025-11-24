clc;
clear;
close all;
load ('datatraffic.mat');

%{
dice_results = RollDice(8)
disp(dice_results);
    histogram(dice_results, 'Normalization', 'probability'); 
    title('Histogram of Dice Throw Results');
    xlabel('resultat');
    ylabel('probability');

%}

throwFive();
%returnVector = throwFive();
%throwAgain(returnVector)


%%
% Plot assignment 
figure();
plot(years, traffic.*1E9)
lableAndlegend('years', 'Traffic(GB)', {'2G-3G-4G', '5G', 'Fixed'})
title('my first plot')

figure();
bar(years, traffic)
lableAndlegend('years', 'Traffic(GB)', {'2G-3G-4G', '5G', 'Fixed'})
title('my first bar cahrt')

figure();
subplot(2,1,1)
bar(years, traffic)
lableAndlegend('years', 'Traffic(GB)', {'2G-3G-4G', '5G', 'Fixed'})
title('Grouped Bar Char')

subplot(2,1,2)
bar(years, traffic, 'stacked')
lableAndlegend('years', 'Traffic(GB)', {'2G-3G-4G', '5G', 'Fixed'})
title('Stacked Bar Char')

