T = readtable('Data on hospital and ICU admission rates and current occupancy for COVID-19.xlsx');
data = T(datetime(T.date) > datetime("2021-01-01"),:);
data_PL = data(data.country == "Poland",:);
data_CZ = data(data.country == "Czechia",:);

%Zad 1
%PL
diff_PL = diff(data_PL.value);
absolute_diff_PL = abs(diff_PL);
log_diff_PL = abs(diff(log(data_PL.value)));
figure
plot(diff_PL);
title('PL przyrost wzglêdny')
figure
plot(absolute_diff_PL)
title('PL przyrost bezwzglêdny')
figure
plot(log_diff_PL)
title('PL przyrost logarytmiczny')

mean_PL = mean(data_PL.value)
std_PL = std(data_PL.value)

% CZ
diff_CZ = diff(data_CZ.value);
absolute_diff_CZ = abs(diff_CZ);
log_diff_CZ = abs(diff(log(data_CZ.value)));
figure
plot(diff_CZ);
title('CZ przyrost wzglêdny')
figure
plot(absolute_diff_CZ)
title('CZ przyrost bezwzglêdny')
figure
plot(log_diff_CZ)
title('CZ przyrost logarytmiczny')

mean_CZ = mean(data_CZ.value)
std_CZ = std(data_CZ.value)

% Zad 2
% model linowy
%PL
x_PL = linspace(1, length(data_PL.value), length(data_PL.value));
par_PL = polyfit(x_PL, data_PL.value.',1);
newY_PL=polyval(par_PL,x_PL);
linear_app_PL = norm(newY_PL - data_PL.value)

figure
plot(x_PL, newY_PL)
title('PL trend liniowy')

%CZ
x_CZ = linspace(1, length(data_CZ.value), length(data_CZ.value));
par_CZ = polyfit(x_CZ, data_CZ.value.',1);
newY_CZ=polyval(par_CZ,x_CZ);
linear_app_CZ = norm(newY_CZ - data_CZ.value)

figure
plot(x_CZ, newY_CZ)
title('CZ trend liniowy')

%Zad 3
%movmean
%PL
movmean_PL_5 = movmean(data_PL.value,5);
figure
plot(x_PL, data_PL.value);
hold on;
plot(x_PL, movmean_PL_5);
title('PL œrednia krocz¹ce k=5')

movmean_PL_22 = movmean(data_PL.value,22);
figure
plot(x_PL, data_PL.value);
hold on;
plot(x_PL, movmean_PL_22);
title('PL œrednia krocz¹ce k=22')

%CZ
movmean_CZ_5 = movmean(data_CZ.value,5);
figure
plot(x_CZ, data_CZ.value);
hold on;
plot(x_CZ, movmean_CZ_5);
title('CZ œrednia krocz¹ce k=5')

movmean_CZ_22 = movmean(data_CZ.value,22);
figure
plot(x_CZ, data_CZ.value);
hold on;
plot(x_CZ, movmean_CZ_22);
title('CZ œrednia krocz¹ce k=22')

norm_movmean_5_PL = norm(data_PL.value - movmean_PL_5)
norm_movmean_22_PL = norm(data_PL.value - movmean_PL_22)

norm_movmean_5_CZ = norm(data_CZ.value - movmean_CZ_5)
norm_movmean_22_CZ = norm(data_CZ.value - movmean_CZ_22)
%mniejszy b³¹d dla k=5 dla Czech i Polski

% Zad3
data_PL_100 = data_PL(end-100+1:end,:);
data_CZ_100 = data_CZ(end-100+1:end,:);
k_values = [5, 10, 22, 50];
for i = 1 : length(k_values)
 movmean_PL = movmean(data_PL_100.value,k_values(i));
 norm_movmean_PL = norm(data_PL_100.value - movmean_PL);
 fprintf('PL norm for movmean for k=%d - %d \n', k_values(i), norm_movmean_PL);

 movmean_CZ = movmean(data_CZ_100.value,k_values(i));
 norm_movmean_CZ = norm(data_CZ_100.value - movmean_CZ);
 fprintf('CZ norm for movmean for k=%d - %d \n', k_values(i), norm_movmean_CZ);
end

for i = 1:3
  x_PL = linspace(1, length(data_PL_100.value), length(data_PL_100.value));
  par_PL = polyfit(x_PL, data_PL_100.value.',i);
  newY_PL=polyval(par_PL,x_PL);
  linear_app_PL = norm(newY_PL - data_PL_100.value);
  fprintf('PL norm for polyfit for k=%d - %d \n', i, linear_app_PL);
  
  x_CZ = linspace(1, length(data_CZ_100.value), length(data_CZ_100.value));
  par_CZ = polyfit(x_CZ, data_CZ_100.value.',i);
  newY_CZ=polyval(par_CZ,x_CZ);
  linear_app_CZ = norm(newY_CZ - data_CZ_100.value);
  fprintf('CZ norm for polyfit for k=%d - %d \n', i, linear_app_CZ);
  
  figure
  plot(x_PL, newY_PL)
  hold on;
  plot(x_PL, data_PL_100.value)
  title('Polyfit for PL');
  
  figure
  plot(x_CZ, newY_CZ)
  hold on;
  plot(x_CZ, data_CZ_100.value)
  title('Polyfit for CZ');
end
%najlepiej aproksymowaæ œredni¹ ruchom¹ z k=5
   








