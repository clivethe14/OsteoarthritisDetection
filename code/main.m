
cases = csvread('casenames.csv',1);
imagesFolder = 'TestImages/';

filenums = [59,66,68,80,100,126];

thicknesses = zeros(1,numel(filenums));
for c=1:1%numel(cases)
    for i = 1:numel(filenums)
        if numel(num2str(filenums(i))) == 1
            fpath = char(strcat(imagesFolder,num2str(cases(c)),'_00', num2str(filenums(i)), '_pred','.png'));
        elseif numel(num2str(filenums(i))) == 2
            fpath = char(strcat(imagesFolder,num2str(cases(c)),'_0', num2str(filenums(i)), '_pred','.png'));
        else
            fpath = char(strcat(imagesFolder,num2str(cases(c)),'_', num2str(filenums(i)), '_pred','.png'));
        end
        img = imread(fpath);
        thicknesses(i) = AverageCartilageThickness(img);
    end
end

disp(['average thickness:',num2str(mean(thicknesses))]);