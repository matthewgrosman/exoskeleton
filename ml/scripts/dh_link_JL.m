function [matrix] = dh_link_JL(theta,alpha,a,d)

matrix = [...
cosd(theta) -sind(theta).*cosd(alpha) sind(theta).*sind(alpha) a.*cosd(theta)
sind(theta) cosd(theta).*cosd(alpha) -cosd(theta).*sind(alpha) a.*sind(theta)
0 sind(alpha) cosd(alpha) d
0 0 0 1];

% Homogenouse Transforms
% matrix = vpa(matrix);
end

