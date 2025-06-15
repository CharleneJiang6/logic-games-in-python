% QUESTION 1
nBienPlace([],[],0).

nBienPlace([T|R],[T|B], N):- 
	nBienPlace(R,B,M),
    N is M+1.

nBienPlace([X|A],[Y|B], N):-
    X\=Y,
	nBienPlace(A,B,N).


longueur([],0).
longueur([_|L],N):-
    longueur(L,M),
    N is M+1.

%gagne(A,B):-A=B.

gagne(A,B):-
    nBienPlace(A,B,M),
    longueur(A,N),
    N=M.



% QUESTION 2

element([],_).
element(T,[T|_]).
element(X,[T|R]):-
    X\=T,
    element(X,R).

%enleve premiere occurence
enleve(_,[],[]).
enleve(T,[T|R],R).
enleve(X,[T|R],[T|Q]):-
    X\=T,
    enleve(X,R,Q).

% A contient les elm nn communs entre C1 et C2

enleveBP([],[],[],[]).

%si meme tete, on ne garde pas la tete dans la sortie
enleveBP([T|R1],[T|R2],A,B):-
	enleveBP(R1,R2,A,B).

%si tete differente, alors la tete se retrouve dans la sortie aussi
enleveBP([T1|R1],[T2|R2],[T1|R11],[T2|R22]):-
	T1\=T2,
    enleveBP(R1,R2,R11,R22).


/*
nMalPlacesAux(A,B,MP):- 
    A\=B,
    longueur(A,MP).

nMalPlaces([],[],0).

nMalPlaces([A1|B1],[A1|B2],N):-
    nMalPlaces(B1,B2,N).

nMalPlaces([A1|B1],[A2|B2],N):-
    A1\=A2,
    nMalPlaces(B1,B2,M),
    N is M+1.
*/

%cor
nMalPlaceAux([],_,0).
nMalPlaceAux([E|Q1],L,MP):-
    element(E,L),
    enleve(E,L,S),
    nMalPlaceAux(Q1,S,MP2),
    MP is MP2+1.

nMalPlaceAux([_|Q1],L,MP):-
    nMalPlaceAux(Q1,L,MP).

nMalPlace(X,Y,MP):-
    enleveBP(X,Y,A,B),
    nMalPlaceAux(A,B,MP).
