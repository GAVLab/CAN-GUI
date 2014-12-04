%%%%%%%%%%%%% Wheel Speed to Vel %%%%%%%%%%
Odom.WheelSpeedL = (Odom.WheelSpeedFL + Odom.WheelSpeedRL)...
    * G35.WheelCircumference / 120; % m/s
Odom.WheelSpeedR = (Odom.WheelSpeedFR + Odom.WheelSpeedRR)...
    * G35.WheelCircumference / 120; % m/s

% Odom.WheelSpeedRL = (Odom.WheelSpeedRL)...
%     * G35.WheelCircumference / 60; % m/s
% Odom.WheelSpeedRR = (Odom.WheelSpeedRR)...
%     * G35.WheelCircumference / 60; % m/s

% Vehicle Velocity Calculations
Odom.Vel = (Odom.WheelSpeedL + Odom.WheelSpeedR) / 2;


G35.WheelDiameter =  0.651; % meters
G35.WheelRad = (G35.WheelDiameter / 2); % meters
G35.WheelCircumference = G35.WheelDiameter*pi;
G35.TrackWidth_F = 1.50114; % meters
G35.TrackWidth_R = 1.50622; % meters


%%%%%%%%%%% STEER RATIO %%%%%%%%%%%%
CAN.SteerAngle = CAN.SteerAngle(:,2)./G35.steerRatio;

G35.steerRatio = 15.9*2;  %%% Treating it as single axle
% G35.steerRatio = 15.9;