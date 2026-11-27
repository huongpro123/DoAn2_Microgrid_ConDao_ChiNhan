function run_all()
clc; close all;
name   = 'sv_KTNL2411002';
root   = fileparts(mfilename('fullpath'));
outdir = fullfile(root,'ket_qua');
if ~exist(outdir,'dir'), mkdir(outdir); end
p = sv_KTNL2411002_params();  assignin('base','p',p);
fprintf('L=%.3fmH C=%.1fuF Lf=%.1fmH Rs=%.3f Rsh=%.1f\n', ...
        p.L*1e3,p.C*1e6,p.Lf*1e3,p.Rs,p.Rsh);
fail = {};
V = linspace(0, 1.05*p.Voc_stc, 600);
Isc_c = local_I(0,1000,25,p); Voc_c = local_Voc(1000,25,p);
I_mp  = local_I(p.Vmp_stc,1000,25,p);
err = max(abs([Isc_c-p.Isc_stc, Voc_c-p.Voc_stc, I_mp-p.Imp_stc])./ ...
          [p.Isc_stc, p.Voc_stc, p.Imp_stc])*100;
FF = p.Pmp_stc/(p.Voc_stc*p.Isc_stc);
fig1 = figure('Visible','off','Position',[100 100 1200 500]);
subplot(1,2,1); hold on; grid on;
for G = p.G_list, [~,P]=pv_iv(V,G,25,p); plot(V,P,'LineWidth',1.4); end
xlabel('V (V)'); ylabel('P (W)'); title('P-V: G thay doi');
subplot(1,2,2); hold on; grid on;
for T = p.T_list, [~,P]=pv_iv(V,1000,T,p); plot(V,P,'LineWidth',1.4); end
xlabel('V (V)'); ylabel('P (W)'); title('P-V: T thay doi');
exportgraphics(fig1,fullfile(outdir,'h1_iv_pv.png'),'Resolution',200);
mdl = [name '_model'];
if ~bdIsLoaded(mdl), load_system(mdl); end
set_param(mdl,'StopTime',num2str(p.Tstop),'Solver',p.solver, ...
              'MaxStep',num2str(p.MaxStep),'SaveOutput','on','SaveFormat','Array');
simOut = sim(mdl);
t = simOut.tout;  Ppv = simOut.Ppv(:);  Ipv = simOut.Ipv(:);
Vpv = simOut.Vpv(:);  Vbus = simOut.Vbus(:);
Vg = simOut.Vg(:);  Ig = simOut.Ig(:);
eff = zeros(1,3);
for j=1:3
    Pmp = local_Pmp(p.G_test_mppt(j),25,p);
    idx = (t>0.25)&(t<0.30);
    eff(j) = 100*mean(Ppv(idx))/Pmp;
