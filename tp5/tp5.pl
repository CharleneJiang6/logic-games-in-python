nBienPlace([],[],0).
nBienPlace([A1|B1],[A1|B2],N):-
	nBienPlace(B1,B2,M),
	N is M+1.
nBienPlace([A1|B1],[A2|B2],N):-
	A1 \= A2,
	nBienPlace(B1,B2,N).

/*gagne(A,B):-A=B. */
/*gagne(C,C). */

longueur([],0).
longueur([_|R],N):-
	longueur(R,M),
	N is M+1.

gagne(C1,C2):-
    nBienPlace(C1,C2,N),
    longueur(C1,N),
    longueur(C2,N).

/*element(_, []). */
/*ca signifie que tout app. [] */

element(X,[X|_]).
element(X,[T|R]):-
    X\=T,
    element(X,R).

enleve(_,[],[]).
enleve(A,[A|B],B).
enleve(A,[T|B],[T|C]):-
    A\=T,
    enleve(A,B,C).

/* si meme tete, alors ne pas garder la tete
si non, garder les tetes diff dans les resultats */
enleveBP([],[],[],[]).
enleveBP([T|R1],[T|R2],C1,C2):-
    enleveBP(R1,R2,C1,C2).
enleveBP([T1|R1],[T2|R2],[T1|C1],[T2|C2]):-
    T1\=T2, /*donne juste une solution */
    enleveBP(R1,R2,C1,C2).

nMalPlacesAux([],_,0).

/* si la tete est un elm du code2, on incremente compteur */
nMalPlacesAux([X|R1],C,N):-
    element(X,C),
    enleve(X,C,C2),
    nMalPlacesAux(R1,C2,M),
    N is M+1.

/* si la tete n'est pas un elm du code 2, on ignore */
nMalPlacesAux([A|R1],C,N):-
    \+element(A,C),
    nMalPlacesAux(R1,C,N).

nMalPlaces([],_,0).
nMalPlaces(X,Y,N):-
    enleveBP(X,Y,C1,C2), /*pour avoir que les elm mal places */
    nMalPlacesAux(C1,C2,N).

codeur(_,0,[]).
codeur(M, N, [T|R]) :-
    Max is M+1,
    random(1, Max, T),
    N1 is N - 1,
    codeur(M, N1, R).

/* JOUER */

/* 0 coup restant */
play(Solution, 0) :-
    write('Perdu ! La solution etait : '),
    write(Solution), nl.

/* encore des coups restants */
play(Solution, NbCoups) :-
    NbCoups > 0,
    write('Il reste '), write(NbCoups), write(' coup(s).'), nl,
    write('Donner un code : '), nl, read(Code), nl,
    nBienPlace(Solution, Code, BP),
    nMalPlaces(Solution, Code, MP),
    write('BP : '), write(BP),
    write('/MP: '), write(MP), nl,
    longueur(Solution, N),
    ( BP =:= N ->    /* if */
        write('Gagné !'), nl
    ;
        NbCoupsRestant is NbCoups - 1, /* else */
        play(Solution, NbCoupsRestant)
    ).


jouons(NbCouleurs,TailleCode,NbCoups):-
    codeur(NbCouleurs,TailleCode,Solution),
    play(Solution, NbCoups).


