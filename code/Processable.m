function bool = Processable(image)
    count = zeros(1,2);
    
    count(1)=sum(image(:)==0);
    count(2)=sum(image(:)~=0);
    
    %disp(['Non-Zero Percentage:',num2str()])
    
    nonzero_percentage = (count(2)/numel(image))*100;
    
    if nonzero_percentage>25
        bool = true;
    else
        bool = false;
    end
    
end
