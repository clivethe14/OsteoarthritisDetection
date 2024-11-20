function trueOrFalse = in(image);
    image = 'C:\Users\Min Jung\Downloads\FemurTibiaBoneMasks197\preds\9002116_073_pred.png';
    BinaryImage = imread(image);

    % binarization using the image using OTSU's Method.
    %global threshold
    %step 2
    threshold = graythresh(BinaryImage);
    BinaryImage = BinaryImage > (threshold * 255);

    %step 3
    % display the image
    figure; imshow(BinaryImage); 
    title(['Binary Image for Slice ', image_path], 'Interpreter', 'none');

    % step 4
    % labels each of the component to a specfic label/value to identify it
    labeledOutputImage = bwlabel(BinaryImage);
    regions = regionprops(labeledOutputImage, 'Area', 'PixelIdxList', 'BoundingBox');

    % step 5
    % idenfiying the femur and tibia
    [sorted_values, sortedIdx] = sort([regions.Area], 'descend');
    if length(sortedIdx) < 2
        disp(['Warning: Not enough regions detected in image ', slice_filename]);
    else
        femurRegion = regions(sortedIdx(1)).PixelIdxList;
        tibiaRegion = regions(sortedIdx(2)).PixelIdxList;

        femurMask = zeros(size(BinaryImage));
        femurMask(femurRegion) = 1;
        tibiaMask = zeros(size(BinaryImage));
        tibiaMask(tibiaRegion) = 1;
    
        % Get count of pixels in mask that are greater than 19892
        bool = false;
        ctr1 = sum(femurMask(:) == 1);
        ctr2 = sum(tibiaMask(:) == 1);
    
        if ctr1 > 19892 && ctr2 > 19892 
            bool = true;
        end;
    
        if ctr1 < 19892 % Based on 9002116_073_pred.png where femur surface measurable lessens from 9002116_072_pred.png
            bool = false;
        end;
    
        if ctr2 < 19892
            bool = false;
        end;
    end;
    
    bool;
end;
    



    
