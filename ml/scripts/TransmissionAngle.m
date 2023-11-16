function [transmission_angle] = TransmissionAngle(theta, alpha, beta, gamma, eta)

% **Use sind/cosd/tand to calculate.** 

transmission_angle = acosd((cosd(beta).*cosd(eta)-cosd(gamma).*cosd(alpha)-sind(gamma).*sind(alpha).*cosd(theta))./...
    (sind(beta).*sind(eta)));

% deg2rad(zeta);
% this is the radians of output angle zeta.
end