end
Pmp_new = local_Pmp(p.G_step_to,25,p);
idx = t>p.Tstep_G;
errp = abs(Ppv(idx)-Pmp_new)/Pmp_new;
tt = t(idx);
i_ok = find(errp<0.03,1,'first');
if isempty(i_ok), T_bam=NaN; else, T_bam = tt(i_ok)-p.Tstep_G; end
fig2 = figure('Visible','off');
plot(t,Ppv); hold on; grid on; yline(Pmp_new,'r--');
xline(p.Tstep_G,'k:'); xlabel('t (s)'); ylabel('P_{pv}');
exportgraphics(fig2,fullfile(outdir,'h2_mppt.png'),'Resolution',200);
idx_ss = t > (t(end)-10/p.fg);
THD = local_THD(t,Ig,p.fg,10,40);
P_avg = mean(Vg(idx_ss).*Ig(idx_ss));
V_rms = rms(Vg(idx_ss)); I_rms = rms(Ig(idx_ss));
PF = P_avg/(V_rms*I_rms);
idx_bus = (t>0.20)&(t<0.30);
Vbus_tb = mean(Vbus(idx_bus));
dVbus_pct = 100*(max(Vbus(idx_bus))-min(Vbus(idx_bus)))/Vbus_tb;
fig3 = figure('Visible','off');
subplot(2,1,1); plot(t,Vg); grid on; ylabel('v_g');
subplot(2,1,2); plot(t,Ig); grid on; xlabel('t'); ylabel('i_g');
exportgraphics(fig3,fullfile(outdir,'h3_dong_luoi.png'),'Resolution',200);
fig4 = figure('Visible','off');
subplot(2,1,1); plot(t,Vbus); grid on; ylabel('V_{bus}');
subplot(2,1,2); plot(t,Ppv);  grid on; xlabel('t'); ylabel('P_{pv}');
exportgraphics(fig4,fullfile(outdir,'h4_bus.png'),'Resolution',200);
fail = [fail, chk('MPPT_1000',eff(1),eff(1)>=90,'%')];
fail = [fail, chk('MPPT_700', eff(2),eff(2)>=90,'%')];
fail = [fail, chk('MPPT_500', eff(3),eff(3)>=90,'%')];
fail = [fail, chk('T_BAM',    T_bam, T_bam<=0.30,'s')];
fail = [fail, chk('VBUS_TB',  Vbus_tb,abs(Vbus_tb-380)/380<=0.02,'V')];
fail = [fail, chk('VBUS_NN',  dVbus_pct,dVbus_pct<=5,'%')];
fail = [fail, chk('PF',       PF, PF>=0.99,'')];
fail = [fail, chk('THD_I',    THD, THD<=5,'%')];
if isempty(fail), KL='DAT'; else, KL='CHUA_DAT'; end
Ppv_ss = mean(Ppv(t>0.25&t<0.30));
eta_sys = 100*P_avg/Ppv_ss;
fid = fopen(fullfile(outdir,'ket_qua.txt'),'w','n','UTF-8');
fprintf(fid,'MSSV=KTNL2411002\nHO_TEN=Bui Hoang Hai\n');
fprintf(fid,'MATLAB_VERSION=%s\n',version('-release'));
fprintf(fid,'NGAY_CHAY=%s\n',datestr(now,'yyyy-mm-ddTHH:MM:SS'));
fprintf(fid,'PMAX_STC_W=%.1f\nVMPP_STC_V=%.1f\nIMPP_STC_A=%.2f\n', ...
        p.Pmp_stc,p.Vmp_stc,p.Imp_stc);
fprintf(fid,'FF_STC=%.3f\nSAI_SO_DATASHEET_PCT=%.2f\n',FF,err);
fprintf(fid,'MPPT_EFF_1000_PCT=%.1f\nMPPT_EFF_700_PCT=%.1f\nMPPT_EFF_500_PCT=%.1f\n',eff);
fprintf(fid,'T_BAM_s=%.2f\nVBUS_TB_V=%.1f\nVBUS_NHAP_NHO_PCT=%.1f\n',T_bam,Vbus_tb,dVbus_pct);
fprintf(fid,'IG_RMS_A=%.2f\nPF=%.3f\nTHD_I_PCT=%.1f\n',I_rms,PF,THD);
fprintf(fid,'P_PV_W=%.1f\nP_GRID_W=%.1f\nHIEU_SUAT_HE_THONG_PCT=%.1f\n', ...
        Ppv_ss,P_avg,eta_sys);
fprintf(fid,'KET_LUAN=%s\n',KL);
fclose(fid);
fprintf('\n===== KET QUA: %s =====\n',KL);
if ~isempty(fail), fprintf('Khong dat: %s\n',strjoin(fail,', ')); end
end
function f = chk(nm,val,ok,u)
if ok, fprintf('  DAT %-14s = %8.3f %s\n',nm,val,u); f = {};
else,  fprintf('  KHONG DAT %-10s = %8.3f %s\n',nm,val,u); f = {nm}; end
end
function I = local_I(V,G,T,p), I = pv_iv(V,G,T,p); end
function Voc = local_Voc(G,T,p)
f = @(V) pv_iv(V,G,T,p);  Voc = fzero(f,[0 p.Voc_stc*1.2]);
end
function Pmp = local_Pmp(G,T,p)
V = linspace(0,p.Voc_stc,800);  [~,P] = pv_iv(V,G,T,p);  Pmp = max(P);
end
function thd = local_THD(t,x,fg,Ncyc,K)
Tw = Ncyc/fg;  t2 = t(end);  t1 = t2-Tw;
tt = linspace(t1,t2,Ncyc*1000+1);
xx = interp1(t,x,tt,'linear');  xx = xx(1:end-1) - mean(xx);
X = abs(fft(xx))/numel(xx);  k = (1:K)*Ncyc;  Ih = X(k+1);
thd = 100*sqrt(sum(Ih(2:end).^2))/Ih(1);
end
