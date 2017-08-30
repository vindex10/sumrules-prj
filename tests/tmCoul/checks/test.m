(* ::Package:: *)

(* ::Input:: *)
(*(* load params *)*)


(* ::Input:: *)
(*path = "../../output/tmCoul";*)
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
(*e1=params["G_e1"];*)
(*eps=params["G_eps"];*)
(*\[Mu]=params["G_mu"];*)
(*dimfactor = params["G_dimfactor"];*)


(* ::Input:: *)
(*minS=params["TEST_minS"];*)
(*maxS =params["TEST_maxS"];*)
(*points=params["TEST_points"];*)


(* ::Input:: *)
(*sigmaRelErr = Floor[-Log10@params["SIGMA_relErr"]];*)
(*sigmaAbsErr = Floor[-Log10@params["SIGMA_absErr"]];*)
(*mpRelErr = Floor[-Log10@params["MP_relErr"]];*)
(*mpAbsErr = Floor[-Log10@params["MP_absErr"]];*)
(*mpMaxP = params["MP_maxP"];*)


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
(*ClearAll["MP"];*)
(*MP[q_?NumericQ, p_?NumericQ, Cqp_?NumericQ, phi_?NumericQ]:=1/(p^2+q^2-2 p q Cqp +m^2)+1/(p^2+q^2+2 p q Cqp + m^2);*)


(* ::Input:: *)
(*ClearAll["\[Psi]colP"];*)
(*\[Psi]colP[k_?NumericQ,p_?NumericQ,Ckp_?NumericQ]:=-4\[Pi] E^(-\[Pi] \[Eta][k]/2) Gamma[1+I \[Eta][k]]((2 (p^2-(k+I eps)^2)^(I \[Eta][k]) eps (-1 -I \[Eta][k]))/(p^2+k^2-2p k Ckp+eps^2)^(2+I \[Eta][k])+(2(k+I eps) \[Eta][k] (p^2-(k+I eps)^2)^(I \[Eta][k]-1))/(p^2+k^2-2p k Ckp+eps^2)^(1+I \[Eta][k]));*)


(* ::Input:: *)
(*ClearAll["McolP"]*)
(*McolP[p_?NumericQ, q_?NumericQ, Cpq_?NumericQ, Fpq_?NumericQ] := NIntegrate[px^2/(2\[Pi])^3 Sqrt[p^2+m^2]/Sqrt[px^2+m^2] Conjugate@\[Psi]colP[p, px, coAngle[Cqpx,Cpq,Fpx]] MP[px, q, Cqpx, Fpx]*)
(*		,{px, 0, mpMaxP}, {Cqpx, -1, 1}, {Fpx, 0, 2\[Pi]}, PrecisionGoal->mpRelErr,AccuracyGoal->mpAbsErr]*)


(* ::Input:: *)
(*ClearAll["sigma"];*)
(*sigma[s_?NumericQ]:= NIntegrate[dimfactor \[Beta][s]/(64 \[Pi]^2 s)Abs[McolP[mom[s], mom[s,m], Cpq, Fpq]]^2, {Cpq, -1,1},{Fpq, 0, 2\[Pi]}, PrecisionGoal->sigmaRelErr, AccuracyGoal->sigmaAbsErr]*)


(* ::Input:: *)
(*(* process *)*)


(* ::Input:: *)
(*(* Freezes here, no sense to continue *)*)
(*AbsoluteTiming@sigma[10]*)


(* ::Input:: *)
(*data = Table[minS+(maxS - minS)/points i, {i, 0, points-1}];*)


(* ::Input:: *)
(*res = AbsoluteTiming@Map[{#, sigma[#]}&, data];*)


(* ::Input:: *)
(*Print["Eval time: ", res[[1]]]*)


(* ::Input:: *)
(*Column[Row[{#1, " ",ScientificForm@#2}]&@@@res[[2]]]*)


(* ::Input:: *)
(*ListLinePlot[res[[2]], PlotRange->All, Mesh-> All]*)
