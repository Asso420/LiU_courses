
clc;
close all;


[xhat, s2hat] = yatzy(10000, false);
fprintf('The mean is: %.2f and the variance: %.2f\n', xhat, s2hat);

debug = true; % Set debug mode

% Call the throwFive function
throwCount = throwFive(debug);
disp(['Assignment 2.5: ' mat2str(throwCount)]);

% Call the analyzeResults function
throwFiveResults = RollDice(5);
analizeThrows = findDie(throwFiveResults, debug); % Call findDie instead of analizeThrows
disp(['Best dice: ' mat2str(analizeThrows)]);

function [data_mean, data_variance] = yatzy(count, debug)  
    %Perform the MonteCarlo simulation
    data = monteCarlo(count, debug);
    %Plot the simulation
    histogram(data, 'BinWidth', 1)
    data_mean = mean(data, 'all');
    data_variance = var(data);
    fprintf('The max is: %d and the min: %d\n', max(data), min(data));
    hold on;
    %Calculate the analytic solution
    normalCurve = normal(max(data)) * count;
    %Plot the analytic solution
    plot(normalCurve, 'LineWidth', 2);
    legend({'Simulation (Monte Carlo)', 'Analytic solution'});
    xlabel('Number of throws to get yatzy');
    ylabel('Frequency');
    hold off;
end


function result = normal(count)
    A = [0  (1/6)   (1/36)  (1/216)     (1/1296);
         0  (5/6)   (10/36) (15/216)    (25/1296);
         0  0       (25/36) (80/216)    (250/1296);
         0  0       0       (129/216)   (900/1296);
         0  0       0       0           (120/1296)];
     e1 = [1 0 0 0 0];
     e5 = [0;0;0;0;1];    
     result = zeros(1, count);
     for k = 1:count
          result(k) = e1 * A^k * e5;
     end
end


function returnValue = monteCarlo(count, debug)  
    returnValue = zeros(1, count);    
    fprintf('Simulating %d yatzy rounds\n', count);  
    startTime = cputime;
    for i = 1:count
        returnValue(i) = throwFive(debug); 
    end
    fprintf('\nDone!\n');
    fprintf('The time it took to run the simulation was: %.1f seconds\n\n', cputime - startTime);
end


function throwCount = throwFive(debug)
    current = [];
    throwCount = 0;
    diesLeft = 5;
    while diesLeft > 0
        data = [simulateThrowDie(diesLeft, debug) current];
        if debug
            fmt = ['Currently have: ' repmat(' %1.0f ', 1, numel(data)) '\n'];
            fprintf(fmt, data)
        end
        current = findDie(data, debug);
        throwCount = throwCount + 1;
        diesLeft = 5 - length(current);  
    end
end

function results = simulateThrowDie(numDies, debug)
    results = randi(6, 1, numDies);
    if debug
        disp(['Rolled dice: ' mat2str(results)]);
    end
end

function analizeThrows = findDie(dice, debug)
    counts = zeros(1, 6);
    for v = 1:6   
        counts(v) = sum(dice == v);
    end
    maxCount = max(counts);
    mostCommon = find(counts == maxCount);
    disp(['MostCommon vectors: ' mat2str(mostCommon)]);

    disp(['the output: ' mat2str(counts)]);
    idex = mostCommon(randi(numel(mostCommon)));
    disp(['The mostCommon: ' mat2str(idex)]);
    analizeThrows = dice(dice == idex);
    if debug
        disp(['Best dice to keep: ' mat2str(analizeThrows)]);
    end
end

function results = RollDice(numDice)
    % Simulate rolling `numDice` dice
    results = randi(6, 1, numDice);
end


