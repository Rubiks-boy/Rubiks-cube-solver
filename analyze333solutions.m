close all;
clearvars;

fig = figure();
set(fig, 'defaultAxesColorOrder', [[0 0.3 0]; [0 0 0]]);

eo_15_movecounts = [29, 29, 21, 24, 32, 29, 31, 34, 30, 31, 33, 32, 30, 31, 31, 34, 31, 30, 29, 32, 30, 32, 29, 28, 30, 31, 32, 32, 29, 30, 32, 30, 32, 30, 32, 30, 31, 32, 31, 31, 32];
eo_2_runtime = [167.17252683639526, 229.22487020492554, 271.39937686920166, 383.63726115226746, 377.717111825943, 426.3180739879608, 1251.019649028778, 628.1440269947052, 672.7786209583282, 2302.945384979248, 2080.2915880680084, 225.59618520736694, 1635.5614399909973, 285.1226351261139, 561.12748503685, 343.7235791683197, 315.45710587501526, 291.76187205314636, 1653.2187778949738, 800.2746827602386, 257.2374119758606, 3967.087249994278, 490.6238341331482, 180.79370999336243, 354.24083518981934, 576.2843079566956, 760.6273550987244, 537.8442950248718, 291.2182002067566, 593.393630027771, 255.99310302734375, 653.4271869659424, 1054.2039639949799, 393.8835561275482, 548.6149570941925, 6260.111709833145, 2008.0906949043274, 186.39898109436035, 825.0711350440979, 2883.248484134674, 486.91264486312866, 8430.553311109543];
eo_2_movecounts = [32, 32, 33, 29, 32, 32, 31, 29, 33, 32, 32, 34, 30, 29, 31, 28, 34, 30, 32, 30, 32, 33, 32, 33, 33, 31, 32, 34, 33, 30, 33, 32, 34, 33, 33, 33];

eo_2_runtime = eo_2_runtime / 60;

bins = linspace(14, 35, 22);
y15 = hist(eo_15_movecounts, bins);
y2 = hist(eo_2_movecounts, bins);

yyaxis right;
b = bar(bins, [y2; y15], 'grouped');
b(2).FaceColor = [0.5 0 0];
b(1).FaceColor = 'b';
hold on;
title("Move Count of 3x3x3 Solver, Compared to Optimal")
xlabel("Move Count")
ylabel("Number of Solutions")
optimal_dist = [91365e12, 1100e15, 12e18, 29e18, 1500e15, 490e6];
yyaxis left
ylabel("Number of States")
legend("Quick Solver", "Slow Solver")
bar(linspace(15, 20, 6), optimal_dist, 0.4)
hold off;

figure();
binsRun = linspace(1, 150, 30);
yrun = hist(eo_2_runtime, binsRun);
bar(binsRun, yrun, 1, 'black')
title("Runtime of Solver (Quick)")
xlabel("Time (min)")
ylabel("Number of Solves")

disp(max(eo_2_movecounts))
disp(median(eo_2_runtime))
