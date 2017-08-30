(* ::Package:: *)

(* ::Input:: *)
(*(* load params *)*)


(* ::Code:: *)
(*path = "../../output/tmPw";*)
(*SetDirectory[NotebookDirectory[]<>path]*)


(* ::Code:: *)
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


(* ::Input:: *)
(*(* define functions *)*)


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
(*MP=Function[{q, p, Cqp, phi},1/(p^2+q^2-2 p q Cqp +m^2)+1/(p^2+q^2+2 p q Cqp + m^2)];*)


(* ::Input:: *)
(*ClearAll["sigma"];*)
(*sigma[s_]:= NIntegrate[dimfactor \[Beta][s]/(64 \[Pi]^2 s) Abs[MP[mom[s], mom[s,m], Cpq, phi]]^2, *)
(*{Cpq, -1,1}, {phi, 0, 2\[Pi]}, PrecisionGoal->sigmaRelErr,AccuracyGoal->sigmaAbsErr]*)


(* ::Input:: *)
(*(* process *)*)


(* ::Input:: *)
(*data = Table[minS+(maxS - minS)/points i, {i, 0, points-1}];*)


(* ::Input:: *)
(*res = AbsoluteTiming@Map[{#, sigma[#]}&, data];*)


(* ::Input:: *)
(*Print["evaltime ", res[[1]]]*)


(* ::Input:: *)
(*Column[Row[{#1, " ",ScientificForm@#2}]&@@@res[[2,1;;20]]]*)


(* ::Input:: *)
(*ListLinePlot[res[[2]], PlotRange->All, Mesh->All]*)
