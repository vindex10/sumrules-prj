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
