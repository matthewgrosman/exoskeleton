function [DH_HTM] = DH_HTM(Matrix,angtype)
% Input Matrix: DH Table of (n,4) Dimension, else throw error
% Output matrix: Homogenous transformation: Dimension (4,4)

if size(Matrix,2) ~= 4
    error("Matrix must have 4 columns");
end

output = eye(4);

len = size(Matrix,1); % Number of Rows

for i = 1 : len
    params = Matrix(i,:);
    theta = params(1);
    alpha = params(3);
    rx = params(4);
    dz = params(2);
    next = dh_link(theta,alpha,rx,dz,angtype);
    output = output * next;
end

output = simplify(output);
DH_HTM = output;

end