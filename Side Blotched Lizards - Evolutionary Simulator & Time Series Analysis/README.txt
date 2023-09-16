Side blotched lizards have a curious mating pattern, resulting in almost perfect replication of a classic game theory game. There exist three different color variation of the reptile, each with different blotch patterns and distinct personality traits. Each of the three color variants have an exclusive mating strategy that strictly dominates another, resulting in a game similar to "Rock Paper Scissors" where there is no equilibrium strategy.

This project explores the creation of a model that simulates population changes over time, according to the probabilities of mating success based on each strategy. A successful strategy results in multiple offspring, a neutral strategy results in one, and an unsuccessful strategy results in none. The cycles that are created by the model imitate the real-life demographic cycles that Side Blotched Lizards face.

The model takes 3 inputs: the initial population, the initial proportions of each type of lizard and the number of generations to simulate. This information is then saved into a dataset, containing information about the breakdown of each generation's demographics and which strategy was the most successful during that mating period. The data is then graphed to visualize the population cycles and analyzed for patterns.

Finally, a time series model is created to use the simulated data to predict the future population cycles. A simple ARIMA model provides the best insights in an accurate and effective way. This model does an excellent job at predicting future oscillations, despite missing the information about the other game players to make educated predictions. 

The insight provided by this project is an excellent educational tool to understand more about simple mating strategies and their consequences. It also provides a good look into basic evolutionary game theory. 

Further work: the framework that is built by this model could potentially be expanded to other species that have more complex mating strategies.