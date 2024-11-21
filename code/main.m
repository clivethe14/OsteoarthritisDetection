
cases = csvread('casenames.csv',1);
%imagesFolder = 'TestImages/case1';
imagesFolder = 'TestImages/case2/';


thicknesses = zeros(1,197);

for c=2:2%numel(cases)
    
    local_thickness = zeros(1,160);
    
    for i = 1:160
        if numel(num2str(i)) == 1
            fpath = char(strcat(imagesFolder,num2str(cases(c)),'_00', num2str(i), '_pred','.png'));
        elseif numel(num2str(i)) == 2
            fpath = char(strcat(imagesFolder,num2str(cases(c)),'_0', num2str(i), '_pred','.png'));
        else
            fpath = char(strcat(imagesFolder,num2str(cases(c)),'_', num2str(i), '_pred','.png'));
        end
        img = imread(fpath);
        if Processable(img)
            average_thickness = AverageCartilageThickness(img);
            if average_thickness < 100
                local_thickness(i) = average_thickness;
            end
            %disp([num2str(i),': ',sprintf('%.6f',local_thickness(i))]);
        end
    end
    
    local_thickness(local_thickness==0) = [];
    
    thicknesses(c) = mean(local_thickness);
end

disp(['average thicknesses:',num2str(thicknesses(2))]);