(* ::Package:: *)

(* ::Input:: *)
(*(* load params *)*)


(* ::Input:: *)
(*path = "../../output/sqedPw";*)
(*SetDirectory[NotebookDirectory[]<>path]*)


(* ::Input:: *)
(*params = Module[{tmp},*)
(*tmp = Import["params", "Lines"];*)
(*tmp = Select[tmp, !StringMatchQ[#, StartOfString~~"# "~~___]&];*)
(*tmp = StringSplit[#, "="]& /@tmp;*)
(*tmp = StringReplace[#, {"e+" :> "*^", "e-" :> "*^-"}]& /@ tmp;*)
(*tmp = {#[[1]], Quiet@Check[ToExpression[#[[2]]], #[[2]]] }&/@tmp;*)
(*tmp = <|#[[1]]->#[[2]]&/@tmp|>*)
(*];*)
(*Column@KeyValueMap[Row[{#1," = ",#2}]&,params]*)


(* ::Input:: *)
(*m=params["G_m"];*)
(*g=params["G_g"];*)
(*e=params["G_e"];*)
(*eps=params["G_eps"];*)
(*Nc=params["G_Nc"];*)
(*dimfactor = params["G_dimfactor"];*)


(* ::Input:: *)
(*minS=params["SUMRULE_minS"];*)
(*maxS =params["SUMRULE_maxS"];*)
(*points=params["TEST_points"];*)


(* ::Input:: *)
(*sigmaRelErr = Floor[-Log10@params["SIGMA_relErr"]];*)
(*sigmaAbsErr = Floor[-Log10@params["SIGMA_absErr"]];*)
(*sumruleRelErr = Floor[-Log10@params["SUMRULE_relErr"]];*)
(*sumruleAbsErr = Floor[-Log10@params["SUMRULE_absErr"]];*)


(* ::Input:: *)
(*(* define functions *)*)


(* ::Input:: *)
(*ClearAll[mom];*)
(*mom[s_,m_]:=Sqrt[s/4-m^2];*)
(*mom[s_]:=mom[s,0];*)


(* ::Input:: *)
(*ClearAll["\[Beta]"];*)
(*\[Beta][s_?NumericQ] := Sqrt[1 - (4 m^2)/s];*)


(* ::Input:: *)
(*ClearAll["\[Eta]"];*)
(*\[Eta][k_?NumericQ]:=(m g)/2/k;*)


(* ::Input:: *)
(*ClearAll["coAngle"];*)
(*coAngle[Cpq_?NumericQ,Cpr_?NumericQ,Fqr_?NumericQ]:=Cpq Cpr + Sqrt[1-Cpq^2] Sqrt[1-Cpr^2]Cos[Fqr];*)


(* ::Input:: *)
(*ClearAll[MP0]*)
(*MP0[p_,q_,Cpq_,\[Phi]_]:=2I e^2(1-p^2(1-Cpq^2)(1/(q^2+p^2-2q p Cpq+m^2)+1/(q^2+p^2+2q p Cpq+m^2))); *)
(*ClearAll[MP2]*)
(*MP2[p_,q_,Cpq_,\[Phi]_]:=2I e^2p^2(1-Cpq^2)(1/(q^2+p^2-2q p Cpq+m^2)+1/(q^2+p^2+2q p Cpq+m^2))E^(2I \[Phi]); *)
(**)


(* ::Input:: *)
(*ClearAll[sigma0];*)
(*sigma0[s_?NumericQ]:=dimfactor \[Beta][s]/(64 \[Pi]^2 s) Nc NIntegrate[Abs[MP0[mom[s, m], mom[s], Cpq, phi]]^2, {Cpq, -1,1},{phi, 0, 2\[Pi]}, PrecisionGoal->sigmaRelErr, AccuracyGoal->sigmaAbsErr];*)
(*ClearAll[sigma2];*)
(*sigma2[s_?NumericQ]:=dimfactor \[Beta][s]/(64 \[Pi]^2 s) Nc NIntegrate[Abs[MP2[mom[s, m], mom[s], Cpq, phi]]^2, {Cpq, -1,1}, {phi, 0, 2\[Pi]},PrecisionGoal->sigmaRelErr, AccuracyGoal->sigmaAbsErr];*)


(* ::Input:: *)
(*\[Sigma]0[s_]:=dimfactor Nc (e^2/(4 \[Pi]))^2 8 \[Pi]/s (m^2/s \[Beta][s]+4 m^4/s^2 Log[Sqrt[s]/(2 m) (1+\[Beta][s])])*)
(*\[Sigma]2[s_]:=dimfactor Nc (e^2/(4 \[Pi]))^2 4 \[Pi]/s ((2 m^2 + s )/s \[Beta][s]+ (8 m^2 (m^2-s))/s^2 Log[Sqrt[s]/(2 m) (1+\[Beta][s])])*)


(* ::Code:: *)
(*ClearAll[sumrule]*)
(*sumrule[f_]:=NIntegrate[f[s]/s,{s, minS, maxS}, PrecisionGoal->sumruleRelErr, AccuracyGoal->sumruleAbsErr]*)


(* ::Code:: *)
(*(* process *)*)


(* ::Code:: *)
(*(* estimate *)*)
(*Column[{*)
(*Row[{"sumrule0  ", AbsoluteTiming[sumrule[sigma0]]}],*)
(*Row[{"sumrule2  ", AbsoluteTiming[sumrule[sigma2]]}],*)
(*Row[{"s0/s2-1  ", sumrule[sigma0]/sumrule[sigma2]-1}]*)
(*}]*)
(**)


(* ::Code:: *)
(*(* precise *)*)
(*Column[{*)
(*Row[{"sumrule0  ", AbsoluteTiming[sumrule[\[Sigma]0]]}],*)
(*Row[{"sumrule2  ", AbsoluteTiming[sumrule[\[Sigma]2]]}],*)
(*Row[{"s0/s2-1  ", sumrule[\[Sigma]0]/sumrule[\[Sigma]2]-1}]*)
(*}]*)
(**)
