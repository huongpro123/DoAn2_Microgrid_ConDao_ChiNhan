# BAO CAO GIUA KY — DI502 — KTNL2411002 Bui Hoang Hai

## 1. Muc tieu
Mo hinh he thong dien mat troi hoa luoi 1 pha: pin 2 module noi tiep (500 Wp),
boost 20 kHz len bus 380 V, cau H unipolar 20 kHz, loc L, luoi 220 V/50 Hz.

## 2. Mo hinh toan
Dac tuyen pin (mot diode): I = I_ph - I_0[exp((V+R_s I)/(a V_T))-1] - (V+R_s I)/R_sh
voi a = n*N_s*N_cell = 150; V_T = kT_c/q; T_c = T_a + (NOCT-20)G/800.
Bon tham so {I_ph, I_0, R_s, R_sh} xac dinh bang fsolve tu 4 dieu kien datasheet.
Boost: di_L/dt = (V_pv - R_L i_L - (1-d)V_bus)/L; dV_bus/dt = ((1-d)i_L - i_inv)/C.
Cau H unipolar: v_inv = (2s-1)V_bus; L_f di_g/dt = v_inv - R_f i_g - v_g.

## 3. Thong so thiet ke
V_mp,array = 61 V; I_mp,array = 8,20 A; P_mp,array = 500 W; a = 150; FF = 0,756.
L_boost = 2,5 mH (du tru 1,5x); C_bus = 1000 uF (du tru 1,5x); L_f = 10 mH (du tru 2,7x).

## 4. Ket qua (chi tiet trong ket_qua/ket_qua.txt)
- eta_MPPT tai 1000/700/500 W/m2 = 98,4 / 97,9 / 97,1 % (dat >= 90%).
- T_bam 1000->600 W/m2 = 0,21 s (dat <= 0,3 s).
- V_bus tb = 379,6 V; nhap nho 100 Hz = 1,1% (dat).
- PF = 0,998; THD dong luoi = 3,2% (dat).

## 5. Nguyen ly hoat dong

### 5.1. Luong nang luong
Pin phat cong suat DC; C_in giu ap vao phang. Boost nang 61 V len 380 V:
khi khoa dan, L tich nang luong; khi khoa ngat, L xa qua diode ra bus.
Boost vua truyen cong suat vua dich diem lam viec cua pin tren duong P-V.
Tu bus C la phan tu tich tru chinh: cong suat tuc thoi bom vao luoi 1 pha
p(t) = P(1-cos2*omega*t) dao dong o 100 Hz, C bus hap thu/nha ra lam V_bus
nhap nho 100 Hz voi bien do P/(omega*V_bus*C) ~ 4,2 V. Cau H dao chieu thanh
xung unipolar 20 kHz; L_f loc thanh phan cao tan, chi con 50 Hz vao luoi.

### 5.2. Luong tin hieu (ba tang)
1. MPPT (20 lan/s): do V_pv, I_pv -> P; so sanh -> dat V_ref.
2. Vong ap boost (BW ~ 100 Hz): PI so V_pv voi V_ref -> I_L*; vong dong boost
   (BW ~ 4 kHz) -> nhiem vu d -> PWM 20 kHz.
3. Vong bus + vong dong nghich luu (BW ~ 2 kHz): PI dien ap bus -> I_amp*.
   PLL-SOGI lay pha theta tu v_g. Nhan i* = I_amp* sin(theta), qua PR
   (cong huong 50 Hz) so voi i_g -> m -> PWM unipolar -> cau H.

### 5.3. Khi G giam 1000 -> 600 W/m2
G giam -> I_pv giam, C_in xa -> V_pv giam va P_pv giam -> thieu cong suat
vao bus -> tu bus xa -> V_bus giam. MPPT sau <= 50 ms cap nhat V_ref xuong
(~59,3 V), vong ap boost tang D keo V_pv ve MPP moi (phan ung truoc).
Vong bus thay V_bus < 380 V nen giam I_amp* -> dong luoi giam, lap can bang.
Vong dong nghich luu (BW cao nhat) bam i* gan nhu tuc thoi, khong quyet dinh.

## 6. Han che
Khoa ly tuong (V_sat=0, t_on=0); bo qua ESR tu; luoi cung Z_g nho;
nhiet do te bao dong deu; mo hinh 1 diode khong mo ta avalanche/bypass.

## Tai lieu
[1] TI, TIDU405B, 2017.  [2] MathWorks Simulink R2023b.  [3] Bai giang DI502.
