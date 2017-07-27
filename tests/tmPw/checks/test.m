(* ::Package:: *)

(* ::Input:: *)
(*m=1.27;*)
(*g=-0.6;*)
(*e1=0.303;*)
(*eps=0.01;*)
(*\[Mu]=m/2;*)
(*INF=\[Infinity];*)


(* ::Input:: *)
(*RANGE={4 m^2, 300};*)
(*POINTS=1000;*)


(* ::Input:: *)
(*ClearAll[mom];*)
(*mom[s_,m_]:=Sqrt[s/4-m^2];*)
(*mom[s_]:=mom[s,0];*)


(* ::Input:: *)
(*ClearAll["\[Beta]"];*)
(*\[Beta] = Function[s, Sqrt[1 - (4 m^2)/s]];*)


(* ::Input:: *)
(*ClearAll["\[Eta]"];*)
(*\[Eta]=Function[k,(\[Mu] g)/k];*)


(* ::Input:: *)
(*ClearAll["coAngle"];*)
(*coAngle = Function[{Cpq,Cpr,Fqr},Cpq Cpr + Sqrt[1-Cpq^2] Sqrt[1-Cpr^2]Cos[Fqr]];*)


(* ::Input:: *)
(*ClearAll["MP"];*)
(*MP=Function[{q, p, Cqp},1/(p^2+q^2-2 p q Cqp +m^2)+1/(p^2+q^2+2 p q Cqp + m^2)];*)


(* ::Input:: *)
(*ClearAll["sigma"];*)
(*sigma[s_]:=\[Beta][s]/(32 \[Pi] s) NIntegrate[Abs[MP[mom[s], mom[s,m], Cpq]]^2, {Cpq, -1,1}, PrecisionGoal->Infinity,AccuracyGoal->4]*)


(* ::Input:: *)
(*points = Table[RANGE[[1]]+(RANGE[[2]] - RANGE[[1]])/POINTS i, {i, 0, POINTS-1}];*)


(* ::Input:: *)
(*res = AbsoluteTiming@Map[{#, sigma[#]}&, points];*)


(* ::Input:: *)
(*Print["Eval time: ", res[[1]]]*)


(* ::Input:: *)
(*Column[Row[{#1, " ",ScientificForm@#2}]&@@@res[[2,1;;20]]]*)


(* ::Input:: *)
(*ListLinePlot[res[[2]], PlotRange->All]*)
