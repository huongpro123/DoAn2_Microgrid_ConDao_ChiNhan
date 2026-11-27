function p = sv_KTNL2411002_params()
p.Pmp_mod = 250;  p.Vmp_mod = 30.5;  p.Imp_mod = 8.20;
p.Voc_mod = 37.8; p.Isc_mod = 8.75;
p.alpha_Isc_rel = 0.050e-2;
p.beta_Voc_rel  = -0.30e-2;
p.NOCT = 45;      p.Ncell = 60;
p.Ns = 2;  p.Np = 1;
p.Vbus_ref = 380;
p.Vg_rms   = 220;  p.fg = 50;
p.Zg_R = 0.1;  p.Zg_L = 0.5e-3;
p.fsw  = 20e3;  p.Cin  = 220e-6;
p.RL   = 0.05;  p.Rf   = 0.1;
p.Tmppt = 50e-3;
p.Vmp_stc = p.Ns*p.Vmp_mod;
p.Imp_stc = p.Np*p.Imp_mod;
p.Voc_stc = p.Ns*p.Voc_mod;
p.Isc_stc = p.Np*p.Isc_mod;
p.Pmp_stc = p.Ns*p.Np*p.Pmp_mod;
p.n = 1.25;
p.a = p.n * p.Ns * p.Ncell;
p.G_stc = 1000;
p = extract_pv_params(p);
p.D_boost   = 1 - p.Vmp_stc/p.Vbus_ref;
p.dIL_max   = 0.20 * p.Imp_stc;
p.L_min     = p.Vmp_stc * p.D_boost / (p.fsw * p.dIL_max);
p.kL = 1.5;
p.L  = p.kL * ceil(p.L_min*1e4)/1e4;
p.w1        = 2*pi*p.fg;
p.dVbus_max = 0.02 * p.Vbus_ref;
p.C_min     = p.Pmp_stc / (p.w1 * p.Vbus_ref * p.dVbus_max);
p.kC = 1.5;
p.C  = p.kC * ceil(p.C_min*1e-4)/1e-3;
p.Ig_rms   = p.Pmp_stc / p.Vg_rms;
p.Ig_pk    = sqrt(2) * p.Ig_rms;
p.dIpp_max = 0.20 * p.Ig_pk;
p.Lf_min   = p.Vbus_ref / (8 * p.fsw * p.dIpp_max);
p.kLf = 2.7;
p.Lf  = p.kLf * p.Lf_min;
p.kp_v  = 0.5;    p.ki_v  = 20;
p.kp_ib = 2.0;    p.ki_ib = 2000;
p.kp_i  = 5;      p.kr_i  = 500;    p.wc_i  = 5;
p.kp_pll = 200;   p.ki_pll = 20000;  p.k_sogi = 1.41;
p.w0     = 2*pi*50;
p.w_notch    = 2*pi*100;
p.zeta_notch = 0.1;
p.Tstop  = 0.60;  p.Tstep_G = 0.30;
p.solver = 'ode23tb';  p.MaxStep = 1e-6;
p.G0 = 1000;  p.Ta = 25;
p.G_list = [1000 800 600 400];
p.T_list = [25 45 65];
p.G_test_mppt = [1000 700 500];
p.G_step_to   = 600;
end
function p = extract_pv_params(p)
k = 1.380649e-23;  q = 1.602176634e-19;
VT  = k * 298.15 / q;
aVT = p.a * VT;
Isc = p.Isc_stc;  Voc = p.Voc_stc;
Vmp = p.Vmp_stc;  Imp = p.Imp_stc;
fun = @(x) [ ...
    x(1) - x(2)*(exp(x(3)*Isc/aVT) - 1) - x(3)*Isc/x(4) - Isc; ...
    x(1) - x(2)*(exp(Voc/aVT) - 1) - Voc/x(4); ...
    x(1) - x(2)*(exp((Vmp+x(3)*Imp)/aVT) - 1) - (Vmp+x(3)*Imp)/x(4) - Imp; ...
    x(2)/aVT*exp((Vmp+x(3)*Imp)/aVT) + 1/x(4) - Imp/(Vmp - Imp*x(3))];
x0 = [Isc, 2.6e-8, 0.48, 1e6];
opts = optimoptions('fsolve','Display','off','MaxIterations',2000, ...
    'FunctionTolerance',1e-14,'StepTolerance',1e-14, ...
    'MaxFunctionEvaluations',10000);
x = fsolve(fun, x0, opts);
p.Iph_stc = x(1);  p.I0_stc = x(2);
p.Rs      = x(3);  p.Rsh    = x(4);
p.fsolve_residual = max(abs(fun(x)));
end
