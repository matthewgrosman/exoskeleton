clear all; close all; clc

function [NewTheta1, NewTheta2] = getEndEffectorFunction(sensor1, sensor2, sensor3)



%% Spherical Shoulder Exoskeleton kinematics and 2R Robotic simulation

% This code is to calculate the kinematic equation of the Spherical Shoulder Exoskeleton,
% and then use a 2R robotic system located on the shoulder joint to achieve the same end-effector frame.

% Some notes:
% 1. The Spherical Shoulder Exoskeleton is solved by using the geometry relationships of spherical 4-bar linkage.
% 2. Two rotation angle of 2R system: theta1 and theta2 will be calculated in the end.


%%%%%%%%%%%%%% Sensor data input here %%%%%%%%%%%%%%

% [sensor1,sensor2,sensor3] = ReadData('data.txt');

% sensor1 = 0;
% sensor2 = 0;
% sensor3 = 0;
%%%%%%%%%%%%%% Sensor data input here %%%%%%%%%%%%%%


%% 1. Spherical Shoulder Exoskeloton Kinematics

    %% 1.a. spatial spherical 4R linkage position analysis

S4R_alpha = 35.005; % add 0.005 to avoid singularity.
S4R_beta = 35.005; % add 0.005 to avoid singularity.
S4R_gamma = 35;
S4R_eta = 35;


S4R_theta = 98.489 - sensor2';

S4R_psi = OutputAngle(S4R_theta, S4R_alpha, S4R_beta, S4R_gamma, S4R_eta) ;
% output angle of sperical 4R
S4R_phi = CouplerAngle(S4R_theta, S4R_psi, S4R_alpha, S4R_beta, S4R_gamma, S4R_eta) ;
% coupler angle of sperical 4R
S4R_zeta = TransmissionAngle(S4R_theta, S4R_alpha, S4R_beta, S4R_gamma, S4R_eta) ;
% transmission angle of sperical 4R


    %% 1.b. DH Table Input

theta_1 = -49.296 + sensor1';
theta_2 = -S4R_psi;
theta_3 = 98.489 - sensor2';
theta_4 = S4R_phi;
theta_5 = -S4R_zeta-23.97 + sensor3';

DH_theta = [theta_1 theta_2 theta_3 theta_4 theta_5];
DH_d = [-122.98 0 0 0 85.06];
DH_alpha = [35 35 35 35 0];
DH_a = [0 0 0 0 0];

DH_Table = [DH_theta' DH_d' DH_alpha' DH_a'];
% A = DH_HTM(DH_Table,'d');

    %% 1.c. Device Transfermation Matrix

G = [...
    0.1949    0.8851   -0.4227  -14.3574
    0.9787   -0.1468    0.1437   25.3417
    0.0651   -0.4417   -0.8948 -121.6040
         0         0         0    1.0000];
% Transfermation matrix between the base frame of the 2R robot and the base
% frame of the spherical shoulder exoskeleton.

H = [...
    1 0 0 37.623
    0 1 0 -11.555
    0 0 1 77.397
    0 0 0 1];

% Transfermation matrix between the end-effector frame of the 2R robot and
% the end-effector frame of the spherical shoulder exoskeleton.


%% 2. Solve the rotational angles (two thetas) in 2R robot at shoulder joint

A = zeros(4,4,size(DH_theta,1)); % initiate the kinematic equation of the device
T = zeros(4,4,size(DH_theta,1)); % initiate the global transfermation matrix

NewTheta1 = zeros(size(DH_theta,1),1); % initiate the rotation angle theta1 in 2R robot
NewTheta2 = zeros(size(DH_theta,1),1); % initiate the rotation angle theta2 in 2R robot

B = zeros(4,4,size(DH_theta,1)); % initiate the kinematic equation of the 2R robot

for i = 1:size(DH_theta,1)
    % loop for each sensor reading

    output = eye(4); % initialize output

    for j = 1:size(DH_theta,2)
        % loop for theta 1 to 5
        A_j = dh_link_JL(DH_theta(i,j),DH_alpha(j),DH_a(j),DH_d(j));
        output = output*A_j;
    end

    A(:,:,i) = output;
    T(:,:,i) = G*A(:,:,i)*H^(-1);
     % T = G*A*H^(-1);

    NewTheta1(i,1) = rad2deg(atan2(T(1,3,i),-T(2,3,i)));
    NewTheta2(i,1) = rad2deg(atan2(T(3,1,i),T(3,2,i)));

    B(:,:,i) = [...
    cosd(NewTheta1(i,1))*cosd(NewTheta2(i,1)) -cosd(NewTheta1(i,1))*sind(NewTheta2(i,1)) sind(NewTheta1(i,1)) 0
    sind(NewTheta1(i,1))*cosd(NewTheta2(i,1)) -sind(NewTheta1(i,1))*sind(NewTheta2(i,1)) -cosd(NewTheta1(i,1)) 0
    sind(NewTheta2(i,1)) cosd(NewTheta2(i,1)) 0 0
    0 0 0 1];

    % Check if B == T
    % The biggest error of every element between B and T is
end


%% 3. Plot

% NewTheta2_adjusted = NewTheta2;
% min_value = min(NewTheta2(NewTheta2>-89)); % Find the minumum y value in the middle dip
%
% for i = 1:length(NewTheta2_adjusted)
%     if NewTheta2_adjusted(i)>=min_value && NewTheta2_adjusted(i)<=180 % Select data from the middle section
%         NewTheta2_adjusted(i) = NewTheta2_adjusted(i) - 360;
%     end
% end
% NewTheta2_adjusted = -(NewTheta2_adjusted + 90); % normalize NewTheta2 so that the initial degree is 0.


figure
plot(NewTheta1,'LineWidth',4,'LineStyle','-')
hold on
plot(NewTheta2,'LineWidth',4,'LineStyle','-')
hold on
% plot(NewTheta2_adjusted,'LineWidth',4,'LineStyle','-')
ax=gca;
ax.FontName = 'Times New Roman';
ax.FontSize = 14;
% title('Position 1 Flexion 45^{\circ}', 'FontSize',15,'FontName','Times New Roman', 'FontWeight','bold')
legend({'\phi_{1}','\phi_{2}'}, 'FontSize',14,'FontName','Times New Roman', 'FontWeight','bold')
xlabel('# of Readings','FontSize',15,'FontName','Times New Roman')
ylabel('Degrees','FontSize',15,'FontName','Times New Roman')



end
