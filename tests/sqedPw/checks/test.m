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
(*tmp = StringSplit[#, " "]& /@tmp;*)
(*tmp = {#[[1]], Quiet@Check[ToExpression[#[[2]]], #[[2]]] }&/@tmp;*)
(*tmp = <|#[[1]]->#[[2]]&/@tmp|>*)
(*];*)
(*Column@KeyValueMap[Row[{#1," = ",#2}]&,params]*)


(* ::Input:: *)
(*m=params["m"];*)
(*g=params["g"];*)
(*e1=params["e1"];*)
(*eps=params["eps"];*)
(*\[Mu]=params["mu"];*)


(* ::Input:: *)
(*minS=params["minS"];*)
(*maxS =params["maxS"];*)
(*points=params["points"];*)


(* ::Input:: *)
(*relerr = Floor[-Log10@params["rel_err"]];*)
(*abserr = Floor[-Log10@params["abs_err"]];*)


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
(*\[Eta][k_?NumericQ]:=(\[Mu] g)/k;*)


(* ::Input:: *)
(*ClearAll["coAngle"];*)
(*coAngle[Cpq_?NumericQ,Cpr_?NumericQ,Fqr_?NumericQ]:=Cpq Cpr + Sqrt[1-Cpq^2] Sqrt[1-Cpr^2]Cos[Fqr];*)


(* ::Input:: *)
(*ClearAll[MP0]*)
(*MP0[p_,q_,Cpq_,\[Phi]_]:=2I e1^2(1-p^2(1-Cpq^2)(1/(q^2+p^2-2q p Cpq+m^2)+1/(q^2+p^2+2q p Cpq+m^2))); *)
(*ClearAll[MP2]*)
(*MP2[p_,q_,Cpq_,\[Phi]_]:=2I e1^2p^2(1-Cpq^2)(1/(q^2+p^2-2q p Cpq+m^2)+1/(q^2+p^2+2q p Cpq+m^2))E^(2I \[Phi]); *)
(**)


(* ::Input:: *)
(*ClearAll[sigma0];*)
(*sigma0[s_?NumericQ]:=\[Beta][s]/(32 \[Pi] s) NIntegrate[Abs[MP0[mom[s, m], mom[s], Cpq, 0]]^2, {Cpq, -1,1}, PrecisionGoal->relerr, AccuracyGoal->abserr];*)
(*ClearAll[sigma2];*)
(*sigma2[s_?NumericQ]:=\[Beta][s]/(32 \[Pi] s) NIntegrate[Abs[MP2[mom[s, m], mom[s], Cpq, 0]]^2, {Cpq, -1,1}, PrecisionGoal->relerr, AccuracyGoal->abserr];*)


(* ::Input:: *)
(*(* analytical result *)*)
(*\[Sigma]0[s_]:=3*(2/3)^4*((e1)^2/(4\[Pi]))^2*2\[Pi] *1 /s*((4*(m^2*Sqrt[1-(4*m^2)/s]*s+4*m^4*Log[((1+Sqrt[1-(4*m^2)/s])*Sqrt[s])/(2*m)]))/s^2)(1.973)^2 10^5; *)
(**)
(*\[Sigma]2[s_]:=3*(2/3)^4*((e1)^2/(4\[Pi]))^2*2\[Pi] *1/s*((2*Sqrt[1-(4*m^2)/s]*s*(2*m^2+s)+16*(m^4-m^2*s)*Log[((1+Sqrt[1-(4*m^2)/s])*Sqrt[s])/(2*m)])/s^2) (1.973)^2 10^5;*)


(* ::Code:: *)
(*ClearAll[sumrule]*)
(*sumrule[f_]:=NIntegrate[f[s]/s,{s, minS, maxS}, PrecisionGoal->3, AccuracyGoal->Infinity]*)


(* ::Code:: *)
(*(* process *)*)


(* ::Code:: *)
(*(* estimate *)*)
(*Column[{*)
(*Row[{"sumrule0  ", AbsoluteTiming[(1.973)^2 10^5 sumrule[sigma0]]}],*)
(*Row[{"sumrule2  ", AbsoluteTiming[(1.973)^2 10^5 sumrule[sigma2]]}],*)
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
