function [out_angle] = OutputAngle(theta, alpha, beta, gamma, eta)

% **Use sind/cosd/tand to calculate.** 

A1 = cosd(theta).*sind(alpha).*cosd(gamma).*sind(beta)-cosd(alpha).*sind(gamma).*sind(beta);
B1 = sind(theta).*sind(alpha).*sind(beta);
C1 = cosd(eta)-cosd(theta).*sind(alpha).*sind(gamma).*cosd(beta)-cosd(alpha).*cosd(gamma).*cosd(beta);

psi_p1 = atan2d(B1,A1);
psi_p2 = acosd(C1./sqrt(A1.^2+B1.^2));

% psi = [psi_p1+psi_p2, psi_p1-psi_p2]
% psi_true = psi(2);


out_angle = psi_p1-psi_p2;

% out_angle = deg2rad(psi);
% this is the radians of output angle psi.
end

