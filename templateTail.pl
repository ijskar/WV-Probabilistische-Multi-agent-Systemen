%Condition evaluation:
%This function exists in order to seperate between different kinds of conditions in while- and if-statements. There are the following types of conditions:
%1. trueInState(X): is true iff X is true in the given state.
%2. falseInState(X): is true iff x is false in the given state.
%3. evaluatableCondition(X): is true if X is true on itself (X has to be an evaluatable condition on itself, and is independent of the given state).
conditionIsTrue(State, trueInState(X)) :-
	member(X, State).
conditionIsTrue(State, falseInState(X)) :-
	\+ member(X, State).
conditionIsTrue(State, evaluatableCondition(X)) :-
	X.

%Conditional exec: handles if and if-else
%if-then
exec(BT, [if(Condition, Then) | R], ET, StepN) :-
	conditionIsTrue(BT, Condition),
	flatten([Then|R], NewPlan),
	exec(BT, NewPlan, ET, StepN).

exec(BT, [if(Condition, Then) | R], ET, StepN) :-
	\+ conditionIsTrue(BT, Condition),
	exec(BT, R, ET, StepN).

%if-then-else
exec(BT, [if(Condition, Then, Else) | R], ET, StepN) :-
	conditionIsTrue(BT, Condition),
	flatten([Then|R], NewPlan),
	exec(BT, NewPlan, ET, StepN).

exec(BT, [if(Condition, Then, Else) | R], ET, StepN) :-
	\+ conditionIsTrue(BT, Condition),
	flatten([Else|R], NewPlan),
	exec(BT, NewPlan, ET, StepN).

%while
exec(BT, [while(Condition, Do, Limit) | R], ET, StepN) :-
	limitedWhile(BT, while(Condition, Do, Limit), StepN, TempT),
	flatten([Do], FlattenedDo),
	length(FlattenedDo, DoLength),
	ConsumedSteps is DoLength*Limit,
	NewStepN is StepN + ConsumedSteps,
	exec(TempT, R, ET, NewStepN).
	

%execWhile
limitedWhile(BT,while(_,_,0),_,BT).

limitedWhile(BT,while(Cond, Do, Limit),_, BT):-
    \+ conditionIsTrue(BT, Cond).

limitedWhile(BT, while(Cond, Do, Limit), StepN, EndState) :-
	Limit \= 0,
	conditionIsTrue(BT, Cond),
	flatten([Do], NewPlan),
	exec(BT, NewPlan, ET, StepN),
	NewLimit is Limit - 1,
	length(NewPlan, NewPlanLength),
	NewStepN is StepN + NewPlanLength,
	limitedWhile(ET, while(Cond, Do, NewLimit), NewStepN, EndState).

%endStateContains is true if Endstate can be reached from the given begin state by executing the given plan, and if EndState contains ToContain (ToContain could, for example, be on(a, b)).
endStateContains(BeginState, Plan, ToContain) :-
	flatten([ToContain],NToContain),
	exec(BeginState, Plan, EndState, 1),
	subset(NToContain, EndState).

%calculate chance for while
endStateContainsWhileVersion(BeginState, while(Cond,Do,Limit), ToContain) :-
	flatten([ToContain],NToContain),
   	limitedWhile(BeginState, while(Cond,Do,Limit), 1, EndState),
  	subset(NToContain, EndState).

iterateOverLimit(BeginState, while(Cond, Do, Limit), UpperLimit, ToContain) :-
	numlist(0, UpperLimit, ListOfLimits),
	member(Limit, ListOfLimits),
	endStateContainsWhileVersion(BeginState, while(Cond, Do, Limit), ToContain).

%endStateContains is true if Endstate can be reached from the given begin state by executing the given plan, and if EndState satisfies a given predicate
endStateSatisfies(BeginState,Plan):-
	exec(BeginState,Plan,EndState,1),
	satisfies(EndState).
