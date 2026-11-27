function [I, P, dIdV] = pv_iv(V, G, T, p)
% Mo hinh mot diode cho day pin quang dien (2 module noi tiep)
k = 1.380649e-23;  q = 1.602176634e-19;
Tc = T + 273.15;
VT = k*Tc/q;
aVT = p.a * VT;
if aVT <= 0, error('a*VT khong hop le'); end
alpha_Isc_abs = p.alpha_Isc_rel * p.Isc_stc;
Iph = (G/1000) * (p.Iph_stc + alpha_Isc_abs*(Tc - 298.15));
Eg = 1.12;
I0 = p.I0_stc * (Tc/298.15)^3 * ...
     exp((q*Eg/(p.n*k))*(1/298.15 - 1/Tc));
I = zeros(size(V));
for i = 1:numel(V)
    Vi = V(i);  Ii = max(Iph, 0);
    for it = 1:50
        u  = Vi + p.Rs*Ii;
        ex = exp(min(u/aVT, 700));
        f  = Iph - I0*(ex - 1) - u/p.Rsh - Ii;
        df = -I0/aVT*ex * p.Rs - p.Rs/p.Rsh - 1;
        if abs(df) < 1e-15, break; end
        d  = f/df;  Ii = Ii - d;
        if abs(d) < 1e-10*max(1,abs(Ii)), break; end
    end
    I(i) = Ii;
end
P = V .* I;
if nargout > 2
    dIdV = zeros(size(V));
    for i = 1:numel(V)
        u = V(i) + p.Rs*I(i);
        A = I0/aVT * exp(min(u/aVT, 700));
        B = A + 1/p.Rsh;
        dIdV(i) = -B / (1 + p.Rs*B);
    end
end
end
