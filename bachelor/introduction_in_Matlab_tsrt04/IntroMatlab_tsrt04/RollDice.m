
function dice_results = RollDice(num_dice)
    % Generate random numbers for each die
    random_values = rand(1, num_dice); 
    
    % Calculate the outcomes of rolling each die
    dice_results = ceil(random_values * 6);
end

