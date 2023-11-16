function [sensor1,sensor2,sensor3] = ReadData(filename)

data = readlines(filename);

sensor1 = [];
sensor2 = [];
sensor3 = [];

for i = 1:length(data)
    if data{i}(8) == 'A'
       sensor1(end+1) = str2num(data{i}(10:end-1));
    end
    if data{i}(8) == 'B'
       sensor2(end+1) = str2num(data{i}(10:end-1));
    end
    if data{i}(8) == 'C'
       sensor3(end+1) = str2num(data{i}(10:end-1));
    end
end

sensor1 = sensor1./5.613;
sensor2 = sensor2./5.340;
sensor3 = sensor3./5.716;

figure
hold on
plot(sensor1)
plot(sensor2)
plot(sensor3)
xlabel('# of Readings') 
ylabel('Degrees of Respective Angles') 
legend('sensor 1','sensor 2','sensor 3')

end

